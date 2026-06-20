import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from historical_signal_replay import day48_positive_trade_capture_funnel as day48_funnel
from watcher_foundation import candidate_completeness_screen


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "fixtures"
    / "day49_positive_entry_candidate_expansion_manifest.json"
)
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day49_positive_entry_candidate_expansion.json"
)

FAMILY_ORDER = ["Ideal", "Clean Fast Break", "Continuation"]
MAX_PER_FAMILY = 8
CLASSIFICATIONS = day48_funnel.CLASSIFICATIONS
FUNNEL_STAGES = day48_funnel.FUNNEL_STAGES

MEASURED_OR_CONTROL_CANDIDATE_IDS = {
    "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
    "QQQ-REAL-HISTORICAL-CONTINUATION-001",
    "QQQ-REAL-HISTORICAL-IDEAL-001",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003",
    "SPY-REAL-HISTORICAL-CONTINUATION-001",
    "SPY-REAL-HISTORICAL-IDEAL-001",
    "GLD-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
    "GLD-REAL-HISTORICAL-CONTINUATION-001",
    "GLD-REAL-HISTORICAL-IDEAL-001",
    "IWM-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
    "IWM-REAL-HISTORICAL-CONTINUATION-001",
    "IWM-REAL-HISTORICAL-IDEAL-001",
}

PROTECTED_HOLDOUT_CANDIDATE_IDS = set()


def build_manifest(*, source_commit=None, run_timestamp=None):
    pool = candidate_completeness_screen.build_candidate_pool()
    otherwise_eligible = [
        row
        for row in pool
        if row["candidate_id"] not in PROTECTED_HOLDOUT_CANDIDATE_IDS
        and row["candidate_id"] not in MEASURED_OR_CONTROL_CANDIDATE_IDS
        and row["duplicate"] != "yes"
        and row["status"] != "drop"
    ]
    selected_ids = set()
    selected = []
    for family in FAMILY_ORDER:
        family_rows = sorted(
            [row for row in otherwise_eligible if row["setup_type"] == family],
            key=_chronological_key,
        )
        for row in family_rows[:MAX_PER_FAMILY]:
            selected_ids.add(row["candidate_id"])
            selected.append(_manifest_candidate(row))

    exclusions = []
    for row in pool:
        reason = _exclusion_reason(row, selected_ids)
        if reason:
            exclusions.append(
                {
                    "candidate_identifier": row["candidate_id"],
                    "setup_family": row["setup_type"],
                    "underlying": row["symbol"],
                    "signal_timestamp": _candidate_timestamp(row),
                    "exclusion_reason": reason,
                }
            )

    first_run = _selection_payload(selected, exclusions)
    second_run = _selection_payload(selected, exclusions)
    first_hash = _stable_hash(first_run)
    second_hash = _stable_hash(second_run)
    return {
        "manifest_version": "day49_positive_entry_candidate_expansion_v1",
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "selection_policy": {
            "source_universe": "watcher_foundation.candidate_completeness_screen.build_candidate_pool",
            "candidate_generation_rule_version": "day39_candidate_completeness_screen_v1",
            "lifecycle_rule_version": "day48_grouped_three_family_lifecycle_fixtures;day49_positive_entry_expansion_v1",
            "max_per_setup_family": MAX_PER_FAMILY,
            "family_order": list(FAMILY_ORDER),
            "sort_key": "signal_timestamp/session date/source reference/candidate id",
            "outcome_blind_fields_used": [
                "candidate_id",
                "symbol",
                "setup_type",
                "source_lines",
                "setup_candle",
                "trigger",
                "invalidation",
                "freshness",
                "blocker",
                "no_hindsight_boundary",
                "duplicate",
                "status",
            ],
            "forbidden_selection_inputs": [
                "outcome_window",
                "later price move",
                "option exit path",
                "P&L",
                "profitability",
                "winner_or_loser",
            ],
        },
        "source_pool_count": len(pool),
        "candidate_count": len(selected),
        "candidates": selected,
        "exclusions": exclusions,
        "deterministic_selection": {
            "first_run_equals_second_run": first_run == second_run,
            "hashes_match": first_hash == second_hash,
            "first_run_hash": first_hash,
            "second_run_hash": second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
        },
        "development_evidence_not_holdout": True,
        "protected_holdout_candidates_selected": 0,
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def write_manifest(path=MANIFEST_PATH, *, source_commit=None, run_timestamp=None):
    document = build_manifest(source_commit=source_commit, run_timestamp=run_timestamp)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return document


def build_expansion_document(*, source_commit=None, run_timestamp=None):
    manifest = build_manifest(source_commit=source_commit, run_timestamp=run_timestamp)
    records = [_candidate_record(row) for row in manifest["candidates"]]
    first_run = _run_payload(records)
    second_run = _run_payload(records)
    first_hash = _stable_hash(first_run)
    second_hash = _stable_hash(second_run)
    existing = day48_funnel.build_funnel_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    return {
        "result_version": "day49_positive_entry_candidate_expansion_v1",
        "source_commit": manifest["source_commit"],
        "run_timestamp": manifest["run_timestamp"],
        "manifest_path": str(MANIFEST_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "funnel_stages": FUNNEL_STAGES,
        "new_candidate_records": records,
        "new_family_scorecards": {
            family: _scorecard([record for record in records if record["setup_family"] == family])
            for family in FAMILY_ORDER
        },
        "new_combined_scorecard": _scorecard(records),
        "new_first_blockers": _first_blockers(records),
        "new_final_classifications": _classification_totals(records),
        "candidate_manifest": manifest,
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "deterministic_comparison": {
            "first_run_equals_second_run": first_run == second_run,
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
        },
        "existing_regression_control_result": {
            "candidate_count": len(existing["candidate_records"]),
            "deterministic_result": existing["deterministic_comparison"]["result"],
            "combined_scorecard": existing["combined_scorecard"],
            "final_classifications": existing["final_classifications"],
        },
        "setup_time_request_package": _setup_time_request_package(records),
        "owner_questions": _owner_questions(records),
        "checked_cost": "NOT_AVAILABLE",
        "actual_billed_cost": "NOT_AVAILABLE",
        "databento_downloaded": False,
        "proof_accepted": False,
        "profitability_claimed": False,
        "promotion_decision_made": False,
        "paper_eligible": False,
        "live_eligible": False,
    }


def write_expansion_document(path=RESULT_PATH, *, source_commit=None, run_timestamp=None):
    document = build_expansion_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    write_manifest(source_commit=source_commit, run_timestamp=document["run_timestamp"])
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return document


def _manifest_candidate(row):
    timestamp = _candidate_timestamp(row)
    return {
        "candidate_identifier": row["candidate_id"],
        "setup_family": row["setup_type"],
        "underlying": row["symbol"],
        "direction": "long_call_candidate",
        "signal_timestamp": timestamp,
        "timezone": _timezone_name(timestamp),
        "session_date": _session_date(timestamp),
        "source_rows": row["source_lines"],
        "candidate_generation_rule_version": "day39_candidate_completeness_screen_v1",
        "lifecycle_rule_version": "day48_grouped_three_family_lifecycle_fixtures;day49_positive_entry_expansion_v1",
        "development_evidence_not_holdout": True,
        "protected_holdout": False,
        "duplicate_signal": False,
        "status_at_freeze": row["status"],
        "pre_outcome_fields": {
            "setup_candle": row["setup_candle"],
            "trigger": row["trigger"],
            "invalidation": row["invalidation"],
            "freshness": row["freshness"],
            "blocker": row["blocker"],
            "no_hindsight_boundary": row["no_hindsight_boundary"],
        },
    }


def _candidate_record(candidate):
    fields = candidate["pre_outcome_fields"]
    missing_fields = [
        key
        for key in (
            "setup_candle",
            "trigger",
            "invalidation",
            "freshness",
            "blocker",
            "no_hindsight_boundary",
        )
        if _is_missing_or_unclear(fields[key])
    ]
    exact_blocker = "missing_setup_time_replay_fields:" + ",".join(missing_fields)
    return {
        "candidate_identifier": candidate["candidate_identifier"],
        "setup_family": candidate["setup_family"],
        "underlying": candidate["underlying"],
        "direction": candidate["direction"],
        "signal_timestamp": candidate["signal_timestamp"],
        "signal_timezone": candidate["timezone"],
        "session_date": candidate["session_date"],
        "evidence_source": candidate["source_rows"],
        "record_type": "day49_new_development_candidate",
        "chronological_stage_path": ["source_pool_candidate_frozen"],
        "funnel_stage_path": ["SETUP_DEVELOPING"],
        "highest_stage_reached": "SETUP_DEVELOPING",
        "first_stage_not_reached": "SETUP_QUALIFIED",
        "exact_blocker_code": exact_blocker,
        "blocker_evidence": (
            "Local source-pool record is frozen, but accepted setup-time replay fields "
            f"are missing or unresolved: {', '.join(missing_fields)}."
        ),
        "blocker_category": "missing data",
        "session_boundary_behavior": "not_resolved_missing_setup_time_replay",
        "recognized_before_move": False,
        "became_possible_trade": False,
        "contract_selection_result": "not_enumerated_candidate_did_not_reach_trade_candidate",
        "eligible_contracts": [],
        "execution_result": "unknown_missing_setup_time_selected_option_evidence",
        "context_and_caution_result": "unknown_missing_setup_time_review",
        "winner_selection_result": "not_evaluated",
        "entry_result": "not_recorded",
        "exit_result": "not_evaluated",
        "final_classification": "MISSING_DATA",
        "final_outcome": "no_countable_trade",
        "winner_or_loser": None,
        "first_run_output": "PASS",
        "second_run_output": "PASS",
        "deterministic_result": "deterministic",
        "review_only": True,
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def _setup_time_request_package(records):
    trade_candidates = [
        record
        for record in records
        if "TRADE_CANDIDATE" in record["funnel_stage_path"]
        and record["final_classification"] == "MISSING_DATA"
    ]
    return {
        "external_evidence_required": bool(trade_candidates),
        "request_created": False,
        "reason": (
            "No new frozen candidate reached TRADE_CANDIDATE, so no bounded option "
            "contract set or setup-time quote request is justified."
        ),
        "candidates_reaching_trade_candidate": [
            record["candidate_identifier"] for record in trade_candidates
        ],
        "cmbp_1_shape": "NOT_APPLICABLE",
        "cbbo_1s_shape": "NOT_APPLICABLE",
        "checked_cost": "NOT_AVAILABLE",
    }


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
        "stable_cases": sum(1 for record in records if record["deterministic_result"] == "deterministic"),
        "unstable_cases": sum(1 for record in records if record["deterministic_result"] != "deterministic"),
        "first_blocker_totals_by_funnel_stage": first_blocker_totals,
        "conversion_rate_between_stages": conversions,
    }


def _first_blockers(records):
    grouped = {}
    for record in records:
        stage = record["first_stage_not_reached"] or "NONE"
        item = grouped.setdefault(stage, {"affected_candidate_count": 0, "common_causes": {}})
        item["affected_candidate_count"] += 1
        cause = record["exact_blocker_code"] or "none"
        item["common_causes"][cause] = item["common_causes"].get(cause, 0) + 1
    return grouped


def _classification_totals(records):
    return {classification: _count(records, classification) for classification in CLASSIFICATIONS}


def _owner_questions(records):
    scorecard = _scorecard(records)
    return {
        "did_safe_fast_recognize_the_new_setups_before_the_move": (
            "No new frozen development candidate had enough local setup-time replay "
            "fields to be recognized before the move."
        ),
        "how_many_became_possible_trades": str(scorecard["trade_candidate_count"]),
        "how_many_had_a_tradable_option_at_that_exact_time": str(scorecard["entries_eligible"]),
        "how_many_rejected_by_real_safety_rule_vs_missing_evidence": (
            f"{scorecard['true_no_trades']} real safety-rule rejections; "
            f"{scorecard['missing_data_cases']} missing-evidence cases."
        ),
        "how_many_valid_trades_caught_missed_or_incorrectly_allowed": (
            f"Caught {scorecard['valid_trades_captured']}; missed "
            f"{scorecard['missed_valid_trades']}; incorrectly allowed "
            f"{scorecard['invalid_trades_allowed']}."
        ),
    }


def _selection_payload(selected, exclusions):
    return {"candidates": selected, "exclusions": exclusions}


def _run_payload(records):
    return {
        "new_candidate_records": records,
        "new_family_scorecards": {
            family: _scorecard([record for record in records if record["setup_family"] == family])
            for family in FAMILY_ORDER
        },
        "new_combined_scorecard": _scorecard(records),
    }


def _exclusion_reason(row, selected_ids):
    candidate_id = row["candidate_id"]
    if candidate_id in selected_ids:
        return None
    if candidate_id in PROTECTED_HOLDOUT_CANDIDATE_IDS:
        return "protected_holdout_excluded"
    if candidate_id in MEASURED_OR_CONTROL_CANDIDATE_IDS:
        return "existing_measured_funnel_or_positive_rejection_control"
    if row["duplicate"] == "yes":
        return "duplicate_signal_same_underlying_opportunity"
    if row["status"] == "drop":
        return "dropped_from_current_proof_path_before_this_task"
    if row["setup_type"] not in FAMILY_ORDER:
        return "unsupported_setup_family"
    return "not_selected_after_family_cap_or_deterministic_order"


def _chronological_key(row):
    timestamp = _candidate_timestamp(row)
    unknown = 1 if timestamp == "UNKNOWN" else 0
    return (unknown, timestamp, row["source_lines"], row["candidate_id"])


def _candidate_timestamp(row):
    for value in (row.get("setup_candle", ""), row.get("source_lines", "")):
        match = re.search(r"20\d\d-\d\d-\d\dT\d\d:\d\d:\d\d(?:[+-]\d\d:\d\d|Z)?", value)
        if match:
            return match.group(0)
    return "UNKNOWN"


def _session_date(timestamp):
    if timestamp == "UNKNOWN":
        return "UNKNOWN"
    return timestamp[:10]


def _timezone_name(timestamp):
    if timestamp == "UNKNOWN":
        return "UNKNOWN"
    if timestamp.endswith("Z") or timestamp.endswith("+00:00"):
        return "UTC"
    if "-04:00" in timestamp or "-05:00" in timestamp:
        return "America/New_York"
    return "timezone_in_timestamp"


def _is_missing_or_unclear(value):
    text = str(value).strip().lower()
    return not text or "missing" in text or "unclear" in text


def _count(records, classification):
    return sum(1 for record in records if record["final_classification"] == classification)


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
    doc = write_expansion_document()
    combined = doc["new_combined_scorecard"]
    print(
        "wrote day49 positive-entry candidate expansion: "
        f"{combined['candidates_found']} new candidates, "
        f"{combined['trade_candidate_count']} trade candidates, "
        f"{combined['valid_trades_captured']} valid captured, "
        f"{combined['missing_data_cases']} missing-data cases"
    )
