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
EXPECTED_TRIGGER = "668.360000000"
EXPECTED_INVALIDATION = "667.870000000"


def validate_result_document(result_path=RESULT_PATH):
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    problems = []

    if result.get("result_version") != "day52_full_session_recognition_manifest_v2":
        problems.append("unexpected_result_version")
    if result.get("implementation_version") != "day52_full_session_recognition_manifest_impl_v2":
        problems.append("unexpected_implementation_version")

    scope = result.get("scope", {})
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

    numeric = result.get("numeric_trigger_invalidation_reference", {})
    if numeric.get("result_version") != "day52_numeric_trigger_invalidation_v2":
        problems.append("unexpected_numeric_result_version")
    summary = numeric.get("summary", {})
    if summary.get("numeric_values_established") != 6:
        problems.append("numeric_values_established_not_6")
    if summary.get("numeric_values_unresolved") != 0:
        problems.append("numeric_values_unresolved_not_0")
    if summary.get("setup_qualified_allowed_count") != 3:
        problems.append("setup_qualified_allowed_not_3")

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
        if session.get("strict_no_trade_behavior", {}).get("trade_candidates") != 0:
            problems.append("trade_candidates_nonzero")
        counts = session.get("counts_by_setup_family_and_final_disposition", {})
        if set(counts) != EXPECTED_FAMILIES:
            problems.append("unexpected_count_family_set")
        for family, family_counts in counts.items():
            if family_counts.get("rejected") != 389:
                problems.append(f"{family}_rejected_count_not_389")
            if family_counts.get("duplicate") != 361:
                problems.append(f"{family}_duplicate_count_not_361")
            if family_counts.get("blocked by missing evidence") != 0:
                problems.append(f"{family}_blocked_count_not_0")
            if family == "Clean Fast Break":
                if family_counts.get("selected winner") != 1:
                    problems.append("clean_fast_break_selected_winner_not_1")
            elif family_counts.get("suppressed") != 1:
                problems.append(f"{family}_suppressed_not_1")
        records.extend(session.get("recognition_records", []))

    if len(records) != 2253:
        problems.append(f"expected_2253_records_got_{len(records)}")
    if {record.get("setup_family") for record in records} != EXPECTED_FAMILIES:
        problems.append("unexpected_record_family_set")
    if any(record.get("no_hindsight_cutoff") != record.get("observation_timestamp_utc") for record in records):
        problems.append("no_hindsight_cutoff_mismatch")
    if any(record.get("stage_contract_predicates", {}).get("illegal_stage_skipping_detected") for record in records):
        problems.append("illegal_stage_skipping_detected")

    primary_setup = [
        record
        for record in records
        if record.get("observation_timestamp_utc") == "2026-03-16T13:30:00Z"
        and record.get("duplicate_sequence") == 0
    ]
    if len(primary_setup) != 3:
        problems.append("expected_three_primary_setup_records")
    for record in primary_setup:
        if record.get("stage_contract_predicates", {}).get("setup_qualified_predicate_passed") is not True:
            problems.append("primary_setup_record_not_setup_qualified")
        if record.get("missing_required_evidence") != []:
            problems.append("primary_setup_missing_evidence_not_empty")
        trigger = record.get("trigger") or {}
        invalidation = record.get("invalidation") or {}
        if trigger.get("numeric_value") != EXPECTED_TRIGGER:
            problems.append("unexpected_trigger")
        if invalidation.get("numeric_value") != EXPECTED_INVALIDATION:
            problems.append("unexpected_invalidation")

    accounting = result.get("complete_session_accounting", {})
    expected_accounting = {
        "sessions_scanned": 1,
        "rows_scanned": 751,
        "recognition_records": 2253,
        "primary_timestamp_family_records": 1170,
        "duplicate_records": 1083,
        "rejected_records": 1167,
        "blocked_missing_evidence_records": 0,
        "setup_qualified_records": 3,
        "selected_winner_records": 1,
        "suppressed_records": 2,
        "recognition_layer_executable_records": 1,
        "trade_candidates": 0,
        "selected_contracts": 0,
        "eligible_entries": 0,
        "recorded_entries": 0,
    }
    for key, expected in expected_accounting.items():
        if accounting.get(key) != expected:
            problems.append(f"{key}_expected_{expected}_got_{accounting.get(key)}")

    bias = result.get("known_window_bias_exposure", {})
    if bias.get("known_window_primary_records") != 3:
        problems.append("known_window_primary_count_changed")
    if bias.get("known_window_only_would_omit_primary_records") != 1167:
        problems.append("known_window_bias_omitted_count_changed")
    if bias.get("known_window_records_setup_qualified_after_numeric_promotion") != 3:
        problems.append("known_window_setup_qualified_count_not_3")

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
