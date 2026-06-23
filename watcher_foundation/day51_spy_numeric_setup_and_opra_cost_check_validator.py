import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day51_spy_numeric_setup_and_opra_cost_check.json"
)


def validate_result_document(result_path=RESULT_PATH):
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    problems = []

    if result.get("result_version") != "day51_spy_numeric_setup_and_opra_cost_check_v1":
        problems.append("unexpected_result_version")

    scope = result.get("execution_scope", {})
    for field in (
        "bounded_to_spy_2026_03_16",
        "processes_each_setup_family_separately",
        "cost_check_only",
    ):
        if scope.get(field) is not True:
            problems.append(f"{field}_not_true")
    for field in (
        "paid_data_downloaded",
        "timeseries_download_called",
        "main_py_changed",
        "railway_or_deploy_changed",
        "broker_or_account_or_order_touched",
        "credentials_or_env_changed",
        "sizing_or_alerts_changed",
        "frozen_patch8_thresholds_changed",
        "profitability_claimed",
        "paper_eligible",
        "live_eligible",
    ):
        if scope.get(field):
            problems.append(f"{field}_true")

    expected = {"Ideal", "Clean Fast Break", "Continuation"}
    contracts = result.get("numeric_setup_contracts", [])
    if {item.get("setup_family") for item in contracts} != expected:
        problems.append("unexpected_numeric_setup_family_set")
    if len(contracts) != 3:
        problems.append("expected_three_numeric_setup_contracts")
    for contract in contracts:
        family = contract.get("setup_family")
        if contract.get("setup_timestamp_utc") != "2026-03-16T13:30:00Z":
            problems.append(f"{family}_unexpected_setup_timestamp")
        if contract.get("numeric_underlying_evidence", {}).get("rows_found") != 3:
            problems.append(f"{family}_missing_setup_minute_evidence")
        if contract.get("trigger_numeric") is not None:
            problems.append(f"{family}_trigger_numeric_invented")
        if contract.get("invalidation_numeric") is not None:
            problems.append(f"{family}_invalidation_numeric_invented")
        if contract.get("trigger_numeric_status") != "RULE_GAP_NOT_NUMERICALLY_ESTABLISHED":
            problems.append(f"{family}_unexpected_trigger_numeric_status")
        if contract.get("invalidation_numeric_status") != "RULE_GAP_NOT_NUMERICALLY_ESTABLISHED":
            problems.append(f"{family}_unexpected_invalidation_numeric_status")
        if contract.get("no_hindsight_boundary") != "future_rows_ignored_for_setup_labels":
            problems.append(f"{family}_no_hindsight_not_preserved")
        if contract.get("session_boundary_behavior") != "same_session_reset_only_no_prior_session_carry":
            problems.append(f"{family}_session_boundary_not_preserved")

    specs = result.get("exact_option_evidence_specifications", [])
    if {item.get("setup_family") for item in specs} != expected:
        problems.append("unexpected_option_spec_family_set")
    for spec in specs:
        family = spec.get("setup_family")
        if spec.get("dataset") != "OPRA.PILLAR":
            problems.append(f"{family}_unexpected_dataset")
        for schema in ("definition", "tcbbo", "trades", "statistics"):
            if schema not in spec.get("schemas", []):
                problems.append(f"{family}_missing_{schema}")
        if spec.get("definition_window", {}).get("query_type") != "parent_symbol":
            problems.append(f"{family}_definition_not_parent_symbol")
        if spec.get("exit_evidence_window", {}).get("end_timestamp_utc") != "2026-03-16T19:45:00Z":
            problems.append(f"{family}_unexpected_exit_window")

    cost = result.get("grouped_opra_cost_check", {})
    if cost.get("paid_data_downloaded"):
        problems.append("cost_check_downloaded")
    if cost.get("download_created"):
        problems.append("cost_check_created_download")
    if cost.get("currency") != "USD":
        problems.append("unexpected_cost_currency")
    if not cost.get("api_or_local_command_used"):
        problems.append("missing_cost_command")
    if cost.get("status") == "CHECKED":
        if cost.get("grouped_total") in (None, "NOT_AVAILABLE"):
            problems.append("checked_cost_missing_grouped_total")
        if cost.get("sufficient_for_explicit_approval") is not True:
            problems.append("checked_cost_not_sufficient")
    else:
        if cost.get("grouped_total") != "NOT_AVAILABLE":
            problems.append("unchecked_cost_has_total")
        if cost.get("sufficient_for_explicit_approval") is not False:
            problems.append("unchecked_cost_marked_sufficient")

    approval = result.get("approval_required", {})
    if not str(approval.get("status", "")).startswith("APPROVAL_REQUIRED"):
        problems.append("approval_required_status_missing")
    if not approval.get("precise_data_unlocked"):
        problems.append("approval_precise_data_missing")

    replay = result.get("costed_backtest_results_by_setup_family", {})
    if set(replay) != expected:
        problems.append("unexpected_replay_family_set")
    for family, item in replay.items():
        if item.get("costed_exit_replay_run"):
            problems.append(f"{family}_costed_replay_unexpected")
        if item.get("selected_contract") is not None:
            problems.append(f"{family}_selected_contract_invented")
        if item.get("net_pnl") is not None:
            problems.append(f"{family}_pnl_invented")

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
    for key, expected_value in expected_after.items():
        if after.get(key) != expected_value:
            problems.append(f"{key}_expected_{expected_value}_got_{after.get(key)}")

    tests = result.get("test_coverage_contract", {})
    for key, value in tests.items():
        if value is not True:
            problems.append(f"{key}_not_true")

    if result.get("deterministic_comparison", {}).get("result") != "PASS":
        problems.append("determinism_not_pass")
    if result.get("control_results", {}).get("accepted_mapper_regression_case_count") != 17:
        problems.append("accepted_mapper_regression_count_changed")

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
        "setup_records": len(contracts),
        "option_specs": len(specs),
        "cost_status": cost.get("status"),
        "grouped_cost": cost.get("grouped_total"),
    }


if __name__ == "__main__":
    validation = validate_result_document()
    print(json.dumps(validation, indent=2, sort_keys=True))
    if validation["problems"]:
        raise SystemExit(1)
