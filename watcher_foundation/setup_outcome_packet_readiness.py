"""Local-only setup outcome evidence packet readiness evaluation.

This module accepts one caller-provided in-memory setup outcome evidence packet
summary and returns one in-memory readiness summary. It does not fetch data,
write files, start shadow/live workflows, emit alerts, call subprocesses, touch
brokers/accounts/options/P&L, optimize rules, or make trade decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.setup_outcome_evidence_packet import (
    SETUP_OUTCOME_EVIDENCE_PACKET_RESULT_FIELDS,
)
from watcher_foundation.setup_outcome_proof import (
    FORBIDDEN_SETUP_OUTCOME_FIELD_NAMES,
)


SETUP_OUTCOME_PACKET_READINESS_STATUSES = (
    "ready_for_lower_tier_review",
    "needs_lower_tier_evidence_fix",
    "blocked_by_packet_contract_gap",
)

SETUP_OUTCOME_PACKET_READINESS_RESULT_FIELDS = (
    "watch_only",
    "setup_outcome_packet_readiness_only",
    "setup_outcome_evidence_packet_only",
    "setup_outcome_diagnostics_only",
    "setup_outcome_proof_only",
    "final_viability_proven",
    "optimization_started",
    "no_rule_change_started",
    "records_processed",
    "records_accepted",
    "records_rejected",
    "packet_item_count",
    "readiness_status",
    "complete_enough_to_review",
    "ready_for_lower_tier_review",
    "readiness_gaps",
    "missing_evidence",
    "packet_items",
    "items_by_setup_type",
    "setup_type_separated",
    "symbol_separated",
    "diagnosis_clear_enough",
    "next_fix_path_clear_enough",
    "regression_named",
    "lower_tier_handoff_required",
    "lower_tier_handoff_items",
    "rejected_records",
    "proof_limited_records",
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

SETUP_OUTCOME_PACKET_READINESS_ITEM_FIELDS = (
    "packet_item_id",
    "setup_type",
    "symbol",
    "readiness_status",
    "complete_enough_to_review",
    "missing_evidence",
    "readiness_gaps",
    "setup_type_separated",
    "symbol_separated",
    "diagnosis_clear_enough",
    "next_fix_path_clear_enough",
    "regression_named",
    "lower_tier_handoff_required",
    "lower_tier_handoff_reason",
    "no_hindsight_boundary_confirmed",
    "no_trade_boundary_confirmed",
    "no_optimization_boundary_confirmed",
)

_EXPECTED_TRUE_PACKET_FIELDS = (
    "watch_only",
    "setup_outcome_evidence_packet_only",
    "setup_outcome_diagnostics_only",
    "setup_outcome_proof_only",
    "no_rule_change_started",
    "no_hindsight_boundary_preserved",
    "no_trade_boundary_preserved",
)

_EXPECTED_FALSE_PACKET_FIELDS = (
    "final_viability_proven",
    "optimization_started",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

_REQUIRED_REVIEW_ITEM_FIELDS = (
    "setup_type",
    "symbol",
    "what_setup_appeared",
    "what_happened_after_setup",
    "why_it_happened",
    "evidence_support",
    "next_fix_path",
    "regression_needed",
    "lower_tier_handoff_required",
    "no_hindsight_boundary_confirmed",
    "no_trade_boundary_confirmed",
)

_VAGUE_TEXT = {
    "bad",
    "good",
    "weak",
    "strong",
    "unclear",
    "unknown",
    "needs review",
    "fix later",
    "todo",
    "tbd",
    "n/a",
}


def evaluate_setup_outcome_packet_readiness(
    packet_summary: dict[str, Any],
) -> dict[str, Any]:
    """Return one in-memory setup outcome evidence packet readiness summary."""
    if type(packet_summary) is not dict:
        raise TypeError(
            "Setup outcome packet readiness input must be a dict"
        )

    _validate_packet_summary_contract(packet_summary)

    item_summaries = [
        _evaluate_packet_item(index, item)
        for index, item in enumerate(packet_summary["packet_items"])
    ]
    grouping_gaps = _grouping_gaps(packet_summary, item_summaries)
    readiness_gaps = []
    for item_summary in item_summaries:
        readiness_gaps.extend(deepcopy(item_summary["readiness_gaps"]))
    readiness_gaps.extend(grouping_gaps)
    readiness_gaps.extend(_summary_evidence_gaps(packet_summary))

    lower_tier_handoff_items = [
        deepcopy(item_summary)
        for item_summary in item_summaries
        if item_summary["lower_tier_handoff_required"] is True
    ]
    missing_evidence = _collect_missing_evidence(packet_summary, item_summaries)
    complete_enough = not readiness_gaps
    ready_for_lower_tier = complete_enough
    readiness_status = _readiness_status(
        complete_enough,
        grouping_gaps,
        packet_summary,
        item_summaries,
    )

    setup_type_separated = all(
        item["setup_type_separated"] is True for item in item_summaries
    ) and not any(gap["gap_type"] == "setup_symbol_grouping" for gap in grouping_gaps)
    symbol_separated = all(
        item["symbol_separated"] is True for item in item_summaries
    ) and not any(gap["gap_type"] == "setup_symbol_grouping" for gap in grouping_gaps)

    return {
        "watch_only": True,
        "setup_outcome_packet_readiness_only": True,
        "setup_outcome_evidence_packet_only": True,
        "setup_outcome_diagnostics_only": True,
        "setup_outcome_proof_only": True,
        "final_viability_proven": False,
        "optimization_started": False,
        "no_rule_change_started": True,
        "records_processed": packet_summary["records_processed"],
        "records_accepted": packet_summary["records_accepted"],
        "records_rejected": packet_summary["records_rejected"],
        "packet_item_count": packet_summary["packet_item_count"],
        "readiness_status": readiness_status,
        "complete_enough_to_review": complete_enough,
        "ready_for_lower_tier_review": ready_for_lower_tier,
        "readiness_gaps": deepcopy(readiness_gaps),
        "missing_evidence": missing_evidence,
        "packet_items": deepcopy(item_summaries),
        "items_by_setup_type": _group_item_summaries(item_summaries),
        "setup_type_separated": setup_type_separated,
        "symbol_separated": symbol_separated,
        "diagnosis_clear_enough": all(
            item["diagnosis_clear_enough"] is True for item in item_summaries
        ),
        "next_fix_path_clear_enough": all(
            item["next_fix_path_clear_enough"] is True for item in item_summaries
        ),
        "regression_named": all(
            item["regression_named"] is True for item in item_summaries
        ),
        "lower_tier_handoff_required": bool(
            lower_tier_handoff_items
            or packet_summary["lower_tier_handoff_required"] is True
            or packet_summary["records_rejected"]
            or packet_summary["proof_limited_records"]
            or readiness_status != "ready_for_lower_tier_review"
        ),
        "lower_tier_handoff_items": lower_tier_handoff_items,
        "rejected_records": deepcopy(packet_summary["rejected_records"]),
        "proof_limited_records": deepcopy(packet_summary["proof_limited_records"]),
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


def _validate_packet_summary_contract(packet_summary: Mapping[str, Any]) -> None:
    missing_fields = [
        field_name
        for field_name in SETUP_OUTCOME_EVIDENCE_PACKET_RESULT_FIELDS
        if field_name not in packet_summary
    ]
    if missing_fields:
        raise ValueError(
            "Missing required setup outcome evidence packet fields: "
            + ", ".join(missing_fields)
        )

    unexpected_fields = [
        field_name
        for field_name in packet_summary
        if field_name not in SETUP_OUTCOME_EVIDENCE_PACKET_RESULT_FIELDS
    ]
    if unexpected_fields:
        raise ValueError(
            "Unexpected setup outcome evidence packet fields: "
            + ", ".join(unexpected_fields)
        )

    _reject_forbidden_readiness_fields(packet_summary, path=())

    for field_name in _EXPECTED_TRUE_PACKET_FIELDS:
        if packet_summary[field_name] is not True:
            raise ValueError(
                f"Setup outcome packet readiness requires {field_name}=True"
            )
    for field_name in _EXPECTED_FALSE_PACKET_FIELDS:
        if packet_summary[field_name] is not False:
            raise ValueError(
                f"Setup outcome packet readiness requires {field_name}=False"
            )

    for field_name in ("records_processed", "records_accepted", "records_rejected", "packet_item_count"):
        if type(packet_summary[field_name]) is not int:
            raise TypeError(
                f"Setup outcome packet readiness {field_name} must be an int"
            )
        if packet_summary[field_name] < 0:
            raise ValueError(
                f"Setup outcome packet readiness {field_name} must be non-negative"
            )

    for field_name in (
        "packet_items",
        "lower_tier_handoff_items",
        "missing_evidence",
        "regression_needed",
        "rejected_records",
        "proof_limited_records",
    ):
        if type(packet_summary[field_name]) is not list:
            raise TypeError(
                f"Setup outcome packet readiness {field_name} must be a list"
            )
    for field_name in ("packet_items_by_setup_type", "next_fix_paths"):
        if type(packet_summary[field_name]) is not dict:
            raise TypeError(
                f"Setup outcome packet readiness {field_name} must be a dict"
            )
    if packet_summary["lower_tier_handoff_required"] not in {True, False}:
        raise TypeError(
            "Setup outcome packet readiness lower_tier_handoff_required must be a bool"
        )
    if packet_summary["packet_item_count"] != len(packet_summary["packet_items"]):
        raise ValueError(
            "Setup outcome packet readiness packet_item_count must match packet_items"
        )


def _evaluate_packet_item(index: int, item: Any) -> dict[str, Any]:
    if type(item) is not dict:
        return _blocked_item_summary(
            index,
            "packet item must be a dict",
            gap_type="packet_item_contract",
        )

    gaps = []
    for field_name in _REQUIRED_REVIEW_ITEM_FIELDS:
        if field_name not in item:
            gaps.append(_gap(index, "missing_packet_item_field", field_name))

    setup_type_separated = _clean_identity_value(item.get("setup_type"))
    symbol_separated = _clean_identity_value(item.get("symbol"))
    if not setup_type_separated:
        gaps.append(_gap(index, "setup_type_separation", "setup_type"))
    if not symbol_separated:
        gaps.append(_gap(index, "symbol_separation", "symbol"))
    if _identity_merged(item.get("setup_type"), item.get("symbol")):
        gaps.append(_gap(index, "setup_symbol_merged", "setup_type/symbol"))

    missing_evidence = _item_missing_evidence(item)
    if missing_evidence:
        gaps.append(_gap(index, "missing_evidence", "missing_evidence"))

    diagnosis_clear = _diagnosis_clear(item)
    if not diagnosis_clear:
        gaps.append(_gap(index, "unclear_diagnosis", "why_it_happened"))

    next_fix_clear = _specific_text(item.get("next_fix_path")) and _fix_path_has_area(item)
    if not next_fix_clear:
        gaps.append(_gap(index, "unclear_next_fix_path", "next_fix_path"))

    regression_named = _named_regression(item.get("regression_needed"))
    if not regression_named:
        gaps.append(_gap(index, "missing_regression", "regression_needed"))

    if item.get("no_hindsight_boundary_confirmed") is not True:
        gaps.append(_gap(index, "boundary_gap", "no_hindsight_boundary_confirmed"))
    if item.get("no_trade_boundary_confirmed") is not True:
        gaps.append(_gap(index, "boundary_gap", "no_trade_boundary_confirmed"))

    handoff_required = (
        bool(gaps)
        or item.get("lower_tier_handoff_required") is True
        or bool(missing_evidence)
    )

    return {
        "packet_item_id": deepcopy(item.get("packet_item_id", f"UNAVAILABLE-{index + 1}")),
        "setup_type": deepcopy(item.get("setup_type")),
        "symbol": deepcopy(item.get("symbol")),
        "readiness_status": (
            "ready_for_lower_tier_review"
            if not gaps and item.get("lower_tier_handoff_required") is not True
            else "needs_lower_tier_evidence_fix"
        ),
        "complete_enough_to_review": (
            not gaps and item.get("lower_tier_handoff_required") is not True
        ),
        "missing_evidence": deepcopy(missing_evidence),
        "readiness_gaps": deepcopy(gaps),
        "setup_type_separated": setup_type_separated,
        "symbol_separated": symbol_separated,
        "diagnosis_clear_enough": diagnosis_clear,
        "next_fix_path_clear_enough": next_fix_clear,
        "regression_named": regression_named,
        "lower_tier_handoff_required": handoff_required,
        "lower_tier_handoff_reason": _handoff_reason(item, gaps, missing_evidence),
        "no_hindsight_boundary_confirmed": item.get("no_hindsight_boundary_confirmed") is True,
        "no_trade_boundary_confirmed": item.get("no_trade_boundary_confirmed") is True,
        "no_optimization_boundary_confirmed": True,
    }


def _blocked_item_summary(index: int, reason: str, gap_type: str) -> dict[str, Any]:
    gap = {
        "packet_item_index": index,
        "gap_type": gap_type,
        "field_name": "packet_items",
        "reason": reason,
    }
    return {
        "packet_item_id": f"UNAVAILABLE-{index + 1}",
        "setup_type": None,
        "symbol": None,
        "readiness_status": "blocked_by_packet_contract_gap",
        "complete_enough_to_review": False,
        "missing_evidence": [],
        "readiness_gaps": [gap],
        "setup_type_separated": False,
        "symbol_separated": False,
        "diagnosis_clear_enough": False,
        "next_fix_path_clear_enough": False,
        "regression_named": False,
        "lower_tier_handoff_required": True,
        "lower_tier_handoff_reason": reason,
        "no_hindsight_boundary_confirmed": False,
        "no_trade_boundary_confirmed": False,
        "no_optimization_boundary_confirmed": True,
    }


def _summary_evidence_gaps(packet_summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    gaps = []
    if packet_summary["records_rejected"]:
        gaps.append(
            _summary_gap(
                "rejected_proof_records",
                "rejected_records",
                "rejected proof records require lower-tier contract or fixture review",
            )
        )
    if packet_summary["proof_limited_records"]:
        gaps.append(
            _summary_gap(
                "proof_limited_records",
                "proof_limited_records",
                "proof-limited records require lower-tier evidence review",
            )
        )
    if packet_summary["lower_tier_handoff_required"] is True:
        gaps.append(
            _summary_gap(
                "lower_tier_handoff_required",
                "lower_tier_handoff_required",
                "packet builder marked lower-tier handoff as required",
            )
        )
    return gaps


def _grouping_gaps(
    packet_summary: Mapping[str, Any],
    item_summaries: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped = packet_summary["packet_items_by_setup_type"]
    gaps = []
    for item in item_summaries:
        setup_type = item["setup_type"]
        symbol = item["symbol"]
        if not _clean_identity_value(setup_type) or not _clean_identity_value(symbol):
            continue
        if setup_type not in grouped:
            gaps.append(
                _summary_gap(
                    "setup_symbol_grouping",
                    "packet_items_by_setup_type",
                    "setup type is absent from grouped packet output",
                )
            )
            continue
        if type(grouped[setup_type]) is not dict or symbol not in grouped[setup_type]:
            gaps.append(
                _summary_gap(
                    "setup_symbol_grouping",
                    "packet_items_by_setup_type",
                    "symbol is absent beneath its setup type in grouped packet output",
                )
            )
    for setup_type, symbols in grouped.items():
        if not _clean_identity_value(setup_type) or type(symbols) is not dict:
            gaps.append(
                _summary_gap(
                    "setup_symbol_grouping",
                    "packet_items_by_setup_type",
                    "grouped packet output must use setup type keys with nested symbol keys",
                )
            )
            continue
        for symbol, records in symbols.items():
            if not _clean_identity_value(symbol) or type(records) is not list:
                gaps.append(
                    _summary_gap(
                        "setup_symbol_grouping",
                        "packet_items_by_setup_type",
                        "grouped packet output must keep symbol keys separate from setup type",
                    )
                )
    return gaps


def _readiness_status(
    complete_enough: bool,
    grouping_gaps: list[dict[str, Any]],
    packet_summary: Mapping[str, Any],
    item_summaries: list[dict[str, Any]],
) -> str:
    if complete_enough:
        return "ready_for_lower_tier_review"
    if grouping_gaps or any(
        item["setup_type_separated"] is not True or item["symbol_separated"] is not True
        for item in item_summaries
    ):
        return "blocked_by_packet_contract_gap"
    if packet_summary["records_rejected"]:
        return "blocked_by_packet_contract_gap"
    return "needs_lower_tier_evidence_fix"


def _collect_missing_evidence(
    packet_summary: Mapping[str, Any],
    item_summaries: list[dict[str, Any]],
) -> list[Any]:
    missing = []
    missing.extend(deepcopy(packet_summary["missing_evidence"]))
    for item in item_summaries:
        missing.extend(deepcopy(item["missing_evidence"]))
    return missing


def _group_item_summaries(
    item_summaries: list[dict[str, Any]],
) -> dict[str, dict[str, list[dict[str, Any]]]]:
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for item in item_summaries:
        setup_type = item["setup_type"] if _clean_identity_value(item["setup_type"]) else "UNAVAILABLE_SETUP_TYPE"
        symbol = item["symbol"] if _clean_identity_value(item["symbol"]) else "UNAVAILABLE_SYMBOL"
        grouped.setdefault(str(setup_type), {})
        grouped[str(setup_type)].setdefault(str(symbol), [])
        grouped[str(setup_type)][str(symbol)].append(deepcopy(item))
    return grouped


def _item_missing_evidence(item: Mapping[str, Any]) -> list[Any]:
    missing = []
    item_missing = item.get("missing_evidence")
    if type(item_missing) is list:
        missing.extend(deepcopy(item_missing))
    elif item_missing:
        missing.append(deepcopy(item_missing))
    evidence_support = item.get("evidence_support")
    if type(evidence_support) is not dict or not _has_evidence_support(evidence_support):
        missing.append(
            {
                "field_name": "evidence_support",
                "status": "missing_evidence",
                "reason": "packet item lacks explicit evidence support",
            }
        )
    return missing


def _has_evidence_support(evidence_support: Mapping[str, Any]) -> bool:
    for field_name in ("evidence_refs", "evidence_supports", "after_setup_evidence"):
        value = evidence_support.get(field_name)
        if value:
            return True
    return False


def _diagnosis_clear(item: Mapping[str, Any]) -> bool:
    what_happened = _specific_text(item.get("what_happened_after_setup"))
    why = item.get("why_it_happened")
    if type(why) is dict:
        return what_happened and bool(why.get("diagnostic_category")) and bool(
            why.get("likely_cause_candidates")
        )
    return what_happened and _specific_text(why)


def _specific_text(value: Any) -> bool:
    if type(value) is not str:
        return False
    normalized = value.strip().lower()
    return len(normalized) >= 12 and normalized not in _VAGUE_TEXT


def _fix_path_has_area(item: Mapping[str, Any]) -> bool:
    area = item.get("affected_system_area")
    if type(area) is str and area:
        return True
    path = item.get("next_fix_path")
    if type(path) is str:
        normalized = path.lower()
        return any(token in normalized for token in ("contract", "fixture", "test", "evidence", "review"))
    return False


def _named_regression(value: Any) -> bool:
    if not _specific_text(value):
        return False
    normalized = value.lower()
    return "regression" in normalized and any(
        token in normalized for token in ("test", "coverage", "preserve", "add", "keep")
    )


def _clean_identity_value(value: Any) -> bool:
    if type(value) is not str or not value.strip():
        return False
    normalized = value.strip().upper()
    if normalized.startswith("UNAVAILABLE"):
        return False
    return True


def _identity_merged(setup_type: Any, symbol: Any) -> bool:
    if type(setup_type) is str and any(separator in setup_type for separator in ("/", "|", "::")):
        return True
    if type(symbol) is str and any(separator in symbol for separator in ("/", "|", "::")):
        return True
    return False


def _handoff_reason(
    item: Mapping[str, Any],
    gaps: list[dict[str, Any]],
    missing_evidence: list[Any],
) -> str:
    if missing_evidence:
        return "missing or unavailable packet evidence requires lower-tier review"
    if gaps:
        return "packet readiness gaps require lower-tier review before broader changes"
    if item.get("lower_tier_handoff_required") is True:
        return str(item.get("lower_tier_handoff_reason", "packet item requested lower-tier handoff"))
    return "not required by packet readiness"


def _gap(index: int, gap_type: str, field_name: str) -> dict[str, Any]:
    return {
        "packet_item_index": index,
        "gap_type": gap_type,
        "field_name": field_name,
        "reason": _gap_reason(gap_type, field_name),
    }


def _summary_gap(gap_type: str, field_name: str, reason: str) -> dict[str, Any]:
    return {
        "packet_item_index": None,
        "gap_type": gap_type,
        "field_name": field_name,
        "reason": reason,
    }


def _gap_reason(gap_type: str, field_name: str) -> str:
    reasons = {
        "missing_packet_item_field": "packet item is missing a required review field",
        "setup_type_separation": "setup type must be a separate explicit field",
        "symbol_separation": "symbol must be a separate explicit field",
        "setup_symbol_merged": "setup type and symbol must not be merged into one field",
        "missing_evidence": "missing or unavailable evidence must be fixed before review-ready status",
        "unclear_diagnosis": "diagnosis must explain what happened and why using evidence-backed candidates",
        "unclear_next_fix_path": "next fix path must name a specific local contract, fixture, test, evidence, or review area",
        "missing_regression": "regression coverage must be named before lower-tier review-ready status",
        "boundary_gap": "packet item must preserve no-hindsight and no-trade boundaries",
    }
    return reasons.get(gap_type, f"{field_name} is not review-ready")


def _reject_forbidden_readiness_fields(value: Any, path: tuple[str, ...]) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.lower()
            if (
                normalized_key in FORBIDDEN_SETUP_OUTCOME_FIELD_NAMES
                and normalized_key not in SETUP_OUTCOME_EVIDENCE_PACKET_RESULT_FIELDS
            ):
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden execution/trade field: {dotted_path}")
            _reject_forbidden_readiness_fields(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_forbidden_readiness_fields(nested_value, (*path, str(index)))
