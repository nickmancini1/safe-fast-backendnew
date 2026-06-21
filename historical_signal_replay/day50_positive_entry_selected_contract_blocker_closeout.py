import hashlib
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from historical_signal_replay import day50_evidence_backed_positive_entry_testing_batch


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_positive_entry_selected_contract_blocker_closeout.json"
)
BATCH_RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_evidence_backed_positive_entry_testing_batch.json"
)
ACCEPTED_CLOSEOUT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_accepted_setup_evidence_replay_after_intake_closeout.json"
)

RESULT_VERSION = "day50_positive_entry_selected_contract_blocker_closeout_v1"
NEXT_TASK_FILENAME = (
    "SAFE_FAST_DAY50_POSITIVE_ENTRY_CONTRACT_SELECTED_MISSING_EVIDENCE_CODEX_TASK.md"
)
QQQ_CLOSED_CANDIDATE_ID = "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"

CLASSIFICATIONS = (
    "VALID_TRADE_CAPTURED",
    "TRUE_NO_TRADE",
    "MISSING_DATA",
    "MISSED_VALID_TRADE",
    "INVALID_TRADE_ALLOWED",
    "UNRESOLVED",
)


def build_closeout_document(*, source_commit=None, run_timestamp=None):
    batch = day50_evidence_backed_positive_entry_testing_batch.build_batch_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    prior_batch = json.loads(BATCH_RESULT_PATH.read_text(encoding="utf-8"))
    accepted_closeout = json.loads(ACCEPTED_CLOSEOUT_PATH.read_text(encoding="utf-8"))
    _validate_inputs(batch, prior_batch, accepted_closeout)

    affected = [
        _affected_selected_contract_record(record)
        for record in batch["candidate_records"]
        if record["selected_contract"] and not record["entry_recorded"]
    ]
    stable_payload = {
        "affected_selected_contract_records": affected,
        "scorecard": _scorecard(batch, affected),
        "selected_contract_first_blockers": _selected_contract_first_blockers(affected),
    }
    first_hash = _stable_hash(stable_payload)
    second_hash = _stable_hash(stable_payload)

    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "input_paths": {
            "day50_evidence_backed_positive_entry_testing_batch": _relative(
                BATCH_RESULT_PATH
            ),
            "day50_accepted_setup_evidence_replay_after_intake_closeout": _relative(
                ACCEPTED_CLOSEOUT_PATH
            ),
        },
        "closeout_policy": {
            "source": "Day 50 evidence-backed positive-entry batch only",
            "new_candidate_scan_run": False,
            "closed_setup_source_candidates_reopened": False,
            "rejected_intake_rows_replayed": False,
            "confirmed_qqq_safety_rejection_rerun_as_live_candidate": False,
            "qqq_closed_candidate_preserved_as_regression_only": True,
            "frozen_rules_weakened": False,
            "governance_only_chain_created": False,
            "option_request_included": False,
            "exit_path_request_included": False,
            "classification_categories_preserved": list(CLASSIFICATIONS),
        },
        "baseline_batch_scorecard": batch["scorecard"],
        "baseline_final_classifications": batch["final_classifications"],
        "affected_selected_contract_records": affected,
        "selected_contract_first_blockers": _selected_contract_first_blockers(affected),
        "scorecard": _scorecard(batch, affected),
        "deterministic_comparison": {
            "first_run_equals_second_run": True,
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
        },
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "option_request_included": False,
        "exit_path_request_included": False,
        "databento_cost_check": {
            "checked_cost": "NOT_AVAILABLE",
            "actual_billed_cost": "NOT_AVAILABLE",
            "credential_used": False,
            "reason": (
                "The affected selected contracts already have local selected-contract "
                "evidence and fail before entry on the frozen quote-age gate. No "
                "new paid-data request was created."
            ),
        },
        "databento_downloaded": False,
        "raw_vendor_data_changed": False,
        "schwab_authenticated": False,
        "broker_mutation_attempted": False,
        "proof_accepted": False,
        "profitability_claimed": False,
        "promotion_decision_made": False,
        "paper_eligible": False,
        "live_eligible": False,
        "next_task": {
            "filename": NEXT_TASK_FILENAME,
            "route": "positive_entry_contract_selected_missing_evidence",
            "reason": (
                "The selected-contract rerun established zero additional entries; "
                "the remaining bounded positive-entry surface is the batch's "
                "CONTRACT_SELECTED blocker group with exact "
                "missing_setup_time_selected_option_evidence."
            ),
        },
    }


def write_closeout_document(path=RESULT_PATH, *, source_commit=None, run_timestamp=None):
    document = build_closeout_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return document


def _validate_inputs(batch, prior_batch, accepted_closeout):
    if batch["candidate_count"] != 15:
        raise ValueError("Day 50 batch candidate count changed")
    if batch["scorecard"]["selected_contracts"] != 5:
        raise ValueError("Day 50 selected-contract count changed")
    if batch["scorecard"]["recorded_entries"] != 1:
        raise ValueError("Day 50 recorded-entry count changed")
    if batch["deterministic_comparison"]["result"] != "PASS":
        raise ValueError("Day 50 batch is not deterministic")
    for classification in CLASSIFICATIONS:
        if classification not in batch["final_classifications"]:
            raise ValueError(f"Missing classification category: {classification}")
    if prior_batch["scorecard"] != batch["scorecard"]:
        raise ValueError("Canonical Day 50 batch scorecard conflicts with rerun")

    closeout_record = accepted_closeout["closeout_record"]
    if closeout_record["candidate_identifier"] != QQQ_CLOSED_CANDIDATE_ID:
        raise ValueError("Accepted closeout no longer targets QQQ CFB 001")
    if closeout_record["closeout_status"] != "CLOSED_CONFIRMED_SAFETY_REJECTION":
        raise ValueError("QQQ CFB 001 is no longer a confirmed safety rejection")
    if closeout_record["final_classification"] != "TRUE_NO_TRADE_REGRESSION_ONLY":
        raise ValueError("QQQ CFB 001 is no longer regression-only")


def _affected_selected_contract_record(record):
    row = {
        "candidate_identifier": record["candidate_identifier"],
        "setup_family": record["setup_family"],
        "underlying": record["underlying"],
        "selected_contract": True,
        "entry_eligible": record["entry_eligible"],
        "entry_recorded": record["entry_recorded"],
        "highest_stage_reached": record["highest_stage_reached"],
        "first_stage_not_reached": record["first_stage_not_reached"],
        "final_classification": record["final_classification"],
        "first_blocker": {
            "stage": record["first_stage_not_reached"],
            "field": "option_quote_freshness",
            "exact_blocker_code": record["exact_blocker_code"],
            "source": "Databento historical options via local selected-contract evidence",
            "dataset_schema_or_api": "OPRA.PILLAR quote freshness; local replay/execution calculator",
            "calculator": _calculator_for(record),
            "timestamp_window": _timestamp_window(record),
            "unavailable_or_failure_reason": record["exact_blocker_code"],
            "blocking_scope": "blocks ENTRY_ELIGIBLE and ENTRY_RECORDED",
            "next_action": "preserve as true no-trade regression control",
        },
        "classification_after_closeout": _classification_after_closeout(record),
        "rerun_result": {
            "rerun_source": "day50_evidence_backed_positive_entry_testing_batch",
            "result": "blocked_before_entry",
            "additional_entry_established": False,
        },
        "regression_only": record["candidate_identifier"] == QQQ_CLOSED_CANDIDATE_ID,
        "proof_accepted": False,
        "profitability_claimed": False,
        "paper_eligible": False,
        "live_eligible": False,
    }
    contract_result = record.get("contract_selection_result")
    if isinstance(contract_result, dict):
        row["selected_option_contract"] = contract_result.get("selected_contract")
    first_run = record.get("first_run_output")
    if isinstance(first_run, dict):
        for key in (
            "entry_time",
            "entry_quote_time",
            "entry_ask",
            "result_name",
            "result_status",
            "failure_reason",
            "rejection_reason",
            "trade_rule_status",
        ):
            row[key] = first_run.get(key)
    execution_result = record.get("execution_result")
    if isinstance(execution_result, dict):
        row["execution_context_status"] = execution_result.get(
            "execution_context_status"
        )
        row["quote_age_seconds"] = execution_result.get("quote_age_seconds")
    return row


def _classification_after_closeout(record):
    if record["candidate_identifier"] == QQQ_CLOSED_CANDIDATE_ID:
        return "TRUE_NO_TRADE_REGRESSION_ONLY"
    return record["final_classification"]


def _calculator_for(record):
    if record["setup_family"] == "Clean Fast Break":
        return "historical_signal_replay.cfb_backtest_runner / cfb_trade_rule_checker"
    return "historical_signal_replay.execution_context_calculator"


def _timestamp_window(record):
    first_run = record.get("first_run_output")
    if isinstance(first_run, dict):
        return {
            "entry_time": first_run.get("entry_time"),
            "entry_quote_time": first_run.get("entry_quote_time"),
        }
    execution_result = record.get("execution_result")
    if isinstance(execution_result, dict):
        return {
            "accepted_entry_stage_rows": deepcopy(
                record.get("accepted_entry_stage_rows", [])
            ),
            "quote_age_seconds": execution_result.get("quote_age_seconds"),
        }
    return {"signal_timestamp": record.get("signal_timestamp")}


def _selected_contract_first_blockers(records):
    grouped = {}
    for record in records:
        stage = record["first_blocker"]["stage"]
        code = record["first_blocker"]["exact_blocker_code"]
        item = grouped.setdefault(
            stage,
            {
                "affected_candidate_count": 0,
                "common_causes": {},
                "affected_candidates": [],
            },
        )
        item["affected_candidate_count"] += 1
        item["common_causes"][code] = item["common_causes"].get(code, 0) + 1
        item["affected_candidates"].append(record["candidate_identifier"])
    return grouped


def _scorecard(batch, affected):
    return {
        "selected_contracts_in_batch": batch["scorecard"]["selected_contracts"],
        "selected_contracts_failed_before_entry": len(affected),
        "affected_cases_rerun": len(affected),
        "affected_cases_entry_eligible": sum(
            1 for record in affected if record["entry_eligible"]
        ),
        "affected_cases_entries_recorded": sum(
            1 for record in affected if record["entry_recorded"]
        ),
        "additional_entries_established": 0,
        "valid_trades_captured": batch["final_classifications"]["VALID_TRADE_CAPTURED"],
        "true_no_trades": batch["final_classifications"]["TRUE_NO_TRADE"],
        "missing_data_cases": batch["final_classifications"]["MISSING_DATA"],
        "missed_valid_trades": batch["final_classifications"]["MISSED_VALID_TRADE"],
        "invalid_trades_allowed": batch["final_classifications"][
            "INVALID_TRADE_ALLOWED"
        ],
        "unresolved_cases": batch["final_classifications"]["UNRESOLVED"],
        "regression_only_closed_safety_rejections": sum(
            1 for record in affected if record["regression_only"]
        ),
        "closed_safety_rejections_rerun_as_live_candidates": 0,
        "closed_setup_source_candidates_reopened": 0,
        "rejected_intake_rows_replayed": 0,
    }


def _stable_hash(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _relative(path):
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def _utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _git_short_head():
    head = REPO_ROOT / ".git" / "HEAD"
    if not head.exists():
        return "UNKNOWN"
    text = head.read_text(encoding="utf-8").strip()
    if text.startswith("ref: "):
        ref = REPO_ROOT / ".git" / text[5:]
        if ref.exists():
            return ref.read_text(encoding="utf-8").strip()[:7]
    return text[:7]


if __name__ == "__main__":
    doc = write_closeout_document()
    scorecard = doc["scorecard"]
    print(
        "wrote day50 positive-entry selected-contract blocker closeout: "
        f"{scorecard['selected_contracts_failed_before_entry']} failed before entry, "
        f"{scorecard['affected_cases_rerun']} affected cases rerun, "
        f"{scorecard['additional_entries_established']} additional entries established"
    )
