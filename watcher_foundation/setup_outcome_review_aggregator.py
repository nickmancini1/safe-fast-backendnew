"""Local-only setup outcome proof review aggregation.

This module accepts caller-provided in-memory setup outcome packet readiness
summaries only and returns one in-memory aggregate review summary. It does not
fetch data, write files, start shadow/live workflows, emit alerts, call
subprocesses, touch brokers/accounts/options/P&L, optimize rules, or make trade
decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.setup_outcome_packet_readiness import (
    SETUP_OUTCOME_PACKET_READINESS_RESULT_FIELDS,
)
from watcher_foundation.setup_outcome_proof import (
    FORBIDDEN_SETUP_OUTCOME_FIELD_NAMES,
)


SETUP_OUTCOME_REVIEW_AGGREGATOR_DECISIONS = (
    "continue_review_with_ready_packets",
    "needs_more_evidence_before_review",
    "blocked_by_readiness_contract_gap",
)

SETUP_OUTCOME_REVIEW_AGGREGATOR_RESULT_FIELDS = (
    "watch_only",
    "setup_outcome_review_aggregator_only",
    "setup_outcome_packet_readiness_only",
    "setup_outcome_evidence_packet_only",
    "setup_outcome_diagnostics_only",
    "setup_outcome_proof_only",
    "final_viability_proven",
    "optimization_started",
    "no_rule_change_started",
    "packet_summary_count",
    "reviewed_packets",
    "represented_setup_types",
    "represented_symbols",
    "represented_setup_type_symbol_pairs",
    "outcome_groups",
    "readiness_gap_counts",
    "repeated_readiness_gaps",
    "repeated_next_fix_paths",
    "repeated_regression_needs",
    "regression_needed",
    "proof_gaps",
    "missing_evidence",
    "lower_tier_handoff_required",
    "lower_tier_handoff_items",
    "rejected_records",
    "proof_limited_records",
    "setup_type_separated",
    "symbol_separated",
    "sufficient_proof_to_continue_review",
    "proof_continuation_decision",
    "no_hindsight_boundary_preserved",
    "no_trade_boundary_preserved",
    "no_live_data_boundary_preserved",
    "no_controlled_shadow_boundary_preserved",
    "no_alert_boundary_preserved",
    "no_file_write_boundary_preserved",
    "no_broker_boundary_preserved",
    "no_optimization_boundary_preserved",
    "no_trade_or_optimization_boundary_preserved",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

SETUP_OUTCOME_REVIEW_OUTCOME_GROUPS = (
    "worked",
    "failed",
    "inconclusive",
    "pending",
    "stale",
    "invalidated",
    "missing_evidence",
)

_EXPECTED_TRUE_READINESS_FIELDS = (
    "watch_only",
    "setup_outcome_packet_readiness_only",
    "setup_outcome_evidence_packet_only",
    "setup_outcome_diagnostics_only",
    "setup_outcome_proof_only",
    "no_rule_change_started",
    "no_hindsight_boundary_preserved",
    "no_trade_boundary_preserved",
    "no_live_data_boundary_preserved",
    "no_controlled_shadow_boundary_preserved",
    "no_alert_boundary_preserved",
    "no_file_write_boundary_preserved",
    "no_broker_boundary_preserved",
    "no_optimization_boundary_preserved",
    "no_trade_or_optimization_boundary_preserved",
)

_EXPECTED_FALSE_READINESS_FIELDS = (
    "final_viability_proven",
    "optimization_started",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

_GAP_FIX_PATHS = {
    "missing_packet_item_field": "return to setup outcome evidence packet contract before review aggregation",
    "setup_type_separation": "fix setup type identity as a separate packet readiness field",
    "symbol_separation": "fix symbol identity as a separate packet readiness field",
    "setup_symbol_merged": "fix packet grouping so setup type and symbol are not merged",
    "setup_symbol_grouping": "fix packet items_by_setup_type nested setup-type then symbol grouping",
    "missing_evidence": "collect or preserve missing setup outcome packet evidence",
    "unclear_diagnosis": "return to setup outcome diagnostics clarity before broader changes",
    "unclear_next_fix_path": "name the smallest local contract, fixture, test, evidence, or review fix path",
    "missing_regression": "add named regression coverage before broader changes",
    "boundary_gap": "preserve no-hindsight and no-trade packet item boundaries",
    "rejected_proof_records": "return rejected proof records to lower-tier contract or fixture review",
    "proof_limited_records": "return proof-limited records to lower-tier evidence review",
    "lower_tier_handoff_required": "complete lower-tier handoff before broader changes",
    "packet_item_contract": "fix packet readiness item contract before aggregation",
}

_GAP_REGRESSIONS = {
    "missing_packet_item_field": "add regression coverage for required packet item review fields",
    "setup_type_separation": "add regression coverage preserving setup type as its own field",
    "symbol_separation": "add regression coverage preserving symbol as its own field",
    "setup_symbol_merged": "add regression coverage rejecting merged setup type and symbol identity",
    "setup_symbol_grouping": "add regression coverage for nested setup-type then symbol packet grouping",
    "missing_evidence": "add regression coverage carrying missing evidence into packet review",
    "unclear_diagnosis": "add regression coverage requiring evidence-backed diagnosis clarity",
    "unclear_next_fix_path": "add regression coverage requiring named lower-tier next fix paths",
    "missing_regression": "add regression coverage requiring named regression needs",
    "boundary_gap": "add regression coverage preserving no-hindsight and no-trade item boundaries",
    "rejected_proof_records": "add regression coverage preserving rejected proof record handoff",
    "proof_limited_records": "add regression coverage preserving proof-limited record handoff",
    "lower_tier_handoff_required": "add regression coverage preserving lower-tier handoff requirements",
    "packet_item_contract": "add regression coverage for packet item contract gaps",
}


def aggregate_setup_outcome_proof_review(
    readiness_summaries: list[dict[str, Any]],
) -> dict[str, Any]:
    """Return one in-memory aggregate review for packet readiness summaries."""
    if type(readiness_summaries) is not list:
        raise TypeError(
            "Setup outcome review aggregator input must be a list"
        )

    for index, readiness_summary in enumerate(readiness_summaries):
        _validate_readiness_summary(readiness_summary, index)

    reviewed_packets = []
    represented_setup_types: list[str] = []
    represented_symbols: list[str] = []
    represented_pairs = []
    outcome_groups = {group: [] for group in SETUP_OUTCOME_REVIEW_OUTCOME_GROUPS}
    readiness_gap_counts: dict[str, int] = {}
    next_fix_path_counts: dict[str, int] = {}
    regression_counts: dict[str, int] = {}
    proof_gaps = []
    missing_evidence = []
    lower_tier_handoff_items = []
    rejected_records = []
    proof_limited_records = []

    for summary_index, readiness_summary in enumerate(readiness_summaries):
        reviewed_packets.append(_reviewed_packet(summary_index, readiness_summary))
        _extend_unique(
            represented_setup_types,
            _setup_types_from_summary(readiness_summary),
        )
        _extend_unique(
            represented_symbols,
            _symbols_from_summary(readiness_summary),
        )
        _extend_unique(
            represented_pairs,
            _pairs_from_summary(readiness_summary),
        )
        missing_evidence.extend(deepcopy(readiness_summary["missing_evidence"]))
        lower_tier_handoff_items.extend(
            deepcopy(readiness_summary["lower_tier_handoff_items"])
        )
        rejected_records.extend(deepcopy(readiness_summary["rejected_records"]))
        proof_limited_records.extend(deepcopy(readiness_summary["proof_limited_records"]))

        for item in readiness_summary["packet_items"]:
            _group_outcome_item(outcome_groups, summary_index, item, proof_gaps)

        for gap in readiness_summary["readiness_gaps"]:
            gap_type = _gap_type(gap)
            readiness_gap_counts[gap_type] = readiness_gap_counts.get(gap_type, 0) + 1
            fix_path = _GAP_FIX_PATHS.get(
                gap_type,
                f"review lower-tier readiness gap: {gap_type}",
            )
            regression = _GAP_REGRESSIONS.get(
                gap_type,
                f"add regression coverage for readiness gap: {gap_type}",
            )
            next_fix_path_counts[fix_path] = next_fix_path_counts.get(fix_path, 0) + 1
            regression_counts[regression] = regression_counts.get(regression, 0) + 1

        if readiness_summary["readiness_status"] != "ready_for_lower_tier_review":
            proof_gaps.append(
                {
                    "packet_index": summary_index,
                    "gap_type": "packet_not_ready_for_review",
                    "field_name": "readiness_status",
                    "reason": "packet readiness summary is not ready_for_lower_tier_review",
                    "readiness_status": readiness_summary["readiness_status"],
                }
            )

    if not readiness_summaries:
        proof_gaps.append(
            {
                "packet_index": None,
                "gap_type": "no_ready_packets",
                "field_name": "readiness_summaries",
                "reason": "no caller-provided packet readiness summaries were supplied",
            }
        )
    if not represented_setup_types:
        proof_gaps.append(
            _summary_proof_gap("setup_type", "no represented setup types were available")
        )
    if not represented_symbols:
        proof_gaps.append(
            _summary_proof_gap("symbol", "no represented symbols were available")
        )

    lower_tier_handoff_required = bool(
        proof_gaps
        or missing_evidence
        or lower_tier_handoff_items
        or rejected_records
        or proof_limited_records
        or any(
            summary["lower_tier_handoff_required"] is True
            for summary in readiness_summaries
        )
    )
    setup_type_separated = bool(represented_setup_types) and all(
        summary["setup_type_separated"] is True for summary in readiness_summaries
    )
    symbol_separated = bool(represented_symbols) and all(
        summary["symbol_separated"] is True for summary in readiness_summaries
    )
    sufficient = bool(readiness_summaries) and not lower_tier_handoff_required
    decision = _proof_decision(readiness_summaries, proof_gaps, sufficient)

    return {
        "watch_only": True,
        "setup_outcome_review_aggregator_only": True,
        "setup_outcome_packet_readiness_only": True,
        "setup_outcome_evidence_packet_only": True,
        "setup_outcome_diagnostics_only": True,
        "setup_outcome_proof_only": True,
        "final_viability_proven": False,
        "optimization_started": False,
        "no_rule_change_started": True,
        "packet_summary_count": len(readiness_summaries),
        "reviewed_packets": deepcopy(reviewed_packets),
        "represented_setup_types": deepcopy(represented_setup_types),
        "represented_symbols": deepcopy(represented_symbols),
        "represented_setup_type_symbol_pairs": deepcopy(represented_pairs),
        "outcome_groups": deepcopy(outcome_groups),
        "readiness_gap_counts": deepcopy(readiness_gap_counts),
        "repeated_readiness_gaps": _repeated_counts(readiness_gap_counts),
        "repeated_next_fix_paths": _repeated_counts(next_fix_path_counts),
        "repeated_regression_needs": _repeated_counts(regression_counts),
        "regression_needed": list(regression_counts),
        "proof_gaps": deepcopy(proof_gaps),
        "missing_evidence": deepcopy(missing_evidence),
        "lower_tier_handoff_required": lower_tier_handoff_required,
        "lower_tier_handoff_items": deepcopy(lower_tier_handoff_items),
        "rejected_records": deepcopy(rejected_records),
        "proof_limited_records": deepcopy(proof_limited_records),
        "setup_type_separated": setup_type_separated,
        "symbol_separated": symbol_separated,
        "sufficient_proof_to_continue_review": sufficient,
        "proof_continuation_decision": decision,
        "no_hindsight_boundary_preserved": True,
        "no_trade_boundary_preserved": True,
        "no_live_data_boundary_preserved": True,
        "no_controlled_shadow_boundary_preserved": True,
        "no_alert_boundary_preserved": True,
        "no_file_write_boundary_preserved": True,
        "no_broker_boundary_preserved": True,
        "no_optimization_boundary_preserved": True,
        "no_trade_or_optimization_boundary_preserved": True,
        "live_data_started": False,
        "controlled_shadow_data_started": False,
        "alerts_sent": False,
        "files_written": False,
        "broker_or_trade_behavior_enabled": False,
    }


def _validate_readiness_summary(
    readiness_summary: Any,
    index: int,
) -> None:
    if type(readiness_summary) is not dict:
        raise TypeError(
            f"Setup outcome review readiness_summaries[{index}] must be a dict"
        )

    missing_fields = [
        field_name
        for field_name in SETUP_OUTCOME_PACKET_READINESS_RESULT_FIELDS
        if field_name not in readiness_summary
    ]
    if missing_fields:
        raise ValueError(
            f"Missing required setup outcome packet readiness fields at {index}: "
            + ", ".join(missing_fields)
        )

    unexpected_fields = [
        field_name
        for field_name in readiness_summary
        if field_name not in SETUP_OUTCOME_PACKET_READINESS_RESULT_FIELDS
    ]
    if unexpected_fields:
        raise ValueError(
            f"Unexpected setup outcome packet readiness fields at {index}: "
            + ", ".join(unexpected_fields)
        )

    _reject_forbidden_review_fields(readiness_summary, path=(str(index),))

    for field_name in _EXPECTED_TRUE_READINESS_FIELDS:
        if readiness_summary[field_name] is not True:
            raise ValueError(
                f"Setup outcome review aggregator requires {field_name}=True"
            )
    for field_name in _EXPECTED_FALSE_READINESS_FIELDS:
        if readiness_summary[field_name] is not False:
            raise ValueError(
                f"Setup outcome review aggregator requires {field_name}=False"
            )

    for field_name in (
        "packet_items",
        "readiness_gaps",
        "missing_evidence",
        "lower_tier_handoff_items",
        "rejected_records",
        "proof_limited_records",
    ):
        if type(readiness_summary[field_name]) is not list:
            raise TypeError(
                f"Setup outcome review aggregator {field_name} must be a list"
            )
    if type(readiness_summary["items_by_setup_type"]) is not dict:
        raise TypeError(
            "Setup outcome review aggregator items_by_setup_type must be a dict"
        )
    if readiness_summary["packet_item_count"] != len(readiness_summary["packet_items"]):
        raise ValueError(
            "Setup outcome review aggregator packet_item_count must match packet_items"
        )


def _reviewed_packet(
    summary_index: int,
    readiness_summary: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "packet_index": summary_index,
        "packet_identifier": f"UNAVAILABLE-{summary_index + 1}",
        "readiness_status": readiness_summary["readiness_status"],
        "packet_item_count": readiness_summary["packet_item_count"],
        "complete_enough_to_review": readiness_summary["complete_enough_to_review"],
        "ready_for_lower_tier_review": readiness_summary["ready_for_lower_tier_review"],
    }


def _setup_types_from_summary(readiness_summary: Mapping[str, Any]) -> list[str]:
    setup_types = []
    for item in readiness_summary["packet_items"]:
        setup_type = item.get("setup_type") if type(item) is dict else None
        if _clean_identity_value(setup_type):
            _append_unique(setup_types, str(setup_type))
    return setup_types


def _symbols_from_summary(readiness_summary: Mapping[str, Any]) -> list[str]:
    symbols = []
    for item in readiness_summary["packet_items"]:
        symbol = item.get("symbol") if type(item) is dict else None
        if _clean_identity_value(symbol):
            _append_unique(symbols, str(symbol))
    return symbols


def _pairs_from_summary(readiness_summary: Mapping[str, Any]) -> list[dict[str, str]]:
    pairs = []
    for item in readiness_summary["packet_items"]:
        if type(item) is not dict:
            continue
        setup_type = item.get("setup_type")
        symbol = item.get("symbol")
        if _clean_identity_value(setup_type) and _clean_identity_value(symbol):
            pair = {"setup_type": str(setup_type), "symbol": str(symbol)}
            if pair not in pairs:
                pairs.append(pair)
    return pairs


def _group_outcome_item(
    outcome_groups: dict[str, list[dict[str, Any]]],
    summary_index: int,
    item: Any,
    proof_gaps: list[dict[str, Any]],
) -> None:
    if type(item) is not dict:
        proof_gaps.append(
            {
                "packet_index": summary_index,
                "gap_type": "packet_item_contract",
                "field_name": "packet_items",
                "reason": "packet item was not a dict",
            }
        )
        return

    outcome_status = item.get("outcome_status")
    outcome_group = _outcome_group(outcome_status)
    if outcome_group is None:
        proof_gaps.append(
            {
                "packet_index": summary_index,
                "packet_item_id": deepcopy(
                    item.get("packet_item_id", "UNAVAILABLE")
                ),
                "setup_type": deepcopy(item.get("setup_type")),
                "symbol": deepcopy(item.get("symbol")),
                "gap_type": "outcome_status_unavailable",
                "field_name": "outcome_status",
                "reason": "packet readiness item did not carry outcome_status",
            }
        )
        return

    outcome_groups[outcome_group].append(
        {
            "packet_index": summary_index,
            "packet_item_id": deepcopy(item.get("packet_item_id", "UNAVAILABLE")),
            "setup_type": deepcopy(item.get("setup_type")),
            "symbol": deepcopy(item.get("symbol")),
            "outcome_status": deepcopy(outcome_status),
            "readiness_status": deepcopy(item.get("readiness_status")),
            "missing_evidence": deepcopy(item.get("missing_evidence", [])),
            "lower_tier_handoff_required": item.get("lower_tier_handoff_required") is True,
        }
    )


def _outcome_group(outcome_status: Any) -> str | None:
    normalized = _normalized(outcome_status)
    mapping = {
        "triggered_worked": "worked",
        "worked": "worked",
        "triggered_failed": "failed",
        "failed": "failed",
        "triggered_inconclusive": "inconclusive",
        "inconclusive": "inconclusive",
        "stayed_valid_pending": "pending",
        "pending": "pending",
        "stale_without_trigger": "stale",
        "stale": "stale",
        "spent": "stale",
        "invalidated_before_trigger": "invalidated",
        "invalidated": "invalidated",
        "insufficient_evidence": "missing_evidence",
        "missing_evidence": "missing_evidence",
        "unavailable_evidence": "missing_evidence",
    }
    return mapping.get(normalized)


def _proof_decision(
    readiness_summaries: list[dict[str, Any]],
    proof_gaps: list[dict[str, Any]],
    sufficient: bool,
) -> str:
    if any(
        summary["readiness_status"] == "blocked_by_packet_contract_gap"
        for summary in readiness_summaries
    ):
        return "blocked_by_readiness_contract_gap"
    if sufficient:
        return "continue_review_with_ready_packets"
    return "needs_more_evidence_before_review"


def _repeated_counts(counts: dict[str, int]) -> dict[str, int]:
    return {
        key: count
        for key, count in counts.items()
        if count > 1
    }


def _gap_type(gap: Any) -> str:
    if type(gap) is dict and type(gap.get("gap_type")) is str and gap["gap_type"]:
        return gap["gap_type"]
    return "unclassified_readiness_gap"


def _summary_proof_gap(field_name: str, reason: str) -> dict[str, Any]:
    return {
        "packet_index": None,
        "gap_type": "aggregate_identity_gap",
        "field_name": field_name,
        "reason": reason,
    }


def _extend_unique(target: list[Any], values: list[Any]) -> None:
    for value in values:
        _append_unique(target, value)


def _append_unique(target: list[Any], value: Any) -> None:
    if value not in target:
        target.append(deepcopy(value))


def _clean_identity_value(value: Any) -> bool:
    if type(value) is not str or not value.strip():
        return False
    normalized = value.strip().upper()
    if normalized.startswith("UNAVAILABLE"):
        return False
    return True


def _reject_forbidden_review_fields(value: Any, path: tuple[str, ...]) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.lower()
            if (
                normalized_key in FORBIDDEN_SETUP_OUTCOME_FIELD_NAMES
                and normalized_key not in SETUP_OUTCOME_PACKET_READINESS_RESULT_FIELDS
            ):
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden execution/trade field: {dotted_path}")
            _reject_forbidden_review_fields(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_forbidden_review_fields(nested_value, (*path, str(index)))


def _normalized(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower().replace("-", "_").replace(" ", "_").replace("/", "_")
