"""Rule-gate checks for seven strict freshness/blocker rows.

This module records whether the repo contains source-backed rule evidence for
the freshness/final-signal and blocker/caution families that currently block
Day 39 strict intake. It does not inspect outcomes and does not accept proof.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


GATE_STATUSES = (
    "SOURCE_BACKED",
    "MISSING_RULE",
    "SOURCE_DATA_INSUFFICIENT",
    "LOWER_TIMEFRAME_REQUIRED",
    "THRESHOLD_MISSING",
    "UNRESOLVED",
)

PROMOTING_GATE_STATUSES = ("SOURCE_BACKED",)

NO_PROOF_ACCEPTED = True
PROFITABILITY_CLAIMED = False


@dataclass(frozen=True)
class RuleGate:
    rule_family: str
    setup_type: str
    symbol_or_scope: str
    gate_status: str
    source_reference: str
    reason: str
    affected_candidate_ids: tuple[str, ...]
    next_action: str

    def as_row(self) -> dict[str, object]:
        return {
            "rule_family": self.rule_family,
            "setup_type": self.setup_type,
            "symbol_or_scope": self.symbol_or_scope,
            "gate_status": self.gate_status,
            "source_reference": self.source_reference,
            "reason": self.reason,
            "affected_candidate_ids": self.affected_candidate_ids,
            "next_action": self.next_action,
        }


STRICT_CANDIDATE_IDS = (
    "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
    "QQQ-REAL-HISTORICAL-CONTINUATION-001",
    "QQQ-REAL-HISTORICAL-IDEAL-001",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003",
    "SPY-REAL-HISTORICAL-CONTINUATION-001",
    "SPY-REAL-HISTORICAL-IDEAL-001",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
)

_CFB_IDS = (
    "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
)
_CONTINUATION_IDS = (
    "QQQ-REAL-HISTORICAL-CONTINUATION-001",
    "SPY-REAL-HISTORICAL-CONTINUATION-001",
)
_IDEAL_IDS = (
    "QQQ-REAL-HISTORICAL-IDEAL-001",
    "SPY-REAL-HISTORICAL-IDEAL-001",
)


_RULE_GATES: tuple[RuleGate, ...] = (
    RuleGate(
        rule_family="Clean Fast Break initial-break / higher-base / fresh-break expiry",
        setup_type="Clean Fast Break",
        symbol_or_scope="QQQ/SPY",
        gate_status="MISSING_RULE",
        source_reference=(
            "SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md; "
            "SAFE_FAST_DAY38_SPY_QQQ_BATCH_CANDIDATE_EXPANSION_REVIEW.md; "
            "historical_signal_replay/THIRD_REAL_HISTORICAL_REPLAY_V1_FIXTURE_DESIGN_REVIEW.md"
        ),
        reason=(
            "Repo replay rows label initial, higher-base, fresh-break, and spent states, "
            "but no accepted stale/spent expiry rule defines when these Clean Fast Break "
            "signals remain fresh enough for intake."
        ),
        affected_candidate_ids=_CFB_IDS,
        next_action=(
            "Define and regression-test the Clean Fast Break initial-break, higher-base, "
            "and fresh-break stale/spent expiry rule before proof review."
        ),
    ),
    RuleGate(
        rule_family="Clean Fast Break gap-context completeness",
        setup_type="Clean Fast Break",
        symbol_or_scope="QQQ",
        gate_status="SOURCE_DATA_INSUFFICIENT",
        source_reference=(
            "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv; "
            "historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl"
        ),
        reason=(
            "The source CSV has OHLCV plus unconfirmed context columns, and the replay log "
            "has shape/lifecycle labels only; no source-backed gap-context completeness field "
            "or rule exists for the QQQ gap/impulse setup-time decision."
        ),
        affected_candidate_ids=("QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",),
        next_action=(
            "Add source-backed gap-context completeness evidence or keep QQQ Clean Fast Break "
            "gap-context rows blocked."
        ),
    ),
    RuleGate(
        rule_family="Continuation next-session carry-forward freshness",
        setup_type="Continuation",
        symbol_or_scope="QQQ",
        gate_status="MISSING_RULE",
        source_reference=(
            "SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md; "
            "historical_signal_replay/reports/first_real_qqq_continuation_replay_v1_signal_log.jsonl"
        ),
        reason=(
            "Repo evidence records a 2026-04-30 15:30 Continuation trigger and a later spent "
            "row, but no accepted rule authorizes or rejects next-session entry freshness."
        ),
        affected_candidate_ids=("QQQ-REAL-HISTORICAL-CONTINUATION-001",),
        next_action=(
            "Define and test Continuation next-session carry-forward freshness before any "
            "next-session candidate can become intake-ready."
        ),
    ),
    RuleGate(
        rule_family="Continuation session-boundary freshness",
        setup_type="Continuation",
        symbol_or_scope="QQQ/SPY",
        gate_status="MISSING_RULE",
        source_reference=(
            "SAFE_FAST_ARCHITECT_CONTROL_AND_PROJECT_TIGHTENING.md; "
            "SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_PACKET.md"
        ),
        reason=(
            "Session-boundary ambiguity is documented as a blocker, but no machine-checkable "
            "freshness rule exists for Continuation candidates at or across a session boundary."
        ),
        affected_candidate_ids=_CONTINUATION_IDS,
        next_action=(
            "Define session-boundary freshness requirements for Continuation rows and preserve "
            "blocked behavior until the rule is source-backed."
        ),
    ),
    RuleGate(
        rule_family="Ideal stale/spent expiry",
        setup_type="Ideal",
        symbol_or_scope="QQQ/SPY",
        gate_status="MISSING_RULE",
        source_reference=(
            "SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md; "
            "historical_signal_replay/reports/first_real_qqq_ideal_replay_v1_signal_log.jsonl; "
            "historical_signal_replay/reports/second_real_spy_ideal_replay_v1_signal_log.jsonl"
        ),
        reason=(
            "Ideal replay rows identify trigger and later spent lifecycle states, but no "
            "accepted Ideal stale/spent expiry rule exists for setup-time intake."
        ),
        affected_candidate_ids=_IDEAL_IDS,
        next_action="Define and regression-test Ideal stale/spent expiry before promotion.",
    ),
    RuleGate(
        rule_family="Ideal fast-swing freshness",
        setup_type="Ideal",
        symbol_or_scope="QQQ",
        gate_status="MISSING_RULE",
        source_reference="SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md",
        reason=(
            "The QQQ Ideal packet marks fast-swing hold freshness as unfilled; no accepted "
            "rule defines whether a fast-swing Ideal remains fresh."
        ),
        affected_candidate_ids=("QQQ-REAL-HISTORICAL-IDEAL-001",),
        next_action="Define fast-swing Ideal freshness before using the row for proof review.",
    ),
    RuleGate(
        rule_family="intrabar ordering / order-of-events inside 1H candles",
        setup_type="Continuation",
        symbol_or_scope="SPY",
        gate_status="LOWER_TIMEFRAME_REQUIRED",
        source_reference=(
            "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv; "
            "SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md"
        ),
        reason=(
            "The available source is completed 1H OHLCV. It cannot prove the order of trigger, "
            "pullback, and invalidation behavior inside the setup/entry candles."
        ),
        affected_candidate_ids=("SPY-REAL-HISTORICAL-CONTINUATION-001",),
        next_action=(
            "Provide lower-timeframe source rows or a source-backed rule that explicitly does "
            "not require intrabar ordering for this candidate family."
        ),
    ),
    RuleGate(
        rule_family="wide-risk / room threshold",
        setup_type="Ideal",
        symbol_or_scope="QQQ",
        gate_status="THRESHOLD_MISSING",
        source_reference=(
            "SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md; "
            "SAFE_FAST_DAY39_COMBINED_HANDOFF_AND_FAST_CANDIDATE_FUNNEL.md"
        ),
        reason=(
            "QQQ Ideal wide chart-risk/room is called out as unresolved, but no accepted "
            "risk/room threshold exists to decide whether the row is tradably useful."
        ),
        affected_candidate_ids=("QQQ-REAL-HISTORICAL-IDEAL-001",),
        next_action="Define accepted wide-risk and room thresholds before promotion.",
    ),
    RuleGate(
        rule_family="complete context/caution review",
        setup_type="all",
        symbol_or_scope="QQQ/SPY",
        gate_status="SOURCE_DATA_INSUFFICIENT",
        source_reference=(
            "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv; "
            "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv; "
            "historical_signal_replay/reports/*.jsonl used by the seven strict rows"
        ),
        reason=(
            "The seven rows carry MACRO_UNCONFIRMED, IV_UNCONFIRMED, EVENT_UNCONFIRMED, "
            "CONTEXT_24H_DAILY_UNCONFIRMED, room_status unconfirmed, and no complete "
            "context/caution review field."
        ),
        affected_candidate_ids=STRICT_CANDIDATE_IDS,
        next_action=(
            "Add complete source-backed context/caution review fields or keep all seven rows "
            "blocked from intake-ready status."
        ),
    ),
    RuleGate(
        rule_family="primary blocker null is not enough",
        setup_type="all",
        symbol_or_scope="QQQ/SPY",
        gate_status="SOURCE_BACKED",
        source_reference=(
            "SAFE_FAST_ARCHITECT_CONTROL_AND_PROJECT_TIGHTENING.md; "
            "watcher_foundation/candidate_freshness_blocker_state.py"
        ),
        reason=(
            "Repo guardrails require blocker/caution state to be clean before intake-ready; "
            "the existing state helper classifies primary_blocker null without complete review "
            "as context_incomplete."
        ),
        affected_candidate_ids=STRICT_CANDIDATE_IDS,
        next_action=(
            "Continue requiring complete blocker/caution review; do not promote from "
            "primary_blocker null or final_verdict TRADE alone."
        ),
    ),
)


def build_rule_gate_result() -> dict[str, object]:
    rows = [gate.as_row() for gate in _RULE_GATES]
    by_candidate = _gates_by_candidate(_RULE_GATES)
    return {
        "rule_families_checked": len(rows),
        "source_backed_rule_count": sum(
            1 for row in rows if row["gate_status"] == "SOURCE_BACKED"
        ),
        "missing_unresolved_rule_count": sum(
            1 for row in rows if row["gate_status"] != "SOURCE_BACKED"
        ),
        "affected_candidate_ids": STRICT_CANDIDATE_IDS,
        "gate_rows": rows,
        "gate_by_candidate": {
            candidate_id: [gate.as_row() for gate in gates]
            for candidate_id, gates in by_candidate.items()
        },
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def gates_for_candidate(candidate_id: str) -> tuple[RuleGate, ...]:
    gates = tuple(gate for gate in _RULE_GATES if candidate_id in gate.affected_candidate_ids)
    if not gates:
        raise KeyError(f"no rule gates for {candidate_id}")
    return gates


def candidate_rule_gate_status(candidate_id: str) -> str:
    gates = gates_for_candidate(candidate_id)
    if all(gate.gate_status in PROMOTING_GATE_STATUSES for gate in gates):
        return "pass"
    return "blocked"


def candidate_can_promote(
    candidate_id: str,
    *,
    final_verdict: object = None,
    primary_blocker: object = None,
    complete_context_caution_review: bool = False,
) -> bool:
    """Return whether rule gates permit promotion.

    final_verdict and primary_blocker are intentionally insufficient without
    source-backed gates and a complete context/caution review.
    """

    if str(final_verdict).strip().upper() == "TRADE" and not complete_context_caution_review:
        return False
    if _primary_blocker_is_nullish(primary_blocker) and not complete_context_caution_review:
        return False
    return candidate_rule_gate_status(candidate_id) == "pass"


def format_rule_gate_report(result: dict[str, object]) -> str:
    lines = [
        f"rule families checked: {result['rule_families_checked']}",
        f"source-backed rule count: {result['source_backed_rule_count']}",
        f"missing/unresolved rule count: {result['missing_unresolved_rule_count']}",
        f"affected candidate IDs: {', '.join(result['affected_candidate_ids'])}",
        "exact next fix per rule family:",
        "rule-gate table:",
    ]
    for row in result["gate_rows"]:
        lines.append(
            " | ".join(
                (
                    str(row["rule_family"]),
                    f"setup_type={row['setup_type']}",
                    f"scope={row['symbol_or_scope']}",
                    f"gate_status={row['gate_status']}",
                    f"affected={', '.join(row['affected_candidate_ids'])}",
                    f"next_fix={row['next_action']}",
                )
            )
        )
    lines.extend(
        (
            "proof accepted: NO",
            "profitability claim made: NO",
        )
    )
    return "\n".join(lines)


def _gates_by_candidate(gates: Iterable[RuleGate]) -> Mapping[str, tuple[RuleGate, ...]]:
    by_candidate: dict[str, list[RuleGate]] = {candidate_id: [] for candidate_id in STRICT_CANDIDATE_IDS}
    for gate in gates:
        if gate.gate_status not in GATE_STATUSES:
            raise ValueError(f"unsupported gate_status: {gate.gate_status}")
        for candidate_id in gate.affected_candidate_ids:
            by_candidate[candidate_id].append(gate)
    return {candidate_id: tuple(candidate_gates) for candidate_id, candidate_gates in by_candidate.items()}


def _primary_blocker_is_nullish(value: object) -> bool:
    if value is None:
        return True
    return str(value).strip().lower() in {"", "none", "null"}


def main() -> None:
    print(format_rule_gate_report(build_rule_gate_result()))


if __name__ == "__main__":
    main()
