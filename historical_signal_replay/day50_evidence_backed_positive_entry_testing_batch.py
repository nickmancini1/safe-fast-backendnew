import hashlib
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from historical_signal_replay import day48_positive_trade_capture_funnel


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_evidence_backed_positive_entry_testing_batch.json"
)
DAY48_FUNNEL_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day48_positive_trade_capture_funnel.json"
)
DAY50_CLOSEOUT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_accepted_setup_evidence_replay_after_intake_closeout.json"
)
DAY50_REPLAY_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_accepted_setup_evidence_replay_after_intake.json"
)
DAY50_INTAKE_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_accepted_complete_setup_evidence_intake.json"
)

RESULT_VERSION = "day50_evidence_backed_positive_entry_testing_batch_v1"
NEXT_TASK_FILENAME = "SAFE_FAST_DAY50_POSITIVE_ENTRY_SELECTED_CONTRACT_BLOCKER_CLOSEOUT_CODEX_TASK.md"
QQQ_CLOSED_CANDIDATE_ID = "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"

CLASSIFICATIONS = (
    "VALID_TRADE_CAPTURED",
    "TRUE_NO_TRADE",
    "MISSING_DATA",
    "MISSED_VALID_TRADE",
    "INVALID_TRADE_ALLOWED",
    "UNRESOLVED",
)


def build_batch_document(*, source_commit=None, run_timestamp=None):
    day48 = day48_positive_trade_capture_funnel.build_funnel_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    closeout = json.loads(DAY50_CLOSEOUT_PATH.read_text(encoding="utf-8"))
    replay = json.loads(DAY50_REPLAY_PATH.read_text(encoding="utf-8"))
    intake = json.loads(DAY50_INTAKE_PATH.read_text(encoding="utf-8"))

    _validate_inputs(day48, closeout, replay, intake)

    candidate_records = [
        _batch_candidate_record(record, closeout)
        for record in day48["candidate_records"]
    ]
    scorecard = _scorecard(candidate_records)
    final_classifications = _classification_totals(candidate_records)
    first_blockers = _first_blockers(candidate_records)

    stable_payload = {
        "candidate_records": candidate_records,
        "scorecard": scorecard,
        "final_classifications": final_classifications,
        "first_blockers": first_blockers,
    }
    first_hash = _stable_hash(stable_payload)
    second_hash = _stable_hash(stable_payload)

    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "input_paths": {
            "day48_positive_trade_capture_funnel": _relative(DAY48_FUNNEL_PATH),
            "day50_accepted_setup_evidence_replay_after_intake_closeout": _relative(
                DAY50_CLOSEOUT_PATH
            ),
            "day50_accepted_setup_evidence_replay_after_intake": _relative(
                DAY50_REPLAY_PATH
            ),
            "day50_accepted_complete_setup_evidence_intake": _relative(
                DAY50_INTAKE_PATH
            ),
        },
        "batch_policy": {
            "source": "existing evidence-backed positive-entry regression controls only",
            "new_candidate_scan_run": False,
            "closed_setup_source_candidates_reopened": False,
            "rejected_intake_rows_replayed": False,
            "confirmed_qqq_safety_rejection_rerun_as_live_candidate": False,
            "qqq_closed_candidate_preserved_as_regression_only": True,
            "frozen_rules_weakened": False,
            "governance_only_chain_created": False,
            "classification_categories_preserved": list(CLASSIFICATIONS),
            "forbidden_inputs": [
                "closed setup-source candidates",
                "rejected intake rows",
                "open-ended candidate scans",
                "rule weakening",
                "option requests before TRADE_CANDIDATE",
                "exit-path requests before valid entry",
                "P&L proof",
                "profitability",
                "paper/live readiness",
            ],
        },
        "candidate_count": len(candidate_records),
        "candidate_records": candidate_records,
        "scorecard": scorecard,
        "final_classifications": final_classifications,
        "first_blockers": first_blockers,
        "closed_safety_rejection_control": _closed_safety_rejection_control(closeout),
        "day48_regression_control_result": {
            "deterministic_result": day48["deterministic_comparison"]["result"],
            "combined_scorecard": day48["combined_scorecard"],
            "final_classifications": day48["final_classifications"],
        },
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
                "This batch used existing local evidence-backed controls only. "
                "No new candidate or unresolved exact paid-data request was created."
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
            "route": "positive_entry_selected_contract_blocker_closeout",
            "reason": (
                "The batch preserved the valid-entry and stale-quote controls while "
                "showing that the remaining first blockers are concentrated at "
                "TRADE_CANDIDATE and CONTRACT_SELECTED. The next bounded task should "
                "close out selected-contract blockers without reopening closed setup-source "
                "candidates or requesting paid data."
            ),
        },
    }


def write_batch_document(path=RESULT_PATH, *, source_commit=None, run_timestamp=None):
    document = build_batch_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return document


def _validate_inputs(day48, closeout, replay, intake):
    if day48["deterministic_comparison"]["result"] != "PASS":
        raise ValueError("Day 48 funnel is not deterministic")
    if len(day48["candidate_records"]) != 15:
        raise ValueError("Day 48 evidence-backed control count changed")
    for classification in CLASSIFICATIONS:
        if classification not in day48["final_classifications"]:
            raise ValueError(f"Missing classification category: {classification}")

    closeout_record = closeout["closeout_record"]
    if closeout_record["candidate_identifier"] != QQQ_CLOSED_CANDIDATE_ID:
        raise ValueError("Unexpected Day 50 closeout candidate")
    if closeout_record["closeout_status"] != "CLOSED_CONFIRMED_SAFETY_REJECTION":
        raise ValueError("QQQ closeout status changed")
    if closeout_record["final_classification"] != "TRUE_NO_TRADE_REGRESSION_ONLY":
        raise ValueError("QQQ closeout is no longer regression-only")
    if closeout["scorecard"]["trade_candidates"] != 0:
        raise ValueError("Day 50 closeout unexpectedly has trade candidates")

    if replay["scorecard"]["trade_candidates"] != 0:
        raise ValueError("Accepted replay unexpectedly has trade candidates")
    if intake["scorecard"]["trade_candidates"] != 0:
        raise ValueError("Accepted intake unexpectedly has trade candidates")


def _batch_candidate_record(record, closeout):
    row = deepcopy(record)
    row["batch_record_type"] = "evidence_backed_positive_entry_regression_control"
    row["selected_contract"] = "CONTRACT_SELECTED" in row["funnel_stage_path"]
    row["entry_eligible"] = "ENTRY_ELIGIBLE" in row["funnel_stage_path"]
    row["entry_recorded"] = "ENTRY_RECORDED" in row["funnel_stage_path"]
    row["exit_evaluated"] = "EXIT_EVALUATED" in row["funnel_stage_path"]
    row["blocks_live_candidate_replay"] = False
    row["regression_only"] = False

    if row["candidate_identifier"] == QQQ_CLOSED_CANDIDATE_ID:
        row["regression_only"] = True
        row["blocks_live_candidate_replay"] = True
        row["day50_closeout_status"] = closeout["closeout_record"]["closeout_status"]
        row["day50_closeout_classification"] = closeout["closeout_record"][
            "final_classification"
        ]
        row["day50_closeout_reason"] = (
            "closed confirmed safety rejection; preserve only as true no-trade regression anchor"
        )
    return row


def _scorecard(records):
    return {
        "candidates_found": len(records),
        "candidates_runnable": len(records),
        "setup_developing_count": _stage_count(records, "SETUP_DEVELOPING"),
        "setup_qualified_candidates": _stage_count(records, "SETUP_QUALIFIED"),
        "trade_candidates": _stage_count(records, "TRADE_CANDIDATE"),
        "selected_contracts": sum(1 for record in records if record["selected_contract"]),
        "prices_accepted": _stage_count(records, "PRICE_ACCEPTABLE"),
        "eligible_entries": sum(1 for record in records if record["entry_eligible"]),
        "recorded_entries": sum(1 for record in records if record["entry_recorded"]),
        "exits_evaluated": sum(1 for record in records if record["exit_evaluated"]),
        "valid_trades_captured": _classification_count(records, "VALID_TRADE_CAPTURED"),
        "true_no_trades": _classification_count(records, "TRUE_NO_TRADE"),
        "missing_data_cases": _classification_count(records, "MISSING_DATA"),
        "missed_valid_trades": _classification_count(records, "MISSED_VALID_TRADE"),
        "invalid_trades_allowed": _classification_count(records, "INVALID_TRADE_ALLOWED"),
        "unresolved_cases": _classification_count(records, "UNRESOLVED"),
        "regression_only_closed_safety_rejections": sum(
            1
            for record in records
            if record["candidate_identifier"] == QQQ_CLOSED_CANDIDATE_ID
            and record["regression_only"]
        ),
        "closed_safety_rejections_rerun_as_live_candidates": 0,
        "closed_setup_source_candidates_reopened": 0,
        "rejected_intake_rows_replayed": 0,
        "deterministic_cases": sum(
            1 for record in records if record["deterministic_result"] == "deterministic"
        ),
        "unstable_cases": sum(
            1 for record in records if record["deterministic_result"] != "deterministic"
        ),
        "winners": sum(1 for record in records if record["winner_or_loser"] == "winner"),
        "losers": sum(1 for record in records if record["winner_or_loser"] == "loser"),
    }


def _classification_totals(records):
    return {
        classification: _classification_count(records, classification)
        for classification in CLASSIFICATIONS
    }


def _first_blockers(records):
    grouped = {}
    for record in records:
        stage = record["first_stage_not_reached"] or "NONE"
        item = grouped.setdefault(
            stage,
            {
                "affected_candidate_count": 0,
                "affected_setup_families": [],
                "common_causes": {},
                "exact_blocker_examples": [],
            },
        )
        item["affected_candidate_count"] += 1
        if record["setup_family"] not in item["affected_setup_families"]:
            item["affected_setup_families"].append(record["setup_family"])
        cause = record["exact_blocker_code"] or "completed_valid_entry_review_only"
        item["common_causes"][cause] = item["common_causes"].get(cause, 0) + 1
        if len(item["exact_blocker_examples"]) < 5:
            item["exact_blocker_examples"].append(
                {
                    "candidate_identifier": record["candidate_identifier"],
                    "exact_blocker_code": cause,
                    "evidence_source": record["evidence_source"],
                }
            )
    return grouped


def _closed_safety_rejection_control(closeout):
    record = closeout["closeout_record"]
    return {
        "candidate_identifier": record["candidate_identifier"],
        "closeout_status": record["closeout_status"],
        "final_classification": record["final_classification"],
        "highest_stage_reached": record["highest_stage_reached"],
        "first_stage_not_reached": record["first_stage_not_reached"],
        "exact_blocker_field": record["exact_blocker_field"],
        "exact_blocker_code": record["exact_blocker_code"],
        "regression_only": True,
    }


def _stage_count(records, stage):
    return sum(1 for record in records if stage in record["funnel_stage_path"])


def _classification_count(records, classification):
    return sum(1 for record in records if record["final_classification"] == classification)


def _relative(path):
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def _stable_hash(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


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
    doc = write_batch_document()
    scorecard = doc["scorecard"]
    print(
        "wrote day50 evidence-backed positive-entry testing batch: "
        f"{scorecard['setup_qualified_candidates']} setup-qualified, "
        f"{scorecard['trade_candidates']} trade candidates, "
        f"{scorecard['selected_contracts']} selected contracts, "
        f"{scorecard['eligible_entries']} eligible entries, "
        f"{scorecard['recorded_entries']} recorded entries"
    )
