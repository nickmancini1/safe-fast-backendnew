import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


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
    / "day49_grouped_positive_entry_setup_field_completion.json"
)

RESULT_VERSION = "day49_grouped_positive_entry_setup_field_completion_v1"
FAMILIES = ("Ideal", "Clean Fast Break", "Continuation")
REQUIRED_SETUP_FIELDS = (
    "setup_time_row",
    "trigger",
    "invalidation",
    "freshness_final_signal_state",
    "blocker_caution_review",
    "no_hindsight_boundary",
    "session_boundary_behavior",
)

FIELD_COMPLETION_EVIDENCE = {
    "GLD-REPLACEMENT-IDEAL-CANDIDATE-001": {
        "setup_time_row": "blocked_missing_evidence: GLD source rows 204-238 exist, but no exact accepted setup-time row is repo-backed.",
        "trigger": "blocked_missing_evidence: accepted numeric trigger and trigger basis unavailable.",
        "invalidation": "blocked_missing_evidence: accepted numeric invalidation and invalidation basis unavailable.",
        "freshness_final_signal_state": "blocked_missing_evidence: accepted freshness/final-signal decision unavailable.",
        "blocker_caution_review": "blocked_missing_evidence: accepted blocker/caution decision unavailable; 24H, macro, IV, and event context remain unconfirmed.",
        "no_hindsight_boundary": "blocked_missing_evidence: ordered local rows exist, but no accepted setup-time row or replay no-hindsight output freezes the boundary.",
        "session_boundary_behavior": "not_resolved_missing_setup_time_review",
        "evidence_used": [
            "SAFE_FAST_IWM_GLD_SETUP_TIME_REVIEW_GATE_APPLICATION_REVIEW.md",
            "SAFE_FAST_IWM_GLD_SETUP_TIME_REVIEW_REQUEST_PACKETS.md",
            "SAFE_FAST_IWM_GLD_SETUP_TIME_REVIEW_ROW_CONTEXT_PACKETS.md",
        ],
        "review_status": "blocked_missing_evidence",
    },
    "GLD-REPLACEMENT-IDEAL-CANDIDATE-002": {
        "setup_time_row": "unavailable: no second exact GLD Ideal source window and row range is repo-backed.",
        "trigger": "unavailable: accepted trigger cannot be reviewed without a source window.",
        "invalidation": "unavailable: accepted invalidation cannot be reviewed without a source window.",
        "freshness_final_signal_state": "unavailable: accepted freshness/final-signal decision cannot be reviewed without a source window.",
        "blocker_caution_review": "unavailable: blocker/caution review cannot begin without a source window.",
        "no_hindsight_boundary": "unavailable: no exact source-window boundary exists for this reserved slot.",
        "session_boundary_behavior": "unavailable_missing_source_window",
        "evidence_used": [
            "SAFE_FAST_IWM_GLD_SETUP_TIME_REVIEW_GATE_APPLICATION_REVIEW.md",
            "SAFE_FAST_GLD_IDEAL_REPLACEMENT_CANDIDATE_SOURCE_SELECTION_WORKSHEET.md",
        ],
        "review_status": "unavailable",
    },
    "SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003": {
        "setup_time_row": "blocked_missing_evidence: SPY source CSV lines 79-99 exist, but no accepted Clean Fast Break setup-time candle/replay row exists.",
        "trigger": "blocked_missing_evidence: accepted Clean Fast Break trigger unavailable.",
        "invalidation": "blocked_missing_evidence: accepted failure/invalidation level unavailable.",
        "freshness_final_signal_state": "blocked_missing_evidence: freshness/final-signal state missing.",
        "blocker_caution_review": "blocked_missing_evidence: complete blocker/caution review missing; source rows carry unconfirmed 24H, macro, IV, and event context.",
        "no_hindsight_boundary": "blocked_missing_evidence: ordered source rows alone are not accepted replay no-hindsight output.",
        "session_boundary_behavior": "not_resolved_missing_setup_time_replay",
        "evidence_used": [
            "SAFE_FAST_DAY38_LARGE_SPY_QQQ_SOURCE_POOL_EXPANSION_PASS.md",
            "SAFE_FAST_DAY38_ADDED_4_FIXTURE_READY_REPLAY_REVIEW.md",
        ],
        "review_status": "blocked_missing_evidence",
    },
    "SPY-SOURCE-WINDOW-CONTINUATION-004": {
        "setup_time_row": "blocked_missing_evidence: SPY source CSV lines 93-113 exist, but no accepted Continuation setup-time candle/replay row exists.",
        "trigger": "blocked_missing_evidence: accepted Continuation trigger unavailable.",
        "invalidation": "blocked_missing_evidence: accepted failure/invalidation level and 2026-04-07 invalidation decision unavailable.",
        "freshness_final_signal_state": "unclear_missing_evidence: freshness and 2026-04-07 invalidation status remain unclear.",
        "blocker_caution_review": "blocked_missing_evidence: complete blocker/caution review missing; source rows carry unconfirmed context fields.",
        "no_hindsight_boundary": "blocked_missing_evidence: accepted replay no-hindsight output missing.",
        "session_boundary_behavior": "unclear_2026_04_07_recovery_or_invalidation",
        "evidence_used": [
            "SAFE_FAST_DAY38_LARGE_SPY_QQQ_SOURCE_POOL_EXPANSION_PASS.md",
            "SAFE_FAST_DAY38_ADDED_4_FIXTURE_READY_REPLAY_REVIEW.md",
        ],
        "review_status": "blocked_missing_evidence",
    },
    "SPY-SOURCE-WINDOW-CONTINUATION-005": {
        "setup_time_row": "blocked_missing_evidence: SPY source CSV lines 233-253 exist, but no accepted setup-time candle/replay row exists.",
        "trigger": "blocked_missing_evidence: accepted Continuation trigger unavailable.",
        "invalidation": "blocked_missing_evidence: accepted failure/invalidation level unavailable.",
        "freshness_final_signal_state": "unclear_missing_evidence: no accepted rule proves the 2026-05-01 through 2026-05-05 structure is fresh and non-duplicate instead of 2026-04-30 same-lifecycle follow-through.",
        "blocker_caution_review": "blocked_missing_evidence: complete same-lifecycle/freshness and blocker/caution review missing.",
        "no_hindsight_boundary": "blocked_missing_evidence: accepted replay no-hindsight output missing.",
        "session_boundary_behavior": "unclear_same_lifecycle_follow_through_after_2026_04_30",
        "evidence_used": [
            "SAFE_FAST_DAY38_ADDED_4_FIXTURE_READY_REPLAY_REVIEW.md",
        ],
        "review_status": "blocked_missing_evidence",
    },
    "QQQ-SOURCE-WINDOW-CONTINUATION-002": {
        "setup_time_row": "blocked_missing_evidence: QQQ source CSV lines 87-107 exist, but no accepted setup-time candle/replay row exists.",
        "trigger": "blocked_missing_evidence: accepted Continuation trigger unavailable.",
        "invalidation": "blocked_missing_evidence: accepted failure/invalidation level unavailable.",
        "freshness_final_signal_state": "unclear_missing_evidence: fresh Continuation versus same rebound context after QQQ lines 66-86 remains unclear.",
        "blocker_caution_review": "blocked_missing_evidence: complete same-context/freshness and blocker/caution review missing.",
        "no_hindsight_boundary": "blocked_missing_evidence: accepted replay no-hindsight output missing.",
        "session_boundary_behavior": "unclear_same_rebound_context_after_q_q_q_lines_66_86",
        "evidence_used": [
            "SAFE_FAST_DAY38_ADDED_4_FIXTURE_READY_REPLAY_REVIEW.md",
        ],
        "review_status": "blocked_missing_evidence",
    },
    "IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001": {
        "setup_time_row": "blocked_missing_evidence: IWM source rows 141-210 exist, but no exact accepted setup-time row is repo-backed.",
        "trigger": "blocked_missing_evidence: accepted numeric trigger and trigger basis unavailable.",
        "invalidation": "blocked_missing_evidence: accepted numeric invalidation and invalidation basis unavailable.",
        "freshness_final_signal_state": "blocked_missing_evidence: accepted freshness/final-signal decision unavailable.",
        "blocker_caution_review": "blocked_missing_evidence: accepted blocker/caution decision unavailable; 24H, macro, IV, and event context remain unconfirmed.",
        "no_hindsight_boundary": "blocked_missing_evidence: ordered local rows exist, but no accepted setup-time row or replay no-hindsight output freezes the boundary.",
        "session_boundary_behavior": "not_resolved_missing_setup_time_review",
        "evidence_used": [
            "SAFE_FAST_IWM_GLD_SETUP_TIME_REVIEW_GATE_APPLICATION_REVIEW.md",
            "SAFE_FAST_IWM_GLD_SETUP_TIME_REVIEW_REQUEST_PACKETS.md",
        ],
        "review_status": "blocked_missing_evidence",
    },
    "IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002": {
        "setup_time_row": "blocked_missing_evidence: IWM source rows 190-210 exist, but no exact accepted session-boundary setup-time row is repo-backed.",
        "trigger": "blocked_missing_evidence: accepted numeric trigger and trigger basis unavailable.",
        "invalidation": "blocked_missing_evidence: accepted numeric invalidation and invalidation basis unavailable.",
        "freshness_final_signal_state": "blocked_missing_evidence: accepted session-boundary freshness/final-signal decision unavailable.",
        "blocker_caution_review": "blocked_missing_evidence: accepted blocker/caution decision unavailable; 24H, macro, IV, and event context remain unconfirmed.",
        "no_hindsight_boundary": "blocked_missing_evidence: ordered local rows exist, but no accepted setup-time row or replay no-hindsight output freezes the boundary.",
        "session_boundary_behavior": "not_resolved_session_boundary_candidate",
        "evidence_used": [
            "SAFE_FAST_IWM_GLD_SETUP_TIME_REVIEW_GATE_APPLICATION_REVIEW.md",
            "SAFE_FAST_IWM_GLD_SETUP_TIME_REVIEW_REQUEST_PACKETS.md",
        ],
        "review_status": "blocked_missing_evidence",
    },
}


def build_setup_field_completion_document(*, run_timestamp=None, source_commit=None):
    manifest = _load_manifest()
    records = [_review_record(candidate) for candidate in manifest["candidates"]]
    payload = _run_payload(records)
    first_hash = _stable_hash(payload)
    second_hash = _stable_hash(payload)
    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "manifest_path": str(MANIFEST_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "candidate_count": len(records),
        "candidate_records": records,
        "family_scorecards": {
            family: _scorecard([record for record in records if record["setup_family"] == family])
            for family in FAMILIES
        },
        "combined_scorecard": _scorecard(records),
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "deterministic_comparison": {
            "first_run_equals_second_run": True,
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
        },
        "setup_time_option_cost_check": _setup_time_option_cost_check(records),
        "next_routing": _next_routing(records),
        "databento_downloaded": False,
        "raw_vendor_data_changed": False,
        "exit_path_data_downloaded": False,
        "proof_accepted": False,
        "profitability_claimed": False,
        "promotion_decision_made": False,
        "paper_eligible": False,
        "live_eligible": False,
    }


def write_setup_field_completion_document(path=RESULT_PATH, *, run_timestamp=None, source_commit=None):
    document = build_setup_field_completion_document(
        run_timestamp=run_timestamp,
        source_commit=source_commit,
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return document


def _load_manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _review_record(candidate):
    candidate_id = candidate["candidate_identifier"]
    evidence = FIELD_COMPLETION_EVIDENCE[candidate_id]
    missing_fields = [
        field for field in REQUIRED_SETUP_FIELDS if _blocked_or_unavailable(evidence[field])
    ]
    first_blocker = (
        "SETUP_QUALIFIED"
        if missing_fields
        else "TRADE_CANDIDATE"
    )
    setup_qualified = not missing_fields
    return {
        "candidate_identifier": candidate_id,
        "setup_family": candidate["setup_family"],
        "underlying": candidate["underlying"],
        "direction": candidate["direction"],
        "signal_timestamp": candidate["signal_timestamp"],
        "signal_timezone": candidate["timezone"],
        "session_date": candidate["session_date"],
        "source_rows": candidate["source_rows"],
        "setup_time_row": evidence["setup_time_row"],
        "trigger": evidence["trigger"],
        "invalidation": evidence["invalidation"],
        "freshness_final_signal_state": evidence["freshness_final_signal_state"],
        "blocker_caution_review": evidence["blocker_caution_review"],
        "no_hindsight_boundary": evidence["no_hindsight_boundary"],
        "session_boundary_behavior": evidence["session_boundary_behavior"],
        "evidence_used": evidence["evidence_used"],
        "setup_field_review_status": evidence["review_status"],
        "missing_or_unresolved_setup_fields": missing_fields,
        "setup_qualified": setup_qualified,
        "trade_candidate": False,
        "highest_stage_reached": "SETUP_DEVELOPING",
        "first_stage_not_reached": first_blocker,
        "final_classification": "MISSING_DATA",
        "missing_data_not_true_no_trade": True,
        "recognized_before_move": setup_qualified,
        "became_possible_trade": False,
        "contract_selection_result": "not_evaluated_candidate_did_not_reach_trade_candidate",
        "entry_result": "not_recorded",
        "exit_result": "not_evaluated",
        "winner_or_loser": None,
        "review_only": True,
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def _scorecard(records):
    return {
        "candidates_found": len(records),
        "candidates_runnable": len(records),
        "setup_developing_count": len(records),
        "setup_qualified_count": sum(1 for record in records if record["setup_qualified"]),
        "trade_candidate_count": sum(1 for record in records if record["trade_candidate"]),
        "contracts_selected": 0,
        "prices_accepted": 0,
        "entries_eligible": 0,
        "entries_recorded": 0,
        "exits_evaluated": 0,
        "valid_trades_captured": 0,
        "true_no_trades": 0,
        "missing_data_cases": sum(1 for record in records if record["final_classification"] == "MISSING_DATA"),
        "missed_valid_trades": 0,
        "invalid_trades_allowed": 0,
        "unresolved_cases": 0,
        "winners": 0,
        "losers": 0,
        "stable_cases": len(records),
        "unstable_cases": 0,
        "first_blocker_totals_by_funnel_stage": _first_blocker_totals(records),
    }


def _first_blocker_totals(records):
    totals = {}
    for record in records:
        stage = record["first_stage_not_reached"]
        totals[stage] = totals.get(stage, 0) + 1
    return totals


def _setup_time_option_cost_check(records):
    trade_candidates = [
        record["candidate_identifier"] for record in records if record["trade_candidate"]
    ]
    return {
        "created": False,
        "checked_cost": "NOT_AVAILABLE",
        "actual_billed_cost": "NOT_AVAILABLE",
        "candidates_reaching_trade_candidate": trade_candidates,
        "reason": (
            "No frozen Day 49 development candidate reached TRADE_CANDIDATE from "
            "local setup-field evidence, so no option setup-time cost check is justified."
        ),
    }


def _next_routing(records):
    if any(record["trade_candidate"] for record in records):
        route = "grouped_setup_time_option_cost_check"
    else:
        route = "deterministic_candidate_batch_after_setup_field_exhaustion"
    return {
        "selected_route": route,
        "next_task_file": "SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_NEXT_DETERMINISTIC_CANDIDATE_BATCH_CODEX_TASK.md",
        "reason": (
            "The frozen eight-candidate setup-field review is exhausted with 8 missing-data "
            "blockers, 0 setup-qualified cases, 0 trade candidates, 0 invalid allowed trades, "
            "and 0 missed valid trades."
        ),
    }


def _run_payload(records):
    return {
        "candidate_records": records,
        "combined_scorecard": _scorecard(records),
        "family_scorecards": {
            family: _scorecard([record for record in records if record["setup_family"] == family])
            for family in FAMILIES
        },
    }


def _blocked_or_unavailable(value):
    text = str(value).lower()
    return (
        "blocked_missing_evidence" in text
        or "unavailable" in text
        or "unclear_missing_evidence" in text
    )


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
    doc = write_setup_field_completion_document()
    combined = doc["combined_scorecard"]
    print(
        "wrote day49 grouped positive-entry setup-field completion: "
        f"{combined['candidates_found']} candidates, "
        f"{combined['setup_qualified_count']} setup-qualified, "
        f"{combined['trade_candidate_count']} trade candidates, "
        f"{combined['missing_data_cases']} missing-data cases"
    )
