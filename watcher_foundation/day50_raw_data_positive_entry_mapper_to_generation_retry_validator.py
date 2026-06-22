import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_raw_data_positive_entry_mapper_to_generation_retry.json"
)


def validate_result_document(result_path=RESULT_PATH):
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    problems = []

    if result.get("result_version") != "day50_raw_data_positive_entry_mapper_to_generation_retry_v1":
        problems.append("unexpected_result_version")

    policy = result.get("retry_policy", {})
    for field in (
        "bounded_to_day50_spy_2026_03_16",
        "processes_each_setup_family_separately",
        "setup_time_boundary_frozen",
        "no_hindsight_preserved",
        "session_boundary_preserved",
        "developing_stage_transitions_validated",
        "stable_winner_selection_preserved",
        "no_trade_preservation_validated",
    ):
        if not policy.get(field):
            problems.append(f"{field}_not_true")
    for field in (
        "raw_vendor_bars_treated_as_safe_fast_labels",
        "frozen_trading_rules_changed",
        "thresholds_loosened",
        "missing_fields_invented",
        "option_evidence_invented",
        "main_py_changed",
        "railway_or_deploy_changed",
        "paid_data_downloaded",
    ):
        if policy.get(field):
            problems.append(f"{field}_true")

    records = result.get("setup_family_retry_records", [])
    if len(records) != 3:
        problems.append("expected_three_retry_records")
    if {record.get("setup_family") for record in records} != {
        "Ideal",
        "Clean Fast Break",
        "Continuation",
    }:
        problems.append("unexpected_setup_family_set")

    for record in records:
        family = record.get("setup_family")
        stages = record.get("stage_reached", {})
        if not stages.get("mapped_package"):
            problems.append(f"{family}_mapped_package_not_reached")
        for stage in (
            "generated_candidate",
            "setup_qualified",
            "trade_candidate",
            "selected_contract",
            "eligible_entry",
            "recorded_entry",
        ):
            if stages.get(stage):
                problems.append(f"{family}_{stage}_unexpectedly_reached")
        if record.get("first_stage_not_reached") != "generated_candidate":
            problems.append(f"{family}_unexpected_first_stage_not_reached")
        if record.get("failure_category") != "accepted_mapper_package_review_only_not_generation_input":
            problems.append(f"{family}_unexpected_failure_category")
        if record.get("raw_vendor_bars_treated_as_safe_fast_labels"):
            problems.append(f"{family}_raw_vendor_label_used")
        if record.get("costed_entry_exit_replay_status") != "NOT_RUN_NO_TRADE_CANDIDATE":
            problems.append(f"{family}_unexpected_costed_replay_status")

    after = result.get("after_funnel_totals", {})
    expected_after = {
        "raw_opportunities_mapped": 3,
        "exact_setup_time_field_packages_established": 3,
        "new_generated_candidates": 0,
        "new_setup_qualified_candidates": 0,
        "new_trade_candidates": 0,
        "new_selected_contracts": 0,
        "new_eligible_entries": 0,
        "new_recorded_entries": 0,
        "new_exact_generation_contract_required_cases": 3,
        "new_exact_data_required_cases": 0,
        "new_valid_trades_captured": 0,
        "new_true_no_trades": 0,
        "new_missed_valid_trades": 0,
        "new_invalid_trades_allowed": 0,
        "new_unresolved_cases": 0,
        "new_winners": 0,
        "new_losers": 0,
    }
    for key, expected in expected_after.items():
        if after.get(key) != expected:
            problems.append(f"{key}_expected_{expected}_got_{after.get(key)}")

    if result.get("accepted_mapper_regression_case_count") != 17:
        problems.append("accepted_mapper_regression_case_count_not_17")
    if any(case.get("status") != "PASS" for case in result.get("accepted_mapper_regression_cases", [])):
        problems.append("accepted_mapper_case_not_pass")
    if result.get("deterministic_comparison", {}).get("result") != "PASS":
        problems.append("determinism_not_pass")
    if result.get("exact_grouped_evidence_request", {}).get("created"):
        problems.append("unexpected_option_or_exit_evidence_request")

    controls = result.get("preserved_day50_controls", {})
    if controls != {
        "setup_qualified": 13,
        "trade_candidates": 9,
        "selected_contracts": 5,
        "eligible_entries": 1,
        "recorded_entries": 1,
        "closed_safety_rejections_reopened": 0,
    }:
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
        "retry_records": len(records),
        "generated_candidates": after.get("new_generated_candidates"),
        "trade_candidates": after.get("new_trade_candidates"),
    }


if __name__ == "__main__":
    validation = validate_result_document()
    print(json.dumps(validation, indent=2, sort_keys=True))
    if validation["problems"]:
        raise SystemExit(1)
