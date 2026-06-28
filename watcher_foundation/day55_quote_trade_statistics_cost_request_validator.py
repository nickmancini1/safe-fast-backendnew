import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day55_quote_trade_statistics_cost_request_for_selected_contracts.json"
)
REQUIRED_SCHEMAS = {"cmbp-1", "tcbbo", "trades", "statistics"}


def validate_result_document(result_path=RESULT_PATH):
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    problems = []

    if (
        result.get("result_version")
        != "safe_fast_day55_quote_trade_statistics_cost_request_for_selected_contracts_v1"
    ):
        problems.append("unexpected_result_version")
    if result.get("decision") != "QUOTE_TRADE_STATISTICS_COST_REQUEST_READY_FOR_OPERATOR_REVIEW":
        problems.append("unexpected_decision")
    if result.get("dataset") != "OPRA.PILLAR":
        problems.append("unexpected_dataset")
    for field in ("cost_only",):
        if result.get(field) is not True:
            problems.append(f"{field}_not_true")
    for field in ("vendor_call_performed", "download_performed", "credential_env_var_read"):
        if result.get(field) is not False:
            problems.append(f"{field}_not_false")
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
    if not REQUIRED_SCHEMAS.issubset(schemas_seen):
        problems.append("missing_required_request_schema")
    if "definition" in schemas_seen:
        problems.append("definition_schema_requested")

    for request in requests:
        if request.get("dataset") != "OPRA.PILLAR":
            problems.append("request_dataset_mismatch")
        if request.get("schema") not in REQUIRED_SCHEMAS:
            problems.append(f"unexpected_request_schema_{request.get('schema')}")
        if request.get("stype_in") != "raw_symbol":
            problems.append("request_stype_in_not_raw_symbol")
        if not request.get("symbols"):
            problems.append("request_symbol_missing")
        if not request.get("start") or not request.get("end"):
            problems.append("request_window_missing")
        if not request.get("candidate_ids"):
            problems.append("request_candidate_ids_missing")
        if request.get("leg") not in {"long", "short"}:
            problems.append("request_leg_missing")
        if not request.get("contract_identities"):
            problems.append("request_contract_identities_missing")
        for identity in request.get("contract_identities", []):
            if identity.get("profitability_proof") != "NO":
                problems.append("identity_profitability_proof_not_no")
            if identity.get("paper_live_eligibility") != "NO":
                problems.append("identity_paper_live_eligibility_not_no")
            if identity.get("entry_status") != "NOT_EVALUATED":
                problems.append("identity_entry_status_changed")
            if identity.get("exit_status") != "NOT_EVALUATED":
                problems.append("identity_exit_status_changed")
            if identity.get("gross_pnl") is not None:
                problems.append("identity_gross_pnl_invented")
            if identity.get("net_pnl") is not None:
                problems.append("identity_net_pnl_invented")

    return {
        "status": "PASS" if not problems else "FAIL",
        "problems": sorted(set(problems)),
        "request_count": result.get("request_count"),
        "schemas": sorted(schemas_seen),
    }


if __name__ == "__main__":
    validation = validate_result_document()
    print(json.dumps(validation, indent=2, sort_keys=True))
    if validation["problems"]:
        raise SystemExit(1)
