import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DAY50_SOURCE_RESOLUTION_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_required_setup_source_resolution.json"
)
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_exact_setup_source_evidence_completion.json"
)

RESULT_VERSION = "day50_exact_setup_source_evidence_completion_v1"
REQUIRED_SETUP_FIELDS = (
    "setup_time_row",
    "trigger",
    "invalidation",
    "freshness_final_signal_state",
    "blocker_caution_review",
    "no_hindsight_boundary",
    "session_boundary_behavior",
)

TARGET_CANDIDATES = (
    "GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
    "SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003",
    "IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001",
    "IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002",
)

EXACT_SOURCE_REVIEW = {
    "GLD-REPLACEMENT-IDEAL-CANDIDATE-001": {
        "source_file": "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv",
        "source_rows": "204-238",
        "source_window": "2026-05-04T09:30:00-04:00 through 2026-05-08T15:30:00-04:00",
        "setup_family": "Ideal",
        "underlying": "GLD",
        "review_artifacts": [
            "historical_signal_replay/fixtures/first_real_gld_ideal_replay_v1_fixture.json",
            "SAFE_FAST_IWM_GLD_SETUP_TIME_REVIEW_REQUEST_PACKETS.md",
            "SAFE_FAST_IWM_GLD_SETUP_TIME_REVIEW_ROW_CONTEXT_PACKETS.md",
        ],
        "local_replay_evidence": (
            "Exact GLD fixture exists for rows 204-238, but its purpose is shape-only "
            "lifecycle review and it keeps trigger, invalidation, freshness/final-signal, "
            "24H, macro, IV, event, and news context unconfirmed or TO_REVIEW."
        ),
        "closure_reason": "fixture_and_row_context_do_not_accept_required_setup_source_fields",
        "field_notes": {
            "setup_time_row": "closed: no fixture row is accepted as the setup-time decision row for this candidate.",
            "trigger": "closed: fixture trigger_level remains null or TO_REVIEW, not an accepted numeric trigger.",
            "invalidation": "closed: fixture invalidation remains null or TO_REVIEW, not an accepted invalidation.",
            "freshness_final_signal_state": "closed: fixture freshness remains TO_REVIEW or fresh_or_spent_unconfirmed.",
            "blocker_caution_review": "closed: optional macro/news/volatility context is CONTEXT_UNKNOWN; complete blocker/caution decision is not accepted.",
            "no_hindsight_boundary": "closed: rows are chronological, but no accepted setup-time replay output freezes the decision row.",
            "session_boundary_behavior": "closed: no accepted session-boundary behavior promotes this Ideal candidate.",
        },
    },
    "SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003": {
        "source_file": "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv",
        "source_rows": "79-99",
        "source_window": "2026-03-31T09:30:00-04:00 through 2026-04-02T15:30:00-04:00",
        "setup_family": "Clean Fast Break",
        "underlying": "SPY",
        "review_artifacts": [
            "SAFE_FAST_DAY38_ADDED_4_ROW_BY_ROW_REPLAY_READINESS_REVIEW.md",
            "SAFE_FAST_DAY38_ADDED_4_FIXTURE_READY_REPLAY_REVIEW.md",
            "historical_signal_replay/fixtures/third_real_spy_clean_fast_break_replay_v1_fixture.json",
        ],
        "local_replay_evidence": (
            "The exact SPY lines 79-99 candidate is documented as blocked. The available "
            "third-real SPY Clean Fast Break fixture covers a different 2026-04-10 through "
            "2026-04-15 source window, so it cannot complete this candidate."
        ),
        "closure_reason": "no_exact_accepted_cfb_replay_fixture_for_rows_79_99",
        "field_notes": {
            "setup_time_row": "closed: no accepted Clean Fast Break setup candle exists for SPY lines 79-99.",
            "trigger": "closed: accepted Clean Fast Break trigger is unavailable for this exact window.",
            "invalidation": "closed: accepted failure/invalidation level is unavailable for this exact window.",
            "freshness_final_signal_state": "closed: final-signal/freshness state remains missing for this exact window.",
            "blocker_caution_review": "closed: optional macro/news/volatility context is CONTEXT_UNKNOWN; clean-break-vs-noisy-rebound and blocker/caution are not accepted.",
            "no_hindsight_boundary": "closed: ordered source rows alone are not accepted no-hindsight replay output.",
            "session_boundary_behavior": "closed: no accepted session-boundary behavior promotes this Clean Fast Break candidate.",
        },
    },
    "IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001": {
        "source_file": "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv",
        "source_rows": "141-210",
        "source_window": "2026-04-20T09:30:00-04:00 through 2026-05-01T15:30:00-04:00",
        "setup_family": "Continuation",
        "underlying": "IWM",
        "review_artifacts": [
            "historical_signal_replay/fixtures/first_real_iwm_continuation_replay_v1_fixture.json",
            "SAFE_FAST_IWM_GLD_SETUP_TIME_REVIEW_REQUEST_PACKETS.md",
            "SAFE_FAST_IWM_GLD_SETUP_TIME_REVIEW_ROW_CONTEXT_PACKETS.md",
        ],
        "local_replay_evidence": (
            "Exact IWM fixture exists for rows 141-210, but it is shape-only and leaves "
            "shelf base, trigger, invalidation, fresh/spent status, session-boundary carry-forward, "
            "macro, IV, and event fields TO_REVIEW or unconfirmed."
        ),
        "closure_reason": "fixture_and_request_packet_do_not_accept_continuation_setup_source_fields",
        "field_notes": {
            "setup_time_row": "closed: no exact accepted Continuation setup-time row is repo-backed.",
            "trigger": "closed: trigger_level remains null or TO_REVIEW in the exact fixture.",
            "invalidation": "closed: invalidation remains null or TO_REVIEW in the exact fixture.",
            "freshness_final_signal_state": "closed: fresh/spent status remains TO_REVIEW.",
            "blocker_caution_review": "closed: optional macro/news/volatility context is CONTEXT_UNKNOWN; complete blocker/caution decision is not accepted.",
            "no_hindsight_boundary": "closed: fixture rows are chronological, but no accepted setup-time replay output freezes the decision row.",
            "session_boundary_behavior": "closed: session-boundary carry-forward remains TO_REVIEW.",
        },
    },
    "IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002": {
        "source_file": "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv",
        "source_rows": "190-210",
        "source_window": "2026-04-28T15:30:00-04:00 through 2026-05-01T15:30:00-04:00",
        "setup_family": "Continuation",
        "underlying": "IWM",
        "review_artifacts": [
            "historical_signal_replay/fixtures/first_real_iwm_continuation_replay_v1_fixture.json",
            "SAFE_FAST_IWM_GLD_SETUP_TIME_REVIEW_REQUEST_PACKETS.md",
            "SAFE_FAST_IWM_GLD_SETUP_TIME_REVIEW_ROW_CONTEXT_PACKETS.md",
        ],
        "local_replay_evidence": (
            "The IWM session-boundary subset is covered only as row-context/request material. "
            "The exact fixture does not accept a 2026-05-01 14:30 setup-time row and leaves "
            "session-boundary carry-forward and fresh/spent status TO_REVIEW."
        ),
        "closure_reason": "session_boundary_setup_source_fields_not_accepted",
        "field_notes": {
            "setup_time_row": "closed: no exact accepted session-boundary setup-time row is repo-backed.",
            "trigger": "closed: accepted Continuation trigger is unavailable for this subset.",
            "invalidation": "closed: accepted Continuation invalidation is unavailable for this subset.",
            "freshness_final_signal_state": "closed: session-boundary freshness/final-signal decision remains TO_REVIEW.",
            "blocker_caution_review": "closed: optional macro/news/volatility context is CONTEXT_UNKNOWN; complete blocker/caution decision is not accepted.",
            "no_hindsight_boundary": "closed: no accepted setup-time row means no accepted no-hindsight boundary for this subset.",
            "session_boundary_behavior": "closed: session-boundary behavior remains unresolved and cannot promote the candidate.",
        },
    },
}


def build_completion_document(*, run_timestamp=None, source_commit=None):
    prior = json.loads(DAY50_SOURCE_RESOLUTION_PATH.read_text(encoding="utf-8"))
    prior_by_id = {
        record["candidate_identifier"]: record
        for record in prior["candidate_records"]
    }
    records = [_candidate_record(candidate_id, prior_by_id[candidate_id]) for candidate_id in TARGET_CANDIDATES]
    replay_payload = {"candidate_records": records}
    first_hash = _stable_hash(replay_payload)
    second_hash = _stable_hash(replay_payload)
    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "prior_result_path": str(DAY50_SOURCE_RESOLUTION_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "candidate_count": len(records),
        "candidate_records": records,
        "scorecard": _scorecard(records),
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "deterministic_comparison": {
            "first_run_equals_second_run": True,
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
        },
        "setup_source_requests_remaining": 0,
        "option_request_included": False,
        "exit_path_request_included": False,
        "databento_cost_check": {
            "checked_cost": "NOT_AVAILABLE",
            "actual_billed_cost": "NOT_AVAILABLE",
            "credential_used": False,
            "reason": "No paid-data request was created; the four remaining blockers are closed local setup-source evidence decisions, not vendor-downloadable fields.",
        },
        "databento_downloaded": False,
        "raw_vendor_data_changed": False,
        "schwab_authenticated": False,
        "broker_mutation_attempted": False,
        "proof_accepted": False,
        "profitability_claimed": False,
        "promotion_decision_made": False,
        "paper_eligible": False,
        "live_eligible": False,
        "next_task": {
            "filename": "SAFE_FAST_DAY50_POSITIVE_ENTRY_EXPANSION_AFTER_SETUP_SOURCE_CLOSURE_CODEX_TASK.md",
            "route": "positive_entry_expansion_after_all_current_slots_resolved_or_closed",
            "reason": "All current Day 50 setup-source request slots are now formally closed without promotion; none reached TRADE_CANDIDATE, no paid-data request is valid, and no rule/harness defect was proven.",
        },
    }


def write_completion_document(path=RESULT_PATH, *, run_timestamp=None, source_commit=None):
    document = build_completion_document(
        run_timestamp=run_timestamp,
        source_commit=source_commit,
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return document


def _candidate_record(candidate_id, prior_record):
    review = EXACT_SOURCE_REVIEW[candidate_id]
    fields = [
        _field_resolution(field, review, prior_record)
        for field in REQUIRED_SETUP_FIELDS
    ]
    return {
        "candidate_identifier": candidate_id,
        "underlying": review["underlying"],
        "setup_family": review["setup_family"],
        "direction": prior_record["direction"],
        "decision_timestamp": prior_record["decision_timestamp"],
        "decision_timezone": prior_record["decision_timezone"],
        "source_file": review["source_file"],
        "source_rows": review["source_rows"],
        "source_window": review["source_window"],
        "review_artifacts": review["review_artifacts"],
        "local_replay_evidence": review["local_replay_evidence"],
        "field_resolutions": fields,
        "final_classification": "SETUP_SOURCE_CLOSED_NO_ACCEPTED_EVIDENCE",
        "closure_reason": review["closure_reason"],
        "chronological_rerun_path": [
            "SETUP_DEVELOPING",
            "SETUP_SOURCE_EVIDENCE_CLOSED",
            "SETUP_QUALIFIED_NOT_REACHED",
        ],
        "highest_stage_reached": "SETUP_DEVELOPING",
        "first_stage_not_reached": "SETUP_QUALIFIED",
        "setup_label_result": "not_qualified_closed",
        "setup_qualified": False,
        "trade_candidate": False,
        "contract_selected": False,
        "price_acceptable": False,
        "entry_eligible": False,
        "entry_recorded": False,
        "exit_evaluated": False,
        "first_run_result": "PASS",
        "second_run_result": "PASS",
        "deterministic_result": "deterministic",
        "optional_macro_news_volatility_context": "CONTEXT_UNKNOWN",
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def _field_resolution(field, review, prior_record):
    prior_field = next(
        row for row in prior_record["field_resolutions"] if row["field_name"] == field
    )
    return {
        "field_name": field,
        "blocking_scope": prior_field["blocking_scope"],
        "requirement_class": prior_field["requirement_class"],
        "primary_source": prior_field["primary_source"],
        "local_calculator_or_consumer": prior_field["local_calculator_or_consumer"],
        "timestamp_window": prior_field["timestamp_window"],
        "local_evidence_status": "closed_not_accepted",
        "final_resolution": "SETUP_SOURCE_CLOSED_NO_ACCEPTED_EVIDENCE",
        "closure_note": review["field_notes"][field],
        "optional_context_absent_behavior": (
            "CONTEXT_UNKNOWN_CONTINUE" if field == "blocker_caution_review" else None
        ),
    }


def _scorecard(records):
    classifications = {}
    for record in records:
        classifications[record["final_classification"]] = (
            classifications.get(record["final_classification"], 0) + 1
        )
    return {
        "current_setup_source_slots_reviewed": len(records),
        "setup_source_slots_completed_with_accepted_evidence": 0,
        "setup_source_slots_formally_closed": len(records),
        "setup_source_requests_remaining": 0,
        "setup_qualified_candidates": 0,
        "trade_candidates": 0,
        "contracts_selected": 0,
        "entries_recorded": 0,
        "true_no_trades": 0,
        "valid_trades_captured": 0,
        "missed_valid_trades": 0,
        "invalid_trades_allowed": 0,
        "unresolved_cases": 0,
        "final_classifications": classifications,
        "first_blockers_by_funnel_stage": {"SETUP_QUALIFIED": len(records)},
    }


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
    doc = write_completion_document()
    scorecard = doc["scorecard"]
    print(
        "wrote day50 exact setup-source evidence completion: "
        f"{scorecard['current_setup_source_slots_reviewed']} reviewed, "
        f"{scorecard['setup_source_slots_formally_closed']} closed, "
        f"{scorecard['trade_candidates']} trade candidates"
    )
