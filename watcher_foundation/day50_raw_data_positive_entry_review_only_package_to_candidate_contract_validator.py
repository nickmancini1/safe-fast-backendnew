import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_raw_data_positive_entry_review_only_package_to_candidate_contract.json"
)


def validate_result_document(result_path=RESULT_PATH):
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    problems = []

    if (
        result.get("result_version")
        != "day50_raw_data_positive_entry_review_only_package_to_candidate_contract_v1"
    ):
        problems.append("unexpected_result_version")

    policy = result.get("contract_policy", {})
    for field in (
        "bounded_to_day50_spy_2026_03_16",
        "processes_each_setup_family_separately",
        "setup_time_boundary_frozen",
        "no_hindsight_preserved",
        "session_boundary_preserved",
        "developing_stage_transitions_validated",
        "stable_winner_selection_preserved",
        "no_trade_preservation_validated",
        "setup_qualified_requires_generated_candidate",
    ):
        if not policy.get(field):
            problems.append(f"{field}_not_true")
    for field in (
        "raw_vendor_bars_treated_as_safe_fast_labels",
        "frozen_trading_rules_changed",
        "thresholds_loosened",
        "missing_fields_invented",
        "option_evidence_invented",
        "exit_evidence_invented",
        "main_py_changed",
        "railway_or_deploy_changed",
        "paid_data_downloaded",
    ):
        if policy.get(field):
            problems.append(f"{field}_true")

    expected_families = {"Ideal", "Clean Fast Break", "Continuation"}
    records = result.get("setup_family_contract_records", [])
    if len(records) != 3:
        problems.append("expected_three_contract_records")
    if {record.get("setup_family") for record in records} != expected_families:
        problems.append("unexpected_setup_family_set")

    for record in records:
        family = record.get("setup_family")
        stages = record.get("stage_reached", {})
        for stage in ("mapped_package", "generated_candidate", "setup_qualified"):
            if not stages.get(stage):
                problems.append(f"{family}_{stage}_not_reached")
        for stage in ("trade_candidate", "selected_contract", "eligible_entry", "recorded_entry"):
            if stages.get(stage):
                problems.append(f"{family}_{stage}_unexpectedly_reached")
        if record.get("highest_stage_reached") != "setup_qualified":
            problems.append(f"{family}_unexpected_highest_stage")
        if record.get("first_stage_not_reached") != "trade_candidate":
            problems.append(f"{family}_unexpected_first_stage_not_reached")
        if record.get("exact_outcome") != "setup_qualified_created":
            problems.append(f"{family}_unexpected_exact_outcome")
        if record.get("exact_remaining_blocker") != "selected_contract_option_evidence_missing":
            problems.append(f"{family}_unexpected_remaining_blocker")
        if record.get("raw_vendor_bars_treated_as_safe_fast_labels"):
            problems.append(f"{family}_raw_vendor_label_used")
        gap = record.get("contract_gap", {})
        if gap.get("missing_setup_fields") != []:
            problems.append(f"{family}_unexpected_setup_gap")
        expected_trade_gap = [
            "selected_contract_identity",
            "selected_contract_quote_freshness",
            "selected_contract_liquidity",
            "entry_execution_context",
        ]
        if gap.get("missing_trade_candidate_fields") != expected_trade_gap:
            problems.append(f"{family}_unexpected_trade_gap")
        if record.get("costed_entry_exit_replay_status") != "NOT_RUN_NO_TRADE_CANDIDATE":
            problems.append(f"{family}_unexpected_costed_replay_status")

    after = result.get("after_funnel_totals", {})
    expected_after = {
        "raw_opportunities_mapped": 3,
        "exact_setup_time_field_packages_established": 3,
        "new_generated_candidates": 3,
        "new_setup_qualified_candidates": 3,
        "new_trade_candidates": 0,
        "new_selected_contracts": 0,
        "new_eligible_entries": 0,
        "new_recorded_entries": 0,
        "new_exact_generation_contract_required_cases": 0,
        "new_exact_option_contract_evidence_required_cases": 3,
        "new_exact_data_required_cases": 3,
        "new_valid_trades_captured": 0,
        "new_true_no_trades": 0,
        "new_missed_valid_trades": 0,
        "new_invalid_trades_allowed": 0,
        "new_unresolved_cases": 0,
        "new_winners": 0,
        "new_losers": 0,
    }
    for key, expected in expected_after.items():
        if after.get(key) != expected:
            problems.append(f"{key}_expected_{expected}_got_{after.get(key)}")

    request = result.get("exact_grouped_evidence_request", {})
    if not request.get("created"):
        problems.append("grouped_evidence_request_not_created")
    if len(request.get("requests", [])) != 3:
        problems.append("expected_three_grouped_evidence_requests")
    for item in request.get("requests", []):
        if item.get("contract") != "NOT_KNOWN_BEFORE_SELECTED_CONTRACT_EVIDENCE":
            problems.append("unexpected_contract_identity_in_request")
        for block in ("trade_candidate", "entry", "costs", "P&L"):
            if block not in item.get("blocks", []):
                problems.append(f"request_missing_block_{block}")

    if result.get("accepted_mapper_regression_case_count") != 17:
        problems.append("accepted_mapper_regression_case_count_not_17")
    if any(case.get("status") != "PASS" for case in result.get("accepted_mapper_regression_cases", [])):
        problems.append("accepted_mapper_case_not_pass")
    if result.get("retry_control_result", {}).get("deterministic_result") != "PASS":
        problems.append("retry_control_not_pass")
    if result.get("deterministic_comparison", {}).get("result") != "PASS":
        problems.append("determinism_not_pass")

    controls = result.get("preserved_day50_controls", {})
    if controls != {
        "setup_qualified": 13,
        "trade_candidates": 9,
        "selected_contracts": 5,
        "eligible_entries": 1,
        "recorded_entries": 1,
        "closed_safety_rejections_reopened": 0,
    }:
        problems.append("preserved_controls_changed")

    guardrails = result.get("guardrails", {})
    for field in (
        "schwab_authenticated",
        "broker_mutation_attempted",
        "proof_accepted",
        "profitability_claimed",
        "promotion_decision_made",
        "paper_eligible",
        "live_eligible",
    ):
        if guardrails.get(field):
            problems.append(f"{field}_true")

    return {
        "status": "PASS" if not problems else "FAIL",
        "problems": problems,
        "contract_records": len(records),
        "generated_candidates": after.get("new_generated_candidates"),
        "setup_qualified": after.get("new_setup_qualified_candidates"),
        "trade_candidates": after.get("new_trade_candidates"),
    }


if __name__ == "__main__":
    validation = validate_result_document()
    print(json.dumps(validation, indent=2, sort_keys=True))
    if validation["problems"]:
        raise SystemExit(1)
