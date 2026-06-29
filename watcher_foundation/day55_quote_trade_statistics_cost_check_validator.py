import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day55_quote_trade_statistics_cost_check_for_selected_contracts.json"
)
REQUIRED_SCHEMAS = {"cmbp-1", "tcbbo", "trades", "statistics"}


def validate_result_document(result_path=RESULT_PATH):
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    problems = []

    if (
        result.get("result_version")
        != "safe_fast_day55_quote_trade_statistics_cost_check_for_selected_contracts_v1"
    ):
        problems.append("unexpected_result_version")
    if result.get("status") not in {"BLOCKED", "SUCCESS", "FAILURE"}:
        problems.append("unexpected_status")
    if result.get("dataset") != "OPRA.PILLAR":
        problems.append("unexpected_dataset")
    if result.get("cost_only") is not True:
        problems.append("cost_only_not_true")
    if result.get("download_performed") is not False:
        problems.append("download_performed_not_false")
    if result.get("credential_value_printed") is not False:
        problems.append("credential_value_printed_not_false")
    if result.get("profitability_proof") != "NO":
        problems.append("profitability_proof_not_no")
    if result.get("paper_live_eligibility") != "NO":
        problems.append("paper_live_eligibility_not_no")
    if result.get("entry_status") != "NOT_EVALUATED":
        problems.append("entry_status_changed")
    if result.get("exit_status") != "NOT_EVALUATED":
        problems.append("exit_status_changed")
    if result.get("gross_pnl") is not None:
        problems.append("gross_pnl_invented")
    if result.get("net_pnl") is not None:
        problems.append("net_pnl_invented")

    if set(result.get("required_schemas", [])) != REQUIRED_SCHEMAS:
        problems.append("required_schema_set_mismatch")
    if "definition" not in set(result.get("forbidden_schemas", [])):
        problems.append("definition_not_marked_forbidden")

    requests = result.get("requests", [])
    if result.get("request_count") != len(requests):
        problems.append("request_count_mismatch")
    if not requests:
        problems.append("requests_missing")

    schemas_seen = {request.get("schema") for request in requests}
    if schemas_seen != REQUIRED_SCHEMAS:
        problems.append("request_schema_set_mismatch")
    if "definition" in schemas_seen:
        problems.append("definition_schema_requested")

    for request in requests:
        if sorted(request.keys()) != ["dataset", "end", "schema", "start", "stype_in", "symbols"]:
            problems.append("vendor_request_contains_non_vendor_fields")
        if request.get("dataset") != "OPRA.PILLAR":
            problems.append("request_dataset_mismatch")
        if request.get("schema") not in REQUIRED_SCHEMAS:
            problems.append(f"unexpected_request_schema_{request.get('schema')}")
        if request.get("stype_in") != "raw_symbol":
            problems.append("request_stype_in_not_raw_symbol")
        if not request.get("symbols") or not request.get("start") or not request.get("end"):
            problems.append("request_window_or_symbol_missing")

    schema_costs = result.get("schema_costs", [])
    if result.get("status") == "SUCCESS":
        if result.get("vendor_metadata_call_performed") is not True:
            problems.append("success_vendor_metadata_call_not_true")
        if result.get("grouped_cost") is None:
            problems.append("success_grouped_cost_missing")
        if len(schema_costs) != len(requests):
            problems.append("success_schema_cost_count_mismatch")
    else:
        if result.get("download_performed") is not False:
            problems.append("non_success_download_performed")
        if result.get("grouped_cost") is not None:
            problems.append("non_success_grouped_cost_present")

    return {
        "status": "PASS" if not problems else "FAIL",
        "problems": sorted(set(problems)),
        "result_status": result.get("status"),
        "request_count": result.get("request_count"),
        "schemas": sorted(schemas_seen),
    }


if __name__ == "__main__":
    validation = validate_result_document()
    print(json.dumps(validation, indent=2, sort_keys=True))
    if validation["problems"]:
        raise SystemExit(1)
