import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day52_existing_setup_option_evidence_end_to_end_backtest.json"
)


def validate_result_document(result_path=RESULT_PATH):
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    problems = []

    if result.get("result_version") != "day52_existing_setup_option_evidence_end_to_end_backtest_v1":
        problems.append("unexpected_result_version")

    scope = result.get("scope", {})
    for field in (
        "selected_duplicate_group_only",
        "broad_candidate_hunting",
        "provisional_recognition_layer_created",
        "main_py_changed",
        "railway_or_deploy_changed",
        "broker_account_order_alert_touched",
        "credentials_or_env_changed",
        "sizing_changed",
        "paid_data_downloaded",
        "schwab_wait_or_oauth",
    ):
        expected = field == "selected_duplicate_group_only"
        if scope.get(field) is not expected:
            problems.append(f"{field}_expected_{expected}_got_{scope.get(field)}")

    decision = result.get("first_required_decision", {})
    if decision.get("selected_winner_id") != "DAY52-SPY-2026-03-16-CLEAN-FAST-BREAK-20260316T133000Z-P39":
        problems.append("selected_winner_id_changed")
    if decision.get("setup_family_used_for_economic_winner") != "Clean Fast Break":
        problems.append("unexpected_economic_family")
    if decision.get("direction") != "bullish_long_call":
        problems.append("unexpected_direction")
    if decision.get("trigger_timestamp_utc") != "2026-03-16T13:31:00Z":
        problems.append("unexpected_trigger_timestamp")
    if decision.get("trigger_numeric") != "668.360000000":
        problems.append("trigger_changed")
    if decision.get("invalidation_numeric") != "667.870000000":
        problems.append("invalidation_changed")

    timing = decision.get("option_entry_timing_rule", {})
    if timing.get("earliest_allowed_option_price") != "2026-03-16T13:31:00Z":
        problems.append("unexpected_entry_start")
    if timing.get("latest_allowed_option_price") != "2026-03-16T13:36:00Z":
        problems.append("unexpected_entry_end")
    if timing.get("field_used_for_entry") != "ask":
        problems.append("entry_field_not_ask")
    if timing.get("maximum_quote_age_seconds_for_clean_entry") != 60:
        problems.append("clean_quote_age_not_60")
    if timing.get("maximum_quote_age_seconds_absolute_no_trade") != 300:
        problems.append("absolute_quote_age_not_300")

    local = result.get("local_evidence", {})
    if local.get("has_march16_spy_opra_evidence") is not False:
        problems.append("local_march16_evidence_unexpected")
    if local.get("has_selected_candidate_contract_evidence") is not False:
        problems.append("local_selected_contract_evidence_unexpected")

    contract = result.get("contract_selection_result", {})
    if contract.get("status") != "BLOCKED_DEFINITION_EVIDENCE_MISSING":
        problems.append("unexpected_contract_selection_status")
    if contract.get("selected_contract") is not None:
        problems.append("selected_contract_invented")
    candidate = contract.get("deterministic_candidate_if_listed", {})
    if candidate.get("vendor_symbol") != "SPY   260330C00669000":
        problems.append("unexpected_vendor_symbol")
    if candidate.get("expiration") != "2026-03-30":
        problems.append("unexpected_expiration")
    if candidate.get("strike") != "669":
        problems.append("unexpected_strike")

    entry = result.get("complete_entry_window_result", {})
    if entry.get("status") != "BLOCKED_COMPLETE_OPTION_PRICE_WINDOW_MISSING":
        problems.append("unexpected_entry_window_status")
    if entry.get("first_valid_price") is not None:
        problems.append("first_valid_price_invented")
    if entry.get("updates_inspected") != []:
        problems.append("entry_updates_invented")

    tastytrade = result.get("tastytrade_result", {})
    if tastytrade.get("status") != "FIELD_LIMITATION_BLOCKED":
        problems.append("unexpected_tastytrade_status")
    if tastytrade.get("historical_bid_ask_supplied") is not False:
        problems.append("tastytrade_bid_ask_claimed")

    databento = result.get("databento_result", {})
    if databento.get("status") != "NETWORK_EXECUTION_BLOCKED":
        problems.append("unexpected_databento_status")
    if databento.get("cost_check_run_in_sandbox") is not False:
        problems.append("sandbox_cost_check_claimed")
    if not databento.get("operator_script"):
        problems.append("operator_script_missing")
    if not databento.get("expected_output_file"):
        problems.append("expected_output_missing")

    replay = result.get("entry_exit_pnl_result", {})
    if replay.get("stage_reached") != "EXACT_EVIDENCE_REQUEST":
        problems.append("unexpected_stage")
    for field in ("entry_price", "exit_price", "net_pnl", "contract"):
        if replay.get(field) is not None:
            problems.append(f"{field}_invented")

    request = result.get("exact_evidence_request", {})
    if request.get("request_status") != "EXACT_PRICED_REQUEST_PENDING_OPERATOR_COST_OUTPUT":
        problems.append("unexpected_request_status")
    schemas = {item.get("schema") for item in request.get("schemas", [])}
    for schema in ("definition", "cmbp-1", "tcbbo", "trades", "statistics"):
        if schema not in schemas:
            problems.append(f"missing_request_schema_{schema}")
    if request.get("numerical_cost") != "PENDING_OPERATOR_COST_OUTPUT":
        problems.append("cost_invented")

    after = result.get("after_funnel_totals", {})
    expected_counts = {
        "selected_duplicate_groups_processed": 1,
        "selected_winner_records": 1,
        "suppressed_duplicate_records": 2,
        "trade_candidates": 0,
        "selected_contracts": 0,
        "eligible_entries": 0,
        "recorded_entries": 0,
        "costed_exits": 0,
        "net_pnl_results": 0,
        "exact_priced_requests": 1,
        "invalid_trades_allowed": 0,
    }
    for key, expected in expected_counts.items():
        if after.get(key) != expected:
            problems.append(f"{key}_expected_{expected}_got_{after.get(key)}")

    guardrails = result.get("guardrails", {})
    for field in (
        "pre_trigger_price_rejected",
        "late_price_rejected",
        "stale_quote_rejected",
        "spread_liquidity_rejected_when_over_limits",
        "duplicate_suppression_preserved",
        "strict_no_trade_until_valid_entry",
        "network_failure_not_reported_as_market_data_unavailable",
    ):
        if guardrails.get(field) is not True:
            problems.append(f"{field}_not_true")
    for field in ("profitability_claimed", "paper_eligible", "live_eligible"):
        if guardrails.get(field):
            problems.append(f"{field}_true")

    return {
        "status": "PASS" if not problems else "FAIL",
        "problems": problems,
        "stage_reached": replay.get("stage_reached"),
        "databento_status": databento.get("status"),
        "selected_winner": decision.get("selected_winner_id"),
    }


if __name__ == "__main__":
    validation = validate_result_document()
    print(json.dumps(validation, indent=2, sort_keys=True))
    if validation["problems"]:
        raise SystemExit(1)
