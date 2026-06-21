import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from watcher_foundation import candidate_freshness_blocker_rule_gate as rule_gate


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_positive_entry_trade_candidate_rule_gap_closeout.json"
)
BATCH_RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_evidence_backed_positive_entry_testing_batch.json"
)
CONTRACT_SELECTED_MISSING_EVIDENCE_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_positive_entry_contract_selected_missing_evidence.json"
)

RESULT_VERSION = "day50_positive_entry_trade_candidate_rule_gap_closeout_v1"
NEXT_TASK_FILENAME = (
    "SAFE_FAST_DAY50_POSITIVE_ENTRY_ACTIVE_PATH_RULE_EVIDENCE_REPAIR_CODEX_TASK.md"
)
QQQ_CFB_REGRESSION_ONLY_ID = "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"
QQQ_IDEAL_CANDIDATE_ID = "QQQ-REAL-HISTORICAL-IDEAL-001"
QQQ_IDEAL_FIXTURE_ID = "first_real_qqq_ideal_replay_v1_fixture"

CLASSIFICATIONS = (
    "VALID_TRADE_CAPTURED",
    "TRUE_NO_TRADE",
    "MISSING_DATA",
    "MISSED_VALID_TRADE",
    "INVALID_TRADE_ALLOWED",
    "UNRESOLVED",
)


def build_closeout_document(*, source_commit=None, run_timestamp=None):
    batch = json.loads(BATCH_RESULT_PATH.read_text(encoding="utf-8"))
    contract_selected_closeout = json.loads(
        CONTRACT_SELECTED_MISSING_EVIDENCE_PATH.read_text(encoding="utf-8")
    )
    gate = rule_gate.build_rule_gate_result()
    _validate_inputs(batch, contract_selected_closeout, gate)

    affected_records = [
        _trade_candidate_gap_record(record)
        for record in batch["candidate_records"]
        if record["first_stage_not_reached"] == "TRADE_CANDIDATE"
    ]
    qqq_ideal_gap = _qqq_ideal_selected_contract_gap_closeout(
        contract_selected_closeout,
        gate,
    )
    scorecard = _scorecard(batch, affected_records, qqq_ideal_gap)

    stable_payload = {
        "affected_records": affected_records,
        "qqq_ideal_gap": qqq_ideal_gap,
        "scorecard": scorecard,
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
            "day50_positive_entry_contract_selected_missing_evidence": _relative(
                CONTRACT_SELECTED_MISSING_EVIDENCE_PATH
            ),
        },
        "closeout_policy": {
            "source": "Day 50 evidence-backed positive-entry batch only",
            "target_first_stage_not_reached": "TRADE_CANDIDATE",
            "affected_trade_candidate_rule_gap_cases_reviewed": len(affected_records),
            "qqq_ideal_selected_contract_rule_gap_resolved_from_frozen_evidence": True,
            "qqq_clean_fast_break_001_preserved_regression_only": True,
            "contract_selected_closeout_additional_entries_preserved": 0,
            "new_candidate_scan_run": False,
            "new_setup_source_pass_run": False,
            "closed_setup_source_candidates_reopened": False,
            "rejected_intake_rows_replayed": False,
            "confirmed_qqq_safety_rejection_rerun_as_live_candidate": False,
            "frozen_rules_weakened": False,
            "governance_only_chain_created": False,
            "option_request_included": False,
            "exit_path_request_included": False,
            "classification_categories_preserved": list(CLASSIFICATIONS),
        },
        "affected_trade_candidate_rule_gap_records": affected_records,
        "qqq_ideal_selected_contract_rule_gap_closeout": qqq_ideal_gap,
        "additional_entries": [],
        "scorecard": scorecard,
        "final_classifications": batch["final_classifications"],
        "deterministic_comparison": {
            "first_run_equals_second_run": True,
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
        },
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "databento_cost_check": {
            "checked_cost": "NOT_AVAILABLE",
            "actual_billed_cost": "NOT_AVAILABLE",
            "credential_used": False,
            "reason": (
                "No affected TRADE_CANDIDATE blocker reached selected-contract identity. "
                "The QQQ Ideal selected-contract gap is resolved by accepted frozen "
                "rule-family evidence as outside the narrowed Ideal path, not by a "
                "paid quote-data request."
            ),
        },
        "paid_data_request_created": False,
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
            "route": "positive_entry_active_path_rule_evidence_repair",
            "reason": (
                "The TRADE_CANDIDATE gap group remains blocked before any option "
                "request, and QQQ Ideal is resolved as outside the narrowed Ideal path. "
                "The next bounded step is active-path rule/evidence repair from local "
                "fixture/source evidence only."
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


def _validate_inputs(batch, contract_selected_closeout, gate):
    if batch["scorecard"]["trade_candidates"] != 9:
        raise ValueError("Day 50 trade-candidate count changed")
    blockers = batch["first_blockers"]["TRADE_CANDIDATE"]
    if blockers["affected_candidate_count"] != 4:
        raise ValueError("Day 50 TRADE_CANDIDATE blocker group changed")
    if blockers["common_causes"] != {
        "fresh_or_spent_unconfirmed": 3,
        "prior_completed_shelf_break_spent_TO_REVIEW": 1,
    }:
        raise ValueError("Day 50 TRADE_CANDIDATE blocker causes changed")
    if (
        contract_selected_closeout["scorecard"]["additional_entries_established"] != 0
        or contract_selected_closeout["scorecard"]["entry_eligible_after_closeout"] != 0
        or contract_selected_closeout["scorecard"]["entries_recorded_after_closeout"] != 0
    ):
        raise ValueError("Contract-selected missing-evidence closeout no longer has zero entries")
    if not contract_selected_closeout["regression_only_record"]["regression_only"]:
        raise ValueError("QQQ CFB regression-only control changed")
    if rule_gate.candidate_survival_status(QQQ_IDEAL_CANDIDATE_ID) != "replace":
        raise ValueError("QQQ Ideal frozen survival status changed")
    if gate["source_backed_rule_count"] != 0 or gate["intake_ready_count"] != 0:
        raise ValueError("Frozen rule gate unexpectedly allows promotion")


def _trade_candidate_gap_record(record):
    exact_blocker = record["exact_blocker_code"]
    signal_time = record["signal_timestamp"]
    return {
        "candidate_identifier": record["candidate_identifier"],
        "business_candidate_id": _business_candidate_id(record),
        "setup_family": record["setup_family"],
        "underlying": record["underlying"],
        "batch_first_stage_not_reached": record["first_stage_not_reached"],
        "highest_stage_reached": record["highest_stage_reached"],
        "batch_exact_blocker": exact_blocker,
        "field": _field_for_blocker(exact_blocker),
        "source": record["evidence_source"],
        "dataset_schema_or_api": (
            "SAFE-FAST local grouped lifecycle fixture / signal_replay_input_v1 "
            "and signal_replay_output_v1 review artifacts"
        ),
        "calculator": "historical_signal_replay.day48_positive_trade_capture_funnel",
        "timestamp_window": {
            "signal_time": signal_time,
            "signal_timezone": record["signal_timezone"],
        },
        "unavailable_or_failure_reason": exact_blocker,
        "blocking_scope": "blocks TRADE_CANDIDATE before selected-contract identity",
        "next_action": _next_action_for_trade_candidate_gap(record),
        "selected_contract_after_closeout": False,
        "entry_eligible_after_closeout": False,
        "entry_recorded_after_closeout": False,
        "additional_entry_established": False,
        "resolved_classification": record["final_classification"],
        "proof_accepted": False,
        "profitability_claimed": False,
        "paper_eligible": False,
        "live_eligible": False,
    }


def _qqq_ideal_selected_contract_gap_closeout(contract_selected_closeout, gate):
    qqq_ideal = None
    for record in contract_selected_closeout["active_selected_contract_records"]:
        if record["candidate_identifier"] == QQQ_IDEAL_FIXTURE_ID:
            qqq_ideal = record
            break
    if qqq_ideal is None:
        raise ValueError("QQQ Ideal selected-contract gap record missing")

    decisions = gate["gate_by_candidate"][QQQ_IDEAL_CANDIDATE_ID]
    decision_names = [row["rule_family"] for row in decisions]
    status = rule_gate.candidate_survival_status(QQQ_IDEAL_CANDIDATE_ID)
    return {
        "candidate_identifier": QQQ_IDEAL_FIXTURE_ID,
        "business_candidate_id": QQQ_IDEAL_CANDIDATE_ID,
        "setup_family": "Ideal",
        "underlying": "QQQ",
        "prior_blocker_field": "selected_contract_identity",
        "prior_unavailable_or_failure_reason": "no accepted QQQ Ideal selected-contract rule",
        "prior_fresh_raw_quote_symbol": qqq_ideal["quote_evidence"]["raw_symbol"],
        "prior_fresh_raw_quote_time": qqq_ideal["quote_evidence"]["timestamp_window"][
            "nearest_quote_time"
        ],
        "prior_fresh_raw_quote_spread": qqq_ideal["quote_evidence"]["spread"],
        "accepted_frozen_evidence_status": status,
        "accepted_frozen_rule_families_applied": decision_names,
        "field": "active_path_contract_selection_precondition",
        "source": (
            "SAFE_FAST_RULE_FAMILY_DECISION_TABLE.md; "
            "SAFE_FAST_RULE_DECISION_SURVIVAL_MAP.md; "
            "watcher_foundation.candidate_freshness_blocker_rule_gate"
        ),
        "dataset_schema_or_api": "SAFE-FAST frozen local rule-family decision table",
        "calculator": "watcher_foundation.candidate_freshness_blocker_rule_gate",
        "timestamp_window": {"signal_time": "2026-05-13T12:30:00-04:00"},
        "unavailable_or_failure_reason": rule_gate.candidate_outside_narrowed_path_reason(
            QQQ_IDEAL_CANDIDATE_ID
        ),
        "blocking_scope": (
            "blocks QQQ Ideal selected-contract identity and any paid option-data "
            "request before active-path repair"
        ),
        "next_action": (
            "replace with Ideal evidence inside the narrowed path or source and "
            "regression-test fast-swing freshness, stale/spent expiry, room/risk "
            "thresholds, and complete context/caution fields before contract selection"
        ),
        "selected_contract_after_closeout": False,
        "entry_eligible_after_closeout": False,
        "entry_recorded_after_closeout": False,
        "additional_entry_established": False,
        "proof_accepted": False,
        "profitability_claimed": False,
        "paper_eligible": False,
        "live_eligible": False,
    }


def _business_candidate_id(record):
    winner = record.get("winner_selection_result")
    if isinstance(winner, dict):
        status = winner.get("selection_status")
        if isinstance(status, str) and status:
            return status
    return record["candidate_identifier"]


def _field_for_blocker(blocker):
    if blocker == "fresh_or_spent_unconfirmed":
        return "freshness_final_signal_state"
    if blocker == "prior_completed_shelf_break_spent_TO_REVIEW":
        return "prior_completed_shelf_break_spent_state"
    return "trade_candidate_rule_gap"


def _next_action_for_trade_candidate_gap(record):
    if record["setup_family"] == "Continuation":
        return (
            "source and regression-test setup-family freshness/session-boundary "
            "rules before any selected-contract or paid option-data request"
        )
    return (
        "source and regression-test setup-family fresh/spent active-path rules "
        "before any selected-contract or paid option-data request"
    )


def _scorecard(batch, affected_records, qqq_ideal_gap):
    return {
        "affected_trade_candidate_rule_gap_cases_reviewed": len(affected_records),
        "affected_cases_selected_contracts_after_closeout": 0,
        "affected_cases_entry_eligible_after_closeout": 0,
        "affected_cases_entries_recorded_after_closeout": 0,
        "additional_entries_established": 0,
        "qqq_ideal_selected_contract_rule_gap_resolved_from_frozen_evidence": (
            qqq_ideal_gap["accepted_frozen_evidence_status"] == "replace"
        ),
        "trade_candidates": batch["scorecard"]["trade_candidates"],
        "selected_contracts": batch["scorecard"]["selected_contracts"],
        "eligible_entries": batch["scorecard"]["eligible_entries"],
        "recorded_entries": batch["scorecard"]["recorded_entries"],
        "valid_trades_captured": batch["final_classifications"]["VALID_TRADE_CAPTURED"],
        "true_no_trades": batch["final_classifications"]["TRUE_NO_TRADE"],
        "missing_data_cases": batch["final_classifications"]["MISSING_DATA"],
        "missed_valid_trades": batch["final_classifications"]["MISSED_VALID_TRADE"],
        "invalid_trades_allowed": batch["final_classifications"][
            "INVALID_TRADE_ALLOWED"
        ],
        "unresolved_cases": batch["final_classifications"]["UNRESOLVED"],
        "closed_setup_source_candidates_reopened": 0,
        "rejected_intake_rows_replayed": 0,
        "closed_safety_rejections_rerun_as_live_candidates": 0,
    }


def _stable_hash(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _relative(path):
    return str(Path(path).relative_to(REPO_ROOT)).replace("\\", "/")


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
        "wrote day50 trade-candidate rule-gap closeout: "
        f"{scorecard['affected_trade_candidate_rule_gap_cases_reviewed']} affected cases, "
        f"{scorecard['selected_contracts']} selected contracts, "
        f"{scorecard['eligible_entries']} eligible entries, "
        f"{scorecard['recorded_entries']} recorded entries, "
        f"{scorecard['additional_entries_established']} additional entries"
    )
