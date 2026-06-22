import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_end_to_end_raw_data_positive_entry_generation.json"
)
MANIFEST_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "fixtures"
    / "day50_raw_data_positive_entry_candidate_manifest.json"
)


def validate_result_document(result_path=RESULT_PATH, manifest_path=MANIFEST_PATH):
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    problems = []

    if result.get("candidate_manifest") != manifest:
        problems.append("result_manifest_and_fixture_manifest_disagree")
    if result.get("deterministic_comparison", {}).get("result") != "PASS":
        problems.append("deterministic_comparison_not_pass")
    if result.get("full_trade_funnel_first_run") != result.get("full_trade_funnel_second_run"):
        problems.append("full_trade_funnel_runs_differ")

    scorecard = result.get("new_candidate_scorecard", {})
    if scorecard.get("candidates_generated") != manifest.get("candidate_count"):
        problems.append("candidate_count_disagrees")
    if scorecard.get("setup_qualified_candidates", 0) < 0:
        problems.append("negative_setup_qualified_count")
    if scorecard.get("trade_candidates", 0) < 0:
        problems.append("negative_trade_candidate_count")

    request = result.get("exact_grouped_underlying_data_request", {})
    if not request.get("created"):
        problems.append("exact_grouped_underlying_request_missing")
    if request.get("dataset") != "DBEQ.BASIC":
        problems.append("unexpected_underlying_request_dataset")
    if request.get("schema") != "ohlcv-1m":
        problems.append("unexpected_underlying_request_schema")
    if request.get("downloaded"):
        problems.append("underlying_request_was_downloaded")
    if not request.get("cost_check", {}).get("checked_cost"):
        problems.append("missing_checked_cost_field")

    if result.get("databento_downloaded"):
        problems.append("databento_downloaded_true")
    if result.get("schwab_authenticated"):
        problems.append("schwab_authenticated_true")
    if result.get("broker_mutation_attempted"):
        problems.append("broker_mutation_attempted_true")
    if result.get("proof_accepted"):
        problems.append("proof_accepted_true")
    if result.get("profitability_claimed"):
        problems.append("profitability_claimed_true")
    if result.get("paper_eligible") or result.get("live_eligible"):
        problems.append("paper_or_live_eligibility_claimed")

    return {
        "status": "PASS" if not problems else "FAIL",
        "problems": problems,
        "raw_opportunities_inspected": result.get("raw_opportunities_inspected"),
        "candidate_count": manifest.get("candidate_count"),
        "checked_cost": request.get("cost_check", {}).get("checked_cost"),
    }


if __name__ == "__main__":
    validation = validate_result_document()
    print(json.dumps(validation, indent=2, sort_keys=True))
    if validation["problems"]:
        raise SystemExit(1)
