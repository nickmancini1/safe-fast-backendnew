import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day49_positive_entry_setup_evidence_completion.json"
)
DEFAULT_REQUEST_MANIFEST_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "source_data"
    / "richer_export_package_work"
    / "day49_positive_entry_exact_setup_data_request_manifest.json"
)

EXPECTED_RESULT_VERSION = "day49_positive_entry_setup_evidence_completion_or_replacement_v1"
EXPECTED_REQUEST_VERSION = "day49_positive_entry_exact_setup_data_request_v1"
ALLOWED_SLOT_CLASSIFICATIONS = {
    "SETUP_EVIDENCE_COMPLETED",
    "EXACT_EXTERNAL_SETUP_DATA_REQUIRED",
    "SOURCE_CONTRADICTION",
    "CANDIDATE_UNUSABLE",
}
REQUIRED_FIELDS = {
    "setup_time_row",
    "trigger",
    "invalidation",
    "freshness_final_signal_state",
    "blocker_caution_review",
    "no_hindsight_boundary",
    "session_boundary_behavior",
}


def validate_result_document(document):
    problems = []
    if document.get("result_version") != EXPECTED_RESULT_VERSION:
        problems.append("unexpected result_version")
    if document.get("candidate_slot_count") != 8:
        problems.append("candidate_slot_count must be 8")
    if document.get("proof_accepted") is not False:
        problems.append("proof_accepted must remain false")
    if document.get("profitability_claimed") is not False:
        problems.append("profitability_claimed must remain false")
    if document.get("databento_downloaded") is not False:
        problems.append("Databento download must remain false")
    if document.get("exit_path_data_downloaded") is not False:
        problems.append("exit-path data download must remain false")

    comparison = document.get("deterministic_comparison", {})
    if comparison.get("result") != "PASS":
        problems.append("deterministic comparison must pass")
    if comparison.get("first_run_hash") != comparison.get("second_run_hash"):
        problems.append("deterministic hashes must match")

    records = document.get("candidate_slot_records")
    if not isinstance(records, list):
        problems.append("candidate_slot_records must be a list")
        records = []
    if len(records) != 8:
        problems.append("candidate_slot_records must contain 8 records")
    if len({record.get("candidate_identifier") for record in records}) != len(records):
        problems.append("candidate identifiers must be unique")
    for index, record in enumerate(records):
        _validate_slot(record, index, problems)

    scorecard = document.get("scorecard", {})
    if scorecard.get("candidate_slots_completed_locally") != 0:
        problems.append("local completed slot count must be 0 for current evidence")
    if scorecard.get("candidate_slots_replaced") != 0:
        problems.append("replacement count must be 0 when no complete replacement exists")
    if scorecard.get("setup_qualified_count") != 0:
        problems.append("setup-qualified total must remain 0")
    if scorecard.get("trade_candidate_count") != 0:
        problems.append("trade-candidate total must remain 0")

    replacement = document.get("replacement_selection", {})
    if replacement.get("complete_local_replacement_count") != 0:
        problems.append("complete_local_replacement_count must be 0")
    if replacement.get("selected_replacements") not in ([], None):
        problems.append("selected_replacements must be empty")

    manifest = document.get("exact_setup_data_request_manifest", {})
    problems.extend(validate_request_manifest_document(manifest))
    return problems


def validate_request_manifest_document(document):
    problems = []
    if document.get("manifest_version") != EXPECTED_REQUEST_VERSION:
        problems.append("unexpected request manifest version")
    if document.get("request_scope") != "underlying_setup_evidence_only_no_options_no_exit_path":
        problems.append("request scope must be setup evidence only")
    if document.get("option_request_included") is not False:
        problems.append("request manifest must not include option requests")
    if document.get("exit_path_request_included") is not False:
        problems.append("request manifest must not include exit-path requests")
    if document.get("databento_downloaded") is not False:
        problems.append("request manifest must not download data")
    requests = document.get("requests")
    if not isinstance(requests, list):
        problems.append("requests must be a list")
        requests = []
    if document.get("request_count") != len(requests):
        problems.append("request_count mismatch")
    for index, request in enumerate(requests):
        _validate_request(request, index, problems)
    cost = document.get("cost_check", {})
    if cost.get("checked_cost") != "NOT_AVAILABLE":
        problems.append("checked cost must be NOT_AVAILABLE unless an exact safe cost check was run")
    if cost.get("credential_used") is not False:
        problems.append("credential_used must remain false when no exact safe cost check ran")
    return problems


def validate_result_file(path=DEFAULT_RESULT_PATH):
    path = Path(path)
    if not path.exists():
        return [f"missing result file: {path}"]
    return validate_result_document(json.loads(path.read_text(encoding="utf-8")))


def validate_request_manifest_file(path=DEFAULT_REQUEST_MANIFEST_PATH):
    path = Path(path)
    if not path.exists():
        return [f"missing request manifest file: {path}"]
    return validate_request_manifest_document(json.loads(path.read_text(encoding="utf-8")))


def _validate_slot(record, index, problems):
    prefix = f"candidate_slot_records[{index}]"
    classification = record.get("slot_classification")
    if classification not in ALLOWED_SLOT_CLASSIFICATIONS:
        problems.append(f"{prefix} has invalid slot_classification")
    if record.get("formal_outcome_not_vague_missing_data") is not True:
        problems.append(f"{prefix} must have formal non-vague outcome")
    if record.get("proof_accepted") is not False:
        problems.append(f"{prefix} proof_accepted must be false")
    if record.get("profitability_claimed") is not False:
        problems.append(f"{prefix} profitability_claimed must be false")
    matrix = record.get("missing_field_matrix", {})
    fields = matrix.get("fields", [])
    field_names = {field.get("field_name") for field in fields}
    if field_names != REQUIRED_FIELDS:
        problems.append(f"{prefix} field matrix must cover every required setup field")
    for field in fields:
        if field.get("field_status") not in {"present", "derivable", "contradictory", "absent"}:
            problems.append(f"{prefix} field has invalid status")
        if not field.get("exact_rule_consumer"):
            problems.append(f"{prefix} field missing exact_rule_consumer")
        if not field.get("smallest_evidence_needed"):
            problems.append(f"{prefix} field missing smallest_evidence_needed")


def _validate_request(request, index, problems):
    prefix = f"requests[{index}]"
    required = (
        "candidate_identifier",
        "missing_fields",
        "decision_resolved",
        "dataset",
        "schema",
        "symbol",
        "start_timestamp",
        "end_timestamp",
        "timezone",
        "source_file",
        "source_rows",
        "required_rows_or_fields",
        "why_local_evidence_is_insufficient",
        "estimated_response_consumer",
    )
    for key in required:
        if key not in request:
            problems.append(f"{prefix} missing {key}")
    if request.get("start_timestamp") == "EXACT_SOURCE_WINDOW_START_REQUIRED":
        problems.append(f"{prefix} start_timestamp must be exact")
    if request.get("end_timestamp") == "EXACT_SOURCE_WINDOW_END_REQUIRED":
        problems.append(f"{prefix} end_timestamp must be exact")
    forbidden = set(request.get("forbidden_scope", []))
    if not {"options", "exit_path", "P&L"} <= forbidden:
        problems.append(f"{prefix} must forbid option, exit path, and P&L scope")


if __name__ == "__main__":
    found = validate_result_file() + validate_request_manifest_file()
    if found:
        for problem in found:
            print(problem)
        raise SystemExit(1)
    print("day49 positive-entry setup evidence completion validation passed")
