"""Local-only historical setup proof review bundle readiness gating.

This module accepts one caller-provided in-memory historical setup proof review
bundle summary and returns one in-memory readiness summary. It does not fetch
data, write files, start shadow/live workflows, emit alerts, call subprocesses,
touch brokers/accounts/options/P&L, optimize rules, or make trade decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.setup_outcome_proof import (
    FORBIDDEN_SETUP_OUTCOME_FIELD_NAMES,
)
from watcher_foundation.setup_outcome_proof_review_bundle import (
    SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_RESULT_FIELDS,
)
from watcher_foundation.setup_outcome_review_aggregator import (
    SETUP_OUTCOME_REVIEW_OUTCOME_GROUPS,
)


SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_READINESS_DECISIONS = (
    "ready_for_lower_tier_review",
    "needs_more_evidence_before_lower_tier_review",
    "blocked_by_bundle_readiness_contract_gap",
)

SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_READINESS_RESULT_FIELDS = (
    "watch_only",
    "setup_outcome_proof_review_bundle_readiness_only",
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
    "bundle_complete_enough_to_review",
    "setup_type_evidence_complete",
    "represented_setup_types",
    "setup_types_needing_more_evidence",
    "symbol_evidence_complete",
    "represented_symbols",
    "symbols_needing_more_evidence",
    "setup_type_symbol_pair_evidence_complete",
    "represented_setup_type_symbol_pairs",
    "setup_type_symbol_pairs_needing_more_evidence",
    "outcome_group_counts",
    "worked_patterns_clear_enough",
    "worked_patterns",
    "unclear_worked_patterns",
    "failed_patterns_clear_enough",
    "failed_patterns",
    "unclear_failed_patterns",
    "unresolved_patterns_clear_enough",
    "inconclusive_patterns",
    "pending_patterns",
    "stale_patterns",
    "invalidated_patterns",
    "missing_evidence_patterns",
    "unclear_unresolved_patterns",
    "repeated_fix_paths_clear_enough",
    "repeated_fix_paths",
    "unclear_repeated_fix_paths",
    "regression_coverage_named",
    "required_regression_tests",
    "missing_regression_coverage",
    "proof_gaps_blocking_review",
    "proof_gaps",
    "bundle_contract_gaps_blocking_review",
    "bundle_contract_gaps",
    "bundle_readiness_contract_gaps",
    "missing_evidence",
    "missing_evidence_by_setup_type",
    "missing_evidence_by_symbol",
    "missing_evidence_by_setup_type_symbol_pair",
    "lower_tier_handoff_required",
    "lower_tier_handoff_items",
    "ready_for_lower_tier_review",
    "bundle_readiness_decision",
    "exact_missing_review_items",
    "proof_review_only",
    "setup_type_separated",
    "symbol_separated",
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

_EXPECTED_TRUE_BUNDLE_FIELDS = (
    "watch_only",
    "setup_outcome_proof_review_bundle_only",
    "setup_outcome_review_readiness_only",
    "setup_outcome_review_aggregator_only",
    "setup_outcome_packet_readiness_only",
    "setup_outcome_evidence_packet_only",
    "setup_outcome_diagnostics_only",
    "setup_outcome_proof_only",
    "no_rule_change_started",
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
)

_EXPECTED_FALSE_BUNDLE_FIELDS = (
    "final_viability_proven",
    "optimization_started",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

_SPECIFIC_FIX_PATH_TOKENS = (
    "contract",
    "fixture",
    "test",
    "evidence",
    "diagnostics",
    "packet",
    "review",
    "readiness",
)


def evaluate_setup_outcome_proof_review_bundle_readiness(
    bundle_summary: dict[str, Any],
) -> dict[str, Any]:
    """Return one in-memory readiness summary for a historical proof bundle."""
    if type(bundle_summary) is not dict:
        raise TypeError(
            "Setup outcome proof review bundle readiness input must be a dict"
        )

    _validate_bundle_summary(bundle_summary)

    bundle_readiness_contract_gaps = _bundle_readiness_contract_gaps(bundle_summary)
    unclear_worked_patterns = _unclear_patterns(
        bundle_summary["worked_patterns"],
        "worked_patterns",
    )
    unclear_failed_patterns = _unclear_patterns(
        bundle_summary["failed_patterns"],
        "failed_patterns",
    )
    unclear_unresolved_patterns = _unclear_patterns(
        bundle_summary["inconclusive_patterns"]
        + bundle_summary["pending_patterns"]
        + bundle_summary["stale_patterns"]
        + bundle_summary["invalidated_patterns"]
        + bundle_summary["missing_evidence_patterns"],
        "unresolved_patterns",
    )
    unclear_repeated_fix_paths = _unclear_repeated_fix_paths(
        bundle_summary["repeated_fix_paths"]
    )
    missing_regression_coverage = deepcopy(
        bundle_summary["missing_regression_coverage"]
    )
    if _gaps_need_regression(bundle_summary) and not bundle_summary[
        "required_regression_tests"
    ]:
        missing_regression_coverage.append(
            {
                "gap_type": "missing_bundle_readiness_regression_coverage",
                "field_name": "required_regression_tests",
                "reason": "bundle evidence, proof, or contract gaps require named regression tests",
            }
        )

    exact_missing_review_items = _exact_missing_review_items(
        bundle_summary,
        bundle_readiness_contract_gaps,
        unclear_worked_patterns,
        unclear_failed_patterns,
        unclear_unresolved_patterns,
        unclear_repeated_fix_paths,
        missing_regression_coverage,
    )
    lower_tier_handoff_required = bool(
        exact_missing_review_items
        or bundle_summary["lower_tier_handoff_required"] is True
        or bundle_summary["lower_tier_handoff_items"]
    )
    ready = not lower_tier_handoff_required
    decision = _readiness_decision(bundle_readiness_contract_gaps, bundle_summary, ready)

    return {
        "watch_only": True,
        "setup_outcome_proof_review_bundle_readiness_only": True,
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
        "review_summary_count": bundle_summary["review_summary_count"],
        "included_group_review_count": bundle_summary["included_group_review_count"],
        "included_group_reviews": deepcopy(bundle_summary["included_group_reviews"]),
        "excluded_group_reviews": deepcopy(bundle_summary["excluded_group_reviews"]),
        "bundle_complete_enough_to_review": ready,
        "setup_type_evidence_complete": not bundle_summary[
            "setup_types_needing_more_evidence"
        ],
        "represented_setup_types": deepcopy(bundle_summary["represented_setup_types"]),
        "setup_types_needing_more_evidence": deepcopy(
            bundle_summary["setup_types_needing_more_evidence"]
        ),
        "symbol_evidence_complete": not bundle_summary[
            "symbols_needing_more_evidence"
        ],
        "represented_symbols": deepcopy(bundle_summary["represented_symbols"]),
        "symbols_needing_more_evidence": deepcopy(
            bundle_summary["symbols_needing_more_evidence"]
        ),
        "setup_type_symbol_pair_evidence_complete": not bundle_summary[
            "setup_type_symbol_pairs_needing_more_evidence"
        ],
        "represented_setup_type_symbol_pairs": deepcopy(
            bundle_summary["represented_setup_type_symbol_pairs"]
        ),
        "setup_type_symbol_pairs_needing_more_evidence": deepcopy(
            bundle_summary["setup_type_symbol_pairs_needing_more_evidence"]
        ),
        "outcome_group_counts": deepcopy(bundle_summary["outcome_group_counts"]),
        "worked_patterns_clear_enough": not unclear_worked_patterns,
        "worked_patterns": deepcopy(bundle_summary["worked_patterns"]),
        "unclear_worked_patterns": unclear_worked_patterns,
        "failed_patterns_clear_enough": not unclear_failed_patterns,
        "failed_patterns": deepcopy(bundle_summary["failed_patterns"]),
        "unclear_failed_patterns": unclear_failed_patterns,
        "unresolved_patterns_clear_enough": not unclear_unresolved_patterns,
        "inconclusive_patterns": deepcopy(bundle_summary["inconclusive_patterns"]),
        "pending_patterns": deepcopy(bundle_summary["pending_patterns"]),
        "stale_patterns": deepcopy(bundle_summary["stale_patterns"]),
        "invalidated_patterns": deepcopy(bundle_summary["invalidated_patterns"]),
        "missing_evidence_patterns": deepcopy(
            bundle_summary["missing_evidence_patterns"]
        ),
        "unclear_unresolved_patterns": unclear_unresolved_patterns,
        "repeated_fix_paths_clear_enough": not unclear_repeated_fix_paths,
        "repeated_fix_paths": deepcopy(bundle_summary["repeated_fix_paths"]),
        "unclear_repeated_fix_paths": unclear_repeated_fix_paths,
        "regression_coverage_named": not missing_regression_coverage,
        "required_regression_tests": deepcopy(
            bundle_summary["required_regression_tests"]
        ),
        "missing_regression_coverage": deepcopy(missing_regression_coverage),
        "proof_gaps_blocking_review": bool(bundle_summary["proof_gaps"]),
        "proof_gaps": deepcopy(bundle_summary["proof_gaps"]),
        "bundle_contract_gaps_blocking_review": bool(
            bundle_summary["bundle_contract_gaps"]
        ),
        "bundle_contract_gaps": deepcopy(bundle_summary["bundle_contract_gaps"]),
        "bundle_readiness_contract_gaps": deepcopy(bundle_readiness_contract_gaps),
        "missing_evidence": deepcopy(bundle_summary["missing_evidence"]),
        "missing_evidence_by_setup_type": deepcopy(
            bundle_summary["missing_evidence_by_setup_type"]
        ),
        "missing_evidence_by_symbol": deepcopy(
            bundle_summary["missing_evidence_by_symbol"]
        ),
        "missing_evidence_by_setup_type_symbol_pair": deepcopy(
            bundle_summary["missing_evidence_by_setup_type_symbol_pair"]
        ),
        "lower_tier_handoff_required": lower_tier_handoff_required,
        "lower_tier_handoff_items": deepcopy(
            bundle_summary["lower_tier_handoff_items"]
        ),
        "ready_for_lower_tier_review": ready,
        "bundle_readiness_decision": decision,
        "exact_missing_review_items": deepcopy(exact_missing_review_items),
        "proof_review_only": True,
        "setup_type_separated": bundle_summary["setup_type_separated"],
        "symbol_separated": bundle_summary["symbol_separated"],
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


def _validate_bundle_summary(bundle_summary: Mapping[str, Any]) -> None:
    missing_fields = [
        field_name
        for field_name in SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_RESULT_FIELDS
        if field_name not in bundle_summary
    ]
    if missing_fields:
        raise ValueError(
            "Missing required setup outcome proof review bundle fields: "
            + ", ".join(missing_fields)
        )

    unexpected_fields = [
        field_name
        for field_name in bundle_summary
        if field_name not in SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_RESULT_FIELDS
    ]
    if unexpected_fields:
        raise ValueError(
            "Unexpected setup outcome proof review bundle fields: "
            + ", ".join(unexpected_fields)
        )

    _reject_forbidden_bundle_readiness_fields(bundle_summary, path=())

    for field_name in _EXPECTED_TRUE_BUNDLE_FIELDS:
        if bundle_summary[field_name] is not True:
            raise ValueError(
                f"Setup outcome proof review bundle readiness requires {field_name}=True"
            )
    for field_name in _EXPECTED_FALSE_BUNDLE_FIELDS:
        if bundle_summary[field_name] is not False:
            raise ValueError(
                f"Setup outcome proof review bundle readiness requires {field_name}=False"
            )

    for field_name in ("review_summary_count", "included_group_review_count"):
        if type(bundle_summary[field_name]) is not int:
            raise TypeError(
                f"Setup outcome proof review bundle readiness {field_name} must be an int"
            )
        if bundle_summary[field_name] < 0:
            raise ValueError(
                f"Setup outcome proof review bundle readiness {field_name} must be non-negative"
            )

    for field_name in (
        "included_group_reviews",
        "excluded_group_reviews",
        "represented_setup_types",
        "setup_types_needing_more_evidence",
        "represented_symbols",
        "symbols_needing_more_evidence",
        "represented_setup_type_symbol_pairs",
        "setup_type_symbol_pairs_needing_more_evidence",
        "worked_patterns",
        "failed_patterns",
        "inconclusive_patterns",
        "pending_patterns",
        "stale_patterns",
        "invalidated_patterns",
        "missing_evidence_patterns",
        "missing_evidence",
        "missing_evidence_by_setup_type_symbol_pair",
        "required_regression_tests",
        "missing_regression_coverage",
        "proof_gaps",
        "bundle_contract_gaps",
        "lower_tier_handoff_items",
    ):
        if type(bundle_summary[field_name]) is not list:
            raise TypeError(
                f"Setup outcome proof review bundle readiness {field_name} must be a list"
            )

    for field_name in (
        "outcome_group_counts",
        "missing_evidence_by_setup_type",
        "missing_evidence_by_symbol",
        "repeated_fix_paths",
        "repeated_regression_needs",
    ):
        if type(bundle_summary[field_name]) is not dict:
            raise TypeError(
                f"Setup outcome proof review bundle readiness {field_name} must be a dict"
            )

    if bundle_summary["included_group_review_count"] != len(
        bundle_summary["included_group_reviews"]
    ):
        raise ValueError(
            "Setup outcome proof review bundle readiness included_group_review_count "
            "must match included_group_reviews"
        )
    if set(bundle_summary["outcome_group_counts"]) != set(
        SETUP_OUTCOME_REVIEW_OUTCOME_GROUPS
    ):
        raise ValueError(
            "Setup outcome proof review bundle readiness outcome_group_counts must "
            "include worked, failed, inconclusive, pending, stale, invalidated, "
            "and missing_evidence"
        )


def _bundle_readiness_contract_gaps(
    bundle_summary: Mapping[str, Any],
) -> list[dict[str, Any]]:
    gaps = []
    if bundle_summary["review_summary_count"] <= 0:
        gaps.append(
            _contract_gap(
                "review_summary_count",
                "no caller-provided bundle review summaries were available",
            )
        )
    if bundle_summary["included_group_review_count"] <= 0:
        gaps.append(
            _contract_gap(
                "included_group_reviews",
                "no included group review is available for serious review",
            )
        )
    if bundle_summary["setup_type_separated"] is not True:
        gaps.append(
            _contract_gap("setup_type_separated", "setup type was not kept separate")
        )
    if bundle_summary["symbol_separated"] is not True:
        gaps.append(_contract_gap("symbol_separated", "symbol was not kept separate"))
    if not bundle_summary["represented_setup_types"]:
        gaps.append(
            _contract_gap("represented_setup_types", "no setup type evidence is represented")
        )
    if not bundle_summary["represented_symbols"]:
        gaps.append(
            _contract_gap("represented_symbols", "no symbol evidence is represented")
        )
    if not bundle_summary["represented_setup_type_symbol_pairs"]:
        gaps.append(
            _contract_gap(
                "represented_setup_type_symbol_pairs",
                "no setup-type-plus-symbol pair evidence is represented",
            )
        )
    return gaps


def _exact_missing_review_items(
    bundle_summary: Mapping[str, Any],
    readiness_contract_gaps: list[dict[str, Any]],
    unclear_worked_patterns: list[dict[str, Any]],
    unclear_failed_patterns: list[dict[str, Any]],
    unclear_unresolved_patterns: list[dict[str, Any]],
    unclear_repeated_fix_paths: list[dict[str, Any]],
    missing_regression_coverage: list[Any],
) -> list[dict[str, Any]]:
    items = []
    items.extend(deepcopy(readiness_contract_gaps))
    for setup_type in bundle_summary["setup_types_needing_more_evidence"]:
        items.append(
            {
                "gap_type": "setup_type_needs_more_evidence",
                "field_name": "setup_types_needing_more_evidence",
                "setup_type": deepcopy(setup_type),
                "reason": "setup type still needs more evidence before review-ready status",
            }
        )
    for symbol in bundle_summary["symbols_needing_more_evidence"]:
        items.append(
            {
                "gap_type": "symbol_needs_more_evidence",
                "field_name": "symbols_needing_more_evidence",
                "symbol": deepcopy(symbol),
                "reason": "symbol still needs more evidence before review-ready status",
            }
        )
    for pair in bundle_summary["setup_type_symbol_pairs_needing_more_evidence"]:
        items.append(
            {
                "gap_type": "setup_type_symbol_pair_needs_more_evidence",
                "field_name": "setup_type_symbol_pairs_needing_more_evidence",
                "pair": deepcopy(pair),
                "reason": "setup-type-plus-symbol pair still needs more evidence",
            }
        )
    items.extend(deepcopy(unclear_worked_patterns))
    items.extend(deepcopy(unclear_failed_patterns))
    items.extend(deepcopy(unclear_unresolved_patterns))
    items.extend(deepcopy(unclear_repeated_fix_paths))
    items.extend(deepcopy(missing_regression_coverage))
    items.extend(_field_gap_items(bundle_summary["proof_gaps"], "proof_gaps"))
    items.extend(
        _field_gap_items(bundle_summary["bundle_contract_gaps"], "bundle_contract_gaps")
    )
    items.extend(_field_gap_items(bundle_summary["missing_evidence"], "missing_evidence"))
    items.extend(
        _field_gap_items(
            bundle_summary["missing_evidence_by_setup_type"],
            "missing_evidence_by_setup_type",
        )
    )
    items.extend(
        _field_gap_items(
            bundle_summary["missing_evidence_by_symbol"],
            "missing_evidence_by_symbol",
        )
    )
    items.extend(
        _field_gap_items(
            bundle_summary["missing_evidence_by_setup_type_symbol_pair"],
            "missing_evidence_by_setup_type_symbol_pair",
        )
    )
    if bundle_summary["excluded_group_reviews"]:
        items.append(
            {
                "gap_type": "excluded_group_reviews_present",
                "field_name": "excluded_group_reviews",
                "reason": "not-ready group reviews remain outside the bundle",
                "count": len(bundle_summary["excluded_group_reviews"]),
            }
        )
    if bundle_summary["lower_tier_handoff_required"] is True:
        items.append(
            {
                "gap_type": "upstream_lower_tier_handoff_required",
                "field_name": "lower_tier_handoff_required",
                "reason": "bundle builder marked lower-tier handoff as required",
            }
        )
    return items


def _field_gap_items(value: Any, field_name: str) -> list[dict[str, Any]]:
    if not value:
        return []
    if type(value) is dict:
        return [
            {
                "gap_type": f"{field_name}_present",
                "field_name": field_name,
                "reason": f"{field_name} still blocks bundle readiness",
                "items": deepcopy(value),
            }
        ]
    return [
        {
            "gap_type": f"{field_name}_present",
            "field_name": field_name,
            "reason": f"{field_name} still blocks bundle readiness",
            "items": deepcopy(value),
        }
    ]


def _unclear_patterns(
    patterns: list[Any],
    field_name: str,
) -> list[dict[str, Any]]:
    if patterns:
        unclear = []
        for index, pattern in enumerate(patterns):
            if not _pattern_clear(pattern):
                unclear.append(
                    {
                        "gap_type": "unclear_pattern",
                        "field_name": field_name,
                        "pattern_index": index,
                        "reason": "pattern must carry setup type, symbol, pair, and count context",
                        "pattern": deepcopy(pattern),
                    }
                )
        return unclear
    return [
        {
            "gap_type": "missing_pattern_coverage",
            "field_name": field_name,
            "reason": f"{field_name} must be explicit before the bundle is review-ready",
        }
    ]


def _pattern_clear(pattern: Any) -> bool:
    if type(pattern) is not dict:
        return False
    if type(pattern.get("count")) is not int or pattern["count"] <= 0:
        return False
    if not pattern.get("represented_setup_types"):
        return False
    if not pattern.get("represented_symbols"):
        return False
    pairs = pattern.get("represented_setup_type_symbol_pairs")
    if type(pairs) is not list or not pairs:
        return False
    return all(_pair_clear(pair) for pair in pairs)


def _pair_clear(pair: Any) -> bool:
    if type(pair) is not dict:
        return False
    return _clean_identity_value(pair.get("setup_type")) and _clean_identity_value(
        pair.get("symbol")
    )


def _unclear_repeated_fix_paths(
    repeated_fix_paths: Mapping[str, Any],
) -> list[dict[str, Any]]:
    unclear = []
    for fix_path, count in repeated_fix_paths.items():
        if type(count) is not int or count <= 1 or not _specific_fix_path(fix_path):
            unclear.append(
                {
                    "gap_type": "unclear_repeated_fix_path",
                    "field_name": "repeated_fix_paths",
                    "next_fix_path": deepcopy(fix_path),
                    "count": deepcopy(count),
                    "reason": "repeated fix path must name lower-tier local contract, fixture, test, evidence, diagnostics, packet, review, or readiness work",
                }
            )
    if not repeated_fix_paths:
        unclear.append(
            {
                "gap_type": "missing_repeated_fix_path",
                "field_name": "repeated_fix_paths",
                "reason": "bundle readiness requires repeated fix paths to be explicit",
            }
        )
    return unclear


def _gaps_need_regression(bundle_summary: Mapping[str, Any]) -> bool:
    return bool(
        bundle_summary["proof_gaps"]
        or bundle_summary["bundle_contract_gaps"]
        or bundle_summary["missing_evidence"]
        or bundle_summary["missing_evidence_by_setup_type"]
        or bundle_summary["missing_evidence_by_symbol"]
        or bundle_summary["missing_evidence_by_setup_type_symbol_pair"]
        or bundle_summary["setup_types_needing_more_evidence"]
        or bundle_summary["symbols_needing_more_evidence"]
        or bundle_summary["setup_type_symbol_pairs_needing_more_evidence"]
    )


def _readiness_decision(
    bundle_readiness_contract_gaps: list[dict[str, Any]],
    bundle_summary: Mapping[str, Any],
    ready: bool,
) -> str:
    if bundle_readiness_contract_gaps or bundle_summary["bundle_contract_gaps"]:
        return "blocked_by_bundle_readiness_contract_gap"
    if ready:
        return "ready_for_lower_tier_review"
    return "needs_more_evidence_before_lower_tier_review"


def _contract_gap(field_name: str, reason: str) -> dict[str, str]:
    return {
        "field_name": field_name,
        "gap_type": "bundle_readiness_contract_gap",
        "reason": reason,
    }


def _specific_fix_path(value: Any) -> bool:
    if type(value) is not str:
        return False
    normalized = value.strip().lower()
    return len(normalized) >= 12 and any(
        token in normalized for token in _SPECIFIC_FIX_PATH_TOKENS
    )


def _clean_identity_value(value: Any) -> bool:
    if type(value) is not str or not value.strip():
        return False
    normalized = value.strip().upper()
    if normalized.startswith("UNAVAILABLE"):
        return False
    return True


def _reject_forbidden_bundle_readiness_fields(
    value: Any,
    path: tuple[str, ...],
) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.lower()
            if (
                normalized_key in FORBIDDEN_SETUP_OUTCOME_FIELD_NAMES
                and normalized_key
                not in SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_RESULT_FIELDS
            ):
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden execution/trade field: {dotted_path}")
            _reject_forbidden_bundle_readiness_fields(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_forbidden_bundle_readiness_fields(nested_value, (*path, str(index)))
