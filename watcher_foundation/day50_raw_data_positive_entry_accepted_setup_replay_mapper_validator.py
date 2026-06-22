import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_raw_data_positive_entry_accepted_setup_replay_mapper.json"
)


def validate_result_document(result_path=RESULT_PATH):
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    problems = []

    if result.get("result_version") != "day50_raw_data_positive_entry_accepted_setup_replay_mapper_v1":
        problems.append("unexpected_result_version")
    if result.get("request_id") != "DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M":
        problems.append("unexpected_request_id")
    if result.get("dataset_schema_stype") != "DBEQ.BASIC / ohlcv-1m / raw_symbol":
        problems.append("unexpected_dataset_schema_stype")

    policy = result.get("mapper_policy", {})
    if not policy.get("bounded_to_day50_spy_2026_03_16"):
        problems.append("mapper_not_bounded_to_day50_spy")
    if policy.get("raw_vendor_bars_treated_as_safe_fast_labels"):
        problems.append("raw_vendor_bars_treated_as_labels")
    if not policy.get("raw_vendor_label_input_rejected"):
        problems.append("raw_vendor_label_rejection_missing")
    for field in (
        "frozen_trading_rules_changed",
        "requested_more_data",
        "requested_option_data",
        "requested_exit_path_data",
        "main_py_changed",
        "railway_or_deploy_changed",
    ):
        if policy.get(field):
            problems.append(f"{field}_true")

    summary = result.get("source_summary", {})
    if summary.get("row_count") != 751:
        problems.append("unexpected_row_count")
    if summary.get("collapsed_minute_count") != 390:
        problems.append("unexpected_collapsed_minute_count")
    if summary.get("symbol_set") != ["SPY"]:
        problems.append("unexpected_symbol_set")
    if not summary.get("complete_chronological_rows"):
        problems.append("source_not_chronological")
    if not summary.get("required_columns_present"):
        problems.append("required_columns_missing")

    required_fields = {
        "setup_time_row",
        "trigger",
        "invalidation",
        "freshness_final_signal_state",
        "blocker_caution_review",
        "session_boundary_behavior",
        "no_hindsight_boundary",
    }
    packages = result.get("setup_family_field_packages", [])
    if len(packages) != 3:
        problems.append("expected_three_field_packages")
    families = {package.get("setup_family") for package in packages}
    if families != {"Ideal", "Clean Fast Break", "Continuation"}:
        problems.append("unexpected_setup_families")
    for package in packages:
        if package.get("status") != "FIELD_PACKAGE_ESTABLISHED_REVIEW_ONLY":
            problems.append(f"{package.get('setup_family')}_unexpected_status")
        if package.get("candidate_generated") or package.get("setup_qualified") or package.get("trade_candidate"):
            problems.append(f"{package.get('setup_family')}_unexpected_candidate_or_trade_stage")
        if package.get("raw_vendor_bars_treated_as_safe_fast_labels"):
            problems.append(f"{package.get('setup_family')}_raw_vendor_label_used")
        fields = package.get("fields", {})
        if set(fields) != required_fields:
            problems.append(f"{package.get('setup_family')}_field_package_incomplete")
        for field_name, field in fields.items():
            if not field.get("source_rule_path"):
                problems.append(f"{package.get('setup_family')}_{field_name}_missing_rule_path")
            if "raw" in field.get("source_boundary", "").lower() and "not" not in field.get("source_boundary", "").lower():
                problems.append(f"{package.get('setup_family')}_{field_name}_raw_boundary_ambiguous")

    scorecard = result.get("after_funnel_totals", {})
    if scorecard.get("raw_opportunities_mapped") != 3:
        problems.append("raw_opportunities_mapped_not_three")
    if scorecard.get("exact_setup_time_field_packages_established") != 3:
        problems.append("field_packages_not_three")
    for zero_field in (
        "new_generated_candidates",
        "new_setup_qualified_candidates",
        "new_trade_candidates",
        "new_selected_contracts",
        "new_eligible_entries",
        "new_recorded_entries",
        "new_valid_trades_captured",
        "new_true_no_trades",
        "new_missed_valid_trades",
        "new_invalid_trades_allowed",
        "new_unresolved_cases",
        "new_winners",
        "new_losers",
    ):
        if scorecard.get(zero_field) != 0:
            problems.append(f"{zero_field}_not_zero")

    cases = result.get("regression_case_results", [])
    required_case_ids = {
        "DAY50-SPY-IDEAL-POSITIVE-MAPPING",
        "DAY50-SPY-CFB-POSITIVE-MAPPING",
        "DAY50-SPY-CONTINUATION-POSITIVE-MAPPING",
        "DAY50-SPY-MISSING-SETUP-TIME-ROW",
        "DAY50-SPY-MISSING-OR-AMBIGUOUS-TRIGGER",
        "DAY50-SPY-MISSING-OR-AMBIGUOUS-INVALIDATION",
        "DAY50-SPY-MISSING-FRESHNESS-FINAL-SIGNAL",
        "DAY50-SPY-MISSING-BLOCKER-CAUTION",
        "DAY50-SPY-SAME-SESSION-BOUNDARY",
        "DAY50-SPY-PRIOR-SESSION-CONTAMINATION",
        "DAY50-SPY-NO-HINDSIGHT",
        "DAY50-SPY-WRONG-SYMBOL",
        "DAY50-SPY-WRONG-WINDOW",
        "DAY50-SPY-DUPLICATE-HANDLING",
        "DAY50-SPY-RAW-VENDOR-LABEL-REJECTION",
        "DAY50-SPY-DETERMINISM",
        "DAY50-SPY-CONTROL-PRESERVATION",
    }
    actual_case_ids = {case.get("case_id") for case in cases}
    if actual_case_ids != required_case_ids:
        problems.append("regression_case_coverage_mismatch")
    for case in cases:
        if case.get("status") != "PASS":
            problems.append(f"{case.get('case_id')}_not_pass")

    if result.get("deterministic_comparison", {}).get("result") != "PASS":
        problems.append("determinism_not_pass")

    controls = result.get("preserved_day50_controls", {})
    expected_controls = {
        "setup_qualified": 13,
        "trade_candidates": 9,
        "selected_contracts": 5,
        "eligible_entries": 1,
        "recorded_entries": 1,
        "closed_safety_rejections_reopened": 0,
    }
    if controls != expected_controls:
        problems.append("preserved_controls_changed")

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
        "field_packages": scorecard.get("exact_setup_time_field_packages_established"),
        "regression_cases": len(cases),
    }


if __name__ == "__main__":
    validation = validate_result_document()
    print(json.dumps(validation, indent=2, sort_keys=True))
    if validation["problems"]:
        raise SystemExit(1)
