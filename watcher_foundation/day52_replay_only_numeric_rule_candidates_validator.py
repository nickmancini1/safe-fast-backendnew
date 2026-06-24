import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day52_replay_only_numeric_rule_candidates.json"
)

EXPECTED_FAMILIES = {"Ideal", "Clean Fast Break", "Continuation"}
EXPECTED_TRIGGER = "668.360000000"
EXPECTED_INVALIDATION = "667.870000000"


def validate_result_document(result_path=RESULT_PATH):
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    problems = []

    if result.get("result_version") != "day52_replay_only_numeric_rule_candidates_v1":
        problems.append("unexpected_result_version")
    if result.get("implementation_version") != "day52_replay_only_numeric_rule_candidates_impl_v1":
        problems.append("unexpected_implementation_version")

    scope = result.get("scope", {})
    if scope.get("mode") != "PROVISIONAL_REPLAY_ONLY":
        problems.append("mode_not_provisional_replay_only")
    if scope.get("accepted_numeric_rules_remain_unresolved") is not False:
        problems.append("accepted_rules_not_marked_established")
    if scope.get("profitability_proof") != "NO":
        problems.append("profitability_proof_not_no")
    if scope.get("paper_live_eligibility") != "NO":
        problems.append("paper_live_eligibility_not_no")
    for field in (
        "option_contract_selection",
        "entry_exit_costs_or_net_result",
        "paid_data_downloaded",
        "main_py_changed",
        "railway_or_deploy_changed",
        "broker_account_order_fill_alert_touched",
        "credentials_or_env_changed",
        "sizing_changed",
        "frozen_patch8_thresholds_changed",
    ):
        if scope.get(field):
            problems.append(f"{field}_true")

    accepted = result.get("accepted_mode_reference", {})
    if accepted.get("accepted_numeric_rules_remain_unresolved") is not False:
        problems.append("accepted_reference_not_established")
    if accepted.get("numeric_values_established") != 6:
        problems.append("accepted_numeric_values_established_changed")
    if accepted.get("numeric_values_unresolved") != 0:
        problems.append("accepted_numeric_values_unresolved_changed")

    records = result.get("setup_time_candidate_records", [])
    if {record.get("setup_family") for record in records} != EXPECTED_FAMILIES:
        problems.append("unexpected_setup_family_set")
    if len(records) != 3:
        problems.append("expected_three_setup_time_records")
    for record in records:
        family = record.get("setup_family")
        if record.get("status") != "PROVISIONAL_REPLAY_ONLY":
            problems.append(f"{family}_status_not_provisional")
        if record.get("candidate_rule_id") != "CANDIDATE_A_SETUP_BAR_RANGE":
            problems.append(f"{family}_candidate_rule_not_a")
        if record.get("selected_by_future_performance") is not False:
            problems.append(f"{family}_selected_by_future_performance")
        if record.get("information_cutoff") != "2026-03-16T13:30:00Z":
            problems.append(f"{family}_unexpected_cutoff")
        if record.get("trigger", {}).get("final_numeric_value") != EXPECTED_TRIGGER:
            problems.append(f"{family}_unexpected_trigger")
        if record.get("invalidation", {}).get("final_numeric_value") != EXPECTED_INVALIDATION:
            problems.append(f"{family}_unexpected_invalidation")
        if record.get("trigger", {}).get("source_field") != "high":
            problems.append(f"{family}_trigger_not_from_high")
        if record.get("invalidation", {}).get("source_field") != "low":
            problems.append(f"{family}_invalidation_not_from_low")
        missing = {
            item.get("candidate_rule_id"): item.get("missing_structural_field")
            for item in record.get("unavailable_higher_priority_candidates", [])
        }
        if "CANDIDATE_B_SETUP_STRUCTURE_RANGE" not in missing:
            problems.append(f"{family}_missing_candidate_b_blocker")
        if "CANDIDATE_C_NAMED_LEVEL" not in missing:
            problems.append(f"{family}_missing_candidate_c_blocker")
        observation = record.get("trigger_observation", {})
        if observation.get("which_occurred_first") != "trigger":
            problems.append(f"{family}_unexpected_trigger_observation")
        if observation.get("outcome_used_to_select_candidate") is not False:
            problems.append(f"{family}_outcome_used_to_select_candidate")

    summary = result.get("candidate_rule_summary", {})
    for family in EXPECTED_FAMILIES:
        candidate_a = summary.get("CANDIDATE_A_SETUP_BAR_RANGE", {}).get(family, {})
        if candidate_a.get("numeric_pairs_produced") != 1:
            problems.append(f"{family}_candidate_a_pair_not_produced")
        if candidate_a.get("setup_qualified_under_provisional_mode") != 1:
            problems.append(f"{family}_candidate_a_setup_qualified_count")

    accounting = result.get("complete_session_opportunity_accounting", {})
    expected_accounting = {
        "sessions_scanned": 1,
        "rows_scanned": 751,
        "recognition_records": 2253,
        "primary_timestamp_family_records": 1170,
        "duplicate_records": 1083,
        "rejected_records": 1167,
        "blocked_missing_evidence_records": 0,
        "setup_qualified_under_provisional_mode_records": 3,
        "selected_winner_records": 1,
        "suppressed_records": 2,
        "recognition_layer_executable_records": 1,
        "trade_candidates": 0,
        "selected_contracts": 0,
        "eligible_entries": 0,
        "recorded_entries": 0,
    }
    for key, expected in expected_accounting.items():
        if accounting.get(key) != expected:
            problems.append(f"{key}_expected_{expected}_got_{accounting.get(key)}")

    review = result.get("compact_setup_time_review", {})
    if review.get("post_cutoff_fields_excluded") is not True:
        problems.append("review_not_cutoff_limited")
    forbidden = {
        "future_high",
        "future_low",
        "later_favorable_move",
        "selected_contract",
        "entry",
        "exit",
        "pnl",
        "net_pnl",
    }
    for record in review.get("records", []):
        if forbidden.intersection(record):
            problems.append("review_leaks_future_or_economic_field")

    determinism = result.get("determinism_protection", {})
    if determinism.get("result") != "PASS":
        problems.append("determinism_not_pass")
    for field in (
        "repeated_runs_identical",
        "candidate_input_order_invariance",
        "replay_chunk_size_invariance",
        "candidate_order_invariance",
        "winner_selection_independent_of_insertion_order",
    ):
        if determinism.get(field) is not True:
            problems.append(f"{field}_not_true")

    guardrails = result.get("guardrails", {})
    for field in (
        "accepted_blockers_overwritten",
        "future_rows_used_to_construct_values",
        "post_cutoff_fields_in_setup_review",
        "outcome_used_for_candidate_priority",
        "option_pnl_calculated",
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
        "provisional_values": {
            record["setup_family"]: {
                "trigger": record["trigger"]["final_numeric_value"],
                "invalidation": record["invalidation"]["final_numeric_value"],
                "candidate_rule_id": record["candidate_rule_id"],
            }
            for record in records
        },
        "complete_session_opportunity_accounting": accounting,
    }


if __name__ == "__main__":
    validation = validate_result_document()
    print(json.dumps(validation, indent=2, sort_keys=True))
    if validation["problems"]:
        raise SystemExit(1)
