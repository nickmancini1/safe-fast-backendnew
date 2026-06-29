import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day55_spy_670c_entry_exit_pnl_evaluation.json"
)

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

    if result.get("result_version") != "day55_spy_670c_entry_exit_pnl_evaluation_v1":
        problems.append("unexpected_result_version")
    if result.get("task") != "SAFE_FAST_DAY55_OPTION_EVIDENCE_ENTRY_EXIT_PNL_REPLAY_TASK.md":
        problems.append("unexpected_task")

    scope = result.get("scope", {})
    expected_true = (
        "local_raw_databento_files_only",
    )
    expected_false = (
        "databento_called",
        "tastytrade_called",
        "schwab_called",
        "more_data_requested",
        "definition_requested_or_needed",
        "main_py_changed",
        "railway_or_deploy_changed",
        "broker_account_order_alert_touched",
        "credentials_or_env_changed",
        "sizing_changed",
        "raw_vendor_files_mutated",
    )
    for field in expected_true:
        if scope.get(field) is not True:
            problems.append(f"{field}_not_true")
    for field in expected_false:
        if scope.get(field) is not False:
            problems.append(f"{field}_not_false")

    setup = result.get("accepted_setup", {})
    if setup.get("selected_winner") != "DAY52-SPY-2026-03-16-CLEAN-FAST-BREAK-20260316T133000Z-P39":
        problems.append("selected_winner_changed")
    if setup.get("setup_family") != "Clean Fast Break":
        problems.append("setup_family_changed")
    if setup.get("trigger") != "668.360000000":
        problems.append("trigger_changed")
    if setup.get("invalidation") != "667.870000000":
        problems.append("invalidation_changed")
    window = setup.get("entry_window", {})
    if window.get("start") != "2026-03-16T13:31:00Z":
        problems.append("entry_window_start_changed")
    if window.get("end") != "2026-03-16T13:36:00Z":
        problems.append("entry_window_end_changed")
    if window.get("end_inclusive") is not False:
        problems.append("entry_window_end_inclusivity_changed")

    contract = result.get("selected_contract", {})
    if contract.get("raw_symbol") != "SPY   260330C00670000":
        problems.append("selected_contract_symbol_changed")
    if contract.get("instrument_id") != 1241515301:
        problems.append("selected_contract_instrument_changed")
    if contract.get("publisher_id") != 30:
        problems.append("selected_contract_publisher_changed")

    input_validation = result.get("input_validation", {})
    if input_validation.get("definition_requested_or_needed") is not False:
        problems.append("definition_needed_unexpected")
    if "definition" in input_validation.get("completed_or_reused_schemas", []):
        problems.append("definition_schema_unexpected")
    if input_validation.get("manifest_status") != "SUCCESS":
        problems.append("manifest_not_success")
    if input_validation.get("download_performed") is not True:
        problems.append("download_not_validated")
    if input_validation.get("request_count") != 32:
        problems.append("request_count_not_32")
    if input_validation.get("completed_or_reused_request_count") != 32:
        problems.append("completed_request_count_not_32")
    if input_validation.get("remaining_request_count") != 0:
        problems.append("remaining_requests_not_zero")
    if input_validation.get("status") == "INPUTS_VALIDATED":
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
    if (
        input_validation.get("previous_blocker") == "open_interest_statistics_zero_rows"
        and input_validation.get("old_blocker_closed_by_raw_statistics") is True
        and not input_validation.get("target_contract_in_manifest")
    ):
        problems.append("old_blocker_closed_without_target_raw_statistics")

    evaluation = result.get("evaluation", {})
    if evaluation.get("entry_status") not in VALID_ENTRY_STATUSES:
        problems.append("unexpected_entry_status")
    if evaluation.get("exit_status") not in VALID_EXIT_STATUSES:
        problems.append("unexpected_exit_status")
    if evaluation.get("net_pnl_status") not in VALID_NET_PNL_STATUSES:
        problems.append("unexpected_net_pnl_status")
    if evaluation.get("entry_status") == "NO_ENTRY_EXACT_REJECTION" and not evaluation.get("first_blocker"):
        problems.append("no_entry_missing_first_blocker")
    if evaluation.get("entry_status") != "VALID_ENTRY_FOUND" and evaluation.get("net_pnl") is not None:
        problems.append("net_pnl_invented_without_entry")
    if (
        input_validation.get("target_contract_in_manifest") is False
        and evaluation.get("first_blocker") != "target_contract_not_in_day55_download_manifest"
    ):
        problems.append("missing_target_contract_not_exactly_rejected")

    proof = result.get("proof_status", {})
    complete = (
        evaluation.get("entry_status") == "VALID_ENTRY_FOUND"
        and evaluation.get("exit_status") == "EXIT_EVALUATED"
        and evaluation.get("net_pnl_status") == "NET_PNL_EVALUATED"
    )
    if proof.get("complete_end_to_end_backtest") != ("YES" if complete else "NO"):
        problems.append("complete_backtest_status_mismatch")
    if proof.get("profitability_proof") != "NO":
        problems.append("profitability_proof_not_no")
    if proof.get("paper_live_eligibility") != "NO":
        problems.append("paper_live_eligibility_not_no")
    if result.get("profitability_status") != "NO":
        problems.append("profitability_status_not_no")
    if result.get("paper_live_eligibility") != "NO":
        problems.append("top_level_paper_live_eligibility_not_no")

    serialized = json.dumps(result, sort_keys=True).lower()
    for forbidden in ("safe_fast_db_auth=", "api_key", "secret", "token"):
        if forbidden in serialized:
            problems.append(f"credential_field_present_{forbidden}")

    return {
        "status": "PASS" if not problems else "FAIL",
        "problems": problems,
        "entry_status": evaluation.get("entry_status"),
        "exit_status": evaluation.get("exit_status"),
        "net_pnl_status": evaluation.get("net_pnl_status"),
        "first_blocker": evaluation.get("first_blocker"),
    }


if __name__ == "__main__":
    validation = validate_result_document()
    print(json.dumps(validation, indent=2, sort_keys=True))
    if validation["problems"]:
        raise SystemExit(1)
