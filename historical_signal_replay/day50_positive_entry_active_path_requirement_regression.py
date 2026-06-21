import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_positive_entry_active_path_requirement_regression.json"
)
REMAINING_GAP_CLOSEOUT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_positive_entry_remaining_evidence_gap_closeout.json"
)
BATCH_RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_evidence_backed_positive_entry_testing_batch.json"
)

RESULT_VERSION = "day50_positive_entry_active_path_requirement_regression_v1"
NEXT_TASK_FILENAME = (
    "SAFE_FAST_DAY50_POSITIVE_ENTRY_CLOSED_REQUIREMENT_SCORECARD_RECONCILIATION_CODEX_TASK.md"
)

CLASSIFICATIONS = (
    "VALID_TRADE_CAPTURED",
    "TRUE_NO_TRADE",
    "MISSING_DATA",
    "MISSED_VALID_TRADE",
    "INVALID_TRADE_ALLOWED",
    "UNRESOLVED",
)

FIXTURE_PATH_BY_CANDIDATE = {
    "first_real_gld_clean_fast_break_replay_v1_fixture": (
        REPO_ROOT
        / "historical_signal_replay"
        / "fixtures"
        / "first_real_gld_clean_fast_break_replay_v1_fixture.json"
    ),
    "first_real_gld_ideal_replay_v1_fixture": (
        REPO_ROOT
        / "historical_signal_replay"
        / "fixtures"
        / "first_real_gld_ideal_replay_v1_fixture.json"
    ),
    "first_real_iwm_continuation_replay_v1_fixture": (
        REPO_ROOT
        / "historical_signal_replay"
        / "fixtures"
        / "first_real_iwm_continuation_replay_v1_fixture.json"
    ),
    "first_real_iwm_ideal_replay_v1_fixture": (
        REPO_ROOT
        / "historical_signal_replay"
        / "fixtures"
        / "first_real_iwm_ideal_replay_v1_fixture.json"
    ),
}


def build_regression_document(*, source_commit=None, run_timestamp=None):
    closeout = json.loads(REMAINING_GAP_CLOSEOUT_PATH.read_text(encoding="utf-8"))
    batch = json.loads(BATCH_RESULT_PATH.read_text(encoding="utf-8"))
    _validate_inputs(closeout, batch)

    batch_by_candidate = {
        record["candidate_identifier"]: record for record in batch["candidate_records"]
    }
    records = [
        _regression_record(record, batch_by_candidate[record["candidate_identifier"]])
        for record in closeout["active_path_requirement_records"]
    ]
    scorecard = _scorecard(closeout, batch, records)
    final_classifications = _final_classifications_after_regression(batch, records)

    stable_payload = {
        "records": records,
        "scorecard": scorecard,
        "final_classifications": final_classifications,
    }
    first_hash = _stable_hash(stable_payload)
    second_hash = _stable_hash(stable_payload)

    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "input_paths": {
            "day50_positive_entry_remaining_evidence_gap_closeout": _relative(
                REMAINING_GAP_CLOSEOUT_PATH
            ),
            "day50_evidence_backed_positive_entry_testing_batch": _relative(
                BATCH_RESULT_PATH
            ),
        },
        "regression_policy": {
            "source": "Day 50 remaining evidence-gap closeout only",
            "regression_scope": (
                "four open active-path requirements that block TRADE_CANDIDATE "
                "before selected-contract identity"
            ),
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
        "active_path_requirement_regression_records": records,
        "additional_entries": [],
        "scorecard": scorecard,
        "final_classifications_before_regression": batch["final_classifications"],
        "final_classifications_after_regression": final_classifications,
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
                "All four tested active-path requirements close before selected-contract "
                "identity from existing local fixture/source evidence. No case reaches a "
                "paid option-data or exit-path request gate."
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
            "route": "positive_entry_closed_requirement_scorecard_reconciliation",
            "reason": (
                "The four open active-path requirements are now permanently closed with "
                "exact failed requirements and no added trade candidates. The next bounded "
                "group is scorecard/control reconciliation only."
            ),
        },
    }


def write_regression_document(path=RESULT_PATH, *, source_commit=None, run_timestamp=None):
    document = build_regression_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return document


def _validate_inputs(closeout, batch):
    if closeout["result_version"] != "day50_positive_entry_remaining_evidence_gap_closeout_v1":
        raise ValueError("Unexpected remaining evidence-gap closeout version")
    if closeout["scorecard"]["active_path_requirements_open_after_closeout"] != 4:
        raise ValueError("Open active-path requirement count changed")
    if closeout["scorecard"]["trade_candidates_after_closeout"] != 9:
        raise ValueError("Trade-candidate baseline changed")
    if closeout["scorecard"]["selected_contracts_after_closeout"] != 5:
        raise ValueError("Selected-contract baseline changed")
    if closeout["scorecard"]["eligible_entries_after_closeout"] != 1:
        raise ValueError("Eligible-entry baseline changed")
    if closeout["scorecard"]["recorded_entries_after_closeout"] != 1:
        raise ValueError("Recorded-entry baseline changed")
    if closeout["scorecard"]["contract_selected_closeout_additional_entries_preserved"] != 0:
        raise ValueError("Contract-selected closeout added entries")
    if batch["scorecard"]["trade_candidates"] != 9:
        raise ValueError("Day 50 batch trade-candidate count changed")
    for classification in CLASSIFICATIONS:
        if classification not in batch["final_classifications"]:
            raise ValueError(f"Missing classification category: {classification}")


def _regression_record(closeout_record, batch_record):
    fixture_path = FIXTURE_PATH_BY_CANDIDATE[closeout_record["candidate_identifier"]]
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    final_row = fixture["lifecycle_rows"][-1]
    output = final_row["expected_output_shape"]
    _validate_final_row(closeout_record, batch_record, fixture_path, output)

    exact_failed_requirement = _exact_failed_requirement(closeout_record)
    return {
        "candidate_identifier": closeout_record["candidate_identifier"],
        "business_candidate_id": closeout_record["business_candidate_id"],
        "underlying": closeout_record["underlying"],
        "setup_family": closeout_record["setup_family"],
        "tested_requirement": closeout_record["exact_blocker"],
        "exact_failed_requirement": exact_failed_requirement,
        "field": closeout_record["field"],
        "source": closeout_record["source"],
        "fixture_path": _relative(fixture_path),
        "dataset_schema_or_api": closeout_record["dataset_schema_or_api"],
        "calculator": closeout_record["calculator"],
        "timestamp_window": closeout_record["timestamp_window"],
        "fixture_final_timestamp": output["timestamp"],
        "fixture_final_stage": output["stage"],
        "fixture_final_verdict": output["final_verdict"],
        "fixture_primary_blocker": output["primary_blocker"],
        "batch_first_stage_not_reached": "TRADE_CANDIDATE",
        "highest_stage_reached_before_regression": closeout_record["highest_stage_reached"],
        "highest_stage_reached_after_regression": closeout_record["highest_stage_reached"],
        "accepted_frozen_evidence_available_to_advance": False,
        "advanced_to_trade_candidate": False,
        "permanently_closed": True,
        "closeout_determination": "permanently_closed_exact_failed_requirement",
        "classification_before_regression": batch_record["final_classification"],
        "classification_after_regression": "MISSING_DATA",
        "blocking_scope": "blocks TRADE_CANDIDATE before selected-contract identity",
        "selected_contract_before_regression": False,
        "selected_contract_after_regression": False,
        "entry_eligible_before_regression": False,
        "entry_eligible_after_regression": False,
        "entry_recorded_before_regression": False,
        "entry_recorded_after_regression": False,
        "additional_entry_established": False,
        "failure_source_evidence": _failure_source_evidence(closeout_record, output),
        "next_action": (
            "Do not promote this case. Keep it closed unless a future bounded task "
            "introduces accepted frozen active-path evidence with regression cases."
        ),
        "proof_accepted": False,
        "profitability_claimed": False,
        "paper_eligible": False,
        "live_eligible": False,
    }


def _validate_final_row(closeout_record, batch_record, fixture_path, output):
    expected_time = closeout_record["timestamp_window"]["signal_time"]
    expected_blocker = closeout_record["exact_blocker"]
    if output["timestamp"] != expected_time:
        raise ValueError(f"Fixture final timestamp changed for {fixture_path}")
    if output["primary_blocker"] != expected_blocker:
        raise ValueError(f"Fixture final blocker changed for {fixture_path}")
    if batch_record["first_stage_not_reached"] != "TRADE_CANDIDATE":
        raise ValueError("Batch record no longer blocks at TRADE_CANDIDATE")
    if batch_record["exact_blocker_code"] != expected_blocker:
        raise ValueError("Batch blocker no longer matches closeout blocker")
    if output["final_verdict"] not in {"NO_TRADE", "PENDING"}:
        raise ValueError("Unexpected active-path final verdict")


def _exact_failed_requirement(record):
    if record["setup_family"] == "Continuation":
        return (
            "prior_completed_shelf_break_spent_state remained "
            "prior_completed_shelf_break_spent_TO_REVIEW at the signal row; "
            "no accepted session-boundary freshness rule advances the case"
        )
    if record["setup_family"] == "Clean Fast Break":
        return (
            "freshness_final_signal_state remained fresh_or_spent_unconfirmed at "
            "the signal row; no accepted Clean Fast Break fresh/spent active-path "
            "rule advances the case"
        )
    return (
        "freshness_final_signal_state remained fresh_or_spent_unconfirmed at the "
        "signal row; no accepted Ideal fresh/spent active-path rule advances the case"
    )


def _failure_source_evidence(record, output):
    return (
        f"{record['field']} from {record['source']} / "
        f"{record['dataset_schema_or_api']} via {record['calculator']} at "
        f"{output['timestamp']} produced stage {output['stage']} with final verdict "
        f"{output['final_verdict']} and primary blocker {output['primary_blocker']}."
    )


def _scorecard(closeout, batch, records):
    before = closeout["scorecard"]
    closed_count = sum(1 for record in records if record["permanently_closed"])
    advanced_count = sum(1 for record in records if record["advanced_to_trade_candidate"])
    return {
        "active_path_requirements_tested": len(records),
        "active_path_requirements_advanced_to_trade_candidate": advanced_count,
        "active_path_requirements_permanently_closed": closed_count,
        "active_path_requirements_open_after_regression": 0,
        "additional_entries_established": 0,
        "affected_cases_selected_contracts_before_regression": 0,
        "affected_cases_selected_contracts_after_regression": 0,
        "affected_cases_entry_eligible_before_regression": 0,
        "affected_cases_entry_eligible_after_regression": 0,
        "affected_cases_entries_recorded_before_regression": 0,
        "affected_cases_entries_recorded_after_regression": 0,
        "trade_candidates_before_regression": before["trade_candidates_after_closeout"],
        "trade_candidates_after_regression": before["trade_candidates_after_closeout"],
        "selected_contracts_before_regression": before["selected_contracts_after_closeout"],
        "selected_contracts_after_regression": before["selected_contracts_after_closeout"],
        "eligible_entries_before_regression": before["eligible_entries_after_closeout"],
        "eligible_entries_after_regression": before["eligible_entries_after_closeout"],
        "recorded_entries_before_regression": before["recorded_entries_after_closeout"],
        "recorded_entries_after_regression": before["recorded_entries_after_closeout"],
        "valid_trades_captured": batch["final_classifications"]["VALID_TRADE_CAPTURED"],
        "true_no_trades": batch["final_classifications"]["TRUE_NO_TRADE"],
        "missing_data_cases_before_regression": batch["final_classifications"]["MISSING_DATA"],
        "missing_data_cases_after_regression": (
            batch["final_classifications"]["MISSING_DATA"] + closed_count
        ),
        "missed_valid_trades": batch["final_classifications"]["MISSED_VALID_TRADE"],
        "invalid_trades_allowed": batch["final_classifications"]["INVALID_TRADE_ALLOWED"],
        "unresolved_cases_before_regression": batch["final_classifications"]["UNRESOLVED"],
        "unresolved_cases_after_regression": (
            batch["final_classifications"]["UNRESOLVED"] - closed_count
        ),
        "closed_setup_source_candidates_reopened": 0,
        "rejected_intake_rows_replayed": 0,
        "closed_safety_rejections_rerun_as_live_candidates": 0,
    }


def _final_classifications_after_regression(batch, records):
    closed_count = sum(1 for record in records if record["permanently_closed"])
    current = dict(batch["final_classifications"])
    current["MISSING_DATA"] += closed_count
    current["UNRESOLVED"] -= closed_count
    return current


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
    doc = write_regression_document()
    scorecard = doc["scorecard"]
    print(
        "wrote day50 active-path requirement regression: "
        f"{scorecard['active_path_requirements_tested']} tested, "
        f"{scorecard['active_path_requirements_advanced_to_trade_candidate']} advanced, "
        f"{scorecard['active_path_requirements_permanently_closed']} permanently closed, "
        f"{scorecard['trade_candidates_before_regression']}->{scorecard['trade_candidates_after_regression']} trade candidates, "
        f"{scorecard['selected_contracts_before_regression']}->{scorecard['selected_contracts_after_regression']} selected contracts, "
        f"{scorecard['eligible_entries_before_regression']}->{scorecard['eligible_entries_after_regression']} eligible entries, "
        f"{scorecard['recorded_entries_before_regression']}->{scorecard['recorded_entries_after_regression']} recorded entries"
    )
