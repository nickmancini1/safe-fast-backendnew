import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day48_positive_trade_capture_funnel.json"
)

REQUIRED_STAGES = [
    "SETUP_DEVELOPING",
    "SETUP_QUALIFIED",
    "TRADE_CANDIDATE",
    "CONTRACT_SELECTED",
    "PRICE_ACCEPTABLE",
    "ENTRY_ELIGIBLE",
    "ENTRY_RECORDED",
    "EXIT_EVALUATED",
    "FINAL_OUTCOME",
]

CLASSIFICATIONS = {
    "VALID_TRADE_CAPTURED",
    "TRUE_NO_TRADE",
    "MISSING_DATA",
    "MISSED_VALID_TRADE",
    "INVALID_TRADE_ALLOWED",
    "UNRESOLVED",
}

SCORECARD_FIELDS = {
    "candidates_found",
    "candidates_runnable",
    "setup_developing_count",
    "setup_qualified_count",
    "trade_candidate_count",
    "contracts_selected",
    "prices_accepted",
    "entries_eligible",
    "entries_recorded",
    "exits_evaluated",
    "valid_trades_captured",
    "true_no_trades",
    "missing_data_cases",
    "missed_valid_trades",
    "invalid_trades_allowed",
    "unresolved_cases",
    "winners",
    "losers",
    "deterministic_cases",
    "unstable_cases",
    "first_blocker_totals_by_funnel_stage",
    "conversion_rate_between_stages",
    "sample_contract_progress",
}


def validate_funnel_document(document):
    problems = []
    _require(document, "frozen_engine_or_rule_version", problems)
    _require(document, "source_commit", problems)
    _require(document, "run_timestamp", problems)
    if document.get("funnel_stages") != REQUIRED_STAGES:
        problems.append("funnel_stages do not match required chronological funnel")

    records = document.get("candidate_records")
    if not isinstance(records, list) or not records:
        problems.append("candidate_records must be a non-empty list")
        records = []

    for index, record in enumerate(records):
        _validate_record(record, index, problems)

    for key in ("Ideal", "Clean Fast Break", "Continuation"):
        scorecard = document.get("family_scorecards", {}).get(key)
        _validate_scorecard(scorecard, f"family_scorecards.{key}", problems)
    _validate_scorecard(document.get("combined_scorecard"), "combined_scorecard", problems)

    final_classifications = document.get("final_classifications", {})
    for classification in CLASSIFICATIONS:
        if classification not in final_classifications:
            problems.append(f"final_classifications missing {classification}")

    combined = document.get("combined_scorecard", {})
    if combined.get("valid_trades_captured", 0) != final_classifications.get(
        "VALID_TRADE_CAPTURED", -1
    ):
        problems.append("combined valid_trades_captured disagrees with classifications")
    if combined.get("true_no_trades", 0) != final_classifications.get("TRUE_NO_TRADE", -1):
        problems.append("combined true_no_trades disagrees with classifications")
    if combined.get("missing_data_cases", 0) != final_classifications.get("MISSING_DATA", -1):
        problems.append("combined missing_data_cases disagrees with classifications")

    comparison = document.get("deterministic_comparison", {})
    if comparison.get("result") != "PASS":
        problems.append("deterministic comparison must pass")
    if document.get("first_run_hash") != document.get("second_run_hash"):
        problems.append("first and second run hashes differ")

    owner_questions = document.get("owner_questions", {})
    if len(owner_questions) != 5:
        problems.append("owner_questions must contain exactly five answers")

    if document.get("proof_accepted") is not False:
        problems.append("proof_accepted must remain false")
    if document.get("profitability_claimed") is not False:
        problems.append("profitability_claimed must remain false")
    if document.get("promotion_decision_made") is not False:
        problems.append("promotion_decision_made must remain false")

    return problems


def validate_funnel_file(path=DEFAULT_RESULT_PATH):
    path = Path(path)
    if not path.exists():
        return [f"missing funnel result file: {path}"]
    return validate_funnel_document(json.loads(path.read_text(encoding="utf-8")))


def _validate_record(record, index, problems):
    prefix = f"candidate_records[{index}]"
    required = (
        "candidate_identifier",
        "setup_family",
        "underlying",
        "direction",
        "signal_timestamp",
        "evidence_source",
        "chronological_stage_path",
        "funnel_stage_path",
        "highest_stage_reached",
        "first_stage_not_reached",
        "blocker_category",
        "contract_selection_result",
        "execution_result",
        "context_and_caution_result",
        "winner_selection_result",
        "entry_result",
        "exit_result",
        "final_classification",
        "final_outcome",
        "first_run_output",
        "second_run_output",
        "deterministic_result",
    )
    for key in required:
        if key not in record:
            problems.append(f"{prefix} missing {key}")

    classification = record.get("final_classification")
    if classification not in CLASSIFICATIONS:
        problems.append(f"{prefix} has invalid final_classification {classification!r}")

    first_not_reached = record.get("first_stage_not_reached")
    if first_not_reached is not None and first_not_reached not in REQUIRED_STAGES:
        problems.append(f"{prefix} first_stage_not_reached is not a valid stage")

    if classification == "TRUE_NO_TRADE" and record.get("blocker_category") != "real frozen-rule failure":
        problems.append(f"{prefix} true no-trade must cite a real frozen-rule failure")
    if classification == "MISSING_DATA" and record.get("blocker_category") != "missing data":
        problems.append(f"{prefix} missing-data case must cite missing data")
    if classification == "VALID_TRADE_CAPTURED":
        if record.get("first_stage_not_reached") is not None:
            problems.append(f"{prefix} valid captured trade must reach final outcome")
        if record.get("winner_or_loser") not in {"winner", "loser"}:
            problems.append(f"{prefix} valid captured trade must record winner/loser")
    if classification in {"MISSED_VALID_TRADE", "INVALID_TRADE_ALLOWED"}:
        problems.append(f"{prefix} found {classification}; promotion must stay blocked")


def _validate_scorecard(scorecard, name, problems):
    if not isinstance(scorecard, dict):
        problems.append(f"{name} must be an object")
        return
    missing = sorted(SCORECARD_FIELDS - set(scorecard))
    for field in missing:
        problems.append(f"{name} missing {field}")


def _require(document, key, problems):
    if not document.get(key):
        problems.append(f"missing {key}")


if __name__ == "__main__":
    found = validate_funnel_file()
    if found:
        for problem in found:
            print(problem)
        raise SystemExit(1)
    print("day48 positive trade capture funnel validation passed")
