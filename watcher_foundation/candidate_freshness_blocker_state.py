"""Freshness/final-signal and blocker/caution states for strict intake rows.

This module classifies only the seven Day 39 strict source-backed rows using
existing repo metadata, review docs, and replay logs. It does not inspect
after-the-fact outcomes and does not accept proof.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from watcher_foundation import candidate_freshness_blocker_rule_gate as rule_gate


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
    freshness_missing_evidence: str
    blocker_missing_evidence: str
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
            "freshness_missing_evidence": self.freshness_missing_evidence,
            "blocker_missing_evidence": self.blocker_missing_evidence,
            "decision": self.decision,
            "next_action": self.next_action,
        }


def build_freshness_blocker_states() -> dict[str, object]:
    rows = [state.as_row() for state in _STATES.values()]
    gate_result = rule_gate.build_rule_gate_result()
    return {
        "state_rows": rows,
        "state_by_id": {row["candidate_id"]: row for row in rows},
        "rule_gate_by_candidate": gate_result["gate_by_candidate"],
        "rule_gate_source_backed_rule_count": gate_result["source_backed_rule_count"],
        "rule_gate_missing_unresolved_rule_count": gate_result["missing_unresolved_rule_count"],
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


def decision_for_candidate(candidate_id: str, freshness_state: str, blocker_state: str) -> str:
    state_decision = decision_for_states(freshness_state, blocker_state)
    if state_decision != "intake-ready":
        return state_decision
    if not rule_gate.candidate_can_promote(candidate_id):
        return "blocked"
    return state_decision


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
    freshness_missing_evidence: str,
    blocker_missing_evidence: str,
    next_action: str,
) -> CandidateState:
    decision = decision_for_candidate(candidate_id, freshness_state, blocker_state)
    return CandidateState(
        candidate_id=candidate_id,
        freshness_state=freshness_state,
        blocker_state=blocker_state,
        freshness_source=freshness_source,
        blocker_source=blocker_source,
        freshness_reason=freshness_reason,
        blocker_reason=blocker_reason,
        freshness_missing_evidence=freshness_missing_evidence,
        blocker_missing_evidence=blocker_missing_evidence,
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
_CSV_CONTEXT_LIMITATION = (
    "source CSV contains OHLCV plus context_24h_status, macro_context_status, "
    "iv_context_status, and event_context_status; those context columns are "
    "UNCONFIRMED and no source-backed complete caution/context review field exists"
)
_REPLAY_CONTEXT_LIMITATION = (
    "replay row has primary_blocker null only; cautions_watchouts remain "
    "MACRO_UNCONFIRMED, IV_UNCONFIRMED, and EVENT_UNCONFIRMED, with "
    "context_24h CONTEXT_24H_DAILY_UNCONFIRMED"
)

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
        freshness_reason=(
            "Replay line 3 proves a triggered signal at the setup-time boundary and line 4 later proves "
            "the same lifecycle became spent, but the setup-time source has no source-backed gap-context "
            "field or rule that can decide whether the 04-13 gap/impulse context was fresh enough at intake."
        ),
        blocker_reason=(
            "Primary blocker is null at replay line 3, but null is not a complete blocker/caution review; "
            "24H, macro, IV, event, gap, room, and complete caution context remain unconfirmed."
        ),
        freshness_missing_evidence=(
            "missing source-backed gap_context field/rule before or at 2026-04-13T12:30:00-04:00; "
            "missing Clean Fast Break stale/spent expiry rule for gap/impulse context"
        ),
        blocker_missing_evidence=_REPLAY_CONTEXT_LIMITATION + "; " + _CSV_CONTEXT_LIMITATION,
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
        freshness_reason=(
            "Replay line 5 proves a 2026-04-30 15:30 triggered Continuation signal and line 6 proves the "
            "same lifecycle was spent on 2026-05-01, but the repo has no next-session carry-forward rule "
            "that says a 15:30 signal remains fresh for a next-session entry."
        ),
        blocker_reason=(
            "Primary blocker is null at the trigger row, but session-boundary handling plus broader "
            "24H/macro/IV/event/room/caution context is still unconfirmed."
        ),
        freshness_missing_evidence=(
            "missing next-session Continuation freshness/carry-forward rule; missing source-backed "
            "session-boundary evidence that authorizes 2026-05-01 entry freshness from the 2026-04-30 15:30 signal"
        ),
        blocker_missing_evidence=_REPLAY_CONTEXT_LIMITATION + "; session-boundary caution review missing",
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
        freshness_reason=(
            "Replay line 5 proves a triggered Ideal signal and line 6 later marks the lifecycle spent, "
            "but repo rules do not define the allowed Ideal stale/spent expiry or fast-swing hold freshness."
        ),
        blocker_reason=(
            "Primary blocker is null, but wide-risk/room remains only a caution with no accepted "
            "risk/room threshold; 24H, macro, IV, event, option/execution, and complete caution context remain unconfirmed."
        ),
        freshness_missing_evidence=(
            "missing Ideal-specific stale/spent expiry rule; missing source-backed fast-swing hold freshness rule"
        ),
        blocker_missing_evidence=(
            "missing accepted wide-risk or room threshold for QQQ Ideal; "
            + _REPLAY_CONTEXT_LIMITATION
        ),
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
            "Replay line 5 proves a fresh break signal candidate at 2026-04-15 14:30 and line 6 later marks "
            "it spent, but the repo does not define the Clean Fast Break higher-base/fresh-break stale/spent "
            "expiry rule needed to clean the added row."
        ),
        blocker_reason=(
            "Primary blocker is null, but the row still has unconfirmed macro/IV/event/24H/room context and "
            "no complete blocker/caution review."
        ),
        freshness_missing_evidence=(
            "missing Clean Fast Break higher-base/fresh-break stale/spent expiry rule for the 2026-04-15 14:30 signal"
        ),
        blocker_missing_evidence=_REPLAY_CONTEXT_LIMITATION + "; complete added-row caution review missing",
        next_action="Define Clean Fast Break higher-base/fresh-break expiry and complete context/caution review before proof review.",
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
        freshness_reason=(
            "Replay line 5 proves a triggered signal at 2026-04-30 12:30 and line 6 later marks it spent, "
            "but only 1H OHLCV source rows exist; they cannot prove the order of trigger, pullback, and "
            "invalidation behavior inside the setup/entry candle."
        ),
        blocker_reason=(
            "Primary blocker is null, but complete 24H/macro/IV/event/headline/room/caution context remains unconfirmed."
        ),
        freshness_missing_evidence=(
            "missing lower-timeframe or order-of-events evidence inside the 2026-04-30 12:30/13:30 1H candles"
        ),
        blocker_missing_evidence=_REPLAY_CONTEXT_LIMITATION + "; headline and finer intrabar caution context missing",
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
        freshness_reason=(
            "Replay line 5 proves a triggered Ideal signal and line 6 later marks it spent, but repo rules do "
            "not define Ideal-specific stale/spent expiry at setup-time intake."
        ),
        blocker_reason=(
            "Primary blocker is null, but 24H, macro, IV, event, gap/headline, room, option/execution, and "
            "complete caution context remain unconfirmed."
        ),
        freshness_missing_evidence="missing Ideal-specific stale/spent expiry rule for SPY same-session Ideal signals",
        blocker_missing_evidence=_REPLAY_CONTEXT_LIMITATION + "; complete Ideal gap/headline/room caution review missing",
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
        freshness_reason=(
            "Replay line 2 proves a triggered initial-break signal and line 3 later marks same-session "
            "follow-through/spent context, but repo rules do not define the Clean Fast Break initial-break "
            "expiry threshold for intake."
        ),
        blocker_reason=(
            "Primary blocker is null, but the replay and source context still leave 24H/macro/IV/event/room "
            "and complete caution review unconfirmed."
        ),
        freshness_missing_evidence=(
            "missing Clean Fast Break initial-break stale/spent expiry rule for the 2026-04-13 12:30 signal"
        ),
        blocker_missing_evidence=_REPLAY_CONTEXT_LIMITATION + "; complete Clean Fast Break caution review missing",
        next_action="Run bounded chart-only outcome review for the exact 2026-04-13 row before proof review.",
    ),
}


def format_state_report(result: dict[str, object]) -> str:
    lines = [
        f"accepted state count: {result['accepted_state_count']}",
        f"intake-ready count: {result['intake_ready_count']}",
        f"blocked count: {result['blocked_count']}",
        f"top remaining blocker family: {result['top_remaining_blocker_family']}",
        "state table:",
    ]
    for row in result["state_rows"]:
        lines.append(
            " | ".join(
                (
                    row["candidate_id"],
                    f"freshness_state={row['freshness_state']}",
                    f"blocker_state={row['blocker_state']}",
                    f"freshness_missing={row['freshness_missing_evidence']}",
                    f"blocker_missing={row['blocker_missing_evidence']}",
                    f"decision={row['decision']}",
                )
            )
        )
    return "\n".join(lines)


def main() -> None:
    print(format_state_report(build_freshness_blocker_states()))


if __name__ == "__main__":
    main()
