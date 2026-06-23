import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day52_full_session_recognition_manifest.json"
)

EXPECTED_FAMILIES = {"Ideal", "Clean Fast Break", "Continuation"}
EXPECTED_DISPOSITIONS = {
    "rejected",
    "developing at session end",
    "setup-qualified",
    "duplicate",
    "suppressed",
    "selected winner",
    "blocked by missing evidence",
    "recognition-layer executable",
}
REQUIRED_SETUP_QUALIFIED_FIELDS = {
    "setup_time_row",
    "numeric_trigger",
    "numeric_invalidation",
    "freshness_final_signal_state",
    "blocker_caution_review",
    "session_boundary_behavior",
    "no_hindsight_boundary",
}
EXPECTED_NUMERIC_BLOCKERS = {
    "Ideal": {
        "trigger": "NUMERIC_RULE_UNRESOLVED_IDEAL_TRIGGER",
        "invalidation": "NUMERIC_RULE_UNRESOLVED_IDEAL_INVALIDATION",
        "combined": "NUMERIC_RULE_UNRESOLVED_IDEAL_TRIGGER__NUMERIC_RULE_UNRESOLVED_IDEAL_INVALIDATION",
    },
    "Clean Fast Break": {
        "trigger": "NUMERIC_RULE_UNRESOLVED_CLEAN_FAST_BREAK_TRIGGER",
        "invalidation": "NUMERIC_RULE_UNRESOLVED_CLEAN_FAST_BREAK_INVALIDATION",
        "combined": "NUMERIC_RULE_UNRESOLVED_CLEAN_FAST_BREAK_TRIGGER__NUMERIC_RULE_UNRESOLVED_CLEAN_FAST_BREAK_INVALIDATION",
    },
    "Continuation": {
        "trigger": "NUMERIC_RULE_UNRESOLVED_CONTINUATION_TRIGGER",
        "invalidation": "NUMERIC_RULE_UNRESOLVED_CONTINUATION_INVALIDATION",
        "combined": "NUMERIC_RULE_UNRESOLVED_CONTINUATION_TRIGGER__NUMERIC_RULE_UNRESOLVED_CONTINUATION_INVALIDATION",
    },
}


def validate_result_document(result_path=RESULT_PATH):
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    problems = []

    if result.get("result_version") != "day52_full_session_recognition_manifest_v1":
        problems.append("unexpected_result_version")
    if result.get("implementation_version") != "day52_full_session_recognition_manifest_impl_v1":
        problems.append("unexpected_implementation_version")

    scope = result.get("scope", {})
    if scope.get("layer") != "underlying_recognition_and_lifecycle_only":
        problems.append("unexpected_scope_layer")
    for field in (
        "option_contract_selection",
        "entry_exit_costs_or_net_result",
        "paid_data_downloaded",
        "main_py_changed",
        "railway_or_deploy_changed",
        "broker_account_order_fill_alert_touched",
        "credentials_or_env_changed",
        "sizing_changed",
        "frozen_patch8_thresholds_changed",
    ):
        if scope.get(field):
            problems.append(f"{field}_true")
    if scope.get("profitability_proof") != "NO":
        problems.append("profitability_proof_not_no")
    if scope.get("paper_live_eligibility") != "NO":
        problems.append("paper_live_eligibility_not_no")

    metadata = result.get("reproducibility_metadata", {})
    if metadata.get("dataset") != "DBEQ.BASIC":
        problems.append("unexpected_dataset")
    if metadata.get("schema") != "ohlcv-1m":
        problems.append("unexpected_schema")
    if metadata.get("symbol") != "SPY":
        problems.append("unexpected_symbol")
    if metadata.get("source_row_count") != 751:
        problems.append("unexpected_source_row_count")
    if metadata.get("missing_intervals") != []:
        problems.append("unexpected_missing_intervals")
    if not metadata.get("frozen_rule_configuration_hash"):
        problems.append("missing_rule_hash")
    if not metadata.get("source_file_hashes"):
        problems.append("missing_source_file_hashes")

    contracts = result.get("stage_contracts", {})
    if set(contracts.get("allowed_final_dispositions", [])) != EXPECTED_DISPOSITIONS:
        problems.append("unexpected_allowed_dispositions")
    transition = contracts.get("transitions", {}).get("setup_time_fields_to_setup_qualified", {})
    if set(transition.get("required_fields", [])) != REQUIRED_SETUP_QUALIFIED_FIELDS:
        problems.append("setup_qualified_required_fields_changed")
    if transition.get("blocker_code") != "family_field_specific_numeric_rule_unresolved":
        problems.append("unexpected_setup_qualified_blocker_code")

    numeric_ref = result.get("numeric_trigger_invalidation_reference", {})
    if numeric_ref.get("result_version") != "day52_numeric_trigger_invalidation_v1":
        problems.append("missing_numeric_trigger_invalidation_reference")
    if numeric_ref.get("deterministic_result") != "PASS":
        problems.append("numeric_trigger_invalidation_determinism_not_pass")
    numeric_summary = numeric_ref.get("summary", {})
    if numeric_summary.get("numeric_values_established") != 0:
        problems.append("numeric_values_established_unexpected")
    if numeric_summary.get("numeric_values_unresolved") != 6:
        problems.append("expected_six_numeric_values_unresolved")

    sessions = result.get("sessions", [])
    if len(sessions) != 1:
        problems.append("expected_one_session")
    records = []
    for session in sessions:
        if session.get("symbol") != "SPY":
            problems.append("session_symbol_not_spy")
        if session.get("session_date") != "2026-03-16":
            problems.append("session_date_not_march16")
        if session.get("source_row_count") != 751:
            problems.append("session_source_row_count_not_751")
        if session.get("unique_timestamp_count") != 390:
            problems.append("session_unique_timestamp_count_not_390")
        coverage = session.get("coverage", {})
        if coverage.get("start_timestamp_utc") != "2026-03-16T13:30:00Z":
            problems.append("unexpected_session_start")
        if coverage.get("end_timestamp_utc") != "2026-03-16T19:59:00Z":
            problems.append("unexpected_session_end")
        if coverage.get("complete_expected_rth_minute_coverage") is not True:
            problems.append("incomplete_rth_coverage")
        records.extend(session.get("recognition_records", []))
        counts = session.get("counts_by_setup_family_and_final_disposition", {})
        if set(counts) != EXPECTED_FAMILIES:
            problems.append("unexpected_count_family_set")
        for family, family_counts in counts.items():
            if family_counts.get("blocked by missing evidence") != 1:
                problems.append(f"{family}_blocked_count_not_1")
            if family_counts.get("rejected") != 389:
                problems.append(f"{family}_rejected_count_not_389")
            if family_counts.get("duplicate") != 361:
                problems.append(f"{family}_duplicate_count_not_361")
            for disposition in ("setup-qualified", "selected winner", "suppressed"):
                if family_counts.get(disposition) != 0:
                    problems.append(f"{family}_{disposition}_unexpected")

    if len(records) != 2253:
        problems.append(f"expected_2253_records_got_{len(records)}")
    if {record.get("setup_family") for record in records} != EXPECTED_FAMILIES:
        problems.append("unexpected_record_family_set")
    if any(record.get("final_disposition") not in EXPECTED_DISPOSITIONS for record in records):
        problems.append("unknown_final_disposition")
    if any(record.get("no_hindsight_cutoff") != record.get("observation_timestamp_utc") for record in records):
        problems.append("no_hindsight_cutoff_mismatch")
    if any(record.get("final_disposition") == "setup-qualified" for record in records):
        problems.append("setup_qualified_invented_despite_numeric_gap")
    if any(record.get("final_disposition") == "selected winner" for record in records):
        problems.append("selected_winner_invented_despite_numeric_gap")
    illegal_skips = [
        record.get("candidate_id")
        for record in records
        if record.get("stage_contract_predicates", {}).get("illegal_stage_skipping_detected")
    ]
    if illegal_skips:
        problems.append("illegal_stage_skipping_detected")
    blocked = [
        record for record in records
        if record.get("final_disposition") == "blocked by missing evidence"
    ]
    if len(blocked) != 3:
        problems.append("expected_three_blocked_known_setup_records")
    for record in blocked:
        if record.get("observation_timestamp_utc") != "2026-03-16T13:30:00Z":
            problems.append("blocked_record_not_at_known_setup_time")
        if record.get("missing_required_evidence") != ["numeric_trigger", "numeric_invalidation"]:
            problems.append("blocked_record_missing_evidence_changed")
        family = record.get("setup_family")
        expected = EXPECTED_NUMERIC_BLOCKERS.get(family, {})
        if record.get("exact_rejection_or_blocker_code") != expected.get("combined"):
            problems.append("blocked_record_reason_changed")
        trigger = record.get("trigger") or {}
        invalidation = record.get("invalidation") or {}
        if trigger.get("blocker_code") != expected.get("trigger"):
            problems.append(f"{family}_trigger_blocker_changed")
        if invalidation.get("blocker_code") != expected.get("invalidation"):
            problems.append(f"{family}_invalidation_blocker_changed")
        if trigger.get("numeric_value") is not None or invalidation.get("numeric_value") is not None:
            problems.append("blocked_record_invented_numeric_trigger_or_invalidation")

    review = result.get("setup_time_review_output", {})
    if review.get("post_cutoff_fields_excluded") is not True:
        problems.append("setup_time_review_not_cutoff_limited")
    review_records = review.get("records", [])
    if len(review_records) != 3:
        problems.append("expected_three_setup_time_review_records")
    forbidden_review_fields = {
        "future_high",
        "future_low",
        "later_favorable_move",
        "selected_contract",
        "entry",
        "exit",
        "pnl",
        "net_pnl",
    }
    for record in review_records:
        if forbidden_review_fields.intersection(record):
            problems.append("setup_time_review_leaks_future_or_economic_field")
        if record.get("post_cutoff_fields_excluded") is not True:
            problems.append("setup_time_review_record_not_cutoff_limited")

    accounting = result.get("complete_session_accounting", {})
    expected_accounting = {
        "sessions_scanned": 1,
        "rows_scanned": 751,
        "recognition_records": 2253,
        "primary_timestamp_family_records": 1170,
        "duplicate_records": 1083,
        "rejected_records": 1167,
        "blocked_missing_evidence_records": 3,
    }
    for key, expected in expected_accounting.items():
        if accounting.get(key) != expected:
            problems.append(f"{key}_expected_{expected}_got_{accounting.get(key)}")

    bias = result.get("known_window_bias_exposure", {})
    if bias.get("known_window_primary_records") != 3:
        problems.append("known_window_primary_count_changed")
    if bias.get("complete_session_primary_records") != 1170:
        problems.append("complete_session_primary_count_changed")
    if bias.get("known_window_only_would_omit_primary_records") != 1167:
        problems.append("known_window_bias_omitted_count_changed")
    if bias.get("bias_exposed") is not True:
        problems.append("known_window_bias_not_exposed")

    determinism = result.get("determinism_protection", {})
    if determinism.get("result") != "PASS":
        problems.append("determinism_not_pass")
    for field in (
        "repeated_runs_identical",
        "candidate_input_order_invariance",
        "replay_chunk_size_invariance",
        "timestamp_preserving_input_reorder_invariance",
        "session_boundary_split_recombination_invariance",
        "winner_selection_independent_of_insertion_order",
    ):
        if determinism.get(field) is not True:
            problems.append(f"{field}_not_true")

    guardrails = result.get("guardrails", {})
    for field in (
        "opra_required_for_layer_1",
        "missing_evidence_converted_to_confidence",
        "future_rows_used_for_setup_time_fields",
        "same_bar_future_information_used",
        "profitability_claimed",
        "promotion_decision_made",
        "paper_eligible",
        "live_eligible",
    ):
        if guardrails.get(field):
            problems.append(f"{field}_true")

    return {
        "status": "PASS" if not problems else "FAIL",
        "problems": problems,
        "sessions_scanned": accounting.get("sessions_scanned"),
        "rows_scanned": accounting.get("rows_scanned"),
        "recognition_records": accounting.get("recognition_records"),
        "counts_by_setup_family_and_final_disposition": (
            sessions[0].get("counts_by_setup_family_and_final_disposition", {})
            if sessions
            else {}
        ),
    }


if __name__ == "__main__":
    validation = validate_result_document()
    print(json.dumps(validation, indent=2, sort_keys=True))
    if validation["problems"]:
        raise SystemExit(1)
