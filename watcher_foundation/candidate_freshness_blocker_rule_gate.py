"""Hard rule-family decisions for the seven strict Day 39 rows.

This module mirrors SAFE_FAST_RULE_FAMILY_DECISION_TABLE.md. It records the
trade-plan decision for each missing freshness/blocker family, blocks silent
promotion through missing evidence, and does not inspect outcomes or accept
proof.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


HARD_DECISIONS = (
    "DEFINE_FROM_REPO_EVIDENCE",
    "SOURCE_DATA_INSUFFICIENT",
    "KILL_OR_NARROW_SETUP_SYMBOL_PATH",
)

PROMOTING_DECISIONS = ("DEFINE_FROM_REPO_EVIDENCE",)

NO_PROOF_ACCEPTED = True
PROFITABILITY_CLAIMED = False


@dataclass(frozen=True)
class RuleFamilyDecision:
    rule_family: str
    hard_decision: str
    setup_type: str
    symbol_or_scope: str
    affected_candidate_ids: tuple[str, ...]
    repo_evidence_checked: str
    exact_reason: str
    intake_ready_effect: str
    smallest_next_action: str
    blocks_proof_review: bool

    def as_row(self) -> dict[str, object]:
        return {
            "rule_family": self.rule_family,
            "hard_decision": self.hard_decision,
            "setup_type": self.setup_type,
            "symbol_or_scope": self.symbol_or_scope,
            "affected_candidate_ids": self.affected_candidate_ids,
            "repo_evidence_checked": self.repo_evidence_checked,
            "exact_reason": self.exact_reason,
            "intake_ready_effect": self.intake_ready_effect,
            "smallest_next_action": self.smallest_next_action,
            "blocks_proof_review": self.blocks_proof_review,
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

OUTSIDE_NARROWED_PATH_CANDIDATE_IDS = (
    "QQQ-REAL-HISTORICAL-CONTINUATION-001",
    "QQQ-REAL-HISTORICAL-IDEAL-001",
)

CLEAN_FAST_BREAK_SOURCE_DATA_INSUFFICIENT_CANDIDATE_IDS = _CFB_IDS

CFB_SOURCE_DATA_INSUFFICIENT_REASONS = {
    "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001": (
        "blocked by Clean Fast Break expiry source-data insufficiency and "
        "gap-context source-data insufficiency"
    ),
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003": (
        "blocked by Clean Fast Break expiry source-data insufficiency and "
        "complete context/caution source-data insufficiency"
    ),
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002": (
        "blocked by Clean Fast Break expiry source-data insufficiency and "
        "complete context/caution source-data insufficiency"
    ),
}

SAME_SESSION_CONTINUATION_CANDIDATE_IDS = (
    "SPY-REAL-HISTORICAL-CONTINUATION-001",
)

OUTSIDE_NARROWED_PATH_REASONS = {
    "QQQ-REAL-HISTORICAL-CONTINUATION-001": (
        "outside narrowed Continuation path; next-session/session-boundary carry-forward "
        "freshness remains unsupported"
    ),
    "QQQ-REAL-HISTORICAL-IDEAL-001": (
        "outside narrowed Ideal path; fast-swing freshness and wide-risk/room threshold "
        "remain unsupported"
    ),
}


_DECISIONS: tuple[RuleFamilyDecision, ...] = (
    RuleFamilyDecision(
        rule_family="Clean Fast Break expiry",
        hard_decision="SOURCE_DATA_INSUFFICIENT",
        setup_type="Clean Fast Break",
        symbol_or_scope="QQQ/SPY",
        affected_candidate_ids=_CFB_IDS,
        repo_evidence_checked=(
            "SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md; "
            "SAFE_FAST_DAY38_SPY_QQQ_BATCH_CANDIDATE_EXPANSION_REVIEW.md; "
            "historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl"
        ),
        exact_reason=(
            "Repo rows show initial-break, higher-base, fresh-break, and spent lifecycle labels, "
            "but no accepted source-backed expiry rule defines when a Clean Fast Break signal "
            "has become stale or spent for intake promotion."
        ),
        intake_ready_effect=(
            "All affected Clean Fast Break rows remain blocked; final_verdict TRADE cannot "
            "satisfy expiry."
        ),
        smallest_next_action=(
            "Define a source-backed Clean Fast Break expiry rule with regression rows before "
            "any Clean Fast Break proof review."
        ),
        blocks_proof_review=True,
    ),
    RuleFamilyDecision(
        rule_family="Clean Fast Break gap context",
        hard_decision="SOURCE_DATA_INSUFFICIENT",
        setup_type="Clean Fast Break",
        symbol_or_scope="QQQ",
        affected_candidate_ids=("QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",),
        repo_evidence_checked=(
            "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv; "
            "historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl"
        ),
        exact_reason=(
            "The QQQ source data has OHLCV plus unconfirmed context fields and the replay log "
            "has lifecycle labels, but no source-backed gap-context completeness field exists "
            "for the setup-time decision."
        ),
        intake_ready_effect="The QQQ gap Clean Fast Break row remains blocked from intake-ready.",
        smallest_next_action=(
            "Add source-backed gap-context evidence fields or keep QQQ gap Clean Fast Break "
            "out of proof review."
        ),
        blocks_proof_review=True,
    ),
    RuleFamilyDecision(
        rule_family="Continuation next-session freshness",
        hard_decision="KILL_OR_NARROW_SETUP_SYMBOL_PATH",
        setup_type="Continuation",
        symbol_or_scope="QQQ",
        affected_candidate_ids=("QQQ-REAL-HISTORICAL-CONTINUATION-001",),
        repo_evidence_checked=(
            "SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md; "
            "historical_signal_replay/reports/first_real_qqq_continuation_replay_v1_signal_log.jsonl"
        ),
        exact_reason=(
            "The repo records a 2026-04-30 15:30 Continuation trigger and a later spent row, "
            "but does not authorize next-session carry-forward freshness. The path is narrowed "
            "away from next-session Continuation entries until source-backed rules exist."
        ),
        intake_ready_effect=(
            "QQQ next-session Continuation is outside the narrowed Continuation path and cannot "
            "become intake-ready under current repo evidence."
        ),
        smallest_next_action=(
            "Either source a tested next-session carry-forward rule or exclude next-session "
            "Continuation rows from the intake-ready path."
        ),
        blocks_proof_review=True,
    ),
    RuleFamilyDecision(
        rule_family="Continuation session-boundary freshness",
        hard_decision="KILL_OR_NARROW_SETUP_SYMBOL_PATH",
        setup_type="Continuation",
        symbol_or_scope="QQQ/SPY",
        affected_candidate_ids=_CONTINUATION_IDS,
        repo_evidence_checked=(
            "SAFE_FAST_ARCHITECT_CONTROL_AND_PROJECT_TIGHTENING.md; "
            "SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_PACKET.md"
        ),
        exact_reason=(
            "Session-boundary handling is a documented blocker and no source-backed rule "
            "defines when Continuation signals survive the boundary. The setup-symbol path is "
            "narrowed to Continuation rows without session-boundary dependency."
        ),
        intake_ready_effect=(
            "Continuation rows with session-boundary dependency cannot become intake-ready; "
            "next-session rows are outside the narrowed path and same-session rows must still "
            "pass intrabar ordering plus complete context/caution gates."
        ),
        smallest_next_action=(
            "Source and test Continuation session-boundary requirements before reviewing these "
            "rows as proof candidates."
        ),
        blocks_proof_review=True,
    ),
    RuleFamilyDecision(
        rule_family="Ideal stale/spent expiry",
        hard_decision="SOURCE_DATA_INSUFFICIENT",
        setup_type="Ideal",
        symbol_or_scope="QQQ/SPY",
        affected_candidate_ids=_IDEAL_IDS,
        repo_evidence_checked=(
            "SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md; "
            "historical_signal_replay/reports/first_real_qqq_ideal_replay_v1_signal_log.jsonl; "
            "historical_signal_replay/reports/second_real_spy_ideal_replay_v1_signal_log.jsonl"
        ),
        exact_reason=(
            "Ideal replay rows show triggers and later spent lifecycle states, but repo evidence "
            "does not define the accepted stale/spent expiry rule at setup time."
        ),
        intake_ready_effect="QQQ/SPY Ideal rows remain blocked from intake-ready.",
        smallest_next_action=(
            "Define and regression-test Ideal stale/spent expiry before Ideal proof review."
        ),
        blocks_proof_review=True,
    ),
    RuleFamilyDecision(
        rule_family="Ideal fast-swing freshness",
        hard_decision="KILL_OR_NARROW_SETUP_SYMBOL_PATH",
        setup_type="Ideal",
        symbol_or_scope="QQQ",
        affected_candidate_ids=("QQQ-REAL-HISTORICAL-IDEAL-001",),
        repo_evidence_checked="SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md",
        exact_reason=(
            "The QQQ Ideal packet leaves fast-swing hold freshness unfilled and no accepted "
            "rule says the fast-swing path remains actionable. The QQQ fast-swing Ideal path "
            "is narrowed out until it earns a source-backed rule."
        ),
        intake_ready_effect="QQQ fast-swing Ideal cannot become intake-ready under current evidence.",
        smallest_next_action=(
            "Either define tested fast-swing freshness or exclude fast-swing Ideal rows from "
            "the proof-review pool."
        ),
        blocks_proof_review=True,
    ),
    RuleFamilyDecision(
        rule_family="Intrabar ordering",
        hard_decision="KILL_OR_NARROW_SETUP_SYMBOL_PATH",
        setup_type="Continuation",
        symbol_or_scope="SPY",
        affected_candidate_ids=("SPY-REAL-HISTORICAL-CONTINUATION-001",),
        repo_evidence_checked=(
            "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv; "
            "SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md"
        ),
        exact_reason=(
            "Available SPY source is completed 1H OHLCV and cannot prove the order of trigger, "
            "pullback, and invalidation events inside the setup candles. The SPY Continuation "
            "intrabar-dependent path is narrowed out unless lower-timeframe evidence exists."
        ),
        intake_ready_effect="SPY Continuation intrabar-dependent rows remain blocked from intake-ready.",
        smallest_next_action=(
            "Provide lower-timeframe source rows or exclude intrabar-dependent Continuation rows "
            "from proof review."
        ),
        blocks_proof_review=True,
    ),
    RuleFamilyDecision(
        rule_family="Wide-risk / room threshold",
        hard_decision="KILL_OR_NARROW_SETUP_SYMBOL_PATH",
        setup_type="Ideal",
        symbol_or_scope="QQQ",
        affected_candidate_ids=("QQQ-REAL-HISTORICAL-IDEAL-001",),
        repo_evidence_checked=(
            "SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md; "
            "SAFE_FAST_DAY39_COMBINED_HANDOFF_AND_FAST_CANDIDATE_FUNNEL.md"
        ),
        exact_reason=(
            "QQQ Ideal wide chart-risk and room are documented as unresolved trade-usefulness "
            "problems, and no accepted threshold defines enough room after risk and costs. "
            "The wide-risk QQQ Ideal path is narrowed out until thresholds exist."
        ),
        intake_ready_effect="QQQ wide-risk Ideal cannot become intake-ready under current evidence.",
        smallest_next_action=(
            "Define accepted room and wide-risk thresholds before restoring this path to proof review."
        ),
        blocks_proof_review=True,
    ),
    RuleFamilyDecision(
        rule_family="Context/caution review",
        hard_decision="SOURCE_DATA_INSUFFICIENT",
        setup_type="all",
        symbol_or_scope="QQQ/SPY",
        affected_candidate_ids=STRICT_CANDIDATE_IDS,
        repo_evidence_checked=(
            "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv; "
            "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv; "
            "historical_signal_replay/reports/*.jsonl used by the seven strict rows; "
            "SAFE_FAST_ARCHITECT_CONTROL_AND_PROJECT_TIGHTENING.md"
        ),
        exact_reason=(
            "Rows still carry unconfirmed 24H, macro, IV, event, room, headline, option, or "
            "execution context. Primary blocker null is source-backed as insufficient because "
            "blocker/caution must be complete and clean before intake-ready."
        ),
        intake_ready_effect=(
            "All seven rows remain blocked; primary blocker null alone and final_verdict TRADE "
            "alone cannot promote."
        ),
        smallest_next_action=(
            "Add complete source-backed context/caution review fields before any of the seven "
            "rows can enter proof review."
        ),
        blocks_proof_review=True,
    ),
)


def build_rule_gate_result() -> dict[str, object]:
    rows = [decision.as_row() for decision in _DECISIONS]
    by_candidate = _decisions_by_candidate(_DECISIONS)
    source_backed_count = sum(
        1 for row in rows if row["hard_decision"] == "DEFINE_FROM_REPO_EVIDENCE"
    )
    blocking_count = sum(
        1 for row in rows if row["hard_decision"] != "DEFINE_FROM_REPO_EVIDENCE"
    )
    return {
        "rule_families_checked": len(rows),
        "source_backed_rule_count": source_backed_count,
        "missing_unresolved_rule_count": blocking_count,
        "hard_decision_counts": {
            decision: sum(1 for row in rows if row["hard_decision"] == decision)
            for decision in HARD_DECISIONS
        },
        "affected_candidate_ids": STRICT_CANDIDATE_IDS,
        "gate_rows": rows,
        "gate_by_candidate": {
            candidate_id: [decision.as_row() for decision in decisions]
            for candidate_id, decisions in by_candidate.items()
        },
        "intake_ready_count": 0,
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def decisions_for_candidate(candidate_id: str) -> tuple[RuleFamilyDecision, ...]:
    decisions = tuple(
        decision for decision in _DECISIONS if candidate_id in decision.affected_candidate_ids
    )
    if not decisions:
        raise KeyError(f"no rule-family decisions for {candidate_id}")
    return decisions


def candidate_rule_gate_status(candidate_id: str) -> str:
    if candidate_id in OUTSIDE_NARROWED_PATH_CANDIDATE_IDS:
        return "outside_narrowed_path"
    decisions = decisions_for_candidate(candidate_id)
    if all(decision.hard_decision in PROMOTING_DECISIONS for decision in decisions):
        return "pass"
    return "blocked"


def candidate_cfb_source_data_insufficiency_reason(candidate_id: str) -> str:
    if candidate_id not in CLEAN_FAST_BREAK_SOURCE_DATA_INSUFFICIENT_CANDIDATE_IDS:
        raise ValueError(f"{candidate_id} is not a Clean Fast Break insufficiency row")
    return CFB_SOURCE_DATA_INSUFFICIENT_REASONS[candidate_id]


def candidate_is_outside_narrowed_path(candidate_id: str) -> bool:
    decisions_for_candidate(candidate_id)
    return candidate_id in OUTSIDE_NARROWED_PATH_CANDIDATE_IDS


def candidate_outside_narrowed_path_reason(candidate_id: str) -> str:
    if not candidate_is_outside_narrowed_path(candidate_id):
        raise ValueError(f"{candidate_id} is not outside the narrowed path")
    return OUTSIDE_NARROWED_PATH_REASONS[candidate_id]


def candidate_can_promote(
    candidate_id: str,
    *,
    final_verdict: object = None,
    primary_blocker: object = None,
    complete_context_caution_review: bool = False,
) -> bool:
    """Return whether hard rule decisions permit intake-ready promotion."""

    if str(final_verdict).strip().upper() == "TRADE" and not complete_context_caution_review:
        return False
    if _primary_blocker_is_nullish(primary_blocker) and not complete_context_caution_review:
        return False
    return candidate_rule_gate_status(candidate_id) == "pass"


def format_rule_gate_report(result: dict[str, object]) -> str:
    lines = [
        f"rule families checked: {result['rule_families_checked']}",
        f"source-backed clean decision count: {result['source_backed_rule_count']}",
        f"blocking decision count: {result['missing_unresolved_rule_count']}",
        f"intake-ready count: {result['intake_ready_count']}",
        f"affected candidate IDs: {', '.join(result['affected_candidate_ids'])}",
        "hard decision table:",
    ]
    for row in result["gate_rows"]:
        lines.append(
            " | ".join(
                (
                    str(row["rule_family"]),
                    f"decision={row['hard_decision']}",
                    f"setup_type={row['setup_type']}",
                    f"scope={row['symbol_or_scope']}",
                    f"affected={', '.join(row['affected_candidate_ids'])}",
                    f"promotion={row['intake_ready_effect']}",
                    f"next_action={row['smallest_next_action']}",
                    f"blocks_proof_review={'YES' if row['blocks_proof_review'] else 'NO'}",
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


def _decisions_by_candidate(
    decisions: Iterable[RuleFamilyDecision],
) -> Mapping[str, tuple[RuleFamilyDecision, ...]]:
    by_candidate: dict[str, list[RuleFamilyDecision]] = {
        candidate_id: [] for candidate_id in STRICT_CANDIDATE_IDS
    }
    for decision in decisions:
        if decision.hard_decision not in HARD_DECISIONS:
            raise ValueError(f"unsupported hard_decision: {decision.hard_decision}")
        for candidate_id in decision.affected_candidate_ids:
            by_candidate[candidate_id].append(decision)
    return {
        candidate_id: tuple(candidate_decisions)
        for candidate_id, candidate_decisions in by_candidate.items()
    }


def _primary_blocker_is_nullish(value: object) -> bool:
    if value is None:
        return True
    return str(value).strip().lower() in {"", "none", "null"}


def main() -> None:
    print(format_rule_gate_report(build_rule_gate_result()))


if __name__ == "__main__":
    main()
