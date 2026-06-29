import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "source_data"
    / "external_option_data_drop"
    / "day55_quote_trade_statistics_selected_contracts"
    / "day55_quote_trade_statistics_download_manifest.json"
)
REQUIRED_SCHEMAS = {"cmbp-1", "tcbbo", "trades", "statistics"}
FINAL_STATUSES = {"COMPLETED_REUSED", "COMPLETED_DOWNLOADED"}


def validate_manifest(manifest_path=MANIFEST_PATH):
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    problems = []

    if manifest.get("result_version") != "safe_fast_day55_quote_trade_statistics_download_manifest_v1":
        problems.append("unexpected_result_version")
    if manifest.get("status") not in {"IN_PROGRESS", "SUCCESS", "FAILURE", "INTERRUPTED"}:
        problems.append("unexpected_status")
    if manifest.get("dataset") != "OPRA.PILLAR":
        problems.append("unexpected_dataset")
    if manifest.get("credential_env_var") != "SAFE_FAST_DB_AUTH":
        problems.append("unexpected_credential_env_var")
    if manifest.get("credential_value_printed") is not False:
        problems.append("credential_value_printed_not_false")
    if manifest.get("credential_value_persisted") is not False:
        problems.append("credential_value_persisted_not_false")
    if manifest.get("operator_approved_grouped_cost_usd") != "0.054846107958":
        problems.append("approved_cost_changed")
    if manifest.get("checked_grouped_cost_usd") != "0.054846107958":
        problems.append("checked_cost_changed")
    if manifest.get("download_allowed_for_exact_cost_checked_requests") is not True:
        problems.append("exact_request_approval_not_recorded")

    requests = manifest.get("exact_requests", [])
    if manifest.get("request_count") != 32 or len(requests) != 32:
        problems.append("request_count_not_32")
    if set(manifest.get("required_schemas", [])) != REQUIRED_SCHEMAS:
        problems.append("required_schema_set_mismatch")
    if "definition" not in set(manifest.get("forbidden_schemas", [])):
        problems.append("definition_not_forbidden")
    if {request.get("schema") for request in requests} != REQUIRED_SCHEMAS:
        problems.append("request_schema_set_mismatch")
    if any(request.get("schema") == "definition" for request in requests):
        problems.append("definition_request_present")

    request_status = manifest.get("request_status", {})
    if len(request_status) != len(requests):
        problems.append("request_status_count_mismatch")
    for request_id, row in request_status.items():
        status = row.get("status")
        if status not in {"MISSING", *FINAL_STATUSES}:
            problems.append(f"unexpected_request_status_{request_id}_{status}")
        request = row.get("request") or {}
        if sorted(request.keys()) != ["dataset", "end", "schema", "start", "stype_in", "symbols"]:
            problems.append("request_status_contains_non_vendor_fields")
        if request.get("dataset") != "OPRA.PILLAR":
            problems.append("request_dataset_mismatch")
        if request.get("schema") not in REQUIRED_SCHEMAS:
            problems.append("unexpected_request_schema")
        if request.get("stype_in") != "raw_symbol":
            problems.append("request_stype_in_not_raw_symbol")

    completed_ids = manifest.get("completed_or_reused_request_ids", [])
    remaining_ids = manifest.get("remaining_request_ids", [])
    if len(set(completed_ids) & set(remaining_ids)) != 0:
        problems.append("completed_remaining_overlap")
    if manifest.get("status") == "SUCCESS":
        if len(completed_ids) != 32 or remaining_ids:
            problems.append("success_not_all_requests_complete")
        if len(manifest.get("output_files", [])) != 32:
            problems.append("success_output_file_count_not_32")
    for output in manifest.get("output_files", []):
        if output.get("schema") not in REQUIRED_SCHEMAS:
            problems.append("output_unexpected_schema")
        if not output.get("dbn_path") or not output.get("csv_path"):
            problems.append("output_path_missing")
        if output.get("contract_identity_validated") is not True:
            problems.append("contract_identity_not_validated")

    if manifest.get("entry_status") != "NOT_EVALUATED":
        problems.append("entry_status_changed")
    if manifest.get("exit_status") != "NOT_EVALUATED":
        problems.append("exit_status_changed")
    if manifest.get("gross_pnl") is not None:
        problems.append("gross_pnl_invented")
    if manifest.get("net_pnl") is not None:
        problems.append("net_pnl_invented")
    if manifest.get("profitability_proof") != "NO":
        problems.append("profitability_proof_not_no")
    if manifest.get("paper_live_eligibility") != "NO":
        problems.append("paper_live_eligibility_not_no")
    if manifest.get("setup_entry_exit_pnl_decision_made") is not False:
        problems.append("entry_exit_pnl_decision_made")

    return {
        "status": "PASS" if not problems else "FAIL",
        "problems": sorted(set(problems)),
        "manifest_status": manifest.get("status"),
        "request_count": manifest.get("request_count"),
        "completed_count": len(completed_ids),
        "remaining_count": len(remaining_ids),
    }


if __name__ == "__main__":
    validation = validate_manifest()
    print(json.dumps(validation, indent=2, sort_keys=True))
    if validation["problems"]:
        raise SystemExit(1)
