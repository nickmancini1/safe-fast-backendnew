"""Local-only discretion audit rule-inventory preflight validator.

This module validates caller-provided in-memory rule/contract inventory items
for later discretion audit work without auditing, changing rules, or touching
live trading systems.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


DISCRETION_AUDIT_INVENTORY_REQUIRED_FIELDS = (
    "item_id",
    "area",
    "source",
    "text",
    "rule_purpose",
    "audit_readiness",
    "unavailable_fields",
    "watch_only",
)

DISCRETION_AUDIT_INVENTORY_ALLOWED_AREAS = (
    "setup recognition",
    "trigger",
    "invalidation",
    "fresh/stale/spent",
    "blocker/caution",
    "ranking/focus",
    "outcome scoring",
    "diagnostics",
    "user workflow",
)

DISCRETION_AUDIT_INVENTORY_RESULT_FIELDS = (
    "watch_only",
    "discretion_audit_inventory_only",
    "audit_started",
    "rules_changed",
    "optimization_started",
    "items_processed",
    "items_accepted",
    "items_rejected",
    "accepted_items",
    "rejected_items",
    "covered_areas",
    "missing_required_areas",
    "unavailable_fields",
    "no_trade_boundary_preserved",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

_STRING_ITEM_FIELDS = (
    "item_id",
    "area",
    "source",
    "text",
    "rule_purpose",
    "audit_readiness",
)

_FORBIDDEN_INVENTORY_FIELD_NAMES = frozenset(
    {
        "account",
        "account_id",
        "account_size",
        "account_sizing",
        "account_sizing_enabled",
        "approved_trade",
        "approved_trades",
        "broker",
        "broker_call",
        "broker_enabled",
        "broker_order",
        "buy",
        "execute_order",
        "live_trade",
        "live_trade_approval",
        "live_trade_decision",
        "live_trade_decision_enabled",
        "option",
        "option_pnl",
        "option_pnl_enabled",
        "options",
        "order",
        "order_id",
        "orders",
        "orders_enabled",
        "p&l",
        "p_and_l",
        "p_l",
        "pl",
        "pnl",
        "position",
        "position_size",
        "sell",
        "trade",
        "trade_approval",
        "trade_decision",
        "trade_decisions",
        "trade-decision",
    }
)


def validate_discretion_audit_inventory_item(
    item: dict[str, Any],
) -> dict[str, Any]:
    """Validate one in-memory rule/contract inventory item."""
    if type(item) is not dict:
        raise TypeError("Discretion audit inventory item must be a dict")

    _validate_item(item, path=("item",))
    return _accepted_item(item)


def validate_discretion_audit_inventory(
    items: list[dict[str, Any]],
) -> dict[str, Any]:
    """Return an in-memory summary of caller-provided inventory validation."""
    if type(items) is not list:
        raise TypeError("Discretion audit inventory input must be a list of dicts")

    accepted_items = []
    rejected_items = []

    for index, item in enumerate(items):
        if type(item) is not dict:
            raise TypeError(f"Discretion audit inventory items[{index}] must be a dict")

        try:
            _validate_item(item, path=(f"items[{index}]",))
        except (TypeError, ValueError) as exc:
            rejected_items.append(
                {
                    "index": index,
                    "item_id": deepcopy(item.get("item_id")),
                    "accepted": False,
                    "reasons": [str(exc)],
                }
            )
            continue

        accepted_items.append(_accepted_item(item, index=index))

    covered_area_set = {item["area"] for item in accepted_items}
    covered_areas = _ordered_area_subset(covered_area_set)
    missing_required_areas = [
        area
        for area in DISCRETION_AUDIT_INVENTORY_ALLOWED_AREAS
        if area not in covered_area_set
    ]
    unavailable_fields = [
        {
            "item_id": deepcopy(item["item_id"]),
            "unavailable_fields": deepcopy(item["unavailable_fields"]),
        }
        for item in accepted_items
    ]

    result = {
        "watch_only": True,
        "discretion_audit_inventory_only": True,
        "audit_started": False,
        "rules_changed": False,
        "optimization_started": False,
        "items_processed": len(items),
        "items_accepted": len(accepted_items),
        "items_rejected": len(rejected_items),
        "accepted_items": deepcopy(accepted_items),
        "rejected_items": deepcopy(rejected_items),
        "covered_areas": deepcopy(covered_areas),
        "missing_required_areas": deepcopy(missing_required_areas),
        "unavailable_fields": deepcopy(unavailable_fields),
        "no_trade_boundary_preserved": True,
        "live_data_started": False,
        "controlled_shadow_data_started": False,
        "alerts_sent": False,
        "files_written": False,
        "broker_or_trade_behavior_enabled": False,
    }
    return deepcopy(result)


def _validate_item(item: Mapping[str, Any], path: tuple[str, ...]) -> None:
    _reject_forbidden_inventory_fields(item, path=path)

    missing = [
        field_name
        for field_name in DISCRETION_AUDIT_INVENTORY_REQUIRED_FIELDS
        if field_name not in item
    ]
    if missing:
        raise ValueError(
            "Missing required discretion audit inventory item fields: "
            + ", ".join(missing)
        )

    for field_name in _STRING_ITEM_FIELDS:
        if type(item[field_name]) is not str:
            dotted_path = ".".join((*path, field_name))
            raise TypeError(f"{dotted_path} must be a string")

    if item["area"] not in DISCRETION_AUDIT_INVENTORY_ALLOWED_AREAS:
        dotted_path = ".".join((*path, "area"))
        raise ValueError(f"{dotted_path} must be an allowed SAFE-FAST area")

    if type(item["unavailable_fields"]) not in (list, dict):
        dotted_path = ".".join((*path, "unavailable_fields"))
        raise TypeError(f"{dotted_path} must be a list or dict")

    if item["watch_only"] is not True:
        dotted_path = ".".join((*path, "watch_only"))
        raise ValueError(f"{dotted_path} must be True")


def _accepted_item(item: Mapping[str, Any], index: int | None = None) -> dict[str, Any]:
    accepted = {
        "item_id": deepcopy(item["item_id"]),
        "area": deepcopy(item["area"]),
        "source": deepcopy(item["source"]),
        "text": deepcopy(item["text"]),
        "rule_purpose": deepcopy(item["rule_purpose"]),
        "audit_readiness": deepcopy(item["audit_readiness"]),
        "unavailable_fields": deepcopy(item["unavailable_fields"]),
        "watch_only": True,
        "accepted": True,
    }
    if index is not None:
        accepted["index"] = index
    return deepcopy(accepted)


def _ordered_area_subset(areas: set[str]) -> list[str]:
    return [
        area
        for area in DISCRETION_AUDIT_INVENTORY_ALLOWED_AREAS
        if area in areas
    ]


def _reject_forbidden_inventory_fields(value: Any, path: tuple[str, ...]) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.strip().lower()
            if normalized_key in _FORBIDDEN_INVENTORY_FIELD_NAMES:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden broker/order/trade field: {dotted_path}")
            _reject_forbidden_inventory_fields(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for nested_index, nested_value in enumerate(value):
            _reject_forbidden_inventory_fields(
                nested_value, (*path, str(nested_index))
            )
