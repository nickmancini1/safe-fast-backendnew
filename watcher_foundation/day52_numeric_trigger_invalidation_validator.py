import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day52_numeric_trigger_invalidation.json"
)

EXPECTED_FAMILIES = {"Ideal", "Clean Fast Break", "Continuation"}
EXPECTED_TRIGGER = "668.360000000"
EXPECTED_INVALIDATION = "667.870000000"


def validate_result_document(result_path=RESULT_PATH):
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    problems = []

    if result.get("result_version") != "day52_numeric_trigger_invalidation_v2":
        problems.append("unexpected_result_version")
    if result.get("implementation_version") != "day52_numeric_trigger_invalidation_impl_v2":
        problems.append("unexpected_implementation_version")

    scope = result.get("scope", {})
    if scope.get("symbol") != "SPY":
        problems.append("unexpected_symbol")
    if scope.get("session_date") != "2026-03-16":
        problems.append("unexpected_session_date")
    if scope.get("setup_timestamp_utc") != "2026-03-16T13:30:00Z":
        problems.append("unexpected_setup_timestamp")
    for field in (
        "opra_required",
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

    source = result.get("source", {})
    if source.get("dataset_schema_stype") != "DBEQ.BASIC / ohlcv-1m / raw_symbol":
        problems.append("unexpected_source_dataset")
    if source.get("setup_rows_found") != 3:
        problems.append("expected_three_setup_source_rows")

    constructors = result.get("numeric_constructors", [])
    if {item.get("setup_family") for item in constructors} != EXPECTED_FAMILIES:
        problems.append("unexpected_family_set")
    if len(constructors) != 3:
        problems.append("expected_three_constructors")
    for constructor in constructors:
        family = constructor.get("setup_family")
        if constructor.get("setup_timestamp_utc") != "2026-03-16T13:30:00Z":
            problems.append(f"{family}_unexpected_setup_timestamp")
        if constructor.get("setup_qualified_allowed") is not True:
            problems.append(f"{family}_setup_qualified_not_allowed")
        if constructor.get("promotion_decision") != "PROMOTE_CANDIDATE_A":
            problems.append(f"{family}_unexpected_promotion_decision")
        audit = constructor.get("binding_audit", {})
        if audit.get("source_row_index") != 2:
            problems.append(f"{family}_unexpected_source_row_index")
        if audit.get("binding_result") != "LEGITIMATE_SHARED_SETUP_TIME_ROW":
            problems.append(f"{family}_binding_not_legitimate_shared_row")
        for field in ("trigger", "invalidation"):
            item = constructor.get(field, {})
            expected_value = EXPECTED_TRIGGER if field == "trigger" else EXPECTED_INVALIDATION
            expected_source = "high" if field == "trigger" else "low"
            if item.get("blocker_code") is not None:
                problems.append(f"{family}_{field}_unexpected_blocker")
            if item.get("numeric_value") != expected_value:
                problems.append(f"{family}_{field}_unexpected_numeric_value")
            if item.get("finite_numeric_value") is not True:
                problems.append(f"{family}_{field}_finite_flag_not_true")
            if item.get("no_hindsight_cutoff") != "2026-03-16T13:30:00Z":
                problems.append(f"{family}_{field}_no_hindsight_cutoff_changed")
            if item.get("source_field") != expected_source:
                problems.append(f"{family}_{field}_unexpected_source_field")
            if item.get("comparison_operator") != (">=" if field == "trigger" else "<="):
                problems.append(f"{family}_{field}_unexpected_operator")

    summary = result.get("summary", {})
    if summary.get("numeric_values_established") != 6:
        problems.append("numeric_values_established_not_six")
    if summary.get("numeric_values_unresolved") != 0:
        problems.append("numeric_values_unresolved_nonzero")
    if summary.get("setup_qualified_allowed_count") != 3:
        problems.append("setup_qualified_allowed_count_not_three")

    determinism = result.get("deterministic_comparison", {})
    if determinism.get("result") != "PASS":
        problems.append("determinism_not_pass")

    guardrails = result.get("guardrails", {})
    for field in (
        "future_rows_used",
        "missing_evidence_converted_to_confidence",
        "profitability_claimed",
        "paper_eligible",
        "live_eligible",
    ):
        if guardrails.get(field):
            problems.append(f"{field}_true")

    return {
        "status": "PASS" if not problems else "FAIL",
        "problems": problems,
        "families": len(constructors),
        "numeric_values_established": summary.get("numeric_values_established"),
        "numeric_values_unresolved": summary.get("numeric_values_unresolved"),
        "blockers_by_code": summary.get("blockers_by_code", {}),
    }


if __name__ == "__main__":
    validation = validate_result_document()
    print(json.dumps(validation, indent=2, sort_keys=True))
    if validation["problems"]:
        raise SystemExit(1)
