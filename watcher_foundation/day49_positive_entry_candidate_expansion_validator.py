import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "fixtures"
    / "day49_positive_entry_candidate_expansion_manifest.json"
)
DEFAULT_RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day49_positive_entry_candidate_expansion.json"
)

REQUIRED_FAMILIES = {"Ideal", "Clean Fast Break", "Continuation"}
FORBIDDEN_SELECTION_INPUTS = {
    "outcome_window",
    "later price move",
    "option exit path",
    "P&L",
    "profitability",
    "winner_or_loser",
}


def validate_manifest_document(document):
    problems = []
    if document.get("manifest_version") != "day49_positive_entry_candidate_expansion_v1":
        problems.append("unexpected manifest_version")
    if document.get("development_evidence_not_holdout") is not True:
        problems.append("manifest must mark candidates as development evidence")
    if document.get("protected_holdout_candidates_selected") != 0:
        problems.append("protected holdout candidates must not be selected")
    if document.get("proof_accepted") is not False:
        problems.append("proof_accepted must remain false")
    if document.get("profitability_claimed") is not False:
        problems.append("profitability_claimed must remain false")

    selection = document.get("selection_policy", {})
    forbidden = set(selection.get("forbidden_selection_inputs", ()))
    if not FORBIDDEN_SELECTION_INPUTS <= forbidden:
        problems.append("selection policy must forbid outcome/profit fields")
    if "outcome_window" in set(selection.get("outcome_blind_fields_used", ())):
        problems.append("selection inputs include outcome_window")

    comparison = document.get("deterministic_selection", {})
    if comparison.get("result") != "PASS":
        problems.append("deterministic selection must pass")
    if comparison.get("first_run_hash") != comparison.get("second_run_hash"):
        problems.append("selection hashes differ")

    candidates = document.get("candidates")
    if not isinstance(candidates, list):
        problems.append("candidates must be a list")
        candidates = []
    if len({row.get("candidate_identifier") for row in candidates}) != len(candidates):
        problems.append("candidate identifiers must be unique")
    for index, row in enumerate(candidates):
        _validate_candidate(row, index, problems)

    selected_ids = {row.get("candidate_identifier") for row in candidates}
    for exclusion in document.get("exclusions", []):
        if exclusion.get("candidate_identifier") in selected_ids:
            problems.append("selected candidate appears in exclusions")
        if not exclusion.get("exclusion_reason"):
            problems.append("exclusion missing reason")
    return problems


def validate_result_document(document):
    problems = []
    if document.get("result_version") != "day49_positive_entry_candidate_expansion_v1":
        problems.append("unexpected result_version")
    problems.extend(validate_manifest_document(document.get("candidate_manifest", {})))
    comparison = document.get("deterministic_comparison", {})
    if comparison.get("result") != "PASS":
        problems.append("result deterministic comparison must pass")
    if document.get("proof_accepted") is not False:
        problems.append("proof_accepted must remain false")
    if document.get("profitability_claimed") is not False:
        problems.append("profitability_claimed must remain false")
    if document.get("databento_downloaded") is not False:
        problems.append("Databento must not be downloaded in this task")

    records = document.get("new_candidate_records")
    if not isinstance(records, list):
        problems.append("new_candidate_records must be a list")
        records = []
    scorecard = document.get("new_combined_scorecard", {})
    if scorecard.get("candidates_found") != len(records):
        problems.append("new_combined_scorecard candidate count mismatch")
    if scorecard.get("true_no_trades", 0) and scorecard.get("missing_data_cases", 0) == 0:
        problems.append("missing evidence must not be hidden as true no-trade")
    if scorecard.get("trade_candidate_count") == 0:
        package = document.get("setup_time_request_package", {})
        if package.get("request_created") is not False:
            problems.append("no setup-time request should be created without trade candidates")

    existing = document.get("existing_regression_control_result", {})
    if existing.get("candidate_count") != 15:
        problems.append("existing regression control must preserve 15 candidates")
    if existing.get("deterministic_result") != "PASS":
        problems.append("existing regression control must be deterministic")
    if len(document.get("owner_questions", {})) != 5:
        problems.append("owner_questions must contain exactly five answers")
    return problems


def validate_manifest_file(path=DEFAULT_MANIFEST_PATH):
    path = Path(path)
    if not path.exists():
        return [f"missing manifest file: {path}"]
    return validate_manifest_document(json.loads(path.read_text(encoding="utf-8")))


def validate_result_file(path=DEFAULT_RESULT_PATH):
    path = Path(path)
    if not path.exists():
        return [f"missing result file: {path}"]
    return validate_result_document(json.loads(path.read_text(encoding="utf-8")))


def _validate_candidate(row, index, problems):
    prefix = f"candidates[{index}]"
    required = (
        "candidate_identifier",
        "setup_family",
        "underlying",
        "direction",
        "signal_timestamp",
        "timezone",
        "session_date",
        "source_rows",
        "candidate_generation_rule_version",
        "lifecycle_rule_version",
        "development_evidence_not_holdout",
        "protected_holdout",
        "duplicate_signal",
        "pre_outcome_fields",
    )
    for key in required:
        if key not in row:
            problems.append(f"{prefix} missing {key}")
    if row.get("setup_family") not in REQUIRED_FAMILIES:
        problems.append(f"{prefix} has unsupported setup_family")
    if row.get("development_evidence_not_holdout") is not True:
        problems.append(f"{prefix} must be development evidence")
    if row.get("protected_holdout") is not False:
        problems.append(f"{prefix} must not be protected holdout")
    if row.get("duplicate_signal") is not False:
        problems.append(f"{prefix} must not be duplicate signal")
    fields = row.get("pre_outcome_fields", {})
    if "outcome_window" in fields:
        problems.append(f"{prefix} pre_outcome_fields must not include outcome_window")


if __name__ == "__main__":
    found = validate_manifest_file() + validate_result_file()
    if found:
        for problem in found:
            print(problem)
        raise SystemExit(1)
    print("day49 positive-entry candidate expansion validation passed")
