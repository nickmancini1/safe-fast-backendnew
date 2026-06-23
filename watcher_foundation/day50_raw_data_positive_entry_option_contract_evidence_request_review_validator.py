import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_raw_data_positive_entry_option_contract_evidence_request_review.json"
)


def validate_result_document(result_path=RESULT_PATH):
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    problems = []

    if (
        result.get("result_version")
        != "day50_raw_data_positive_entry_option_contract_evidence_request_review_v1"
    ):
        problems.append("unexpected_result_version")

    scope = result.get("execution_scope", {})
    for field in (
        "bounded_to_day50_spy_2026_03_16",
        "local_option_evidence_only",
        "processes_each_setup_family_separately",
    ):
        if not scope.get(field):
            problems.append(f"{field}_not_true")
    for field in (
        "paid_data_downloaded",
        "external_cost_api_called",
        "main_py_changed",
        "railway_or_deploy_changed",
        "broker_or_account_or_order_touched",
        "credentials_or_env_changed",
        "frozen_patch8_thresholds_changed",
        "profitability_claimed",
        "paper_eligible",
        "live_eligible",
    ):
        if scope.get(field):
            problems.append(f"{field}_true")

    records = result.get("setup_records", [])
    expected_families = {"Ideal", "Clean Fast Break", "Continuation"}
    if len(records) != 3:
        problems.append("expected_three_setup_records")
    if {record.get("setup_family") for record in records} != expected_families:
        problems.append("unexpected_setup_family_set")

    for record in records:
        family = record.get("setup_family")
        stages = record.get("stage_reached", {})
        if not stages.get("generated_candidate") or not stages.get("setup_qualified"):
            problems.append(f"{family}_setup_not_preserved")
        for stage in ("trade_candidate", "selected_contract", "eligible_entry", "recorded_entry"):
            if stages.get(stage):
                problems.append(f"{family}_{stage}_unexpectedly_reached")
        if record.get("highest_stage_reached") != "setup_qualified":
            problems.append(f"{family}_unexpected_highest_stage")
        if record.get("first_stage_not_reached") != "trade_candidate":
            problems.append(f"{family}_unexpected_first_stage_not_reached")
        if record.get("winner_selection_result", {}).get("contract_selection_status") != "abstain":
            problems.append(f"{family}_contract_not_abstained")
        if record.get("costed_backtest_result", {}).get("costed_entry_exit_replay_run"):
            problems.append(f"{family}_costed_replay_unexpectedly_run")
        if record.get("trigger_numeric") is not None:
            problems.append(f"{family}_trigger_numeric_unexpected")
        if record.get("invalidation_numeric") is not None:
            problems.append(f"{family}_invalidation_numeric_unexpected")

    after = result.get("after_funnel_totals", {})
    expected_after = {
        "raw_opportunities_mapped": 3,
        "exact_setup_time_field_packages_established": 3,
        "new_generated_candidates": 3,
        "new_setup_qualified_candidates": 3,
        "new_trade_candidates": 0,
        "new_selected_contracts": 0,
        "new_eligible_entries": 0,
        "new_recorded_entries": 0,
        "new_exact_option_contract_evidence_required_cases": 3,
        "new_exact_data_required_cases": 3,
        "new_exits_evaluated": 0,
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

    request = result.get("exact_grouped_evidence_request", {})
    if not request.get("created"):
        problems.append("grouped_request_not_created")
    if request.get("downloaded"):
        problems.append("grouped_request_downloaded")
    cost = request.get("cost_check", {})
    if cost.get("checked_cost") != "NOT_AVAILABLE":
        problems.append("unexpected_checked_cost")
    if cost.get("external_cost_api_called"):
        problems.append("external_cost_api_called")
    if len(request.get("requests", [])) != 3:
        problems.append("expected_three_grouped_request_items")
    for item in request.get("requests", []):
        if item.get("dataset") != "OPRA.PILLAR":
            problems.append("unexpected_dataset")
        for schema in ("definition", "tcbbo", "trades", "statistics"):
            if schema not in item.get("schemas", []):
                problems.append(f"request_missing_{schema}")
        if item.get("exact_contract_identifier") != "NOT_DERIVABLE_FROM_LOCAL_EVIDENCE":
            problems.append("unexpected_contract_identifier")

    if result.get("accepted_mapper_regression_case_count") != 17:
        problems.append("accepted_mapper_regression_case_count_not_17")
    if result.get("package_to_candidate_control_result", {}).get("deterministic_result") != "PASS":
        problems.append("package_to_candidate_control_not_pass")
    if result.get("deterministic_comparison", {}).get("result") != "PASS":
        problems.append("determinism_not_pass")

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
        "setup_records": len(records),
        "trade_candidates": after.get("new_trade_candidates"),
        "selected_contracts": after.get("new_selected_contracts"),
        "exact_option_requests": after.get("new_exact_option_contract_evidence_required_cases"),
    }


if __name__ == "__main__":
    validation = validate_result_document()
    print(json.dumps(validation, indent=2, sort_keys=True))
    if validation["problems"]:
        raise SystemExit(1)
