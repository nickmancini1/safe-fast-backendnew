"""Local-only trading-plan discretion audit evaluator.

This module accepts caller-provided in-memory rule/contract descriptions and
returns an in-memory audit summary without changing trading behavior.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


DISCRETION_AUDIT_VAGUE_PHRASES = (
    "looks good",
    "wait for confirmation",
    "strong enough",
    "weak signal",
    "use judgment",
    "good setup",
    "bad setup",
    "probably",
    "maybe",
    "feels right",
)

DISCRETION_AUDIT_AREAS = (
    "setup_recognition",
    "trigger",
    "invalidation",
    "fresh_stale_spent",
    "blocker_caution",
    "ranking_focus",
    "outcome_scoring",
    "diagnostics",
    "user_workflow",
)

DISCRETION_AUDIT_ALLOWED_HUMAN_DISCRETION = (
    "no-trade veto",
    "review note",
    "safety pause",
)

DISCRETION_AUDIT_RESULT_FIELDS = (
    "watch_only",
    "discretion_audit_only",
    "rules_changed",
    "optimization_started",
    "items_reviewed",
    "items_flagged",
    "allowed_safety_discretion_count",
    "forbidden_signal_discretion_count",
    "needs_review_count",
    "findings",
    "no_trade_boundary_preserved",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

_REQUIRED_ITEM_FIELDS = (
    "item_id",
    "area",
    "text",
    "source",
    "review_context",
    "watch_only",
)

_AREA_ALIASES = {
    "setup recognition": "setup_recognition",
    "setup_recognition": "setup_recognition",
    "trigger": "trigger",
    "invalidation": "invalidation",
    "fresh/stale/spent": "fresh_stale_spent",
    "fresh_stale_spent": "fresh_stale_spent",
    "blocker/caution": "blocker_caution",
    "blocker_caution": "blocker_caution",
    "ranking/focus": "ranking_focus",
    "ranking_focus": "ranking_focus",
    "outcome scoring": "outcome_scoring",
    "outcome_scoring": "outcome_scoring",
    "diagnostics": "diagnostics",
    "user workflow": "user_workflow",
    "user_workflow": "user_workflow",
}

_FORBIDDEN_SIGNAL_DISCRETION_PATTERNS = {
    "create_signal": (
        "create a signal",
        "creates a signal",
        "make a signal",
        "signal can be created",
    ),
    "approve_trade": (
        "approve a trade",
        "approves a trade",
        "trade can be approved",
        "approve trade",
    ),
    "override_missing_proof": (
        "override missing proof",
        "ignore missing proof",
        "missing proof can be overridden",
    ),
    "move_triggers": (
        "move triggers",
        "move the trigger",
        "adjust trigger",
        "shift trigger",
    ),
    "hide_failures": (
        "hide failures",
        "hide failed",
        "suppress failure",
        "bury failure",
    ),
    "change_outcome_review_after_fact": (
        "change outcome review after the fact",
        "rewrite outcome after the fact",
        "revise outcome after the fact",
    ),
}

_FORBIDDEN_DISCRETION_FIELD_NAMES = frozenset(
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


def audit_trading_plan_discretion(items: list[dict[str, Any]]) -> dict[str, Any]:
    """Return an in-memory summary of hidden discretion in rule text."""
    if type(items) is not list:
        raise TypeError("Discretion audit items must be a list of dicts")

    findings = []
    allowed_safety_discretion_count = 0
    forbidden_signal_discretion_count = 0
    needs_review_count = 0

    for index, item in enumerate(items):
        _validate_item(item, index)
        finding = _finding_for_item(item, index)
        if finding["flagged"]:
            findings.append(finding)
            if finding["discretion_type"] == "allowed_safety_discretion":
                allowed_safety_discretion_count += 1
            elif finding["discretion_type"] == "forbidden_signal_discretion":
                forbidden_signal_discretion_count += 1
            else:
                needs_review_count += 1
        elif finding["area"] == "needs_review":
            findings.append(finding)
            needs_review_count += 1

    result = {
        "watch_only": True,
        "discretion_audit_only": True,
        "rules_changed": False,
        "optimization_started": False,
        "items_reviewed": len(items),
        "items_flagged": len(findings),
        "allowed_safety_discretion_count": allowed_safety_discretion_count,
        "forbidden_signal_discretion_count": forbidden_signal_discretion_count,
        "needs_review_count": needs_review_count,
        "findings": deepcopy(findings),
        "no_trade_boundary_preserved": True,
        "live_data_started": False,
        "controlled_shadow_data_started": False,
        "alerts_sent": False,
        "files_written": False,
        "broker_or_trade_behavior_enabled": False,
    }
    return deepcopy(result)


def _validate_item(item: Any, index: int) -> None:
    if type(item) is not dict:
        raise TypeError(f"Discretion audit items[{index}] must be a dict")

    _reject_forbidden_discretion_fields(item, path=(f"items[{index}]",))

    missing = [field_name for field_name in _REQUIRED_ITEM_FIELDS if field_name not in item]
    if missing:
        raise ValueError(
            f"Missing required discretion audit item fields at items[{index}]: "
            + ", ".join(missing)
        )

    for field_name in ("item_id", "area", "text", "source", "review_context"):
        if type(item[field_name]) is not str:
            raise TypeError(
                f"Discretion audit items[{index}].{field_name} must be a string"
            )

    if item["watch_only"] is not True:
        raise ValueError(f"Discretion audit items[{index}].watch_only must be True")


def _finding_for_item(item: Mapping[str, Any], index: int) -> dict[str, Any]:
    area = _classify_area(item["area"])
    text = item["text"]
    normalized_text = _normalize_text(text)
    vague_phrases = [
        phrase for phrase in DISCRETION_AUDIT_VAGUE_PHRASES if phrase in normalized_text
    ]
    allowed_phrases = [
        phrase
        for phrase in DISCRETION_AUDIT_ALLOWED_HUMAN_DISCRETION
        if phrase in normalized_text
    ]
    forbidden_actions = _forbidden_signal_actions(normalized_text)

    discretion_type = "none"
    reasons = []
    if area == "needs_review":
        discretion_type = "needs_review"
        reasons.append("unsupported area requires explicit review")
    if forbidden_actions:
        discretion_type = "forbidden_signal_discretion"
        reasons.append("text can alter signal/trade proof behavior")
    elif allowed_phrases and not vague_phrases:
        discretion_type = "allowed_safety_discretion"
        reasons.append("allowed human discretion is limited to safety/review")
    elif vague_phrases:
        if area == "user_workflow" and allowed_phrases:
            discretion_type = "allowed_safety_discretion"
            reasons.append("allowed safety workflow language is explicit")
        else:
            discretion_type = "forbidden_signal_discretion"
            reasons.append("vague language can introduce hidden signal discretion")

    flagged = discretion_type != "none"
    return {
        "index": index,
        "item_id": deepcopy(item["item_id"]),
        "area": area,
        "provided_area": deepcopy(item["area"]),
        "source": deepcopy(item["source"]),
        "review_context": deepcopy(item["review_context"]),
        "watch_only": True,
        "flagged": flagged,
        "vague_phrases": deepcopy(vague_phrases),
        "allowed_human_discretion": deepcopy(allowed_phrases),
        "forbidden_signal_actions": deepcopy(forbidden_actions),
        "discretion_type": discretion_type,
        "safety_discretion": discretion_type == "allowed_safety_discretion",
        "signal_discretion": discretion_type == "forbidden_signal_discretion",
        "reasons": deepcopy(reasons),
    }


def _classify_area(area: str) -> str:
    normalized_area = _normalize_text(area).replace("-", "_")
    if normalized_area in _AREA_ALIASES:
        return _AREA_ALIASES[normalized_area]
    if normalized_area == "needs_review":
        return "needs_review"
    return "needs_review"


def _forbidden_signal_actions(normalized_text: str) -> list[str]:
    actions = []
    for action, patterns in _FORBIDDEN_SIGNAL_DISCRETION_PATTERNS.items():
        if any(pattern in normalized_text for pattern in patterns):
            actions.append(action)
    return actions


def _reject_forbidden_discretion_fields(value: Any, path: tuple[str, ...]) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.strip().lower()
            if normalized_key in _FORBIDDEN_DISCRETION_FIELD_NAMES:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden broker/order/trade field: {dotted_path}")
            _reject_forbidden_discretion_fields(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for nested_index, nested_value in enumerate(value):
            _reject_forbidden_discretion_fields(
                nested_value, (*path, str(nested_index))
            )


def _normalize_text(value: str) -> str:
    return " ".join(value.strip().lower().split())
