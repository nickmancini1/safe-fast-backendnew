"""Local-only discretion audit coverage evaluator.

This module accepts caller-provided in-memory discretion-audit summaries and
returns an in-memory coverage summary without changing trading behavior.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


DISCRETION_AUDIT_REQUIRED_COVERAGE_AREAS = (
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

DISCRETION_AUDIT_COVERAGE_RESULT_FIELDS = (
    "watch_only",
    "discretion_audit_coverage_only",
    "rules_changed",
    "optimization_started",
    "required_areas",
    "covered_areas",
    "missing_areas",
    "forbidden_signal_discretion_areas",
    "safety_discretion_only_areas",
    "needs_review_areas",
    "coverage_complete",
    "findings_reviewed",
    "no_trade_boundary_preserved",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

_REQUIRED_SUMMARY_FIELDS = (
    "watch_only",
    "discretion_audit_only",
    "rules_changed",
    "optimization_started",
    "findings",
    "no_trade_boundary_preserved",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

_EXPECTED_SUMMARY_BOUNDARIES = {
    "watch_only": True,
    "discretion_audit_only": True,
    "rules_changed": False,
    "optimization_started": False,
    "no_trade_boundary_preserved": True,
    "live_data_started": False,
    "controlled_shadow_data_started": False,
    "alerts_sent": False,
    "files_written": False,
    "broker_or_trade_behavior_enabled": False,
}

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

_NEEDS_REVIEW_STATUSES = frozenset(
    {
        "inconclusive",
        "unavailable_evidence",
        "needs_review",
    }
)

_FORBIDDEN_SUMMARY_FIELD_NAMES = frozenset(
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


def evaluate_discretion_audit_coverage(audit_summary: dict[str, Any]) -> dict[str, Any]:
    """Return an in-memory summary of required-area discretion audit coverage."""
    if type(audit_summary) is not dict:
        raise TypeError("Discretion audit coverage input must be a dict")

    _validate_summary(audit_summary)

    covered_areas = set()
    forbidden_signal_discretion_areas = set()
    safety_discretion_only_areas = set()
    needs_review_areas = set()

    for index, finding in enumerate(audit_summary["findings"]):
        _validate_finding(finding, index)
        area = _classify_area(finding["area"])
        if area not in DISCRETION_AUDIT_REQUIRED_COVERAGE_AREAS:
            continue

        finding_status = _finding_status(finding)
        if _has_forbidden_signal_discretion(finding, finding_status):
            forbidden_signal_discretion_areas.add(area)
            continue
        if finding_status in _NEEDS_REVIEW_STATUSES:
            needs_review_areas.add(area)
            continue
        if _has_safety_discretion_only(finding, finding_status):
            safety_discretion_only_areas.add(area)
            covered_areas.add(area)
            continue

        covered_areas.add(area)

    required_areas = list(DISCRETION_AUDIT_REQUIRED_COVERAGE_AREAS)
    missing_areas = [
        area
        for area in required_areas
        if area not in covered_areas
        or area in forbidden_signal_discretion_areas
        or area in needs_review_areas
    ]

    result = {
        "watch_only": True,
        "discretion_audit_coverage_only": True,
        "rules_changed": False,
        "optimization_started": False,
        "required_areas": deepcopy(required_areas),
        "covered_areas": _ordered_required_subset(covered_areas),
        "missing_areas": deepcopy(missing_areas),
        "forbidden_signal_discretion_areas": _ordered_required_subset(
            forbidden_signal_discretion_areas
        ),
        "safety_discretion_only_areas": _ordered_required_subset(
            safety_discretion_only_areas
        ),
        "needs_review_areas": _ordered_required_subset(needs_review_areas),
        "coverage_complete": len(missing_areas) == 0,
        "findings_reviewed": len(audit_summary["findings"]),
        "no_trade_boundary_preserved": True,
        "live_data_started": False,
        "controlled_shadow_data_started": False,
        "alerts_sent": False,
        "files_written": False,
        "broker_or_trade_behavior_enabled": False,
    }
    return deepcopy(result)


def _validate_summary(audit_summary: Mapping[str, Any]) -> None:
    _reject_forbidden_summary_fields(audit_summary, path=("audit_summary",))

    missing = [
        field_name
        for field_name in _REQUIRED_SUMMARY_FIELDS
        if field_name not in audit_summary
    ]
    if missing:
        raise ValueError(
            "Missing required discretion audit summary fields: " + ", ".join(missing)
        )

    for field_name, expected_value in _EXPECTED_SUMMARY_BOUNDARIES.items():
        if audit_summary[field_name] is not expected_value:
            raise ValueError(
                "Discretion audit summary boundary failure: "
                f"{field_name} must be {expected_value!r}"
            )

    if type(audit_summary["findings"]) is not list:
        raise TypeError("Discretion audit summary findings must be a list")


def _validate_finding(finding: Any, index: int) -> None:
    if type(finding) is not dict:
        raise TypeError(f"Discretion audit findings[{index}] must be a dict")
    if "area" not in finding:
        raise ValueError(f"Missing area in discretion audit findings[{index}]")
    if type(finding["area"]) is not str:
        raise TypeError(f"Discretion audit findings[{index}].area must be a string")


def _classify_area(area: str) -> str:
    normalized_area = _normalize_text(area).replace("-", "_")
    return _AREA_ALIASES.get(normalized_area, "needs_review")


def _finding_status(finding: Mapping[str, Any]) -> str:
    for field_name in ("coverage_status", "status", "discretion_type"):
        value = finding.get(field_name)
        if type(value) is str:
            return _normalize_text(value)
    return ""


def _has_forbidden_signal_discretion(
    finding: Mapping[str, Any], finding_status: str
) -> bool:
    return (
        finding.get("signal_discretion") is True
        or finding_status == "forbidden_signal_discretion"
    )


def _has_safety_discretion_only(
    finding: Mapping[str, Any], finding_status: str
) -> bool:
    return (
        finding.get("safety_discretion") is True
        or finding_status == "allowed_safety_discretion"
    )


def _ordered_required_subset(areas: set[str]) -> list[str]:
    return [
        area
        for area in DISCRETION_AUDIT_REQUIRED_COVERAGE_AREAS
        if area in areas
    ]


def _reject_forbidden_summary_fields(value: Any, path: tuple[str, ...]) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.strip().lower()
            if normalized_key in _FORBIDDEN_SUMMARY_FIELD_NAMES:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden broker/order/trade field: {dotted_path}")
            _reject_forbidden_summary_fields(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for nested_index, nested_value in enumerate(value):
            _reject_forbidden_summary_fields(
                nested_value, (*path, str(nested_index))
            )


def _normalize_text(value: str) -> str:
    return " ".join(value.strip().lower().split())
