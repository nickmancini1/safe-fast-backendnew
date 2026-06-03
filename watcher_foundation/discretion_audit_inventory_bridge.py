"""Local-only inventory-to-discretion-audit bridge readiness gate."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.discretion_audit import audit_trading_plan_discretion
from watcher_foundation.discretion_audit_coverage import (
    evaluate_discretion_audit_coverage,
)
from watcher_foundation.discretion_audit_inventory import (
    validate_discretion_audit_inventory,
)


DISCRETION_AUDIT_INVENTORY_BRIDGE_RESULT_FIELDS = (
    "local_only",
    "in_memory_only",
    "watch_only",
    "discretion_audit_inventory_bridge_only",
    "no_trade",
    "no_rule_change",
    "no_optimization",
    "no_file_write",
    "no_live_data",
    "no_controlled_shadow_data",
    "no_alert",
    "no_broker",
    "rules_changed",
    "optimization_started",
    "files_written",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "broker_or_trade_behavior_enabled",
    "inventory_validation",
    "accepted_inventory_items",
    "rejected_inventory_items",
    "unavailable_fields",
    "unavailable_field_blockers",
    "audit_input_items",
    "audit_execution_eligible",
    "audit_executed",
    "audit_readiness",
    "audit_confidence",
    "audit_summary",
    "coverage_execution_eligible",
    "coverage_executed",
    "coverage_readiness",
    "coverage_confidence",
    "coverage_summary",
    "coverage_complete",
    "bridge_ready",
    "no_trade_boundary_preserved",
    "watch_only_boundary_preserved",
)


def evaluate_discretion_audit_inventory_bridge(
    inventory_items: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate caller inventory, then run local audit and coverage if eligible."""
    inventory_validation = validate_discretion_audit_inventory(inventory_items)
    accepted_inventory_items = deepcopy(inventory_validation["accepted_items"])
    rejected_inventory_items = deepcopy(inventory_validation["rejected_items"])
    unavailable_fields = deepcopy(inventory_validation["unavailable_fields"])
    unavailable_field_blockers = _unavailable_field_blockers(accepted_inventory_items)
    watch_only_boundary_preserved = all(
        item.get("watch_only") is True for item in accepted_inventory_items
    )

    audit_input_items = []
    if watch_only_boundary_preserved:
        audit_input_items = [
            _audit_item_from_inventory(item) for item in accepted_inventory_items
        ]

    audit_execution_eligible = bool(audit_input_items) and watch_only_boundary_preserved
    audit_summary = None
    audit_executed = False
    if audit_execution_eligible:
        audit_summary = audit_trading_plan_discretion(audit_input_items)
        audit_executed = True

    audit_boundaries_preserved = (
        _summary_boundaries_preserved(audit_summary) if audit_summary is not None else False
    )
    coverage_execution_eligible = audit_executed and audit_boundaries_preserved
    coverage_summary = None
    coverage_executed = False
    if coverage_execution_eligible:
        coverage_summary = evaluate_discretion_audit_coverage(audit_summary)
        coverage_executed = True

    coverage_boundaries_preserved = (
        _summary_boundaries_preserved(coverage_summary)
        if coverage_summary is not None
        else False
    )
    no_trade_boundary_preserved = (
        inventory_validation["no_trade_boundary_preserved"]
        and watch_only_boundary_preserved
        and (not audit_executed or audit_boundaries_preserved)
        and (not coverage_executed or coverage_boundaries_preserved)
    )
    coverage_complete = (
        bool(coverage_summary["coverage_complete"])
        if coverage_summary is not None
        else False
    )
    unavailable_fields_block_confidence = bool(unavailable_field_blockers)

    result = {
        "local_only": True,
        "in_memory_only": True,
        "watch_only": True,
        "discretion_audit_inventory_bridge_only": True,
        "no_trade": True,
        "no_rule_change": True,
        "no_optimization": True,
        "no_file_write": True,
        "no_live_data": True,
        "no_controlled_shadow_data": True,
        "no_alert": True,
        "no_broker": True,
        "rules_changed": False,
        "optimization_started": False,
        "files_written": False,
        "live_data_started": False,
        "controlled_shadow_data_started": False,
        "alerts_sent": False,
        "broker_or_trade_behavior_enabled": False,
        "inventory_validation": deepcopy(inventory_validation),
        "accepted_inventory_items": deepcopy(accepted_inventory_items),
        "rejected_inventory_items": deepcopy(rejected_inventory_items),
        "unavailable_fields": deepcopy(unavailable_fields),
        "unavailable_field_blockers": deepcopy(unavailable_field_blockers),
        "audit_input_items": deepcopy(audit_input_items),
        "audit_execution_eligible": audit_execution_eligible,
        "audit_executed": audit_executed,
        "audit_readiness": _audit_readiness(
            audit_execution_eligible,
            watch_only_boundary_preserved,
            accepted_inventory_items,
        ),
        "audit_confidence": _confidence_status(
            audit_executed,
            unavailable_fields_block_confidence,
        ),
        "audit_summary": deepcopy(audit_summary),
        "coverage_execution_eligible": coverage_execution_eligible,
        "coverage_executed": coverage_executed,
        "coverage_readiness": _coverage_readiness(
            coverage_execution_eligible,
            audit_executed,
            audit_boundaries_preserved,
            coverage_complete,
            unavailable_fields_block_confidence,
        ),
        "coverage_confidence": _confidence_status(
            coverage_executed,
            unavailable_fields_block_confidence,
        ),
        "coverage_summary": deepcopy(coverage_summary),
        "coverage_complete": coverage_complete and not unavailable_fields_block_confidence,
        "bridge_ready": (
            audit_executed
            and coverage_executed
            and coverage_complete
            and not unavailable_fields_block_confidence
            and no_trade_boundary_preserved
        ),
        "no_trade_boundary_preserved": no_trade_boundary_preserved,
        "watch_only_boundary_preserved": watch_only_boundary_preserved,
    }
    return deepcopy(result)


def _audit_item_from_inventory(item: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "item_id": deepcopy(item["item_id"]),
        "area": deepcopy(item["area"]),
        "text": deepcopy(item["text"]),
        "source": deepcopy(item["source"]),
        "review_context": _review_context_from_inventory(item),
        "watch_only": True,
    }


def _review_context_from_inventory(item: Mapping[str, Any]) -> str:
    unavailable_fields = item["unavailable_fields"]
    unavailable_context = (
        "none"
        if not _has_unavailable_fields(unavailable_fields)
        else repr(unavailable_fields)
    )
    return (
        f"source={item['source']}; "
        f"rule_purpose={item['rule_purpose']}; "
        f"audit_readiness={item['audit_readiness']}; "
        f"unavailable_fields={unavailable_context}"
    )


def _unavailable_field_blockers(
    accepted_inventory_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    blockers = []
    for item in accepted_inventory_items:
        if _has_unavailable_fields(item["unavailable_fields"]):
            blockers.append(
                {
                    "item_id": deepcopy(item["item_id"]),
                    "area": deepcopy(item["area"]),
                    "unavailable_fields": deepcopy(item["unavailable_fields"]),
                    "audit_confidence_blocked": True,
                    "coverage_confidence_blocked": True,
                }
            )
    return deepcopy(blockers)


def _has_unavailable_fields(value: Any) -> bool:
    return (type(value) is list and len(value) > 0) or (
        type(value) is dict and len(value) > 0
    )


def _summary_boundaries_preserved(summary: Mapping[str, Any] | None) -> bool:
    if summary is None:
        return False
    return (
        summary.get("watch_only") is True
        and summary.get("rules_changed") is False
        and summary.get("optimization_started") is False
        and summary.get("no_trade_boundary_preserved") is True
        and summary.get("live_data_started") is False
        and summary.get("controlled_shadow_data_started") is False
        and summary.get("alerts_sent") is False
        and summary.get("files_written") is False
        and summary.get("broker_or_trade_behavior_enabled") is False
    )


def _audit_readiness(
    audit_execution_eligible: bool,
    watch_only_boundary_preserved: bool,
    accepted_inventory_items: list[dict[str, Any]],
) -> str:
    if not watch_only_boundary_preserved:
        return "not_ready_watch_only_boundary_failed"
    if not accepted_inventory_items:
        return "not_ready_no_accepted_inventory_items"
    if audit_execution_eligible:
        return "ready_for_existing_discretion_audit_contract"
    return "not_ready_for_existing_discretion_audit_contract"


def _coverage_readiness(
    coverage_execution_eligible: bool,
    audit_executed: bool,
    audit_boundaries_preserved: bool,
    coverage_complete: bool,
    unavailable_fields_block_confidence: bool,
) -> str:
    if not audit_executed:
        return "not_ready_no_audit_output"
    if not audit_boundaries_preserved:
        return "not_ready_audit_boundary_failed"
    if not coverage_execution_eligible:
        return "not_ready_for_existing_coverage_contract"
    if unavailable_fields_block_confidence:
        return "ran_existing_coverage_with_unavailable_field_confidence_blockers"
    if coverage_complete:
        return "ready_existing_coverage_complete"
    return "ran_existing_coverage_with_gaps"


def _confidence_status(executed: bool, unavailable_fields_block_confidence: bool) -> str:
    if not executed:
        return "not_evaluated"
    if unavailable_fields_block_confidence:
        return "blocked_by_explicit_unavailable_fields"
    return "existing_contract_evaluated_no_unavailable_field_blockers"
