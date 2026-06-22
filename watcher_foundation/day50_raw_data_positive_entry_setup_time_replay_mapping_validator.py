import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_raw_data_positive_entry_setup_time_replay_mapping.json"
)


def validate_result_document(result_path=RESULT_PATH):
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    problems = []

    if result.get("deterministic_comparison", {}).get("result") != "PASS":
        problems.append("deterministic_comparison_not_pass")

    if result.get("request_id") != "DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M":
        problems.append("unexpected_request_id")

    source_summary = result.get("source_summary", {})
    if source_summary.get("row_count") != 751:
        problems.append("unexpected_source_row_count")
    if source_summary.get("symbol_set") != ["SPY"]:
        problems.append("unexpected_source_symbol_set")
    if not source_summary.get("complete_chronological_rows"):
        problems.append("source_rows_not_chronological")
    if not source_summary.get("required_columns_present"):
        problems.append("source_required_columns_missing")

    policy = result.get("mapping_policy", {})
    if not policy.get("used_only_acquired_day50_spy_underlying_evidence"):
        problems.append("mapping_used_wrong_evidence_scope")
    if policy.get("requested_more_data"):
        problems.append("more_data_requested")
    if policy.get("requested_option_data"):
        problems.append("option_data_requested")
    if policy.get("requested_exit_path_data"):
        problems.append("exit_path_data_requested")
    if policy.get("raw_vendor_bars_treated_as_safe_fast_labels"):
        problems.append("raw_vendor_bars_treated_as_labels")
    if policy.get("frozen_rules_changed"):
        problems.append("frozen_rules_changed")
    if policy.get("main_py_changed") or policy.get("railway_or_deploy_changed"):
        problems.append("forbidden_file_scope_changed")

    records = result.get("setup_family_mapping_records", [])
    if len(records) != 3:
        problems.append("expected_three_setup_family_records")

    families = {record.get("setup_family") for record in records}
    if families != {"Ideal", "Clean Fast Break", "Continuation"}:
        problems.append("unexpected_setup_family_records")

    required_fields = {
        "setup_time_row",
        "trigger",
        "invalidation",
        "freshness_final_signal_state",
        "blocker_caution_review",
        "session_boundary_behavior",
        "no_hindsight_boundary",
    }
    for record in records:
        if record.get("exact_setup_time_fields_established"):
            problems.append(f"{record.get('setup_family')}_unexpectedly_established_fields")
        if record.get("candidate_generated"):
            problems.append(f"{record.get('setup_family')}_unexpected_candidate_generated")
        if record.get("exclusion_reason") != "accepted_setup_time_replay_mapping_path_absent":
            problems.append(f"{record.get('setup_family')}_unexpected_exclusion_reason")
        if set(record.get("exact_failed_fields", [])) != required_fields:
            problems.append(f"{record.get('setup_family')}_failed_fields_incomplete")
        blockers = record.get("field_blockers", {})
        if set(blockers) != required_fields:
            problems.append(f"{record.get('setup_family')}_field_blockers_incomplete")
        for field, blocker in blockers.items():
            if blocker.get("exact_field") != field:
                problems.append(f"{record.get('setup_family')}_{field}_blocker_field_mismatch")
            if not blocker.get("exact_source"):
                problems.append(f"{record.get('setup_family')}_{field}_missing_source")
            if not blocker.get("exact_dataset_schema_api_calculator"):
                problems.append(f"{record.get('setup_family')}_{field}_missing_calculator")
            if not blocker.get("exact_reason_unavailable"):
                problems.append(f"{record.get('setup_family')}_{field}_missing_unavailable_reason")

    scorecard = result.get("new_candidate_scorecard", {})
    if scorecard.get("raw_opportunities_mapped") != 3:
        problems.append("raw_opportunities_mapped_not_three")
    for field in (
        "exact_setup_time_fields_established",
        "new_generated_candidates",
        "new_setup_qualified_candidates",
        "new_trade_candidates",
        "new_selected_contracts",
        "new_price_accepted_candidates",
        "new_eligible_entries",
        "new_recorded_entries",
        "new_exits_evaluated",
        "new_valid_trades_captured",
        "new_true_no_trades",
        "new_missed_valid_trades",
        "new_invalid_trades_allowed",
        "new_unresolved_cases",
        "new_winners",
        "new_losers",
    ):
        if scorecard.get(field) != 0:
            problems.append(f"{field}_not_zero")
    if scorecard.get("new_exact_data_required_cases") != 3:
        problems.append("new_exact_data_required_cases_not_three")

    guardrails = result.get("guardrails", {})
    for field in (
        "schwab_authenticated",
        "broker_mutation_attempted",
        "proof_accepted",
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
        "raw_opportunities_mapped": scorecard.get("raw_opportunities_mapped"),
        "new_setup_qualified_candidates": scorecard.get("new_setup_qualified_candidates"),
        "new_trade_candidates": scorecard.get("new_trade_candidates"),
    }


if __name__ == "__main__":
    validation = validate_result_document()
    print(json.dumps(validation, indent=2, sort_keys=True))
    if validation["problems"]:
        raise SystemExit(1)
