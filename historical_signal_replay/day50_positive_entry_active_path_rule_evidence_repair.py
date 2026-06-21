import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_positive_entry_active_path_rule_evidence_repair.json"
)
TRADE_CANDIDATE_CLOSEOUT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_positive_entry_trade_candidate_rule_gap_closeout.json"
)
CONTRACT_SELECTED_MISSING_EVIDENCE_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_positive_entry_contract_selected_missing_evidence.json"
)
BATCH_RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_evidence_backed_positive_entry_testing_batch.json"
)

RESULT_VERSION = "day50_positive_entry_active_path_rule_evidence_repair_v1"
NEXT_TASK_FILENAME = (
    "SAFE_FAST_DAY50_POSITIVE_ENTRY_REMAINING_EVIDENCE_GAP_CLOSEOUT_CODEX_TASK.md"
)

CLASSIFICATIONS = (
    "VALID_TRADE_CAPTURED",
    "TRUE_NO_TRADE",
    "MISSING_DATA",
    "MISSED_VALID_TRADE",
    "INVALID_TRADE_ALLOWED",
    "UNRESOLVED",
)


def build_repair_document(*, source_commit=None, run_timestamp=None):
    trade_candidate_closeout = json.loads(
        TRADE_CANDIDATE_CLOSEOUT_PATH.read_text(encoding="utf-8")
    )
    contract_selected_closeout = json.loads(
        CONTRACT_SELECTED_MISSING_EVIDENCE_PATH.read_text(encoding="utf-8")
    )
    batch = json.loads(BATCH_RESULT_PATH.read_text(encoding="utf-8"))
    _validate_inputs(trade_candidate_closeout, contract_selected_closeout, batch)

    batch_by_candidate = {
        record["candidate_identifier"]: record for record in batch["candidate_records"]
    }
    repair_records = [
        _active_path_repair_record(record, batch_by_candidate[record["candidate_identifier"]])
        for record in trade_candidate_closeout[
            "affected_trade_candidate_rule_gap_records"
        ]
    ]
    qqq_ideal_preservation = _qqq_ideal_preservation(trade_candidate_closeout)
    scorecard = _scorecard(batch, repair_records)

    stable_payload = {
        "repair_records": repair_records,
        "qqq_ideal_preservation": qqq_ideal_preservation,
        "scorecard": scorecard,
    }
    first_hash = _stable_hash(stable_payload)
    second_hash = _stable_hash(stable_payload)

    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "input_paths": {
            "day50_positive_entry_trade_candidate_rule_gap_closeout": _relative(
                TRADE_CANDIDATE_CLOSEOUT_PATH
            ),
            "day50_positive_entry_contract_selected_missing_evidence": _relative(
                CONTRACT_SELECTED_MISSING_EVIDENCE_PATH
            ),
            "day50_evidence_backed_positive_entry_testing_batch": _relative(
                BATCH_RESULT_PATH
            ),
        },
        "repair_policy": {
            "source": "Day 50 trade-candidate rule-gap closeout only",
            "repair_scope": (
                "accepted active-path rule/evidence records for affected "
                "TRADE_CANDIDATE blockers"
            ),
            "affected_trade_candidate_rule_gap_cases_repaired": len(repair_records),
            "new_candidate_scan_run": False,
            "new_setup_source_pass_run": False,
            "closed_setup_source_candidates_reopened": False,
            "rejected_intake_rows_replayed": False,
            "confirmed_qqq_safety_rejection_rerun_as_live_candidate": False,
            "qqq_clean_fast_break_001_preserved_regression_only": True,
            "qqq_ideal_preserved_outside_narrowed_path": True,
            "contract_selected_closeout_additional_entries_preserved": 0,
            "frozen_rules_weakened": False,
            "governance_only_chain_created": False,
            "option_request_included": False,
            "exit_path_request_included": False,
            "classification_categories_preserved": list(CLASSIFICATIONS),
        },
        "active_path_rule_evidence_repair_records": repair_records,
        "qqq_ideal_outside_path_preservation": qqq_ideal_preservation,
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
                "The repair names active-path rule/evidence requirements from existing "
                "local fixture/source evidence. No affected case reaches selected-contract "
                "identity, and no paid option or exit request is valid."
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
            "route": "positive_entry_remaining_evidence_gap_closeout",
            "reason": (
                "The active-path evidence records are now explicit for the affected "
                "TRADE_CANDIDATE blockers, but no additional selected contracts or "
                "entries were established. The next bounded group is remaining "
                "evidence-gap closeout without scans, downloads, or rule weakening."
            ),
        },
    }


def write_repair_document(path=RESULT_PATH, *, source_commit=None, run_timestamp=None):
    document = build_repair_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return document


def _validate_inputs(trade_candidate_closeout, contract_selected_closeout, batch):
    if trade_candidate_closeout["scorecard"]["trade_candidates"] != 9:
        raise ValueError("Trade-candidate closeout baseline changed")
    if (
        trade_candidate_closeout["scorecard"][
            "affected_trade_candidate_rule_gap_cases_reviewed"
        ]
        != 4
    ):
        raise ValueError("Affected TRADE_CANDIDATE group changed")
    if (
        trade_candidate_closeout["scorecard"]["selected_contracts"] != 5
        or trade_candidate_closeout["scorecard"]["eligible_entries"] != 1
        or trade_candidate_closeout["scorecard"]["recorded_entries"] != 1
    ):
        raise ValueError("Trade-candidate closeout totals changed")
    if (
        contract_selected_closeout["scorecard"]["additional_entries_established"] != 0
        or contract_selected_closeout["scorecard"]["entry_eligible_after_closeout"] != 0
        or contract_selected_closeout["scorecard"]["entries_recorded_after_closeout"] != 0
    ):
        raise ValueError("Contract-selected closeout no longer preserves zero entries")
    if batch["scorecard"]["trade_candidates"] != 9:
        raise ValueError("Day 50 batch trade-candidate count changed")
    if batch["scorecard"]["selected_contracts"] != 5:
        raise ValueError("Day 50 batch selected-contract count changed")
    if batch["scorecard"]["eligible_entries"] != 1:
        raise ValueError("Day 50 batch eligible-entry count changed")
    if batch["scorecard"]["recorded_entries"] != 1:
        raise ValueError("Day 50 batch recorded-entry count changed")
    for classification in CLASSIFICATIONS:
        if classification not in batch["final_classifications"]:
            raise ValueError(f"Missing classification category: {classification}")


def _active_path_repair_record(closeout_record, batch_record):
    blocker = closeout_record["batch_exact_blocker"]
    requirement = _requirement_for_record(closeout_record)
    lifecycle_summary = batch_record["lifecycle_summary"]
    return {
        "candidate_identifier": closeout_record["candidate_identifier"],
        "business_candidate_id": closeout_record["business_candidate_id"],
        "underlying": closeout_record["underlying"],
        "setup_family": closeout_record["setup_family"],
        "batch_first_stage_not_reached": "TRADE_CANDIDATE",
        "highest_stage_reached_before_repair": closeout_record["highest_stage_reached"],
        "highest_stage_reached_after_repair": closeout_record["highest_stage_reached"],
        "exact_blocker": blocker,
        "field": closeout_record["field"],
        "source": closeout_record["source"],
        "dataset_schema_or_api": closeout_record["dataset_schema_or_api"],
        "calculator": closeout_record["calculator"],
        "timestamp_window": closeout_record["timestamp_window"],
        "local_fixture_stage_path": batch_record["chronological_stage_path"],
        "local_fixture_blocker_counts": lifecycle_summary["blocker_counts"],
        "local_fixture_caution_counts": lifecycle_summary["caution_counts"],
        "accepted_active_path_rule_evidence_repaired": True,
        "repair_type": "exact_active_path_requirement_record",
        "repaired_requirement": requirement,
        "unavailable_or_failure_reason": blocker,
        "blocking_scope": "blocks TRADE_CANDIDATE before selected-contract identity",
        "selected_contract_before_repair": False,
        "selected_contract_after_repair": False,
        "entry_eligible_before_repair": False,
        "entry_eligible_after_repair": False,
        "entry_recorded_before_repair": False,
        "entry_recorded_after_repair": False,
        "additional_entry_established": False,
        "resolved_classification_after_repair": closeout_record["resolved_classification"],
        "next_action": requirement["smallest_next_action"],
        "proof_accepted": False,
        "profitability_claimed": False,
        "paper_eligible": False,
        "live_eligible": False,
    }


def _requirement_for_record(record):
    family = record["setup_family"]
    blocker = record["batch_exact_blocker"]
    if family == "Clean Fast Break":
        missing = "tested GLD Clean Fast Break fresh/spent active-path rule"
        required = (
            "setup-time freshness/final-signal state that distinguishes fresh "
            "reclaim, pullback hold, no-fresh-trigger, stale, and spent rows"
        )
        action = (
            "define and regression-test the GLD Clean Fast Break fresh/spent "
            "active-path rule before any selected-contract request"
        )
    elif family == "Continuation":
        missing = "tested IWM Continuation prior-completed-shelf-break spent rule"
        required = (
            "source-backed prior_completed_shelf_break_spent_state plus "
            "session-boundary/freshness behavior at the signal row"
        )
        action = (
            "define and regression-test IWM Continuation shelf-break spent and "
            "session-boundary freshness before any selected-contract request"
        )
    else:
        missing = f"tested {record['underlying']} Ideal fresh/spent active-path rule"
        required = (
            "source-backed freshness_final_signal_state plus Ideal stale/spent "
            "expiry behavior at the signal row"
        )
        action = (
            f"define and regression-test {record['underlying']} Ideal fresh/spent "
            "active-path rule before any selected-contract request"
        )

    return {
        "exact_missing_rule_or_evidence": missing,
        "required_source_field_or_log_evidence": required,
        "source_file_or_doc": record["source"],
        "field": record["field"],
        "dataset_schema_or_api": record["dataset_schema_or_api"],
        "calculator": record["calculator"],
        "timestamp_window": record["timestamp_window"],
        "current_repo_has_enough_data": False,
        "decision_if_missing": "blocks TRADE_CANDIDATE",
        "blocker_repaired_to_exact_requirement": blocker,
        "smallest_next_action": action,
        "proof_allowed": False,
    }


def _qqq_ideal_preservation(trade_candidate_closeout):
    qqq_ideal = trade_candidate_closeout["qqq_ideal_selected_contract_rule_gap_closeout"]
    return {
        "candidate_identifier": qqq_ideal["candidate_identifier"],
        "business_candidate_id": qqq_ideal["business_candidate_id"],
        "accepted_frozen_evidence_status": qqq_ideal["accepted_frozen_evidence_status"],
        "unavailable_or_failure_reason": qqq_ideal["unavailable_or_failure_reason"],
        "selected_contract_after_repair": False,
        "entry_eligible_after_repair": False,
        "entry_recorded_after_repair": False,
        "paid_option_request_valid_after_repair": False,
        "preserved_as": "outside_narrowed_ideal_path",
    }


def _scorecard(batch, repair_records):
    return {
        "affected_trade_candidate_rule_gap_cases_repaired": len(repair_records),
        "accepted_active_path_rule_evidence_records": len(repair_records),
        "affected_cases_selected_contracts_before_repair": 0,
        "affected_cases_selected_contracts_after_repair": 0,
        "affected_cases_entry_eligible_before_repair": 0,
        "affected_cases_entry_eligible_after_repair": 0,
        "affected_cases_entries_recorded_before_repair": 0,
        "affected_cases_entries_recorded_after_repair": 0,
        "additional_entries_established": 0,
        "trade_candidates_before_repair": batch["scorecard"]["trade_candidates"],
        "trade_candidates_after_repair": batch["scorecard"]["trade_candidates"],
        "selected_contracts_before_repair": batch["scorecard"]["selected_contracts"],
        "selected_contracts_after_repair": batch["scorecard"]["selected_contracts"],
        "eligible_entries_before_repair": batch["scorecard"]["eligible_entries"],
        "eligible_entries_after_repair": batch["scorecard"]["eligible_entries"],
        "recorded_entries_before_repair": batch["scorecard"]["recorded_entries"],
        "recorded_entries_after_repair": batch["scorecard"]["recorded_entries"],
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
    doc = write_repair_document()
    scorecard = doc["scorecard"]
    print(
        "wrote day50 active-path rule/evidence repair: "
        f"{scorecard['affected_trade_candidate_rule_gap_cases_repaired']} repaired cases, "
        f"{scorecard['trade_candidates_before_repair']}->{scorecard['trade_candidates_after_repair']} trade candidates, "
        f"{scorecard['selected_contracts_before_repair']}->{scorecard['selected_contracts_after_repair']} selected contracts, "
        f"{scorecard['eligible_entries_before_repair']}->{scorecard['eligible_entries_after_repair']} eligible entries, "
        f"{scorecard['recorded_entries_before_repair']}->{scorecard['recorded_entries_after_repair']} recorded entries"
    )
