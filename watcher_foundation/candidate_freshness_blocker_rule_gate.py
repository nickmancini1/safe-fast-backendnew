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


@dataclass(frozen=True)
class SurvivalMapRow:
    candidate_id: str
    symbol: str
    setup_type: str
    current_status: str
    blocking_rule_family: str
    rule_decision_applied: str
    exact_reason: str
    next_evidence_fix: str
    proof_allowed: bool

    def as_row(self) -> dict[str, object]:
        return {
            "candidate_id": self.candidate_id,
            "symbol": self.symbol,
            "setup_type": self.setup_type,
            "current_status": self.current_status,
            "blocking_rule_family": self.blocking_rule_family,
            "rule_decision_applied": self.rule_decision_applied,
            "exact_reason": self.exact_reason,
            "next_evidence_fix": self.next_evidence_fix,
            "proof_allowed": self.proof_allowed,
        }


@dataclass(frozen=True)
class ActivePathEvidenceRequirement:
    candidate_id: str
    symbol: str
    setup_type: str
    exact_missing_rule_or_evidence: str
    required_source_field_or_log_evidence: str
    source_file_or_doc: str
    current_repo_has_enough_data: bool
    decision_if_missing: str
    smallest_next_action: str
    proof_allowed: bool

    def as_row(self) -> dict[str, object]:
        return {
            "candidate_id": self.candidate_id,
            "symbol": self.symbol,
            "setup_type": self.setup_type,
            "exact_missing_rule_or_evidence": self.exact_missing_rule_or_evidence,
            "required_source_field_or_log_evidence": self.required_source_field_or_log_evidence,
            "source_file_or_doc": self.source_file_or_doc,
            "current_repo_has_enough_data": self.current_repo_has_enough_data,
            "decision_if_missing": self.decision_if_missing,
            "smallest_next_action": self.smallest_next_action,
            "proof_allowed": self.proof_allowed,
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

QQQ_CFB_CANDIDATE_ID = "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"
SPY_CFB_003_CANDIDATE_ID = "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003"
SPY_CFB_002_CANDIDATE_ID = "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002"
SPY_IDEAL_CANDIDATE_ID = "SPY-REAL-HISTORICAL-IDEAL-001"

_CFB_IDS = (
    QQQ_CFB_CANDIDATE_ID,
    SPY_CFB_003_CANDIDATE_ID,
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
    "SPY-REAL-HISTORICAL-CONTINUATION-001",
)

CLEAN_FAST_BREAK_SOURCE_DATA_INSUFFICIENT_CANDIDATE_IDS = _CFB_IDS

QQQ_CFB_SURVIVAL_ACTION_APPLIED = True
QQQ_CFB_SURVIVAL_STATUS = "active_blocked"
QQQ_CFB_EXACT_MISSING_EVIDENCE = (
    "source-backed QQQ gap-context completeness field/rule",
    "tested Clean Fast Break stale/spent expiry rule",
    "complete source-backed context/caution review fields",
)
QQQ_CFB_CLEAN_RULE_EVIDENCE = ()

SPY_CFB_003_SURVIVAL_ACTION_APPLIED = True
SPY_CFB_003_SURVIVAL_STATUS = "active_blocked"
SPY_CFB_003_EXACT_MISSING_EVIDENCE = (
    "tested Clean Fast Break higher-base/fresh-break expiry rule",
    "complete source-backed context/caution review fields",
)
SPY_CFB_003_CLEAN_RULE_EVIDENCE = ()

SPY_CFB_002_SURVIVAL_ACTION_APPLIED = True
SPY_CFB_002_SURVIVAL_STATUS = "active_blocked"
SPY_CFB_002_EXACT_MISSING_EVIDENCE = (
    "tested Clean Fast Break initial-break expiry rule",
    "complete source-backed context/caution review fields",
)
SPY_CFB_002_CLEAN_RULE_EVIDENCE = ()

SPY_IDEAL_SURVIVAL_ACTION_APPLIED = True
SPY_IDEAL_SURVIVAL_STATUS = "active_blocked"
SPY_IDEAL_EXACT_MISSING_EVIDENCE = (
    "tested SPY Ideal stale/spent expiry rule",
    "complete source-backed context/caution review fields",
)
SPY_IDEAL_CLEAN_RULE_EVIDENCE = ()

ACTIVE_BLOCKED_CANDIDATE_IDS = (
    QQQ_CFB_CANDIDATE_ID,
    SPY_CFB_003_CANDIDATE_ID,
    SPY_CFB_002_CANDIDATE_ID,
    SPY_IDEAL_CANDIDATE_ID,
)

CFB_SOURCE_DATA_INSUFFICIENT_REASONS = {
    "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001": (
        "blocked by QQQ gap-context source-data insufficiency, Clean Fast Break "
        "expiry source-data insufficiency, and complete context/caution "
        "source-data insufficiency"
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

CONTEXT_CAUTION_SOURCE_DATA_INSUFFICIENT_CANDIDATE_IDS = STRICT_CANDIDATE_IDS

ACTIVE_CONTEXT_CAUTION_BLOCKED_CANDIDATE_IDS = (
    "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003",
    "SPY-REAL-HISTORICAL-IDEAL-001",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
)

CONTEXT_CAUTION_SOURCE_DATA_INSUFFICIENT_REASONS = {
    "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001": (
        "blocked by complete context/caution source-data insufficiency; "
        "primary blocker null does not prove gap, room, 24H, macro, IV, event, "
        "option, headline, or execution context is complete"
    ),
    "QQQ-REAL-HISTORICAL-CONTINUATION-001": (
        "outside narrowed Continuation path and also lacks complete context/caution "
        "source data"
    ),
    "QQQ-REAL-HISTORICAL-IDEAL-001": (
        "outside narrowed Ideal path and also lacks complete context/caution source data"
    ),
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003": (
        "blocked by complete context/caution source-data insufficiency; "
        "primary blocker null does not prove 24H, macro, IV, event, room, "
        "option, headline, or execution context is complete"
    ),
    "SPY-REAL-HISTORICAL-CONTINUATION-001": (
        "outside narrowed Continuation path and also lacks complete context/caution "
        "source data"
    ),
    "SPY-REAL-HISTORICAL-IDEAL-001": (
        "blocked by complete context/caution source-data insufficiency; "
        "primary blocker null does not prove gap, headline, room, 24H, macro, IV, "
        "event, option, or execution context is complete"
    ),
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002": (
        "blocked by complete context/caution source-data insufficiency; "
        "primary blocker null does not prove 24H, macro, IV, event, room, "
        "option, headline, or execution context is complete"
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
    "SPY-REAL-HISTORICAL-CONTINUATION-001": (
        "outside narrowed Continuation path; intrabar order-of-events inside completed "
        "1H candles remains unsupported without lower-timeframe evidence"
    ),
}

_ACTIVE_PATH_EVIDENCE_REQUIREMENTS: tuple[ActivePathEvidenceRequirement, ...] = (
    ActivePathEvidenceRequirement(
        candidate_id=QQQ_CFB_CANDIDATE_ID,
        symbol="QQQ",
        setup_type="Clean Fast Break",
        exact_missing_rule_or_evidence="source-backed QQQ gap-context completeness field/rule",
        required_source_field_or_log_evidence=(
            "setup-time gap_context completeness field, or replay-log evidence proving gap "
            "context was reviewed before the signal"
        ),
        source_file_or_doc=(
            "historical_signal_replay/source_data/incoming/"
            "first_real_historical_replay_v1_QQQ_source.csv; "
            "historical_signal_replay/reports/"
            "first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl"
        ),
        current_repo_has_enough_data=False,
        decision_if_missing="repair-source",
        smallest_next_action=(
            "Add source-backed QQQ gap-context completeness evidence before any QQQ Clean "
            "Fast Break proof review."
        ),
        proof_allowed=False,
    ),
    ActivePathEvidenceRequirement(
        candidate_id=QQQ_CFB_CANDIDATE_ID,
        symbol="QQQ",
        setup_type="Clean Fast Break",
        exact_missing_rule_or_evidence="tested Clean Fast Break stale/spent expiry rule",
        required_source_field_or_log_evidence=(
            "accepted setup-time expiry rule plus regression rows distinguishing fresh, "
            "stale, and spent Clean Fast Break signals"
        ),
        source_file_or_doc=(
            "SAFE_FAST_RULE_FAMILY_DECISION_TABLE.md; "
            "historical_signal_replay/reports/"
            "first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl; "
            "tests/test_candidate_freshness_blocker_rule_gate.py"
        ),
        current_repo_has_enough_data=False,
        decision_if_missing="add-validator",
        smallest_next_action=(
            "Define and regression-test Clean Fast Break stale/spent expiry before promotion."
        ),
        proof_allowed=False,
    ),
    ActivePathEvidenceRequirement(
        candidate_id=QQQ_CFB_CANDIDATE_ID,
        symbol="QQQ",
        setup_type="Clean Fast Break",
        exact_missing_rule_or_evidence="complete source-backed context/caution review fields",
        required_source_field_or_log_evidence=(
            "complete 24H, macro, IV, event, room, option, headline, execution, and caution "
            "review fields at setup time"
        ),
        source_file_or_doc=(
            "historical_signal_replay/source_data/incoming/"
            "first_real_historical_replay_v1_QQQ_source.csv; "
            "SAFE_FAST_ARCHITECT_CONTROL_AND_PROJECT_TIGHTENING.md"
        ),
        current_repo_has_enough_data=False,
        decision_if_missing="repair-source",
        smallest_next_action=(
            "Add complete source-backed context/caution fields; primary blocker null is not enough."
        ),
        proof_allowed=False,
    ),
    ActivePathEvidenceRequirement(
        candidate_id=SPY_CFB_003_CANDIDATE_ID,
        symbol="SPY",
        setup_type="Clean Fast Break",
        exact_missing_rule_or_evidence="tested Clean Fast Break higher-base/fresh-break expiry rule",
        required_source_field_or_log_evidence=(
            "accepted setup-time expiry rule covering higher-base/fresh-break signals, with "
            "line 5 fresh signal and line 6 later spent lifecycle treated as regression evidence"
        ),
        source_file_or_doc=(
            "historical_signal_replay/reports/"
            "third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl; "
            "historical_signal_replay/source_data/incoming/"
            "first_real_historical_replay_v1_SPY_source.csv; "
            "tests/test_candidate_freshness_blocker_rule_gate.py"
        ),
        current_repo_has_enough_data=False,
        decision_if_missing="add-validator",
        smallest_next_action=(
            "Define and regression-test higher-base/fresh-break expiry before promotion."
        ),
        proof_allowed=False,
    ),
    ActivePathEvidenceRequirement(
        candidate_id=SPY_CFB_003_CANDIDATE_ID,
        symbol="SPY",
        setup_type="Clean Fast Break",
        exact_missing_rule_or_evidence="complete source-backed context/caution review fields",
        required_source_field_or_log_evidence=(
            "complete 24H, macro, IV, event, room, option, headline, execution, and caution "
            "review fields for the 2026-04-15 14:30 setup-time row"
        ),
        source_file_or_doc=(
            "historical_signal_replay/source_data/incoming/"
            "first_real_historical_replay_v1_SPY_source.csv line 154; "
            "historical_signal_replay/reports/"
            "third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl line 5"
        ),
        current_repo_has_enough_data=False,
        decision_if_missing="repair-source",
        smallest_next_action=(
            "Repair source/context fields for the 2026-04-15 14:30 setup-time row."
        ),
        proof_allowed=False,
    ),
    ActivePathEvidenceRequirement(
        candidate_id=SPY_CFB_002_CANDIDATE_ID,
        symbol="SPY",
        setup_type="Clean Fast Break",
        exact_missing_rule_or_evidence="tested Clean Fast Break initial-break expiry rule",
        required_source_field_or_log_evidence=(
            "accepted setup-time expiry rule covering initial-break signals, with line 2 "
            "signal-stage and line 3 follow-through/spent lifecycle treated as regression evidence"
        ),
        source_file_or_doc=(
            "historical_signal_replay/reports/"
            "third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl; "
            "historical_signal_replay/source_data/incoming/"
            "first_real_historical_replay_v1_SPY_source.csv line 138; "
            "tests/test_candidate_freshness_blocker_rule_gate.py"
        ),
        current_repo_has_enough_data=False,
        decision_if_missing="add-validator",
        smallest_next_action=(
            "Define and regression-test Clean Fast Break initial-break expiry before promotion."
        ),
        proof_allowed=False,
    ),
    ActivePathEvidenceRequirement(
        candidate_id=SPY_CFB_002_CANDIDATE_ID,
        symbol="SPY",
        setup_type="Clean Fast Break",
        exact_missing_rule_or_evidence="complete source-backed context/caution review fields",
        required_source_field_or_log_evidence=(
            "complete 24H, macro, IV, event, room, option, headline, execution, and caution "
            "review fields for the 2026-04-13 12:30 setup-time row"
        ),
        source_file_or_doc=(
            "historical_signal_replay/source_data/incoming/"
            "first_real_historical_replay_v1_SPY_source.csv line 138; "
            "historical_signal_replay/reports/"
            "third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl line 2"
        ),
        current_repo_has_enough_data=False,
        decision_if_missing="repair-source",
        smallest_next_action=(
            "Repair source/context fields for the 2026-04-13 12:30 setup-time row."
        ),
        proof_allowed=False,
    ),
    ActivePathEvidenceRequirement(
        candidate_id=SPY_IDEAL_CANDIDATE_ID,
        symbol="SPY",
        setup_type="Ideal",
        exact_missing_rule_or_evidence="tested SPY Ideal stale/spent expiry rule",
        required_source_field_or_log_evidence=(
            "accepted setup-time stale/spent expiry rule covering same-session SPY Ideal, "
            "with line 5 triggered signal and line 6 later spent lifecycle as regression evidence"
        ),
        source_file_or_doc=(
            "historical_signal_replay/reports/"
            "second_real_spy_ideal_replay_v1_signal_log.jsonl; "
            "historical_signal_replay/source_data/incoming/"
            "first_real_historical_replay_v1_SPY_source.csv line 291; "
            "tests/test_candidate_freshness_blocker_rule_gate.py"
        ),
        current_repo_has_enough_data=False,
        decision_if_missing="add-validator",
        smallest_next_action=(
            "Define and regression-test SPY Ideal stale/spent expiry before promotion."
        ),
        proof_allowed=False,
    ),
    ActivePathEvidenceRequirement(
        candidate_id=SPY_IDEAL_CANDIDATE_ID,
        symbol="SPY",
        setup_type="Ideal",
        exact_missing_rule_or_evidence="complete source-backed context/caution review fields",
        required_source_field_or_log_evidence=(
            "complete gap, headline, room, 24H, macro, IV, event, option, execution, and "
            "caution review fields for the 2026-05-13 11:30 setup-time row"
        ),
        source_file_or_doc=(
            "historical_signal_replay/source_data/incoming/"
            "first_real_historical_replay_v1_SPY_source.csv line 291; "
            "historical_signal_replay/reports/"
            "second_real_spy_ideal_replay_v1_signal_log.jsonl line 5"
        ),
        current_repo_has_enough_data=False,
        decision_if_missing="repair-source",
        smallest_next_action=(
            "Repair source/context fields for the 2026-05-13 11:30 Ideal setup-time row."
        ),
        proof_allowed=False,
    ),
)

_SURVIVAL_MAP_ROWS: tuple[SurvivalMapRow, ...] = (
    SurvivalMapRow(
        candidate_id="QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
        symbol="QQQ",
        setup_type="Clean Fast Break",
        current_status="active_blocked",
        blocking_rule_family=(
            "Clean Fast Break expiry; Clean Fast Break gap context; Context/caution review"
        ),
        rule_decision_applied=(
            "SOURCE_DATA_INSUFFICIENT; SOURCE_DATA_INSUFFICIENT; SOURCE_DATA_INSUFFICIENT"
        ),
        exact_reason=(
            "Applied survival action: active_blocked. QQQ gap-context, Clean Fast "
            "Break expiry, and complete context/caution source-backed evidence are "
            "insufficient; final_verdict TRADE and primary blocker null cannot promote."
        ),
        next_evidence_fix=(
            "Add source-backed QQQ gap-context evidence, define a tested Clean Fast Break expiry "
            "rule, and add complete context/caution review fields before proof review."
        ),
        proof_allowed=False,
    ),
    SurvivalMapRow(
        candidate_id="QQQ-REAL-HISTORICAL-CONTINUATION-001",
        symbol="QQQ",
        setup_type="Continuation",
        current_status="replace",
        blocking_rule_family=(
            "Continuation next-session freshness; Continuation session-boundary freshness; "
            "Context/caution review"
        ),
        rule_decision_applied=(
            "KILL_OR_NARROW_SETUP_SYMBOL_PATH; KILL_OR_NARROW_SETUP_SYMBOL_PATH; "
            "SOURCE_DATA_INSUFFICIENT"
        ),
        exact_reason=(
            "Next-session/session-boundary carry-forward freshness is outside the narrowed "
            "Continuation path and complete context/caution evidence is still insufficient."
        ),
        next_evidence_fix=(
            "Replace with same-session Continuation evidence or source and regression-test a "
            "next-session/session-boundary carry-forward rule plus complete context/caution fields."
        ),
        proof_allowed=False,
    ),
    SurvivalMapRow(
        candidate_id="QQQ-REAL-HISTORICAL-IDEAL-001",
        symbol="QQQ",
        setup_type="Ideal",
        current_status="replace",
        blocking_rule_family=(
            "Ideal stale/spent expiry; Ideal fast-swing freshness; Wide-risk / room threshold; "
            "Context/caution review"
        ),
        rule_decision_applied=(
            "SOURCE_DATA_INSUFFICIENT; KILL_OR_NARROW_SETUP_SYMBOL_PATH; "
            "KILL_OR_NARROW_SETUP_SYMBOL_PATH; SOURCE_DATA_INSUFFICIENT"
        ),
        exact_reason=(
            "Fast-swing/wide-risk Ideal is outside the narrowed Ideal path; stale/spent expiry, "
            "room/risk threshold, and complete context/caution evidence are not source-backed."
        ),
        next_evidence_fix=(
            "Replace with Ideal evidence inside the narrowed path or source and regression-test "
            "fast-swing freshness, stale/spent expiry, room/risk thresholds, and complete "
            "context/caution fields."
        ),
        proof_allowed=False,
    ),
    SurvivalMapRow(
        candidate_id="SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003",
        symbol="SPY",
        setup_type="Clean Fast Break",
        current_status="active_blocked",
        blocking_rule_family="Clean Fast Break expiry; Context/caution review",
        rule_decision_applied="SOURCE_DATA_INSUFFICIENT; SOURCE_DATA_INSUFFICIENT",
        exact_reason=(
            "Clean Fast Break higher-base/fresh-break expiry is not source-backed and complete "
            "context/caution review remains insufficient."
        ),
        next_evidence_fix=(
            "Define and regression-test Clean Fast Break higher-base/fresh-break expiry and add "
            "complete context/caution review fields before proof review."
        ),
        proof_allowed=False,
    ),
    SurvivalMapRow(
        candidate_id="SPY-REAL-HISTORICAL-CONTINUATION-001",
        symbol="SPY",
        setup_type="Continuation",
        current_status="replace",
        blocking_rule_family=(
            "Continuation session-boundary freshness; Intrabar ordering; Context/caution review"
        ),
        rule_decision_applied=(
            "KILL_OR_NARROW_SETUP_SYMBOL_PATH; KILL_OR_NARROW_SETUP_SYMBOL_PATH; "
            "SOURCE_DATA_INSUFFICIENT"
        ),
        exact_reason=(
            "Intrabar order-of-events inside completed 1H candles cannot be proven from current "
            "source rows, so this Continuation row is outside the narrowed path; complete "
            "context/caution evidence is also insufficient."
        ),
        next_evidence_fix=(
            "Replace with lower-timeframe/order-of-events evidence or exclude intrabar-dependent "
            "Continuation rows from proof review; add complete context/caution fields if restored."
        ),
        proof_allowed=False,
    ),
    SurvivalMapRow(
        candidate_id="SPY-REAL-HISTORICAL-IDEAL-001",
        symbol="SPY",
        setup_type="Ideal",
        current_status="active_blocked",
        blocking_rule_family="Ideal stale/spent expiry; Context/caution review",
        rule_decision_applied="SOURCE_DATA_INSUFFICIENT; SOURCE_DATA_INSUFFICIENT",
        exact_reason=(
            "Applied survival action: active_blocked. Same-session Ideal has a triggered "
            "signal-stage row and later spent lifecycle row, but no tested SPY Ideal "
            "stale/spent expiry rule and no complete source-backed context/caution review; "
            "primary blocker null cannot promote."
        ),
        next_evidence_fix=(
            "Define and regression-test SPY Ideal stale/spent expiry and add complete "
            "context/caution review fields before proof review."
        ),
        proof_allowed=False,
    ),
    SurvivalMapRow(
        candidate_id="SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
        symbol="SPY",
        setup_type="Clean Fast Break",
        current_status="active_blocked",
        blocking_rule_family="Clean Fast Break expiry; Context/caution review",
        rule_decision_applied="SOURCE_DATA_INSUFFICIENT; SOURCE_DATA_INSUFFICIENT",
        exact_reason=(
            "Clean Fast Break initial-break expiry is not source-backed and complete "
            "context/caution review remains insufficient."
        ),
        next_evidence_fix=(
            "Define and regression-test Clean Fast Break initial-break expiry and add complete "
            "context/caution review fields before proof review."
        ),
        proof_allowed=False,
    ),
)


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
        intake_ready_effect=(
            "SPY Continuation intrabar-dependent rows are outside the narrowed path and cannot "
            "become intake-ready under current repo evidence."
        ),
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
    survival = build_survival_map()
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
        "survival_map_rows": survival["survival_map_rows"],
        "survival_status_by_candidate": survival["status_by_candidate"],
        "survival_active_blocked_count": survival["active_blocked_count"],
        "survival_replace_count": survival["replace_count"],
        "survival_parked_count": survival["parked_count"],
        "survival_intake_ready_count": survival["intake_ready_count"],
        "active_path_evidence_requirements": build_active_path_evidence_requirements(),
        "qqq_cfb_survival_action": qqq_cfb_survival_action(),
        "spy_cfb_003_survival_action": spy_cfb_003_survival_action(),
        "spy_cfb_002_survival_action": spy_cfb_002_survival_action(),
        "spy_ideal_survival_action": spy_ideal_survival_action(),
        "intake_ready_count": 0,
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def build_active_path_evidence_requirements() -> dict[str, object]:
    rows = [requirement.as_row() for requirement in _ACTIVE_PATH_EVIDENCE_REQUIREMENTS]
    covered_ids = tuple(
        candidate_id
        for candidate_id in ACTIVE_BLOCKED_CANDIDATE_IDS
        if any(row["candidate_id"] == candidate_id for row in rows)
    )
    return {
        "requirements_rows": rows,
        "active_blocked_candidate_ids": ACTIVE_BLOCKED_CANDIDATE_IDS,
        "covered_candidate_ids": covered_ids,
        "covered_count": len(covered_ids),
        "requirements_count": len(rows),
        "current_repo_has_enough_data_by_candidate": {
            candidate_id: all(
                bool(row["current_repo_has_enough_data"])
                for row in rows
                if row["candidate_id"] == candidate_id
            )
            for candidate_id in ACTIVE_BLOCKED_CANDIDATE_IDS
        },
        "proof_allowed_by_candidate": {
            candidate_id: any(
                bool(row["proof_allowed"]) for row in rows if row["candidate_id"] == candidate_id
            )
            for candidate_id in ACTIVE_BLOCKED_CANDIDATE_IDS
        },
        "proof_allowed_count": sum(1 for row in rows if row["proof_allowed"]),
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def build_survival_map() -> dict[str, object]:
    rows = [row.as_row() for row in _SURVIVAL_MAP_ROWS]
    status_counts = {
        status: sum(1 for row in rows if row["current_status"] == status)
        for status in ("active_blocked", "replace", "parked", "intake_ready")
    }
    return {
        "survival_map_rows": rows,
        "status_by_candidate": {
            str(row["candidate_id"]): str(row["current_status"]) for row in rows
        },
        "active_blocked_count": status_counts["active_blocked"],
        "replace_count": status_counts["replace"],
        "parked_count": status_counts["parked"],
        "intake_ready_count": status_counts["intake_ready"],
        "proof_allowed_count": sum(1 for row in rows if row["proof_allowed"]),
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


def candidate_survival_status(candidate_id: str) -> str:
    survival_map = build_survival_map()
    try:
        return str(survival_map["status_by_candidate"][candidate_id])
    except KeyError as exc:
        raise KeyError(f"no survival-map status for {candidate_id}") from exc


def active_path_requirements_for_candidate(
    candidate_id: str,
) -> tuple[ActivePathEvidenceRequirement, ...]:
    requirements = tuple(
        requirement
        for requirement in _ACTIVE_PATH_EVIDENCE_REQUIREMENTS
        if requirement.candidate_id == candidate_id
    )
    if not requirements:
        raise KeyError(f"no active-path evidence requirements for {candidate_id}")
    return requirements


def qqq_cfb_survival_action() -> dict[str, object]:
    return {
        "candidate_id": QQQ_CFB_CANDIDATE_ID,
        "action_applied": QQQ_CFB_SURVIVAL_ACTION_APPLIED,
        "status": candidate_survival_status(QQQ_CFB_CANDIDATE_ID),
        "exact_missing_evidence": QQQ_CFB_EXACT_MISSING_EVIDENCE,
        "clean_rule_evidence": QQQ_CFB_CLEAN_RULE_EVIDENCE,
        "proof_allowed": False,
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def spy_cfb_003_survival_action() -> dict[str, object]:
    return {
        "candidate_id": SPY_CFB_003_CANDIDATE_ID,
        "action_applied": SPY_CFB_003_SURVIVAL_ACTION_APPLIED,
        "status": candidate_survival_status(SPY_CFB_003_CANDIDATE_ID),
        "exact_missing_evidence": SPY_CFB_003_EXACT_MISSING_EVIDENCE,
        "clean_rule_evidence": SPY_CFB_003_CLEAN_RULE_EVIDENCE,
        "proof_allowed": False,
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def spy_cfb_002_survival_action() -> dict[str, object]:
    return {
        "candidate_id": SPY_CFB_002_CANDIDATE_ID,
        "action_applied": SPY_CFB_002_SURVIVAL_ACTION_APPLIED,
        "status": candidate_survival_status(SPY_CFB_002_CANDIDATE_ID),
        "exact_missing_evidence": SPY_CFB_002_EXACT_MISSING_EVIDENCE,
        "clean_rule_evidence": SPY_CFB_002_CLEAN_RULE_EVIDENCE,
        "proof_allowed": False,
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def spy_ideal_survival_action() -> dict[str, object]:
    return {
        "candidate_id": SPY_IDEAL_CANDIDATE_ID,
        "action_applied": SPY_IDEAL_SURVIVAL_ACTION_APPLIED,
        "status": candidate_survival_status(SPY_IDEAL_CANDIDATE_ID),
        "exact_missing_evidence": SPY_IDEAL_EXACT_MISSING_EVIDENCE,
        "clean_rule_evidence": SPY_IDEAL_CLEAN_RULE_EVIDENCE,
        "proof_allowed": False,
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def candidate_cfb_source_data_insufficiency_reason(candidate_id: str) -> str:
    if candidate_id not in CLEAN_FAST_BREAK_SOURCE_DATA_INSUFFICIENT_CANDIDATE_IDS:
        raise ValueError(f"{candidate_id} is not a Clean Fast Break insufficiency row")
    return CFB_SOURCE_DATA_INSUFFICIENT_REASONS[candidate_id]


def candidate_context_caution_source_data_insufficiency_reason(candidate_id: str) -> str:
    if candidate_id not in CONTEXT_CAUTION_SOURCE_DATA_INSUFFICIENT_CANDIDATE_IDS:
        raise ValueError(f"{candidate_id} is not a context/caution insufficiency row")
    return CONTEXT_CAUTION_SOURCE_DATA_INSUFFICIENT_REASONS[candidate_id]


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
    lines.append("survival summary:")
    for row in result["survival_map_rows"]:
        lines.append(
            " | ".join(
                (
                    str(row["candidate_id"]),
                    f"symbol={row['symbol']}",
                    f"setup_type={row['setup_type']}",
                    f"status={row['current_status']}",
                    f"blocking_rule_family={row['blocking_rule_family']}",
                    f"rule_decision_applied={row['rule_decision_applied']}",
                    f"reason={row['exact_reason']}",
                    f"next_evidence_fix={row['next_evidence_fix']}",
                    f"proof_allowed={'YES' if row['proof_allowed'] else 'NO'}",
                )
            )
        )
    requirements = result["active_path_evidence_requirements"]
    lines.append("active-path evidence requirements:")
    for row in requirements["requirements_rows"]:
        lines.append(
            " | ".join(
                (
                    str(row["candidate_id"]),
                    f"symbol={row['symbol']}",
                    f"setup_type={row['setup_type']}",
                    f"missing={row['exact_missing_rule_or_evidence']}",
                    f"required_evidence={row['required_source_field_or_log_evidence']}",
                    f"source={row['source_file_or_doc']}",
                    (
                        "current_repo_has_enough_data="
                        f"{'YES' if row['current_repo_has_enough_data'] else 'NO'}"
                    ),
                    f"decision_if_missing={row['decision_if_missing']}",
                    f"smallest_next_action={row['smallest_next_action']}",
                    f"proof_allowed={'YES' if row['proof_allowed'] else 'NO'}",
                )
            )
        )
    lines.extend(
        (
            f"active_blocked count: {result['survival_active_blocked_count']}",
            f"replace count: {result['survival_replace_count']}",
            f"parked count: {result['survival_parked_count']}",
            f"survival intake-ready count: {result['survival_intake_ready_count']}",
            (
                "QQQ CFB survival action applied: "
                f"{'YES' if result['qqq_cfb_survival_action']['action_applied'] else 'NO'}"
            ),
            f"QQQ CFB status: {result['qqq_cfb_survival_action']['status']}",
            (
                "QQQ CFB exact missing evidence: "
                + "; ".join(result["qqq_cfb_survival_action"]["exact_missing_evidence"])
            ),
            (
                "SPY CFB 003 survival action applied: "
                f"{'YES' if result['spy_cfb_003_survival_action']['action_applied'] else 'NO'}"
            ),
            f"SPY CFB 003 status: {result['spy_cfb_003_survival_action']['status']}",
            (
                "SPY CFB 003 exact missing evidence: "
                + "; ".join(result["spy_cfb_003_survival_action"]["exact_missing_evidence"])
            ),
            (
                "SPY CFB 002 survival action applied: "
                f"{'YES' if result['spy_cfb_002_survival_action']['action_applied'] else 'NO'}"
            ),
            f"SPY CFB 002 status: {result['spy_cfb_002_survival_action']['status']}",
            (
                "SPY CFB 002 exact missing evidence: "
                + "; ".join(result["spy_cfb_002_survival_action"]["exact_missing_evidence"])
            ),
            (
                "SPY Ideal survival action applied: "
                f"{'YES' if result['spy_ideal_survival_action']['action_applied'] else 'NO'}"
            ),
            f"SPY Ideal status: {result['spy_ideal_survival_action']['status']}",
            (
                "SPY Ideal exact missing evidence: "
                + "; ".join(result["spy_ideal_survival_action"]["exact_missing_evidence"])
            ),
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
