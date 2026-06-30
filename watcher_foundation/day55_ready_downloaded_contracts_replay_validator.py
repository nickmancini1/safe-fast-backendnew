import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day55_ready_downloaded_contracts_replay.json"
)

ALLOWED_CONTRACTS = {
    "QQQ   260416C00585000",
    "QQQ   260416C00590000",
    "QQQ   260501C00650000",
    "QQQ   260501C00655000",
    "SPY   260414C00645000",
    "SPY   260414C00650000",
    "SPY   260501C00702000",
    "SPY   260501C00707000",
}
VALID_ENTRY_STATUSES = {
    "VALID_ENTRY_FOUND",
    "NO_ENTRY_EXACT_REJECTION",
    "ECONOMIC_REPLAY_BLOCKED",
}
VALID_EXIT_STATUSES = {"EXIT_EVALUATED", "EXIT_BLOCKED"}
VALID_NET_PNL_STATUSES = {"NET_PNL_EVALUATED", "ECONOMIC_REPLAY_BLOCKED"}


def validate_result_document(result_path=RESULT_PATH):
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    problems = []

    if result.get("result_version") != "day55_ready_downloaded_contracts_replay_v1":
        problems.append("unexpected_result_version")
    if result.get("task") != "SAFE_FAST_DAY55_READY_DOWNLOADED_CONTRACTS_REPLAY_TASK.md":
        problems.append("unexpected_task")

    scope = result.get("scope", {})
    for field in ("local_raw_databento_files_only",):
        if scope.get(field) is not True:
            problems.append(f"{field}_not_true")
    for field in (
        "databento_called",
        "tastytrade_called",
        "schwab_called",
        "vendor_download_performed",
        "definition_requested",
        "more_data_requested",
        "main_py_changed",
        "railway_or_deploy_changed",
        "broker_account_order_alert_touched",
        "credentials_or_env_changed",
        "sizing_changed",
        "raw_vendor_files_mutated",
    ):
        if scope.get(field) is not False:
            problems.append(f"{field}_not_false")

    baseline = result.get("baseline", {})
    if baseline.get("download_manifest_status") != "SUCCESS":
        problems.append("download_manifest_not_success")
    if baseline.get("downloaded_request_count") != 32:
        problems.append("downloaded_request_count_not_32")
    if set(baseline.get("required_schemas", [])) != {"cmbp-1", "tcbbo", "trades", "statistics"}:
        problems.append("required_schema_set_mismatch")
    if "definition" not in set(baseline.get("forbidden_schemas", [])):
        problems.append("definition_not_forbidden")
    if set(baseline.get("allowed_contracts", [])) != ALLOWED_CONTRACTS:
        problems.append("allowed_contracts_changed")

    spy_rejection = baseline.get("preserved_spy_670c_rejection", {})
    if spy_rejection.get("preserved") is not True:
        problems.append("spy_670c_exact_rejection_not_preserved")
    if spy_rejection.get("first_blocker") != "target_contract_not_in_day55_download_manifest":
        problems.append("spy_670c_first_blocker_changed")
    if spy_rejection.get("gross_pnl") is not None or spy_rejection.get("net_pnl") is not None:
        problems.append("spy_670c_pnl_invented")

    input_validation = result.get("input_validation", {})
    if input_validation.get("status") != "INPUTS_VALIDATED":
        problems.append("inputs_not_validated")
    if input_validation.get("download_performed") is not True:
        problems.append("download_not_validated")
    if input_validation.get("request_count") != 32:
        problems.append("request_count_not_32")
    if input_validation.get("completed_or_reused_request_count") != 32:
        problems.append("completed_request_count_not_32")
    if input_validation.get("remaining_request_count") != 0:
        problems.append("remaining_requests_not_zero")
    if input_validation.get("ready_contract_count") != 8:
        problems.append("ready_contract_count_not_8")
    if input_validation.get("definition_requested_or_needed") is not False:
        problems.append("definition_needed_unexpected")
    if "definition" in input_validation.get("completed_or_reused_schemas", []):
        problems.append("definition_schema_unexpected")

    schema_status = input_validation.get("schema_file_status", {})
    if len(schema_status) != 32:
        problems.append("downloaded_file_status_count_not_32")
    for request_id, status in schema_status.items():
        if status.get("csv_exists") is not True:
            problems.append(f"{request_id}_csv_missing")
        if status.get("dbn_exists") is not True:
            problems.append(f"{request_id}_dbn_missing")
        if status.get("csv_sha256_match") is not True:
            problems.append(f"{request_id}_csv_sha256_not_validated")
        if status.get("dbn_sha256_match") is not True:
            problems.append(f"{request_id}_dbn_sha256_not_validated")
        if status.get("actual_csv_record_count") != status.get("manifest_record_count"):
            problems.append(f"{request_id}_csv_record_count_mismatch")

    contract_results = result.get("contract_results", [])
    if len(contract_results) != 8:
        problems.append("contract_result_count_not_8")
    if {item.get("raw_symbol") for item in contract_results} != ALLOWED_CONTRACTS:
        problems.append("contract_result_symbols_changed")

    for item in contract_results:
        symbol = item.get("raw_symbol", "unknown")
        if item.get("entry_status") not in VALID_ENTRY_STATUSES:
            problems.append(f"{symbol}_unexpected_entry_status")
        if item.get("exit_status") not in VALID_EXIT_STATUSES:
            problems.append(f"{symbol}_unexpected_exit_status")
        if item.get("net_pnl_status") not in VALID_NET_PNL_STATUSES:
            problems.append(f"{symbol}_unexpected_net_pnl_status")
        if item.get("entry_status") == "NO_ENTRY_EXACT_REJECTION" and not item.get("first_blocker"):
            problems.append(f"{symbol}_no_entry_missing_first_blocker")
        if item.get("entry_status") != "VALID_ENTRY_FOUND" and item.get("net_pnl") is not None:
            problems.append(f"{symbol}_net_pnl_invented_without_entry")
        if item.get("exit_status") != "EXIT_EVALUATED" and item.get("gross_pnl") is not None:
            problems.append(f"{symbol}_gross_pnl_invented_without_exit")
        if item.get("paper_live_eligibility") != "NO":
            problems.append(f"{symbol}_paper_live_eligibility_not_no")
        if item.get("profitability_status") != "NO":
            problems.append(f"{symbol}_profitability_status_not_no")

    summary = result.get("summary", {})
    if summary.get("ready_contracts_evaluated") != len(contract_results):
        problems.append("summary_ready_contract_count_mismatch")
    if summary.get("valid_entries") != sum(1 for item in contract_results if item.get("entry_status") == "VALID_ENTRY_FOUND"):
        problems.append("summary_valid_entries_mismatch")
    if summary.get("evaluated_exits") != sum(1 for item in contract_results if item.get("exit_status") == "EXIT_EVALUATED"):
        problems.append("summary_evaluated_exits_mismatch")
    if summary.get("net_pnl_results") != sum(1 for item in contract_results if item.get("net_pnl_status") == "NET_PNL_EVALUATED"):
        problems.append("summary_net_pnl_results_mismatch")
    if summary.get("exact_no_entry_rejections") != sum(1 for item in contract_results if item.get("entry_status") == "NO_ENTRY_EXACT_REJECTION"):
        problems.append("summary_exact_rejections_mismatch")
    if summary.get("profitability_proof") != "NO" or result.get("profitability_proof") != "NO":
        problems.append("profitability_proof_not_no")
    if summary.get("paper_live_eligibility") != "NO" or result.get("paper_live_eligibility") != "NO":
        problems.append("paper_live_eligibility_not_no")

    serialized = json.dumps(result, sort_keys=True).lower()
    for forbidden in ("safe_fast_db_auth=", "api_key", "secret", "token"):
        if forbidden in serialized:
            problems.append(f"credential_field_present_{forbidden}")

    return {
        "status": "PASS" if not problems else "FAIL",
        "problems": problems,
        "ready_contracts_evaluated": summary.get("ready_contracts_evaluated"),
        "valid_entries": summary.get("valid_entries"),
        "exact_no_entry_rejections": summary.get("exact_no_entry_rejections"),
        "net_pnl_results": summary.get("net_pnl_results"),
    }


if __name__ == "__main__":
    validation = validate_result_document()
    print(json.dumps(validation, indent=2, sort_keys=True))
    if validation["problems"]:
        raise SystemExit(1)
