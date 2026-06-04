"""Local-only setup outcome evidence packet builder.

This module accepts the in-memory setup outcome diagnostics summary only and
returns one compact in-memory evidence packet summary. It does not fetch data,
write files, start shadow/live workflows, emit alerts, call subprocesses, touch
brokers/accounts/options/P&L, optimize rules, or make trade decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.setup_outcome_diagnostics import (
    SETUP_OUTCOME_DIAGNOSTICS_RESULT_FIELDS,
)
from watcher_foundation.setup_outcome_proof import (
    FORBIDDEN_SETUP_OUTCOME_FIELD_NAMES,
)


SETUP_OUTCOME_EVIDENCE_PACKET_RESULT_FIELDS = (
    "watch_only",
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
    "packet_items",
    "packet_items_by_setup_type",
    "lower_tier_handoff_required",
    "lower_tier_handoff_items",
    "missing_evidence",
    "next_fix_paths",
    "regression_needed",
    "rejected_records",
    "proof_limited_records",
    "no_hindsight_boundary_preserved",
    "no_trade_boundary_preserved",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

SETUP_OUTCOME_EVIDENCE_PACKET_ITEM_FIELDS = (
    "packet_item_id",
    "setup_type",
    "symbol",
    "setup_identifier",
    "what_setup_appeared",
    "what_happened_after_setup",
    "why_it_happened",
    "outcome_status",
    "diagnostic_category",
    "evidence_state",
    "evidence_support",
    "missing_evidence",
    "proof_limited_reason",
    "likely_cause_candidates",
    "affected_system_area",
    "next_fix_path",
    "regression_needed",
    "lower_tier_handoff_required",
    "lower_tier_handoff_reason",
    "no_hindsight_boundary_confirmed",
    "no_trade_boundary_confirmed",
)

_EXPECTED_TRUE_DIAGNOSTIC_FIELDS = (
    "watch_only",
    "setup_outcome_diagnostics_only",
    "setup_outcome_proof_only",
    "no_hindsight_boundary_preserved",
    "no_trade_boundary_preserved",
    "no_rule_change_started",
)

_EXPECTED_FALSE_DIAGNOSTIC_FIELDS = (
    "final_viability_proven",
    "optimization_started",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

_REQUIRED_FINDING_FIELDS = (
    "diagnostic_category",
    "record_id",
    "outcome_status",
    "what_happened",
    "evidence_supports",
    "affected_setup_type",
    "affected_symbol",
    "affected_stage",
    "evidence_used",
    "unavailable_evidence",
    "proof_limited_fields",
    "likely_cause_candidates",
    "affected_system_area",
    "next_fix_path",
    "regression_needed",
    "lower_tier_handoff_required",
    "proof_limited_reason",
)


def build_setup_outcome_evidence_packet(
    diagnostics_summary: dict[str, Any],
) -> dict[str, Any]:
    """Return one in-memory setup outcome evidence packet summary."""
    if type(diagnostics_summary) is not dict:
        raise TypeError("Setup outcome evidence packet input must be a dict")

    _validate_diagnostics_summary(diagnostics_summary)

    packet_items = [
        _packet_item_for_finding(index, finding)
        for index, finding in enumerate(diagnostics_summary["diagnostic_findings"])
    ]
    packet_items_by_setup_type = _group_packet_items(packet_items)
    lower_tier_handoff_items = [
        deepcopy(item)
        for item in packet_items
        if item["lower_tier_handoff_required"] is True
    ]

    return {
        "watch_only": True,
        "setup_outcome_evidence_packet_only": True,
        "setup_outcome_diagnostics_only": True,
        "setup_outcome_proof_only": True,
        "final_viability_proven": False,
        "optimization_started": False,
        "no_rule_change_started": True,
        "records_processed": diagnostics_summary["records_processed"],
        "records_accepted": diagnostics_summary["records_accepted"],
        "records_rejected": diagnostics_summary["records_rejected"],
        "packet_item_count": len(packet_items),
        "packet_items": deepcopy(packet_items),
        "packet_items_by_setup_type": packet_items_by_setup_type,
        "lower_tier_handoff_required": bool(lower_tier_handoff_items),
        "lower_tier_handoff_items": lower_tier_handoff_items,
        "missing_evidence": _collect_missing_evidence(packet_items),
        "next_fix_paths": deepcopy(diagnostics_summary["next_fix_paths"]),
        "regression_needed": _collect_regression_needed(packet_items),
        "rejected_records": deepcopy(diagnostics_summary["rejected_records"]),
        "proof_limited_records": deepcopy(diagnostics_summary["proof_limited_records"]),
        "no_hindsight_boundary_preserved": True,
        "no_trade_boundary_preserved": True,
        "live_data_started": False,
        "controlled_shadow_data_started": False,
        "alerts_sent": False,
        "files_written": False,
        "broker_or_trade_behavior_enabled": False,
    }


def _validate_diagnostics_summary(diagnostics_summary: Mapping[str, Any]) -> None:
    missing_fields = [
        field_name
        for field_name in SETUP_OUTCOME_DIAGNOSTICS_RESULT_FIELDS
        if field_name not in diagnostics_summary
    ]
    if missing_fields:
        raise ValueError(
            "Missing required setup outcome diagnostics summary fields: "
            + ", ".join(missing_fields)
        )

    unexpected_fields = [
        field_name
        for field_name in diagnostics_summary
        if field_name not in SETUP_OUTCOME_DIAGNOSTICS_RESULT_FIELDS
    ]
    if unexpected_fields:
        raise ValueError(
            "Unexpected setup outcome diagnostics summary fields: "
            + ", ".join(unexpected_fields)
        )

    _reject_forbidden_packet_fields(diagnostics_summary, path=())

    for field_name in _EXPECTED_TRUE_DIAGNOSTIC_FIELDS:
        if diagnostics_summary[field_name] is not True:
            raise ValueError(
                f"Setup outcome evidence packet requires {field_name}=True"
            )
    for field_name in _EXPECTED_FALSE_DIAGNOSTIC_FIELDS:
        if diagnostics_summary[field_name] is not False:
            raise ValueError(
                f"Setup outcome evidence packet requires {field_name}=False"
            )

    for field_name in ("records_processed", "records_accepted", "records_rejected"):
        if type(diagnostics_summary[field_name]) is not int:
            raise TypeError(
                f"Setup outcome evidence packet {field_name} must be an int"
            )
        if diagnostics_summary[field_name] < 0:
            raise ValueError(
                f"Setup outcome evidence packet {field_name} must be non-negative"
            )

    for field_name in (
        "diagnostic_findings",
        "likely_cause_candidates",
        "unavailable_evidence",
        "rejected_records",
        "proof_limited_records",
    ):
        if type(diagnostics_summary[field_name]) is not list:
            raise TypeError(
                f"Setup outcome evidence packet {field_name} must be a list"
            )
    for field_name in (
        "diagnostics_by_setup_type",
        "diagnostic_gap_counts",
        "next_fix_paths",
    ):
        if type(diagnostics_summary[field_name]) is not dict:
            raise TypeError(
                f"Setup outcome evidence packet {field_name} must be a dict"
            )

    if len(diagnostics_summary["diagnostic_findings"]) != (
        diagnostics_summary["records_accepted"]
        + (1 if diagnostics_summary["records_rejected"] else 0)
    ):
        raise ValueError(
            "Setup outcome evidence packet diagnostic_findings must cover accepted "
            "records plus rejected-record summary when present"
        )

    for index, finding in enumerate(diagnostics_summary["diagnostic_findings"]):
        _validate_diagnostic_finding(finding, index)


def _validate_diagnostic_finding(finding: Any, index: int) -> None:
    if type(finding) is not dict:
        raise TypeError(
            f"Setup outcome evidence packet diagnostic_findings[{index}] must be a dict"
        )
    missing_fields = [
        field_name for field_name in _REQUIRED_FINDING_FIELDS if field_name not in finding
    ]
    if missing_fields:
        raise ValueError(
            f"Missing required setup outcome diagnostic finding fields at {index}: "
            + ", ".join(missing_fields)
        )
    if type(finding["what_happened"]) is not str or not finding["what_happened"]:
        raise ValueError(
            f"Setup outcome diagnostic finding {index} must include what_happened"
        )
    if type(finding["evidence_supports"]) is not dict:
        raise TypeError(
            f"Setup outcome diagnostic finding {index}.evidence_supports must be a dict"
        )
    if not _finding_has_evidence(finding):
        raise ValueError(
            f"Setup outcome diagnostic finding {index} needs explicit evidence support"
        )
    if type(finding["likely_cause_candidates"]) is not list:
        raise TypeError(
            f"Setup outcome diagnostic finding {index}.likely_cause_candidates must be a list"
        )
    if not finding["likely_cause_candidates"]:
        raise ValueError(
            f"Setup outcome diagnostic finding {index} must include likely cause candidates"
        )
    if type(finding["next_fix_path"]) is not str or not finding["next_fix_path"]:
        raise ValueError(
            f"Setup outcome diagnostic finding {index} must include next_fix_path"
        )
    if type(finding["regression_needed"]) is not str or not finding["regression_needed"]:
        raise ValueError(
            f"Setup outcome diagnostic finding {index} must include regression_needed"
        )
    if finding["lower_tier_handoff_required"] not in {True, False}:
        raise TypeError(
            f"Setup outcome diagnostic finding {index}.lower_tier_handoff_required "
            "must be a bool"
        )


def _packet_item_for_finding(index: int, finding: Mapping[str, Any]) -> dict[str, Any]:
    setup_type = deepcopy(finding["affected_setup_type"])
    symbol = deepcopy(finding["affected_symbol"])
    setup_identifier = _setup_identifier(finding)
    missing_evidence = _missing_evidence(finding, setup_identifier)
    lower_tier_handoff_required = (
        finding["lower_tier_handoff_required"] is True or bool(missing_evidence)
    )

    return {
        "packet_item_id": f"setup-outcome-evidence-{index + 1}",
        "setup_type": setup_type,
        "symbol": symbol,
        "setup_identifier": setup_identifier,
        "what_setup_appeared": _what_setup_appeared(finding, setup_identifier),
        "what_happened_after_setup": finding["what_happened"],
        "why_it_happened": _why_it_happened(finding),
        "outcome_status": deepcopy(finding["outcome_status"]),
        "diagnostic_category": deepcopy(finding["diagnostic_category"]),
        "evidence_state": _evidence_state(finding, missing_evidence),
        "evidence_support": {
            "evidence_refs": deepcopy(finding["evidence_used"]),
            "evidence_supports": deepcopy(finding["evidence_supports"]),
            "after_setup_evidence": deepcopy(
                finding["evidence_supports"].get("after_setup_evidence", {})
            ),
        },
        "missing_evidence": missing_evidence,
        "proof_limited_reason": deepcopy(finding["proof_limited_reason"]),
        "likely_cause_candidates": deepcopy(finding["likely_cause_candidates"]),
        "affected_system_area": deepcopy(finding["affected_system_area"]),
        "next_fix_path": deepcopy(finding["next_fix_path"]),
        "regression_needed": deepcopy(finding["regression_needed"]),
        "lower_tier_handoff_required": lower_tier_handoff_required,
        "lower_tier_handoff_reason": _lower_tier_handoff_reason(
            finding,
            missing_evidence,
        ),
        "no_hindsight_boundary_confirmed": True,
        "no_trade_boundary_confirmed": True,
    }


def _setup_identifier(finding: Mapping[str, Any]) -> Any:
    for field_name in ("setup_id", "setup_identifier"):
        value = finding.get(field_name)
        if type(value) is str and value:
            return value
    return _unavailable_field(
        "setup_identifier",
        "setup identifier was not carried in the setup outcome diagnostics finding",
    )


def _what_setup_appeared(
    finding: Mapping[str, Any],
    setup_identifier: Any,
) -> dict[str, Any]:
    return {
        "setup_type": deepcopy(finding["affected_setup_type"]),
        "symbol": deepcopy(finding["affected_symbol"]),
        "setup_identifier": deepcopy(setup_identifier),
        "stage": deepcopy(finding["affected_stage"]),
    }


def _why_it_happened(finding: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "diagnostic_category": deepcopy(finding["diagnostic_category"]),
        "likely_cause_candidates": deepcopy(finding["likely_cause_candidates"]),
        "proof_limited_reason": deepcopy(finding["proof_limited_reason"]),
    }


def _missing_evidence(
    finding: Mapping[str, Any],
    setup_identifier: Any,
) -> list[Any]:
    missing = []
    if type(setup_identifier) is dict:
        missing.append(deepcopy(setup_identifier))
    for field_name in ("unavailable_evidence", "proof_limited_fields"):
        items = finding.get(field_name)
        if type(items) is list:
            missing.extend(deepcopy(items))
    return missing


def _evidence_state(
    finding: Mapping[str, Any],
    missing_evidence: list[Any],
) -> str:
    if missing_evidence:
        return "missing_or_unavailable_evidence"
    if finding["lower_tier_handoff_required"] is True:
        return "handoff_required_with_evidence"
    return "evidence_supported"


def _lower_tier_handoff_reason(
    finding: Mapping[str, Any],
    missing_evidence: list[Any],
) -> str:
    if missing_evidence:
        return "missing or unavailable evidence requires lower-tier review before broader changes"
    if finding["lower_tier_handoff_required"] is True:
        return "diagnostics marked this finding for lower-tier handoff"
    return "not required by the caller-provided diagnostics summary"


def _group_packet_items(
    packet_items: list[dict[str, Any]],
) -> dict[str, dict[str, list[dict[str, Any]]]]:
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for item in packet_items:
        setup_type_key = _group_key(item["setup_type"])
        symbol_key = _group_key(item["symbol"])
        grouped.setdefault(setup_type_key, {})
        grouped[setup_type_key].setdefault(symbol_key, [])
        grouped[setup_type_key][symbol_key].append(deepcopy(item))
    return grouped


def _collect_missing_evidence(packet_items: list[dict[str, Any]]) -> list[Any]:
    missing = []
    for item in packet_items:
        missing.extend(deepcopy(item["missing_evidence"]))
    return missing


def _collect_regression_needed(packet_items: list[dict[str, Any]]) -> list[str]:
    regressions = []
    for item in packet_items:
        regression = item["regression_needed"]
        if regression not in regressions:
            regressions.append(regression)
    return regressions


def _finding_has_evidence(finding: Mapping[str, Any]) -> bool:
    if finding.get("evidence_used"):
        return True
    evidence_supports = finding.get("evidence_supports")
    if type(evidence_supports) is dict and any(evidence_supports.values()):
        return True
    if finding.get("unavailable_evidence") or finding.get("proof_limited_fields"):
        return True
    return finding.get("record_id") == "SUMMARY"


def _group_key(value: Any) -> str:
    if type(value) is str and value:
        return value
    if type(value) is dict and type(value.get("field_name")) is str:
        return f"UNAVAILABLE_{value['field_name']}"
    return "UNAVAILABLE"


def _unavailable_field(field_name: str, reason: str) -> dict[str, str]:
    return {
        "field_name": field_name,
        "status": "unavailable_evidence",
        "reason": reason,
    }


def _reject_forbidden_packet_fields(value: Any, path: tuple[str, ...]) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.lower()
            if (
                normalized_key in FORBIDDEN_SETUP_OUTCOME_FIELD_NAMES
                and normalized_key not in SETUP_OUTCOME_DIAGNOSTICS_RESULT_FIELDS
                and not _is_preserved_no_trade_boundary_field(normalized_key, path)
            ):
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden execution/trade field: {dotted_path}")
            _reject_forbidden_packet_fields(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_forbidden_packet_fields(nested_value, (*path, str(index)))


def _is_preserved_no_trade_boundary_field(
    normalized_key: str,
    path: tuple[str, ...],
) -> bool:
    if not path or path[-1] != "no_trade_boundary":
        return False
    return normalized_key in {
        "broker_enabled",
        "orders_enabled",
        "account_sizing_enabled",
        "option_pnl_enabled",
        "live_trade_decision_enabled",
    }
