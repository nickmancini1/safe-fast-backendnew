"""Local-only historical setup outcome proof review bundle builder.

This module accepts caller-provided in-memory setup outcome review readiness
summaries only and returns one in-memory bundle summary. It does not fetch data,
write files, start shadow/live workflows, emit alerts, call subprocesses, touch
brokers/accounts/options/P&L, optimize rules, or make trade decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.setup_outcome_proof import (
    FORBIDDEN_SETUP_OUTCOME_FIELD_NAMES,
)
from watcher_foundation.setup_outcome_review_aggregator import (
    SETUP_OUTCOME_REVIEW_OUTCOME_GROUPS,
)
from watcher_foundation.setup_outcome_review_readiness import (
    SETUP_OUTCOME_REVIEW_READINESS_RESULT_FIELDS,
)


SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_DECISIONS = (
    "ready_for_lower_tier_review",
    "needs_more_evidence_before_lower_tier_review",
    "blocked_by_bundle_contract_gap",
)

SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_RESULT_FIELDS = (
    "watch_only",
    "setup_outcome_proof_review_bundle_only",
    "setup_outcome_review_readiness_only",
    "setup_outcome_review_aggregator_only",
    "setup_outcome_packet_readiness_only",
    "setup_outcome_evidence_packet_only",
    "setup_outcome_diagnostics_only",
    "setup_outcome_proof_only",
    "final_viability_proven",
    "optimization_started",
    "no_rule_change_started",
    "review_summary_count",
    "included_group_review_count",
    "included_group_reviews",
    "excluded_group_reviews",
    "represented_setup_types",
    "setup_types_needing_more_evidence",
    "represented_symbols",
    "symbols_needing_more_evidence",
    "represented_setup_type_symbol_pairs",
    "setup_type_symbol_pairs_needing_more_evidence",
    "outcome_group_counts",
    "worked_patterns",
    "failed_patterns",
    "inconclusive_patterns",
    "pending_patterns",
    "stale_patterns",
    "invalidated_patterns",
    "missing_evidence_patterns",
    "repeated_worked_patterns",
    "repeated_failed_patterns",
    "repeated_inconclusive_pending_stale_invalidated_or_missing_evidence_patterns",
    "missing_evidence",
    "missing_evidence_by_setup_type",
    "missing_evidence_by_symbol",
    "missing_evidence_by_setup_type_symbol_pair",
    "repeated_fix_paths",
    "repeated_regression_needs",
    "required_regression_tests",
    "missing_regression_coverage",
    "proof_gaps",
    "bundle_contract_gaps",
    "lower_tier_handoff_required",
    "lower_tier_handoff_items",
    "ready_for_lower_tier_review",
    "bundle_review_decision",
    "setup_type_separated",
    "symbol_separated",
    "proof_review_only",
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

_EXPECTED_TRUE_READINESS_FIELDS = (
    "watch_only",
    "setup_outcome_review_readiness_only",
    "setup_outcome_review_aggregator_only",
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


def build_setup_outcome_proof_review_bundle(
    readiness_summaries: list[dict[str, Any]],
) -> dict[str, Any]:
    """Return one in-memory historical proof bundle for readiness summaries."""
    if type(readiness_summaries) is not list:
        raise TypeError(
            "Setup outcome proof review bundle input must be a list"
        )

    for index, readiness_summary in enumerate(readiness_summaries):
        _validate_readiness_summary(readiness_summary, index)

    included_group_reviews = []
    excluded_group_reviews = []
    represented_setup_types: list[str] = []
    setup_types_needing_more_evidence: list[str] = []
    represented_symbols: list[str] = []
    symbols_needing_more_evidence: list[str] = []
    represented_pairs = []
    pairs_needing_more_evidence = []
    outcome_group_counts = {group: 0 for group in SETUP_OUTCOME_REVIEW_OUTCOME_GROUPS}
    patterns = {group: [] for group in SETUP_OUTCOME_REVIEW_OUTCOME_GROUPS}
    missing_evidence = []
    lower_tier_handoff_items = []
    proof_gaps = []
    bundle_contract_gaps = []
    fix_path_counts: dict[str, int] = {}
    regression_counts: dict[str, int] = {}
    required_regression_tests: list[str] = []
    missing_regression_coverage = []

    for review_index, summary in enumerate(readiness_summaries):
        included = _summary_is_included(summary)
        review_descriptor = _group_review_descriptor(review_index, summary)
        _extend_unique(
            setup_types_needing_more_evidence,
            summary["setup_types_needing_more_evidence"],
        )
        _extend_unique(
            symbols_needing_more_evidence,
            summary["symbols_needing_more_evidence"],
        )
        _extend_unique(
            pairs_needing_more_evidence,
            summary["setup_type_symbol_pairs_needing_more_evidence"],
        )
        missing_evidence.extend(deepcopy(summary["missing_evidence"]))
        lower_tier_handoff_items.extend(
            deepcopy(summary["lower_tier_handoff_items"])
        )
        proof_gaps.extend(deepcopy(summary["proof_gaps"]))
        missing_regression_coverage.extend(
            deepcopy(summary["missing_regression_coverage"])
        )
        _add_counts(fix_path_counts, summary["repeated_next_fix_paths"])
        _add_counts(regression_counts, summary["repeated_regression_needs"])
        for regression in summary["repeated_regression_needs"]:
            _append_unique(required_regression_tests, regression)
        if included:
            included_group_reviews.append(review_descriptor)
            _extend_unique(represented_setup_types, summary["represented_setup_types"])
            _extend_unique(represented_symbols, summary["represented_symbols"])
            _extend_unique(
                represented_pairs,
                summary["represented_setup_type_symbol_pairs"],
            )
            for group_name in SETUP_OUTCOME_REVIEW_OUTCOME_GROUPS:
                count = summary["outcome_group_counts"].get(group_name, 0)
                outcome_group_counts[group_name] += count
                if count:
                    patterns[group_name].append(
                        _outcome_pattern(review_index, group_name, count, summary)
                    )
        else:
            excluded_group_reviews.append(
                {
                    **review_descriptor,
                    "exclusion_reason": _exclusion_reason(summary),
                    "lower_tier_review_decision": summary["lower_tier_review_decision"],
                }
            )

    if not readiness_summaries:
        bundle_contract_gaps.append(
            _bundle_contract_gap(
                "readiness_summaries",
                "no caller-provided review readiness summaries were supplied",
            )
        )
    if not included_group_reviews:
        bundle_contract_gaps.append(
            _bundle_contract_gap(
                "included_group_reviews",
                "no group review was complete enough to include in the bundle",
            )
        )
    if not represented_setup_types:
        bundle_contract_gaps.append(
            _bundle_contract_gap(
                "represented_setup_types",
                "no setup types are represented by included group reviews",
            )
        )
    if not represented_symbols:
        bundle_contract_gaps.append(
            _bundle_contract_gap(
                "represented_symbols",
                "no symbols are represented by included group reviews",
            )
        )

    missing_evidence_by_setup_type = _missing_by_identity(
        missing_evidence,
        setup_types_needing_more_evidence,
        "setup_type",
    )
    missing_evidence_by_symbol = _missing_by_identity(
        missing_evidence,
        symbols_needing_more_evidence,
        "symbol",
    )
    missing_evidence_by_pair = _missing_by_pair(
        missing_evidence,
        pairs_needing_more_evidence,
    )
    repeated_fix_paths = _repeated_counts(fix_path_counts)
    repeated_regression_needs = _repeated_counts(regression_counts)
    for regression in repeated_regression_needs:
        _append_unique(required_regression_tests, regression)
    if (
        proof_gaps
        or missing_evidence
        or missing_evidence_by_setup_type
        or missing_evidence_by_symbol
        or missing_evidence_by_pair
        or bundle_contract_gaps
    ) and not required_regression_tests:
        missing_regression_coverage.append(
            {
                "gap_type": "missing_bundle_regression_coverage",
                "field_name": "required_regression_tests",
                "reason": "proof-blocking bundle gaps require named regression tests",
            }
        )

    lower_tier_handoff_required = bool(
        excluded_group_reviews
        or missing_evidence
        or missing_evidence_by_setup_type
        or missing_evidence_by_symbol
        or missing_evidence_by_pair
        or proof_gaps
        or bundle_contract_gaps
        or lower_tier_handoff_items
        or missing_regression_coverage
    )
    ready = bool(included_group_reviews) and not lower_tier_handoff_required
    decision = _bundle_decision(bundle_contract_gaps, ready)

    return {
        "watch_only": True,
        "setup_outcome_proof_review_bundle_only": True,
        "setup_outcome_review_readiness_only": True,
        "setup_outcome_review_aggregator_only": True,
        "setup_outcome_packet_readiness_only": True,
        "setup_outcome_evidence_packet_only": True,
        "setup_outcome_diagnostics_only": True,
        "setup_outcome_proof_only": True,
        "final_viability_proven": False,
        "optimization_started": False,
        "no_rule_change_started": True,
        "review_summary_count": len(readiness_summaries),
        "included_group_review_count": len(included_group_reviews),
        "included_group_reviews": deepcopy(included_group_reviews),
        "excluded_group_reviews": deepcopy(excluded_group_reviews),
        "represented_setup_types": deepcopy(represented_setup_types),
        "setup_types_needing_more_evidence": deepcopy(
            setup_types_needing_more_evidence
        ),
        "represented_symbols": deepcopy(represented_symbols),
        "symbols_needing_more_evidence": deepcopy(symbols_needing_more_evidence),
        "represented_setup_type_symbol_pairs": deepcopy(represented_pairs),
        "setup_type_symbol_pairs_needing_more_evidence": deepcopy(
            pairs_needing_more_evidence
        ),
        "outcome_group_counts": outcome_group_counts,
        "worked_patterns": deepcopy(patterns["worked"]),
        "failed_patterns": deepcopy(patterns["failed"]),
        "inconclusive_patterns": deepcopy(patterns["inconclusive"]),
        "pending_patterns": deepcopy(patterns["pending"]),
        "stale_patterns": deepcopy(patterns["stale"]),
        "invalidated_patterns": deepcopy(patterns["invalidated"]),
        "missing_evidence_patterns": deepcopy(patterns["missing_evidence"]),
        "repeated_worked_patterns": _repeated_patterns(patterns["worked"]),
        "repeated_failed_patterns": _repeated_patterns(patterns["failed"]),
        "repeated_inconclusive_pending_stale_invalidated_or_missing_evidence_patterns": (
            _repeated_patterns(
                patterns["inconclusive"]
                + patterns["pending"]
                + patterns["stale"]
                + patterns["invalidated"]
                + patterns["missing_evidence"]
            )
        ),
        "missing_evidence": deepcopy(missing_evidence),
        "missing_evidence_by_setup_type": missing_evidence_by_setup_type,
        "missing_evidence_by_symbol": missing_evidence_by_symbol,
        "missing_evidence_by_setup_type_symbol_pair": missing_evidence_by_pair,
        "repeated_fix_paths": repeated_fix_paths,
        "repeated_regression_needs": repeated_regression_needs,
        "required_regression_tests": deepcopy(required_regression_tests),
        "missing_regression_coverage": deepcopy(missing_regression_coverage),
        "proof_gaps": deepcopy(proof_gaps),
        "bundle_contract_gaps": deepcopy(bundle_contract_gaps),
        "lower_tier_handoff_required": lower_tier_handoff_required,
        "lower_tier_handoff_items": deepcopy(lower_tier_handoff_items),
        "ready_for_lower_tier_review": ready,
        "bundle_review_decision": decision,
        "setup_type_separated": bool(represented_setup_types),
        "symbol_separated": bool(represented_symbols),
        "proof_review_only": True,
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


def _validate_readiness_summary(readiness_summary: Any, index: int) -> None:
    if type(readiness_summary) is not dict:
        raise TypeError(
            f"Setup outcome proof review bundle readiness_summaries[{index}] "
            "must be a dict"
        )

    missing_fields = [
        field_name
        for field_name in SETUP_OUTCOME_REVIEW_READINESS_RESULT_FIELDS
        if field_name not in readiness_summary
    ]
    if missing_fields:
        raise ValueError(
            f"Missing required setup outcome review readiness fields at {index}: "
            + ", ".join(missing_fields)
        )

    unexpected_fields = [
        field_name
        for field_name in readiness_summary
        if field_name not in SETUP_OUTCOME_REVIEW_READINESS_RESULT_FIELDS
    ]
    if unexpected_fields:
        raise ValueError(
            f"Unexpected setup outcome review readiness fields at {index}: "
            + ", ".join(unexpected_fields)
        )

    _reject_forbidden_bundle_fields(readiness_summary, path=(str(index),))

    for field_name in _EXPECTED_TRUE_READINESS_FIELDS:
        if readiness_summary[field_name] is not True:
            raise ValueError(
                f"Setup outcome proof review bundle requires {field_name}=True"
            )
    for field_name in _EXPECTED_FALSE_READINESS_FIELDS:
        if readiness_summary[field_name] is not False:
            raise ValueError(
                f"Setup outcome proof review bundle requires {field_name}=False"
            )

    for field_name in (
        "packet_summary_count",
    ):
        if type(readiness_summary[field_name]) is not int:
            raise TypeError(
                f"Setup outcome proof review bundle {field_name} must be an int"
            )
        if readiness_summary[field_name] < 0:
            raise ValueError(
                f"Setup outcome proof review bundle {field_name} must be non-negative"
            )
    for field_name in (
        "reviewed_packets",
        "represented_setup_types",
        "setup_types_needing_more_evidence",
        "represented_symbols",
        "symbols_needing_more_evidence",
        "represented_setup_type_symbol_pairs",
        "setup_type_symbol_pairs_needing_more_evidence",
        "missing_outcome_groups",
        "unclear_diagnoses",
        "unclear_repeated_fix_paths",
        "missing_regression_coverage",
        "proof_gaps",
        "missing_evidence",
        "review_contract_gaps",
        "lower_tier_handoff_items",
        "rejected_records",
        "proof_limited_records",
    ):
        if type(readiness_summary[field_name]) is not list:
            raise TypeError(
                f"Setup outcome proof review bundle {field_name} must be a list"
            )
    for field_name in (
        "outcome_group_counts",
        "readiness_gap_counts",
        "repeated_next_fix_paths",
        "repeated_regression_needs",
    ):
        if type(readiness_summary[field_name]) is not dict:
            raise TypeError(
                f"Setup outcome proof review bundle {field_name} must be a dict"
            )
    if set(readiness_summary["outcome_group_counts"]) != set(
        SETUP_OUTCOME_REVIEW_OUTCOME_GROUPS
    ):
        raise ValueError(
            "Setup outcome proof review bundle outcome_group_counts must include "
            "worked, failed, inconclusive, pending, stale, invalidated, and "
            "missing_evidence"
        )


def _summary_is_included(summary: Mapping[str, Any]) -> bool:
    return (
        summary["group_review_complete_enough_to_trust"] is True
        and summary["ready_for_lower_tier_review"] is True
        and summary["lower_tier_review_decision"] == "ready_for_lower_tier_review"
    )


def _group_review_descriptor(
    review_index: int,
    summary: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "group_review_index": review_index,
        "reviewed_packets": deepcopy(summary["reviewed_packets"]),
        "packet_summary_count": summary["packet_summary_count"],
        "represented_setup_types": deepcopy(summary["represented_setup_types"]),
        "represented_symbols": deepcopy(summary["represented_symbols"]),
        "represented_setup_type_symbol_pairs": deepcopy(
            summary["represented_setup_type_symbol_pairs"]
        ),
        "outcome_group_counts": deepcopy(summary["outcome_group_counts"]),
    }


def _exclusion_reason(summary: Mapping[str, Any]) -> str:
    if summary["review_contract_gaps"]:
        return "readiness summary has review contract gaps"
    if summary["proof_gaps_blocking_review"] is True:
        return "readiness summary has proof gaps blocking review"
    if summary["lower_tier_handoff_required"] is True:
        return "readiness summary requires lower-tier handoff before bundling"
    return "readiness summary was not marked complete enough to trust"


def _outcome_pattern(
    review_index: int,
    outcome_group: str,
    count: int,
    summary: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "group_review_index": review_index,
        "outcome_group": outcome_group,
        "count": count,
        "represented_setup_types": deepcopy(summary["represented_setup_types"]),
        "represented_symbols": deepcopy(summary["represented_symbols"]),
        "represented_setup_type_symbol_pairs": deepcopy(
            summary["represented_setup_type_symbol_pairs"]
        ),
    }


def _missing_by_identity(
    missing_evidence: list[Any],
    fallback_values: list[str],
    field_name: str,
) -> dict[str, list[Any]]:
    grouped: dict[str, list[Any]] = {}
    for item in missing_evidence:
        if type(item) is not dict:
            continue
        value = item.get(field_name)
        if _clean_identity_value(value):
            grouped.setdefault(str(value), []).append(deepcopy(item))
    if missing_evidence and not grouped:
        for value in fallback_values:
            if _clean_identity_value(value):
                grouped.setdefault(str(value), []).extend(deepcopy(missing_evidence))
    return grouped


def _missing_by_pair(
    missing_evidence: list[Any],
    fallback_pairs: list[dict[str, str]],
) -> list[dict[str, Any]]:
    grouped = []
    for item in missing_evidence:
        if type(item) is not dict:
            continue
        setup_type = item.get("setup_type")
        symbol = item.get("symbol")
        if _clean_identity_value(setup_type) and _clean_identity_value(symbol):
            _append_pair_evidence(grouped, str(setup_type), str(symbol), item)
    if missing_evidence and not grouped:
        for pair in fallback_pairs:
            if type(pair) is not dict:
                continue
            setup_type = pair.get("setup_type")
            symbol = pair.get("symbol")
            if _clean_identity_value(setup_type) and _clean_identity_value(symbol):
                _append_pair_evidence(
                    grouped,
                    str(setup_type),
                    str(symbol),
                    deepcopy(missing_evidence),
                )
    return grouped


def _append_pair_evidence(
    grouped: list[dict[str, Any]],
    setup_type: str,
    symbol: str,
    evidence: Any,
) -> None:
    for item in grouped:
        if item["setup_type"] == setup_type and item["symbol"] == symbol:
            if type(evidence) is list:
                item["missing_evidence"].extend(deepcopy(evidence))
            else:
                item["missing_evidence"].append(deepcopy(evidence))
            return
    grouped.append(
        {
            "setup_type": setup_type,
            "symbol": symbol,
            "missing_evidence": deepcopy(evidence) if type(evidence) is list else [deepcopy(evidence)],
        }
    )


def _add_counts(target: dict[str, int], source: Mapping[str, Any]) -> None:
    for key, count in source.items():
        if type(key) is not str or type(count) is not int:
            continue
        target[key] = target.get(key, 0) + count


def _repeated_counts(counts: dict[str, int]) -> dict[str, int]:
    return {
        key: count
        for key, count in counts.items()
        if count > 1
    }


def _repeated_patterns(patterns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: dict[tuple[str, str, str], int] = {}
    for pattern in patterns:
        for pair in pattern["represented_setup_type_symbol_pairs"]:
            if type(pair) is not dict:
                continue
            setup_type = pair.get("setup_type")
            symbol = pair.get("symbol")
            if _clean_identity_value(setup_type) and _clean_identity_value(symbol):
                key = (pattern["outcome_group"], str(setup_type), str(symbol))
                counts[key] = counts.get(key, 0) + pattern["count"]
    repeated = []
    for (outcome_group, setup_type, symbol), count in counts.items():
        if count > 1:
            repeated.append(
                {
                    "outcome_group": outcome_group,
                    "setup_type": setup_type,
                    "symbol": symbol,
                    "count": count,
                }
            )
    return repeated


def _bundle_contract_gap(field_name: str, reason: str) -> dict[str, str]:
    return {
        "field_name": field_name,
        "gap_type": "bundle_contract_gap",
        "reason": reason,
    }


def _bundle_decision(
    bundle_contract_gaps: list[dict[str, Any]],
    ready: bool,
) -> str:
    if bundle_contract_gaps:
        return "blocked_by_bundle_contract_gap"
    if ready:
        return "ready_for_lower_tier_review"
    return "needs_more_evidence_before_lower_tier_review"


def _extend_unique(target: list[Any], values: list[Any]) -> None:
    for value in values:
        _append_unique(target, value)


def _append_unique(target: list[Any], value: Any) -> None:
    copied = deepcopy(value)
    if copied not in target:
        target.append(copied)


def _clean_identity_value(value: Any) -> bool:
    if type(value) is not str or not value.strip():
        return False
    normalized = value.strip().upper()
    if normalized.startswith("UNAVAILABLE"):
        return False
    return True


def _reject_forbidden_bundle_fields(value: Any, path: tuple[str, ...]) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.lower()
            if (
                normalized_key in FORBIDDEN_SETUP_OUTCOME_FIELD_NAMES
                and normalized_key not in SETUP_OUTCOME_REVIEW_READINESS_RESULT_FIELDS
            ):
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden execution/trade field: {dotted_path}")
            _reject_forbidden_bundle_fields(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_forbidden_bundle_fields(nested_value, (*path, str(index)))
