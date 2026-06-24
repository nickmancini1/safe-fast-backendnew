import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day52_family_numeric_binding_and_promotion.json"
)

EXPECTED_FAMILIES = {"Ideal", "Clean Fast Break", "Continuation"}
EXPECTED_TRIGGER = "668.360000000"
EXPECTED_INVALIDATION = "667.870000000"


def validate_result_document(result_path=RESULT_PATH):
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    problems = []

    if result.get("result_version") != "day52_family_numeric_binding_and_promotion_v1":
        problems.append("unexpected_result_version")
    if result.get("implementation_version") != "day52_family_numeric_binding_and_promotion_impl_v1":
        problems.append("unexpected_implementation_version")

    scope = result.get("scope", {})
    if scope.get("symbol") != "SPY":
        problems.append("unexpected_symbol")
    if scope.get("session_date") != "2026-03-16":
        problems.append("unexpected_session_date")
    for field in (
        "option_contract_selection",
        "entry_exit_costs_or_net_result",
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

    if result.get("binding_audit_result") != "LEGITIMATE_SHARED_SETUP_TIME_ROW":
        problems.append("binding_audit_not_legitimate_shared_row")
    audit = result.get("binding_audit", [])
    if {item.get("family") for item in audit} != EXPECTED_FAMILIES:
        problems.append("unexpected_binding_audit_families")
    for item in audit:
        family = item.get("family")
        if item.get("expected_opportunity_timestamp") != "2026-03-16T13:30:00Z":
            problems.append(f"{family}_unexpected_expected_timestamp")
        if item.get("actual_bound_setup_time_timestamp") != "2026-03-16T13:30:00Z":
            problems.append(f"{family}_unexpected_bound_timestamp")
        if item.get("source_row_index") != 2:
            problems.append(f"{family}_unexpected_source_row_index")
        row = item.get("source_row", {})
        if row.get("high") != EXPECTED_TRIGGER or row.get("low") != EXPECTED_INVALIDATION:
            problems.append(f"{family}_unexpected_ohlcv_binding")
        if item.get("no_hindsight_cutoff") != "2026-03-16T13:30:00Z":
            problems.append(f"{family}_unexpected_cutoff")

    decisions = result.get("family_decision_matrix", [])
    if {item.get("family") for item in decisions} != EXPECTED_FAMILIES:
        problems.append("unexpected_decision_families")
    for item in decisions:
        family = item.get("family")
        if item.get("decision") != "PROMOTE_CANDIDATE_A":
            problems.append(f"{family}_not_promoted_candidate_a")
        if item.get("trigger") != EXPECTED_TRIGGER:
            problems.append(f"{family}_unexpected_trigger")
        if item.get("invalidation") != EXPECTED_INVALIDATION:
            problems.append(f"{family}_unexpected_invalidation")
        if item.get("accepted_status") != "ACCEPTED":
            problems.append(f"{family}_not_accepted")

    numeric = result.get("accepted_numeric_summary", {})
    if numeric.get("numeric_values_established") != 6:
        problems.append("numeric_values_established_not_6")
    if numeric.get("numeric_values_unresolved") != 0:
        problems.append("numeric_values_unresolved_not_0")
    if numeric.get("setup_qualified_allowed_count") != 3:
        problems.append("setup_qualified_allowed_not_3")

    counts = result.get("accepted_mode_full_session_counts", {}).get("complete_session_accounting", {})
    expected_counts = {
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
        "trade_candidates": 0,
        "selected_contracts": 0,
        "eligible_entries": 0,
        "recorded_entries": 0,
    }
    for key, expected in expected_counts.items():
        if counts.get(key) != expected:
            problems.append(f"{key}_expected_{expected}_got_{counts.get(key)}")

    if result.get("separation_from_provisional_mode", {}).get(
        "accepted_and_provisional_modes_remain_separate"
    ) is not True:
        problems.append("accepted_provisional_separation_not_true")

    guardrails = result.get("guardrails", {})
    for field in (
        "future_rows_used",
        "post_cutoff_mutation_influenced_values",
        "opra_downloaded",
        "option_selection_performed",
        "trade_candidate_created",
        "selected_contract_created",
        "entry_or_exit_recorded",
        "pnl_calculated",
        "profitability_claimed",
        "paper_eligible",
        "live_eligible",
    ):
        if guardrails.get(field):
            problems.append(f"{field}_true")

    return {
        "status": "PASS" if not problems else "FAIL",
        "problems": problems,
        "binding_audit_result": result.get("binding_audit_result"),
        "accepted_numeric_summary": numeric,
        "accepted_mode_counts": counts,
    }


if __name__ == "__main__":
    validation = validate_result_document()
    print(json.dumps(validation, indent=2, sort_keys=True))
    if validation["problems"]:
        raise SystemExit(1)
