"""Local-only setup outcome proof review readiness gating.

This module accepts one caller-provided in-memory setup outcome proof review
aggregate summary and returns one in-memory readiness summary. It does not
fetch data, write files, start shadow/live workflows, emit alerts, call
subprocesses, touch brokers/accounts/options/P&L, optimize rules, or make trade
decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.setup_outcome_proof import (
    FORBIDDEN_SETUP_OUTCOME_FIELD_NAMES,
)
from watcher_foundation.setup_outcome_review_aggregator import (
    SETUP_OUTCOME_REVIEW_AGGREGATOR_RESULT_FIELDS,
    SETUP_OUTCOME_REVIEW_OUTCOME_GROUPS,
)


SETUP_OUTCOME_REVIEW_READINESS_DECISIONS = (
    "ready_for_lower_tier_review",
    "needs_more_evidence_before_lower_tier_review",
    "blocked_by_review_contract_gap",
)

SETUP_OUTCOME_REVIEW_READINESS_RESULT_FIELDS = (
    "watch_only",
    "setup_outcome_review_readiness_only",
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
    "setup_types_needing_more_evidence",
    "represented_symbols",
    "symbols_needing_more_evidence",
    "represented_setup_type_symbol_pairs",
    "setup_type_symbol_pairs_needing_more_evidence",
    "outcome_groups_explicit",
    "outcome_group_counts",
    "missing_outcome_groups",
    "failure_diagnosis_clear_enough",
    "unclear_diagnoses",
    "repeated_fix_paths_clear_enough",
    "unclear_repeated_fix_paths",
    "regression_coverage_named",
    "missing_regression_coverage",
    "proof_gaps_blocking_review",
    "proof_gaps",
    "missing_evidence",
    "readiness_gap_counts",
    "repeated_next_fix_paths",
    "repeated_regression_needs",
    "review_contract_gaps",
    "group_review_complete_enough_to_trust",
    "ready_for_lower_tier_review",
    "lower_tier_review_decision",
    "lower_tier_handoff_required",
    "lower_tier_handoff_items",
    "rejected_records",
    "proof_limited_records",
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

_EXPECTED_TRUE_REVIEW_FIELDS = (
    "watch_only",
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

_EXPECTED_FALSE_REVIEW_FIELDS = (
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
    "review",
    "packet",
    "diagnostics",
)


def evaluate_setup_outcome_review_readiness(
    review_summary: dict[str, Any],
) -> dict[str, Any]:
    """Return one in-memory readiness gate summary for an aggregate review."""
    if type(review_summary) is not dict:
        raise TypeError(
            "Setup outcome review readiness input must be a dict"
        )

    _validate_review_summary(review_summary)

    outcome_group_counts = {
        group_name: len(review_summary["outcome_groups"][group_name])
        for group_name in SETUP_OUTCOME_REVIEW_OUTCOME_GROUPS
    }
    missing_outcome_groups = [
        group_name
        for group_name, count in outcome_group_counts.items()
        if count == 0
    ]
    review_contract_gaps = _review_contract_gaps(review_summary, missing_outcome_groups)
    unclear_diagnoses = _unclear_diagnoses(review_summary)
    unclear_repeated_fix_paths = _unclear_repeated_fix_paths(review_summary)
    missing_regression_coverage = _missing_regression_coverage(review_summary)
    evidence_items = _evidence_gap_items(review_summary, missing_outcome_groups)
    setup_types_needing_more_evidence = _identities_needing_more_evidence(
        evidence_items,
        review_summary["represented_setup_types"],
        "setup_type",
    )
    symbols_needing_more_evidence = _identities_needing_more_evidence(
        evidence_items,
        review_summary["represented_symbols"],
        "symbol",
    )
    pairs_needing_more_evidence = _pairs_needing_more_evidence(
        evidence_items,
        review_summary["represented_setup_type_symbol_pairs"],
    )
    proof_gaps_blocking = bool(
        review_summary["proof_gaps"]
        or review_summary["missing_evidence"]
        or review_summary["rejected_records"]
        or review_summary["proof_limited_records"]
        or review_summary["readiness_gap_counts"]
        or missing_outcome_groups
    )
    repeated_fix_paths_clear = (
        not review_summary["readiness_gap_counts"]
        or (
            bool(review_summary["repeated_next_fix_paths"])
            and not unclear_repeated_fix_paths
        )
    )
    regression_named = (
        not proof_gaps_blocking
        or (
            bool(review_summary["regression_needed"])
            and not missing_regression_coverage
        )
    )
    lower_tier_handoff_required = bool(
        review_summary["lower_tier_handoff_required"]
        or proof_gaps_blocking
        or unclear_diagnoses
        or not repeated_fix_paths_clear
        or not regression_named
        or review_contract_gaps
    )
    complete_enough = not lower_tier_handoff_required
    decision = _lower_tier_decision(
        review_summary,
        review_contract_gaps,
        complete_enough,
    )

    return {
        "watch_only": True,
        "setup_outcome_review_readiness_only": True,
        "setup_outcome_review_aggregator_only": True,
        "setup_outcome_packet_readiness_only": True,
        "setup_outcome_evidence_packet_only": True,
        "setup_outcome_diagnostics_only": True,
        "setup_outcome_proof_only": True,
        "final_viability_proven": False,
        "optimization_started": False,
        "no_rule_change_started": True,
        "packet_summary_count": review_summary["packet_summary_count"],
        "reviewed_packets": deepcopy(review_summary["reviewed_packets"]),
        "represented_setup_types": deepcopy(review_summary["represented_setup_types"]),
        "setup_types_needing_more_evidence": setup_types_needing_more_evidence,
        "represented_symbols": deepcopy(review_summary["represented_symbols"]),
        "symbols_needing_more_evidence": symbols_needing_more_evidence,
        "represented_setup_type_symbol_pairs": deepcopy(
            review_summary["represented_setup_type_symbol_pairs"]
        ),
        "setup_type_symbol_pairs_needing_more_evidence": pairs_needing_more_evidence,
        "outcome_groups_explicit": not missing_outcome_groups,
        "outcome_group_counts": outcome_group_counts,
        "missing_outcome_groups": missing_outcome_groups,
        "failure_diagnosis_clear_enough": not unclear_diagnoses,
        "unclear_diagnoses": unclear_diagnoses,
        "repeated_fix_paths_clear_enough": repeated_fix_paths_clear,
        "unclear_repeated_fix_paths": unclear_repeated_fix_paths,
        "regression_coverage_named": regression_named,
        "missing_regression_coverage": missing_regression_coverage,
        "proof_gaps_blocking_review": proof_gaps_blocking,
        "proof_gaps": deepcopy(review_summary["proof_gaps"]),
        "missing_evidence": deepcopy(review_summary["missing_evidence"]),
        "readiness_gap_counts": deepcopy(review_summary["readiness_gap_counts"]),
        "repeated_next_fix_paths": deepcopy(review_summary["repeated_next_fix_paths"]),
        "repeated_regression_needs": deepcopy(
            review_summary["repeated_regression_needs"]
        ),
        "review_contract_gaps": review_contract_gaps,
        "group_review_complete_enough_to_trust": complete_enough,
        "ready_for_lower_tier_review": complete_enough,
        "lower_tier_review_decision": decision,
        "lower_tier_handoff_required": lower_tier_handoff_required,
        "lower_tier_handoff_items": deepcopy(
            review_summary["lower_tier_handoff_items"]
        ),
        "rejected_records": deepcopy(review_summary["rejected_records"]),
        "proof_limited_records": deepcopy(review_summary["proof_limited_records"]),
        "setup_type_separated": review_summary["setup_type_separated"],
        "symbol_separated": review_summary["symbol_separated"],
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


def _validate_review_summary(review_summary: Mapping[str, Any]) -> None:
    missing_fields = [
        field_name
        for field_name in SETUP_OUTCOME_REVIEW_AGGREGATOR_RESULT_FIELDS
        if field_name not in review_summary
    ]
    if missing_fields:
        raise ValueError(
            "Missing required setup outcome review aggregate fields: "
            + ", ".join(missing_fields)
        )

    unexpected_fields = [
        field_name
        for field_name in review_summary
        if field_name not in SETUP_OUTCOME_REVIEW_AGGREGATOR_RESULT_FIELDS
    ]
    if unexpected_fields:
        raise ValueError(
            "Unexpected setup outcome review aggregate fields: "
            + ", ".join(unexpected_fields)
        )

    _reject_forbidden_readiness_fields(review_summary, path=())

    for field_name in _EXPECTED_TRUE_REVIEW_FIELDS:
        if review_summary[field_name] is not True:
            raise ValueError(
                f"Setup outcome review readiness requires {field_name}=True"
            )
    for field_name in _EXPECTED_FALSE_REVIEW_FIELDS:
        if review_summary[field_name] is not False:
            raise ValueError(
                f"Setup outcome review readiness requires {field_name}=False"
            )

    for field_name in (
        "packet_summary_count",
    ):
        if type(review_summary[field_name]) is not int:
            raise TypeError(
                f"Setup outcome review readiness {field_name} must be an int"
            )
        if review_summary[field_name] < 0:
            raise ValueError(
                f"Setup outcome review readiness {field_name} must be non-negative"
            )

    for field_name in (
        "reviewed_packets",
        "represented_setup_types",
        "represented_symbols",
        "represented_setup_type_symbol_pairs",
        "proof_gaps",
        "missing_evidence",
        "regression_needed",
        "lower_tier_handoff_items",
        "rejected_records",
        "proof_limited_records",
    ):
        if type(review_summary[field_name]) is not list:
            raise TypeError(
                f"Setup outcome review readiness {field_name} must be a list"
            )
    for field_name in (
        "outcome_groups",
        "readiness_gap_counts",
        "repeated_next_fix_paths",
        "repeated_regression_needs",
    ):
        if type(review_summary[field_name]) is not dict:
            raise TypeError(
                f"Setup outcome review readiness {field_name} must be a dict"
            )
    if set(review_summary["outcome_groups"]) != set(SETUP_OUTCOME_REVIEW_OUTCOME_GROUPS):
        raise ValueError(
            "Setup outcome review readiness outcome_groups must include worked, "
            "failed, inconclusive, pending, stale, invalidated, and missing_evidence"
        )
    for group_name, items in review_summary["outcome_groups"].items():
        if type(items) is not list:
            raise TypeError(
                f"Setup outcome review readiness outcome_groups[{group_name}] "
                "must be a list"
            )
    if review_summary["packet_summary_count"] != len(review_summary["reviewed_packets"]):
        raise ValueError(
            "Setup outcome review readiness packet_summary_count must match "
            "reviewed_packets"
        )


def _review_contract_gaps(
    review_summary: Mapping[str, Any],
    missing_outcome_groups: list[str],
) -> list[dict[str, Any]]:
    gaps = []
    if review_summary["setup_type_separated"] is not True:
        gaps.append(_contract_gap("setup_type", "setup type was not kept separate"))
    if review_summary["symbol_separated"] is not True:
        gaps.append(_contract_gap("symbol", "symbol was not kept separate"))
    if not review_summary["represented_setup_types"]:
        gaps.append(_contract_gap("represented_setup_types", "no setup types represented"))
    if not review_summary["represented_symbols"]:
        gaps.append(_contract_gap("represented_symbols", "no symbols represented"))
    for group_name in missing_outcome_groups:
        gaps.append(
            {
                "field_name": "outcome_groups",
                "gap_type": "absent_outcome_coverage",
                "outcome_group": group_name,
                "reason": f"{group_name} outcome coverage was not present",
            }
        )
    return gaps


def _contract_gap(field_name: str, reason: str) -> dict[str, str]:
    return {
        "field_name": field_name,
        "gap_type": "review_contract_gap",
        "reason": reason,
    }


def _unclear_diagnoses(review_summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    unclear = []
    if review_summary["readiness_gap_counts"].get("unclear_diagnosis"):
        unclear.append(
            {
                "gap_type": "unclear_diagnosis",
                "field_name": "readiness_gap_counts",
                "reason": "aggregate review carried unclear diagnosis gaps",
                "count": review_summary["readiness_gap_counts"]["unclear_diagnosis"],
            }
        )
    for item in review_summary["outcome_groups"]["failed"]:
        if type(item) is dict and item.get("lower_tier_handoff_required") is True:
            unclear.append(
                {
                    "gap_type": "failed_outcome_needs_lower_tier_handoff",
                    "field_name": "outcome_groups.failed",
                    "packet_item_id": deepcopy(item.get("packet_item_id", "UNAVAILABLE")),
                    "setup_type": deepcopy(item.get("setup_type")),
                    "symbol": deepcopy(item.get("symbol")),
                    "reason": "failed outcome still needs lower-tier diagnostic review",
                }
            )
    return unclear


def _unclear_repeated_fix_paths(
    review_summary: Mapping[str, Any],
) -> list[dict[str, Any]]:
    unclear = []
    for fix_path, count in review_summary["repeated_next_fix_paths"].items():
        if not _specific_fix_path(fix_path):
            unclear.append(
                {
                    "gap_type": "unclear_repeated_fix_path",
                    "field_name": "repeated_next_fix_paths",
                    "next_fix_path": deepcopy(fix_path),
                    "count": count,
                    "reason": "repeated fix path must name a lower-tier local review area",
                }
            )
    if review_summary["readiness_gap_counts"] and not review_summary["repeated_next_fix_paths"]:
        unclear.append(
            {
                "gap_type": "missing_repeated_fix_path",
                "field_name": "repeated_next_fix_paths",
                "reason": "readiness gaps need named repeated lower-tier fix paths",
            }
        )
    return unclear


def _missing_regression_coverage(
    review_summary: Mapping[str, Any],
) -> list[dict[str, Any]]:
    missing = []
    for regression in review_summary["regression_needed"]:
        if not _named_regression(regression):
            missing.append(
                {
                    "gap_type": "missing_regression_coverage",
                    "field_name": "regression_needed",
                    "regression_needed": deepcopy(regression),
                    "reason": "regression coverage must be named before broader changes",
                }
            )
    if (
        review_summary["readiness_gap_counts"]
        or review_summary["proof_gaps"]
        or review_summary["missing_evidence"]
    ) and not review_summary["regression_needed"]:
        missing.append(
            {
                "gap_type": "missing_regression_coverage",
                "field_name": "regression_needed",
                "reason": "proof-blocking gaps require named regression coverage",
            }
        )
    return missing


def _evidence_gap_items(
    review_summary: Mapping[str, Any],
    missing_outcome_groups: list[str],
) -> list[Any]:
    items = []
    for field_name in (
        "missing_evidence",
        "proof_gaps",
        "lower_tier_handoff_items",
        "rejected_records",
        "proof_limited_records",
    ):
        items.extend(deepcopy(review_summary[field_name]))
    for group_name in missing_outcome_groups:
        items.append(
            {
                "gap_type": "absent_outcome_coverage",
                "outcome_group": group_name,
                "represented_setup_types": deepcopy(
                    review_summary["represented_setup_types"]
                ),
                "represented_symbols": deepcopy(review_summary["represented_symbols"]),
                "represented_setup_type_symbol_pairs": deepcopy(
                    review_summary["represented_setup_type_symbol_pairs"]
                ),
            }
        )
    return items


def _identities_needing_more_evidence(
    evidence_items: list[Any],
    represented_values: list[Any],
    field_name: str,
) -> list[Any]:
    values = []
    represented_key = f"represented_{field_name}s"
    for item in evidence_items:
        if type(item) is not dict:
            continue
        value = item.get(field_name)
        if _clean_identity_value(value):
            _append_unique(values, value)
        for represented_value in item.get(represented_key, []):
            if _clean_identity_value(represented_value):
                _append_unique(values, represented_value)
    if evidence_items and not values:
        for represented_value in represented_values:
            if _clean_identity_value(represented_value):
                _append_unique(values, represented_value)
    return values


def _pairs_needing_more_evidence(
    evidence_items: list[Any],
    represented_pairs: list[Any],
) -> list[dict[str, str]]:
    pairs = []
    for item in evidence_items:
        if type(item) is not dict:
            continue
        setup_type = item.get("setup_type")
        symbol = item.get("symbol")
        if _clean_identity_value(setup_type) and _clean_identity_value(symbol):
            _append_unique(
                pairs,
                {"setup_type": str(setup_type), "symbol": str(symbol)},
            )
        for pair in item.get("represented_setup_type_symbol_pairs", []):
            if type(pair) is not dict:
                continue
            pair_setup_type = pair.get("setup_type")
            pair_symbol = pair.get("symbol")
            if _clean_identity_value(pair_setup_type) and _clean_identity_value(pair_symbol):
                _append_unique(
                    pairs,
                    {"setup_type": str(pair_setup_type), "symbol": str(pair_symbol)},
                )
    if evidence_items and not pairs:
        for pair in represented_pairs:
            if type(pair) is not dict:
                continue
            setup_type = pair.get("setup_type")
            symbol = pair.get("symbol")
            if _clean_identity_value(setup_type) and _clean_identity_value(symbol):
                _append_unique(
                    pairs,
                    {"setup_type": str(setup_type), "symbol": str(symbol)},
                )
    return pairs


def _lower_tier_decision(
    review_summary: Mapping[str, Any],
    review_contract_gaps: list[dict[str, Any]],
    complete_enough: bool,
) -> str:
    if review_contract_gaps or (
        review_summary["proof_continuation_decision"]
        == "blocked_by_readiness_contract_gap"
    ):
        return "blocked_by_review_contract_gap"
    if complete_enough:
        return "ready_for_lower_tier_review"
    return "needs_more_evidence_before_lower_tier_review"


def _specific_fix_path(value: Any) -> bool:
    if type(value) is not str:
        return False
    normalized = value.strip().lower()
    return len(normalized) >= 12 and any(
        token in normalized for token in _SPECIFIC_FIX_PATH_TOKENS
    )


def _named_regression(value: Any) -> bool:
    if type(value) is not str:
        return False
    normalized = value.strip().lower()
    return len(normalized) >= 12 and "regression" in normalized and any(
        token in normalized for token in ("test", "coverage", "add", "keep", "preserve")
    )


def _clean_identity_value(value: Any) -> bool:
    if type(value) is not str or not value.strip():
        return False
    normalized = value.strip().upper()
    if normalized.startswith("UNAVAILABLE"):
        return False
    return True


def _append_unique(target: list[Any], value: Any) -> None:
    copied = deepcopy(value)
    if copied not in target:
        target.append(copied)


def _reject_forbidden_readiness_fields(value: Any, path: tuple[str, ...]) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.lower()
            if (
                normalized_key in FORBIDDEN_SETUP_OUTCOME_FIELD_NAMES
                and normalized_key not in SETUP_OUTCOME_REVIEW_AGGREGATOR_RESULT_FIELDS
            ):
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden execution/trade field: {dotted_path}")
            _reject_forbidden_readiness_fields(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_forbidden_readiness_fields(nested_value, (*path, str(index)))
