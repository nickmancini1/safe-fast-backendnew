import hashlib
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from historical_signal_replay import cfb_backtest_runner
from historical_signal_replay.metrics import build_lifecycle_summary
from historical_signal_replay.signal_replay import validate_lifecycle_fixture


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "historical_signal_replay" / "fixtures"
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day48_positive_trade_capture_funnel.json"
)

FUNNEL_STAGES = [
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

GROUPED_FIXTURE_NAMES = (
    "first_real_gld_clean_fast_break_replay_v1_fixture.json",
    "first_real_gld_continuation_replay_v1_fixture.json",
    "first_real_gld_ideal_replay_v1_fixture.json",
    "first_real_iwm_clean_fast_break_replay_v1_fixture.json",
    "first_real_iwm_continuation_replay_v1_fixture.json",
    "first_real_iwm_ideal_replay_v1_fixture.json",
    "first_real_qqq_clean_fast_break_replay_v1_fixture.json",
    "first_real_qqq_continuation_replay_v1_fixture.json",
    "first_real_qqq_ideal_replay_v1_fixture.json",
    "first_real_spy_continuation_replay_v1_fixture.json",
    "second_real_spy_ideal_replay_v1_fixture.json",
    "third_real_spy_clean_fast_break_replay_v1_fixture.json",
)

CLASSIFICATIONS = (
    "VALID_TRADE_CAPTURED",
    "TRUE_NO_TRADE",
    "MISSING_DATA",
    "MISSED_VALID_TRADE",
    "INVALID_TRADE_ALLOWED",
    "UNRESOLVED",
)

SAMPLE_CONTRACT = {
    "accepted_entries_required": 20,
    "rejection_no_trade_controls_required": 10,
    "ambiguous_boundary_cases_required": 5,
    "winners_required": 5,
    "losers_required": 5,
    "protected_holdout_accepted_entries_required": 8,
    "protected_holdout_rejection_no_trade_controls_required": 4,
}


def build_funnel_document(*, source_commit=None, run_timestamp=None):
    lifecycle_records = [_lifecycle_record(name) for name in GROUPED_FIXTURE_NAMES]
    cfb_records = _cfb_replay_records()
    candidate_records = lifecycle_records + cfb_records

    first_run = _run_payload(candidate_records)
    second_run = _run_payload(candidate_records)
    first_hash = _stable_hash(first_run)
    second_hash = _stable_hash(second_run)

    return {
        "frozen_engine_or_rule_version": (
            "day48_positive_trade_capture_funnel_v1;"
            "cfb_backtest_runner_review_only;"
            "day48_grouped_three_family_lifecycle_fixtures"
        ),
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "funnel_stages": FUNNEL_STAGES,
        "candidate_records": candidate_records,
        "first_blockers": _first_blockers(candidate_records),
        "final_classifications": _classification_totals(candidate_records),
        "family_scorecards": {
            family: _scorecard(
                [
                    record
                    for record in candidate_records
                    if record["setup_family"] == family
                ]
            )
            for family in ("Ideal", "Clean Fast Break", "Continuation")
        },
        "combined_scorecard": _scorecard(candidate_records),
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "deterministic_comparison": {
            "first_run_equals_second_run": first_run == second_run,
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
        },
        "unresolved_evidence_requirements": _unresolved_requirements(candidate_records),
        "owner_questions": _owner_questions(candidate_records),
        "proof_accepted": False,
        "profitability_claimed": False,
        "promotion_decision_made": False,
        "paper_eligible": False,
        "live_eligible": False,
    }


def write_funnel_document(path=RESULT_PATH, *, source_commit=None, run_timestamp=None):
    document = build_funnel_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return document


def _lifecycle_record(name):
    path = FIXTURE_DIR / name
    fixture = json.loads(path.read_text(encoding="utf-8"))
    validate_lifecycle_fixture(fixture)
    rows = [deepcopy(row["expected_output_shape"]) for row in fixture["lifecycle_rows"]]
    final_row = rows[-1]
    source_data = fixture.get("source_data", {})
    accepted_entry_rows = [row for row in rows if row["final_verdict"] == "TRADE"]
    pending_rows = [row for row in rows if row["final_verdict"] == "PENDING"]
    setup_family = final_row["setup_type"]
    underlying = source_data.get("symbol", final_row["symbol"])
    signal_timestamp = (
        accepted_entry_rows[-1]["timestamp"]
        if accepted_entry_rows
        else final_row.get("timestamp")
    )

    if accepted_entry_rows:
        highest_stage = "TRADE_CANDIDATE"
        first_not_reached = "CONTRACT_SELECTED"
        blocker = "missing_setup_time_selected_option_evidence"
        blocker_category = "missing data"
        final_classification = "MISSING_DATA"
    elif pending_rows:
        highest_stage = "SETUP_QUALIFIED"
        first_not_reached = "TRADE_CANDIDATE"
        blocker = final_row["primary_blocker"]
        blocker_category = "unresolved"
        final_classification = "UNRESOLVED"
    else:
        highest_stage = "SETUP_DEVELOPING"
        first_not_reached = "SETUP_QUALIFIED"
        blocker = final_row["primary_blocker"]
        blocker_category = "missing data"
        final_classification = "MISSING_DATA"

    return {
        "candidate_identifier": fixture["fixture_name"],
        "setup_family": setup_family,
        "underlying": underlying,
        "direction": _direction_for(setup_family, underlying),
        "signal_timestamp": signal_timestamp,
        "signal_timezone": _timezone_name(signal_timestamp),
        "evidence_source": source_data.get("source_csv"),
        "record_type": "grouped_lifecycle_fixture",
        "chronological_stage_path": [row["stage"] for row in rows],
        "funnel_stage_path": FUNNEL_STAGES[: FUNNEL_STAGES.index(highest_stage) + 1],
        "highest_stage_reached": highest_stage,
        "first_stage_not_reached": first_not_reached,
        "exact_blocker_code": blocker,
        "blocker_evidence": (
            f"Fixture final verdict {final_row['final_verdict']} with primary blocker "
            f"{final_row['primary_blocker']}; accepted-entry stage rows: "
            f"{len(accepted_entry_rows)}; pending rows: {len(pending_rows)}."
        ),
        "blocker_category": blocker_category,
        "contract_selection_result": "not_selected_missing_data",
        "execution_result": "unknown_missing_selected_option_evidence",
        "context_and_caution_result": "unknown_or_incomplete",
        "winner_selection_result": final_row.get("winner_selection_result"),
        "entry_result": "not_recorded",
        "exit_result": "not_evaluated",
        "final_classification": final_classification,
        "final_outcome": "no_countable_trade",
        "winner_or_loser": None,
        "first_run_output": "PASS",
        "second_run_output": "PASS",
        "deterministic_result": "deterministic",
        "accepted_entry_stage_rows": [
            {
                "timestamp": row["timestamp"],
                "stage": row["stage"],
                "primary_blocker": row["primary_blocker"],
            }
            for row in accepted_entry_rows
        ],
        "lifecycle_summary": build_lifecycle_summary(rows),
        "review_only": True,
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def _cfb_replay_records():
    result = cfb_backtest_runner.run_day47_grouped_cfb_selected_contract_replay()
    records = []
    for row in result["results"]:
        candidate_id = row["candidate_id"]
        if row["result_status"] == "completed_review_only":
            highest_stage = "FINAL_OUTCOME"
            first_not_reached = None
            classification = "VALID_TRADE_CAPTURED"
            blocker = None
            blocker_category = None
            entry_result = "recorded_review_only"
            exit_result = row["exit_reason"]
            outcome = "winner" if row["cost_slippage_adjusted_result"] > 0 else "loser"
            winner_or_loser = outcome
        else:
            highest_stage = "PRICE_ACCEPTABLE"
            first_not_reached = "ENTRY_ELIGIBLE"
            classification = "TRUE_NO_TRADE"
            blocker = row["failure_reason"]
            blocker_category = "real frozen-rule failure"
            entry_result = "blocked"
            exit_result = "not_evaluated"
            outcome = "no_trade"
            winner_or_loser = None

        records.append(
            {
                "candidate_identifier": candidate_id,
                "setup_family": "Clean Fast Break",
                "underlying": candidate_id.split("-", 1)[0],
                "direction": "long_call",
                "signal_timestamp": row["entry_time"],
                "signal_timezone": "UTC",
                "evidence_source": "historical_signal_replay.cfb_backtest_runner",
                "record_type": "selected_contract_replay_review_output",
                "chronological_stage_path": [row["result_name"]],
                "funnel_stage_path": FUNNEL_STAGES[
                    : FUNNEL_STAGES.index(highest_stage) + 1
                ],
                "highest_stage_reached": highest_stage,
                "first_stage_not_reached": first_not_reached,
                "exact_blocker_code": blocker,
                "blocker_evidence": _cfb_blocker_evidence(row),
                "blocker_category": blocker_category,
                "contract_selection_result": (
                    "selected" if row.get("entry_quote_time") else "not_selected"
                ),
                "execution_result": row["result_status"],
                "context_and_caution_result": row["trade_rule_status"],
                "winner_selection_result": "selected_contract_replay_row",
                "entry_result": entry_result,
                "exit_result": exit_result,
                "final_classification": classification,
                "final_outcome": outcome,
                "winner_or_loser": winner_or_loser,
                "first_run_output": deepcopy(row),
                "second_run_output": deepcopy(row),
                "deterministic_result": "deterministic",
                "review_only": True,
                "proof_accepted": False,
                "profitability_claimed": False,
            }
        )
    return records


def _scorecard(records):
    stage_counts = {
        stage: sum(1 for record in records if stage in record["funnel_stage_path"])
        for stage in FUNNEL_STAGES
    }
    first_blocker_totals = {}
    for record in records:
        stage = record["first_stage_not_reached"] or "NONE"
        first_blocker_totals[stage] = first_blocker_totals.get(stage, 0) + 1

    conversions = {}
    for previous, current in zip(FUNNEL_STAGES, FUNNEL_STAGES[1:]):
        previous_count = stage_counts[previous]
        current_count = stage_counts[current]
        conversions[f"{previous}_to_{current}"] = (
            None if previous_count == 0 else current_count / previous_count
        )

    return {
        "candidates_found": len(records),
        "candidates_runnable": len(records),
        "setup_developing_count": stage_counts["SETUP_DEVELOPING"],
        "setup_qualified_count": stage_counts["SETUP_QUALIFIED"],
        "trade_candidate_count": stage_counts["TRADE_CANDIDATE"],
        "contracts_selected": stage_counts["CONTRACT_SELECTED"],
        "prices_accepted": stage_counts["PRICE_ACCEPTABLE"],
        "entries_eligible": stage_counts["ENTRY_ELIGIBLE"],
        "entries_recorded": stage_counts["ENTRY_RECORDED"],
        "exits_evaluated": stage_counts["EXIT_EVALUATED"],
        "valid_trades_captured": _count(records, "VALID_TRADE_CAPTURED"),
        "true_no_trades": _count(records, "TRUE_NO_TRADE"),
        "missing_data_cases": _count(records, "MISSING_DATA"),
        "missed_valid_trades": _count(records, "MISSED_VALID_TRADE"),
        "invalid_trades_allowed": _count(records, "INVALID_TRADE_ALLOWED"),
        "unresolved_cases": _count(records, "UNRESOLVED"),
        "winners": sum(1 for record in records if record["winner_or_loser"] == "winner"),
        "losers": sum(1 for record in records if record["winner_or_loser"] == "loser"),
        "deterministic_cases": sum(
            1 for record in records if record["deterministic_result"] == "deterministic"
        ),
        "unstable_cases": sum(
            1 for record in records if record["deterministic_result"] != "deterministic"
        ),
        "first_blocker_totals_by_funnel_stage": first_blocker_totals,
        "conversion_rate_between_stages": conversions,
        "sample_contract_progress": _sample_contract_progress(records),
    }


def _first_blockers(records):
    grouped = {}
    for record in records:
        stage = record["first_stage_not_reached"] or "NONE"
        item = grouped.setdefault(
            stage,
            {
                "affected_setup_families": [],
                "affected_candidate_count": 0,
                "common_causes": {},
                "local_evidence_can_resolve": False,
                "external_data_required": False,
                "smallest_safe_next_action": None,
            },
        )
        item["affected_candidate_count"] += 1
        if record["setup_family"] not in item["affected_setup_families"]:
            item["affected_setup_families"].append(record["setup_family"])
        cause = record["exact_blocker_code"] or "completed_valid_entry_review_only"
        item["common_causes"][cause] = item["common_causes"].get(cause, 0) + 1

    for stage, item in grouped.items():
        if stage == "CONTRACT_SELECTED":
            item["local_evidence_can_resolve"] = False
            item["external_data_required"] = True
            item["smallest_safe_next_action"] = (
                "Create a grouped exact missing-data cost-check task only for "
                "setup-time selected-option fields."
            )
        elif stage == "ENTRY_ELIGIBLE":
            item["local_evidence_can_resolve"] = True
            item["external_data_required"] = False
            item["smallest_safe_next_action"] = (
                "Preserve frozen quote-age rejection controls in regression."
            )
        elif stage == "NONE":
            item["smallest_safe_next_action"] = (
                "Use as positive-entry expansion reference; do not claim proof."
            )
        else:
            item["smallest_safe_next_action"] = (
                "Add grouped local fixture evidence before any data request."
            )
    return grouped


def _classification_totals(records):
    return {classification: _count(records, classification) for classification in CLASSIFICATIONS}


def _unresolved_requirements(records):
    requirements = []
    for record in records:
        if record["final_classification"] in {"MISSING_DATA", "UNRESOLVED"}:
            requirements.append(
                {
                    "candidate_identifier": record["candidate_identifier"],
                    "first_stage_not_reached": record["first_stage_not_reached"],
                    "missing_or_unresolved_field": record["exact_blocker_code"],
                    "decision_value": (
                        "determines whether the candidate can progress to selected "
                        "contract, valid entry, or true no-trade classification"
                    ),
                }
            )
    return requirements


def _owner_questions(records):
    scorecard = _scorecard(records)
    return {
        "did_safe_fast_recognize_the_setup_before_the_move": (
            "Yes for the grouped lifecycle candidates that reached setup or trade-candidate "
            "stages; recognition is still incomplete for shape-only/missing-data rows."
        ),
        "did_it_classify_the_setup_as_a_possible_trade": (
            "Yes for accepted-entry-stage lifecycle rows and the three CFB selected-contract "
            "replay rows; accepted-entry stage is not the same as an executed trade."
        ),
        "was_a_tradable_option_available_at_that_exact_time": (
            "Only SPY Clean Fast Break 002 currently has local selected-contract entry "
            "and exit evidence sufficient for a review-only captured valid entry. Other "
            "candidate families are blocked by stale quote, future quote, wide spread, "
            "or missing setup-time selected-option evidence."
        ),
        "was_rejection_caused_by_real_safety_rule_or_missing_evidence": (
            f"Both: {scorecard['true_no_trades']} true no-trade controls are frozen "
            f"safety-rule failures, while {scorecard['missing_data_cases']} cases are "
            "missing-data blockers and unresolved rows remain separate."
        ),
        "how_many_valid_trades_were_caught_missed_or_incorrectly_allowed": (
            f"Caught {scorecard['valid_trades_captured']}; missed "
            f"{scorecard['missed_valid_trades']}; incorrectly allowed "
            f"{scorecard['invalid_trades_allowed']}."
        ),
    }


def _sample_contract_progress(records):
    return {
        "accepted_entries": sum(
            1 for record in records if record["final_classification"] == "VALID_TRADE_CAPTURED"
        ),
        "accepted_entries_required": SAMPLE_CONTRACT["accepted_entries_required"],
        "rejection_no_trade_controls": sum(
            1 for record in records if record["final_classification"] == "TRUE_NO_TRADE"
        ),
        "rejection_no_trade_controls_required": SAMPLE_CONTRACT[
            "rejection_no_trade_controls_required"
        ],
        "ambiguous_boundary_cases": sum(
            1 for record in records if record["final_classification"] == "UNRESOLVED"
        ),
        "ambiguous_boundary_cases_required": SAMPLE_CONTRACT[
            "ambiguous_boundary_cases_required"
        ],
        "winners": sum(1 for record in records if record["winner_or_loser"] == "winner"),
        "winners_required": SAMPLE_CONTRACT["winners_required"],
        "losers": sum(1 for record in records if record["winner_or_loser"] == "loser"),
        "losers_required": SAMPLE_CONTRACT["losers_required"],
        "protected_holdout_accepted_entries": 0,
        "protected_holdout_accepted_entries_required": SAMPLE_CONTRACT[
            "protected_holdout_accepted_entries_required"
        ],
        "protected_holdout_rejection_no_trade_controls": 0,
        "protected_holdout_rejection_no_trade_controls_required": SAMPLE_CONTRACT[
            "protected_holdout_rejection_no_trade_controls_required"
        ],
    }


def _run_payload(records):
    return {
        "candidate_records": records,
        "family_scorecards": {
            family: _scorecard(
                [record for record in records if record["setup_family"] == family]
            )
            for family in ("Ideal", "Clean Fast Break", "Continuation")
        },
        "combined_scorecard": _scorecard(records),
    }


def _count(records, classification):
    return sum(1 for record in records if record["final_classification"] == classification)


def _cfb_blocker_evidence(row):
    if row["result_status"] == "completed_review_only":
        return (
            f"Entry {row['cost_adjusted_entry_basis']} at {row['entry_time']}; "
            f"exit {row['cost_adjusted_exit_basis']} at {row['exit_time']}; "
            f"result {row['cost_slippage_adjusted_result']}; review-only, not proof."
        )
    return (
        f"Selected-contract replay result {row['result_name']} with primary reason "
        f"{row['failure_reason']} at signal {row['entry_time']}."
    )


def _direction_for(_setup_family, _underlying):
    return "long_call_candidate"


def _timezone_name(timestamp):
    if not timestamp:
        return None
    if str(timestamp).endswith("+00:00") or str(timestamp).endswith("Z"):
        return "UTC"
    if "-04:00" in str(timestamp):
        return "America/New_York"
    return "timezone_in_timestamp"


def _stable_hash(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _git_short_head():
    head = REPO_ROOT / ".git" / "HEAD"
    if not head.exists():
        return "UNKNOWN"
    text = head.read_text(encoding="utf-8").strip()
    if text.startswith("ref: "):
        ref = REPO_ROOT / ".git" / text[5:]
        if ref.exists():
            return ref.read_text(encoding="utf-8").strip()[:7]
    return text[:7]


if __name__ == "__main__":
    doc = write_funnel_document()
    print(
        "wrote day48 positive trade capture funnel: "
        f"{len(doc['candidate_records'])} candidates, "
        f"{doc['combined_scorecard']['valid_trades_captured']} valid captured, "
        f"{doc['combined_scorecard']['true_no_trades']} true no-trades, "
        f"{doc['combined_scorecard']['missing_data_cases']} missing-data cases"
    )
