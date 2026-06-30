import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day55_spy_670c_target_cost_only_request.json"
)
RAW_SYMBOL = "SPY   260330C00670000"
REQUIRED_SCHEMAS = {"cmbp-1", "tcbbo", "trades", "statistics"}
FORBIDDEN_SCHEMAS = {"definition"}
EXPECTED_WINDOWS = {
    "cmbp-1": ("2026-03-16T13:31:00Z", "2026-03-16T13:36:00Z"),
    "tcbbo": ("2026-03-16T13:31:00Z", "2026-03-16T19:45:00Z"),
    "trades": ("2026-03-16T13:30:00Z", "2026-03-16T19:45:00Z"),
    "statistics": ("2026-03-16T13:30:00Z", "2026-03-16T13:36:00Z"),
}


def validate_result_document(result_path=RESULT_PATH):
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    problems = []

    if result.get("result_version") != "day55_spy_670c_target_cost_only_request_v1":
        problems.append("unexpected_result_version")
    if result.get("decision") != "TARGET_COST_ONLY_REQUEST_READY_FOR_OPERATOR_APPROVAL":
        problems.append("unexpected_decision")
    if result.get("dataset") != "OPRA.PILLAR":
        problems.append("unexpected_dataset")
    if result.get("exact_symbol") != RAW_SYMBOL:
        problems.append("exact_symbol_mismatch")
    if result.get("cost_only") is not True:
        problems.append("cost_only_not_true")
    for field in ("vendor_call_performed", "download_performed", "credential_env_var_read"):
        if result.get(field) is not False:
            problems.append(f"{field}_not_false")
    if set(result.get("required_schemas", [])) != REQUIRED_SCHEMAS:
        problems.append("required_schemas_mismatch")
    if not FORBIDDEN_SCHEMAS.issubset(set(result.get("forbidden_schemas", []))):
        problems.append("definition_not_forbidden")
    if result.get("exact_estimated_cost") != "0.006495481730":
        problems.append("estimated_cost_mismatch")
    if result.get("currency") != "USD":
        problems.append("currency_mismatch")
    if not result.get("destination_for_approved_download"):
        problems.append("destination_missing")
    if not result.get("operator_approval_text"):
        problems.append("operator_approval_text_missing")
    if result.get("profitability_proof") != "NO":
        problems.append("profitability_proof_not_no")
    if result.get("paper_live_eligibility") != "NO":
        problems.append("paper_live_eligibility_not_no")

    requests = result.get("requests", [])
    if result.get("request_count") != 4 or len(requests) != 4:
        problems.append("request_count_mismatch")
    schemas = {request.get("schema") for request in requests}
    if schemas != REQUIRED_SCHEMAS:
        problems.append("request_schema_mismatch")
    if "definition" in schemas:
        problems.append("definition_requested")
    for request in requests:
        schema = request.get("schema")
        if request.get("dataset") != "OPRA.PILLAR":
            problems.append("request_dataset_mismatch")
        if request.get("stype_in") != "raw_symbol":
            problems.append("request_stype_mismatch")
        if request.get("symbols") != RAW_SYMBOL:
            problems.append("request_symbol_mismatch")
        if schema in EXPECTED_WINDOWS:
            expected_start, expected_end = EXPECTED_WINDOWS[schema]
            if request.get("start") != expected_start or request.get("end") != expected_end:
                problems.append(f"{schema}_window_mismatch")

    return {
        "status": "PASS" if not problems else "FAIL",
        "problems": sorted(set(problems)),
        "request_count": result.get("request_count"),
        "exact_estimated_cost": result.get("exact_estimated_cost"),
    }


if __name__ == "__main__":
    validation = validate_result_document()
    print(json.dumps(validation, indent=2, sort_keys=True))
    if validation["problems"]:
        raise SystemExit(1)
