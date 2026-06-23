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
EXPECTED_BLOCKERS = {
    "Ideal": {
        "trigger": "NUMERIC_RULE_UNRESOLVED_IDEAL_TRIGGER",
        "invalidation": "NUMERIC_RULE_UNRESOLVED_IDEAL_INVALIDATION",
    },
    "Clean Fast Break": {
        "trigger": "NUMERIC_RULE_UNRESOLVED_CLEAN_FAST_BREAK_TRIGGER",
        "invalidation": "NUMERIC_RULE_UNRESOLVED_CLEAN_FAST_BREAK_INVALIDATION",
    },
    "Continuation": {
        "trigger": "NUMERIC_RULE_UNRESOLVED_CONTINUATION_TRIGGER",
        "invalidation": "NUMERIC_RULE_UNRESOLVED_CONTINUATION_INVALIDATION",
    },
}


def validate_result_document(result_path=RESULT_PATH):
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    problems = []

    if result.get("result_version") != "day52_numeric_trigger_invalidation_v1":
        problems.append("unexpected_result_version")
    if result.get("implementation_version") != "day52_numeric_trigger_invalidation_impl_v1":
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
        if constructor.get("setup_qualified_allowed") is not False:
            problems.append(f"{family}_setup_qualified_allowed")
        for field in ("trigger", "invalidation"):
            item = constructor.get(field, {})
            if item.get("blocker_code") != EXPECTED_BLOCKERS.get(family, {}).get(field):
                problems.append(f"{family}_{field}_unexpected_blocker")
            if item.get("numeric_value") is not None:
                problems.append(f"{family}_{field}_numeric_value_invented")
            if item.get("finite_numeric_value") is not False:
                problems.append(f"{family}_{field}_finite_flag_not_false")
            if item.get("no_hindsight_cutoff") != "2026-03-16T13:30:00Z":
                problems.append(f"{family}_{field}_no_hindsight_cutoff_changed")
            if "open" not in item.get("observable_ohlcv_fields", {}):
                problems.append(f"{family}_{field}_missing_ohlcv_provenance")
            if "does not bind" not in item.get("calculation", ""):
                problems.append(f"{family}_{field}_missing_rule_gap_calculation")

    summary = result.get("summary", {})
    if summary.get("numeric_values_established") != 0:
        problems.append("numeric_values_established_nonzero")
    if summary.get("numeric_values_unresolved") != 6:
        problems.append("expected_six_unresolved_numeric_values")
    if summary.get("setup_qualified_allowed_count") != 0:
        problems.append("setup_qualified_allowed_count_nonzero")

    determinism = result.get("deterministic_comparison", {})
    if determinism.get("result") != "PASS":
        problems.append("determinism_not_pass")

    guardrails = result.get("guardrails", {})
    for field in (
        "raw_ohlcv_promoted_without_rule",
        "future_rows_used",
        "missing_evidence_converted_to_confidence",
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
