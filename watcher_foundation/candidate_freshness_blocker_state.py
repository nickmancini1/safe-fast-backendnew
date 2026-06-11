"""Freshness/final-signal and blocker/caution states for strict intake rows.

This module classifies only the seven Day 39 strict source-backed rows using
existing repo metadata, review docs, and replay logs. It does not inspect
after-the-fact outcomes and does not accept proof.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


ALLOWED_FRESHNESS_STATES = (
    "clean",
    "stale",
    "spent",
    "session_boundary_unclear",
    "gap_context_incomplete",
    "intrabar_ordering_incomplete",
    "setup_specific_rules_incomplete",
    "unresolved",
    "missing",
)

ALLOWED_BLOCKER_STATES = (
    "clean",
    "blocker_present",
    "caution_incomplete",
    "context_incomplete",
    "wide_risk_caution",
    "unresolved",
    "missing",
)

BLOCKING_FRESHNESS_STATES = tuple(
    state for state in ALLOWED_FRESHNESS_STATES if state != "clean"
)
BLOCKING_BLOCKER_STATES = tuple(state for state in ALLOWED_BLOCKER_STATES if state != "clean")

UNRESOLVED_MARKERS = ("", "none", "missing", "unclear", "incomplete", "unresolved")

NO_PROOF_ACCEPTED = True
PROFITABILITY_CLAIMED = False


@dataclass(frozen=True)
class CandidateState:
    candidate_id: str
    freshness_state: str
    blocker_state: str
    freshness_source: str
    blocker_source: str
    freshness_reason: str
    blocker_reason: str
    decision: str
    next_action: str

    def as_row(self) -> dict[str, str]:
        return {
            "candidate_id": self.candidate_id,
            "freshness_state": self.freshness_state,
            "blocker_state": self.blocker_state,
            "freshness_source": self.freshness_source,
            "blocker_source": self.blocker_source,
            "freshness_reason": self.freshness_reason,
            "blocker_reason": self.blocker_reason,
            "decision": self.decision,
            "next_action": self.next_action,
        }


def build_freshness_blocker_states() -> dict[str, object]:
    rows = [state.as_row() for state in _STATES.values()]
    return {
        "state_rows": rows,
        "state_by_id": {row["candidate_id"]: row for row in rows},
        "accepted_state_count": len(rows),
        "intake_ready_count": sum(1 for row in rows if row["decision"] == "intake-ready"),
        "blocked_count": sum(1 for row in rows if row["decision"] == "blocked"),
        "drop_count": sum(1 for row in rows if row["decision"] == "drop"),
        "replace_count": sum(1 for row in rows if row["decision"] == "replace"),
        "top_remaining_blocker_family": _top_remaining_blocker_family(rows),
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def state_for_candidate(candidate_id: str) -> CandidateState:
    try:
        return _STATES[candidate_id]
    except KeyError as exc:
        raise KeyError(f"no freshness/blocker state for {candidate_id}") from exc


def decision_for_states(freshness_state: str, blocker_state: str) -> str:
    if freshness_state not in ALLOWED_FRESHNESS_STATES:
        raise ValueError(f"unsupported freshness_state: {freshness_state}")
    if blocker_state not in ALLOWED_BLOCKER_STATES:
        raise ValueError(f"unsupported blocker_state: {blocker_state}")
    if freshness_state == "clean" and blocker_state == "clean":
        return "intake-ready"
    return "blocked"


def unresolved_marker_blocks(value: object) -> bool:
    text = "" if value is None else str(value).strip().lower()
    return text in UNRESOLVED_MARKERS or any(marker in text for marker in UNRESOLVED_MARKERS[2:])


def blocker_state_from_primary_blocker(primary_blocker: object, complete_review_present: bool) -> str:
    if unresolved_marker_blocks(primary_blocker) and not complete_review_present:
        return "context_incomplete"
    if not unresolved_marker_blocks(primary_blocker):
        return "blocker_present"
    return "clean"


def _state(
    *,
    candidate_id: str,
    freshness_state: str,
    blocker_state: str,
    freshness_source: str,
    blocker_source: str,
    freshness_reason: str,
    blocker_reason: str,
    next_action: str,
) -> CandidateState:
    decision = decision_for_states(freshness_state, blocker_state)
    return CandidateState(
        candidate_id=candidate_id,
        freshness_state=freshness_state,
        blocker_state=blocker_state,
        freshness_source=freshness_source,
        blocker_source=blocker_source,
        freshness_reason=freshness_reason,
        blocker_reason=blocker_reason,
        decision=decision,
        next_action=next_action,
    )


def _top_remaining_blocker_family(rows: list[dict[str, str]]) -> str:
    freshness_blocked = any(row["freshness_state"] != "clean" for row in rows)
    blocker_blocked = any(row["blocker_state"] != "clean" for row in rows)
    if freshness_blocked and blocker_blocked:
        return "freshness/final-signal plus blocker/caution unresolved"
    if freshness_blocked:
        return "freshness/final-signal unresolved"
    if blocker_blocked:
        return "blocker/caution unresolved"
    return "no blocker family among accepted strict rows"


_TOP5_REVIEW = "SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md"
_EXPANSION_REVIEW = "SAFE_FAST_DAY38_SPY_QQQ_BATCH_CANDIDATE_EXPANSION_REVIEW.md"

_STATES: Mapping[str, CandidateState] = {
    "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001": _state(
        candidate_id="QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
        freshness_state="gap_context_incomplete",
        blocker_state="context_incomplete",
        freshness_source=(
            f"{_TOP5_REVIEW}; "
            "historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl line 3"
        ),
        blocker_source=f"{_TOP5_REVIEW}; replay row primary_blocker null with unconfirmed context",
        freshness_reason="Signal/stage exists, but stale/spent and gap-context freshness rules are incomplete.",
        blocker_reason="Primary blocker is null, but 24H, macro, IV, event, gap, and complete caution context remain unconfirmed.",
        next_action="Add repeat QQQ Clean Fast Break rows in batch form before proof review.",
    ),
    "QQQ-REAL-HISTORICAL-CONTINUATION-001": _state(
        candidate_id="QQQ-REAL-HISTORICAL-CONTINUATION-001",
        freshness_state="session_boundary_unclear",
        blocker_state="context_incomplete",
        freshness_source=(
            f"{_TOP5_REVIEW}; "
            "historical_signal_replay/reports/first_real_qqq_continuation_replay_v1_signal_log.jsonl line 5"
        ),
        blocker_source=f"{_TOP5_REVIEW}; replay row primary_blocker null with session-boundary context missing",
        freshness_reason="next-session entry freshness/session-boundary unresolved.",
        blocker_reason="Primary blocker is null, but session-boundary and complete context/caution review remain incomplete.",
        next_action="Define/review next-session Continuation freshness before promotion.",
    ),
    "QQQ-REAL-HISTORICAL-IDEAL-001": _state(
        candidate_id="QQQ-REAL-HISTORICAL-IDEAL-001",
        freshness_state="setup_specific_rules_incomplete",
        blocker_state="wide_risk_caution",
        freshness_source=(
            f"{_TOP5_REVIEW}; "
            "historical_signal_replay/reports/first_real_qqq_ideal_replay_v1_signal_log.jsonl line 5"
        ),
        blocker_source=f"{_TOP5_REVIEW}; wide chart-risk and complete caution review incomplete",
        freshness_reason="Fast-swing hold and setup-specific stale/spent rules remain incomplete.",
        blocker_reason="primary blocker is null, but wide-risk and complete context/caution review incomplete.",
        next_action="Compare against additional QQQ Ideal rows and resolve wide-risk usefulness before proof review.",
    ),
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003": _state(
        candidate_id="SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003",
        freshness_state="setup_specific_rules_incomplete",
        blocker_state="context_incomplete",
        freshness_source=(
            "historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl line 5; "
            "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv line 154"
        ),
        blocker_source="third_real_spy_clean_fast_break replay line 5 primary_blocker null with unconfirmed context",
        freshness_reason=(
            "freshness/final-signal fresh/non-duplicate state-model review is incomplete for this added source-pool row."
        ),
        blocker_reason="Primary blocker is null, but complete blocker/caution review remains incomplete.",
        next_action="Keep blocked until freshness/final-signal and blocker/caution state review is complete.",
    ),
    "SPY-REAL-HISTORICAL-CONTINUATION-001": _state(
        candidate_id="SPY-REAL-HISTORICAL-CONTINUATION-001",
        freshness_state="intrabar_ordering_incomplete",
        blocker_state="context_incomplete",
        freshness_source=(
            f"{_TOP5_REVIEW}; "
            "historical_signal_replay/reports/first_real_spy_continuation_replay_v1_signal_log.jsonl line 5"
        ),
        blocker_source=f"{_TOP5_REVIEW}; replay row primary_blocker null with finer context missing",
        freshness_reason="Signal/stage exists, but stale/spent and finer intrabar ordering rules remain incomplete.",
        blocker_reason="Primary blocker is null, but complete context/caution review remains incomplete.",
        next_action="Keep only in larger no-hindsight batch and require repeat rows before proof review.",
    ),
    "SPY-REAL-HISTORICAL-IDEAL-001": _state(
        candidate_id="SPY-REAL-HISTORICAL-IDEAL-001",
        freshness_state="setup_specific_rules_incomplete",
        blocker_state="context_incomplete",
        freshness_source=(
            f"{_TOP5_REVIEW}; "
            "historical_signal_replay/reports/second_real_spy_ideal_replay_v1_signal_log.jsonl line 5"
        ),
        blocker_source=f"{_TOP5_REVIEW}; replay row primary_blocker null with complete context missing",
        freshness_reason="Signal/stage exists, but setup-specific stale/spent rules remain incomplete.",
        blocker_reason="Primary blocker is null, but complete context/caution review remains incomplete.",
        next_action="Require more SPY Ideal rows before treating this as more than one selected sample.",
    ),
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002": _state(
        candidate_id="SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
        freshness_state="setup_specific_rules_incomplete",
        blocker_state="context_incomplete",
        freshness_source=(
            f"{_EXPANSION_REVIEW}; "
            "historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl line 2"
        ),
        blocker_source=f"{_EXPANSION_REVIEW}; signal log primary_blocker null with complete caution review incomplete",
        freshness_reason="Signal/stage context exists; final freshness review incomplete.",
        blocker_reason="Primary blocker is null, but complete context/caution review remains incomplete.",
        next_action="Run bounded chart-only outcome review for the exact 2026-04-13 row before proof review.",
    ),
}
