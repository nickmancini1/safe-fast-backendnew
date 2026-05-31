"""Local-only historical optimization readiness gate.

This module accepts the in-memory historical outcome diagnostics summary only
and returns an in-memory optimization readiness summary without side effects.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.historical_outcome_diagnostics import (
    HISTORICAL_OUTCOME_DIAGNOSTICS_RESULT_FIELDS,
)


HISTORICAL_OPTIMIZATION_ALLOWED_SYSTEM_AREAS = (
    "setup_recognition",
    "stage_transition",
    "trigger_card",
    "trigger_level_or_zone",
    "invalidation",
    "fresh_stale_spent",
    "blocker_caution",
    "duplicate_suppression",
    "ranking_focus",
    "session_boundary",
    "data_quality",
    "market_context",
    "outcome_scoring",
    "review_logging",
    "user_facing_workflow",
)

HISTORICAL_OPTIMIZATION_READINESS_REQUIRED_FIELDS = (
    "diagnosed_failure_category",
    "evidence_or_explicit_unavailable",
    "affected_system_area",
    "next_fix_path",
    "regression_test_path",
    "no_trade_boundary_preserved",
)

HISTORICAL_OPTIMIZATION_READINESS_RESULT_FIELDS = (
    "watch_only",
    "historical_optimization_readiness_only",
    "optimization_started",
    "ready_for_optimization",
    "rows_processed",
    "diagnostic_findings_reviewed",
    "readiness_items",
    "blocked_items",
    "missing_evidence_items",
    "regression_test_paths",
    "no_trade_boundary_preserved",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

_EXPECTED_TRUE_BOUNDARY_FIELDS = (
    "watch_only",
    "historical_outcome_diagnostics_only",
    "no_hindsight_boundary_preserved",
    "no_trade_boundary_preserved",
)

_EXPECTED_FALSE_BOUNDARY_FIELDS = (
    "optimization_started",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

_FORBIDDEN_HISTORICAL_OPTIMIZATION_FIELD_NAMES = frozenset(
    {
        "account",
        "account_size",
        "account_sizing",
        "account_sizing_enabled",
        "approved_trade",
        "approved_trades",
        "auto_trade",
        "auto_trading",
        "broker",
        "broker_call",
        "broker_enabled",
        "broker_order",
        "buy",
        "contracts",
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

_SHALLOW_OPTIMIZATION_LABELS = frozenset(
    {
        "failed setup",
        "failed_setup",
        "bad alert",
        "bad_alert",
        "weak signal",
        "weak_signal",
        "bad trade",
        "bad_trade",
    }
)

def evaluate_historical_optimization_readiness(
    historical_diagnostics_summary: dict[str, Any],
) -> dict[str, Any]:
    """Return an in-memory historical optimization readiness summary."""
    if type(historical_diagnostics_summary) is not dict:
        raise TypeError(
            "Historical optimization readiness historical_diagnostics_summary "
            "must be a dict"
        )

    _validate_historical_diagnostics_summary(historical_diagnostics_summary)

    readiness_items = []
    blocked_items = []
    missing_evidence_items = []
    regression_test_paths = []

    for index, finding in enumerate(
        historical_diagnostics_summary["diagnostic_findings"]
    ):
        item = _readiness_item_for_finding(finding, index)
        readiness_items.append(item)
        if item["regression_test_path"]:
            regression_test_paths.append(deepcopy(item["regression_test_path"]))
        if not item["evidence_or_explicit_unavailable"]:
            missing_evidence_items.append(
                {
                    "index": index,
                    "row_id": item["row_id"],
                    "reason": (
                        "evidence is missing without an explicit unavailable marker"
                    ),
                }
            )
        if not item["ready"]:
            blocked_items.append(
                {
                    "index": index,
                    "row_id": item["row_id"],
                    "blocked_reasons": deepcopy(item["blocked_reasons"]),
                }
            )

    return {
        "watch_only": True,
        "historical_optimization_readiness_only": True,
        "optimization_started": False,
        "ready_for_optimization": not blocked_items,
        "rows_processed": historical_diagnostics_summary["rows_processed"],
        "diagnostic_findings_reviewed": len(
            historical_diagnostics_summary["diagnostic_findings"]
        ),
        "readiness_items": deepcopy(readiness_items),
        "blocked_items": deepcopy(blocked_items),
        "missing_evidence_items": deepcopy(missing_evidence_items),
        "regression_test_paths": deepcopy(regression_test_paths),
        "no_trade_boundary_preserved": True,
        "live_data_started": False,
        "controlled_shadow_data_started": False,
        "alerts_sent": False,
        "files_written": False,
        "broker_or_trade_behavior_enabled": False,
    }


def _validate_historical_diagnostics_summary(summary: Mapping[str, Any]) -> None:
    _reject_forbidden_historical_optimization_fields(summary, path=())

    missing_fields = [
        field_name
        for field_name in HISTORICAL_OUTCOME_DIAGNOSTICS_RESULT_FIELDS
        if field_name not in summary
    ]
    if missing_fields:
        raise ValueError(
            "Missing required historical outcome diagnostics fields: "
            + ", ".join(missing_fields)
        )

    for field_name in _EXPECTED_TRUE_BOUNDARY_FIELDS:
        if summary[field_name] is not True:
            raise ValueError(
                f"Historical optimization readiness requires {field_name}=True"
            )
    for field_name in _EXPECTED_FALSE_BOUNDARY_FIELDS:
        if summary[field_name] is not False:
            raise ValueError(
                f"Historical optimization readiness requires {field_name}=False"
            )

    if type(summary["diagnostic_findings"]) is not list:
        raise TypeError(
            "Historical optimization readiness diagnostic_findings must be a list"
        )
    if type(summary["unavailable_evidence"]) is not list:
        raise TypeError(
            "Historical optimization readiness unavailable_evidence must be a list"
        )

    for index, finding in enumerate(summary["diagnostic_findings"]):
        if type(finding) is not dict:
            raise TypeError(
                "Historical optimization readiness diagnostic_findings"
                f"[{index}] must be a dict"
            )
        _reject_shallow_label_without_evidence_or_fix_path(finding, index)
        _reject_fact_language_in_likely_causes(finding, index)


def _readiness_item_for_finding(
    finding: Mapping[str, Any],
    index: int,
) -> dict[str, Any]:
    failure_category = _diagnosed_failure_category(finding)
    evidence_or_unavailable = _has_evidence_or_unavailable_marker(finding)
    affected_system_area = _affected_system_area(finding)
    next_fix_path = _non_empty_string_or_none(finding.get("next_fix_path"))
    regression_test_path = _non_empty_string_or_none(
        finding.get("regression_test_path")
    )
    no_trade_boundary_preserved = finding.get("no_trade_boundary_preserved", True)

    blocked_reasons = []
    if failure_category is None:
        blocked_reasons.append("diagnosed failure category is missing")
    if not evidence_or_unavailable:
        blocked_reasons.append(
            "evidence is missing without an explicit unavailable marker"
        )
    if affected_system_area is None:
        blocked_reasons.append("affected system area is missing or unsupported")
    if next_fix_path is None:
        blocked_reasons.append("next fix path is missing")
    if regression_test_path is None:
        blocked_reasons.append("regression test path is missing")
    if no_trade_boundary_preserved is not True:
        blocked_reasons.append("no-trade boundary is not preserved")

    return {
        "index": index,
        "row_id": deepcopy(finding.get("row_id", "UNAVAILABLE")),
        "diagnosed_failure_category": deepcopy(failure_category),
        "evidence_or_explicit_unavailable": evidence_or_unavailable,
        "affected_setup_type": deepcopy(finding.get("affected_setup_type")),
        "affected_symbol": deepcopy(finding.get("affected_symbol")),
        "affected_stage": deepcopy(finding.get("affected_stage")),
        "trigger_invalidation_freshness_relationship": deepcopy(
            finding.get("trigger_invalidation_freshness_relationship")
        ),
        "affected_system_area": deepcopy(affected_system_area),
        "next_fix_path": deepcopy(next_fix_path),
        "regression_test_path": deepcopy(regression_test_path),
        "no_trade_boundary_preserved": no_trade_boundary_preserved is True,
        "ready": not blocked_reasons,
        "blocked_reasons": blocked_reasons,
    }


def _diagnosed_failure_category(finding: Mapping[str, Any]) -> Any:
    category = finding.get("diagnosed_failure_category")
    if category is None:
        category = finding.get("diagnostic_category")
    if _is_shallow_label(category):
        return None
    if _is_non_empty(category):
        return deepcopy(category)
    return None


def _affected_system_area(finding: Mapping[str, Any]) -> str | None:
    area = _non_empty_string_or_none(finding.get("affected_system_area"))
    if area in HISTORICAL_OPTIMIZATION_ALLOWED_SYSTEM_AREAS:
        return area
    return None


def _has_evidence_or_unavailable_marker(finding: Mapping[str, Any]) -> bool:
    for field_name in ("evidence", "evidence_used", "evidence_refs"):
        evidence = finding.get(field_name)
        if type(evidence) is list and evidence:
            return True
        if type(evidence) is dict and evidence:
            return True
        if _is_non_empty(evidence):
            return True

    if _has_explicit_unavailable_marker(finding.get("unavailable_evidence")):
        return True
    if _has_explicit_unavailable_marker(finding.get("evidence_unavailable")):
        return True
    return False


def _has_explicit_unavailable_marker(value: Any) -> bool:
    if type(value) is dict:
        return value.get("status") in {"unavailable", "unconfirmed"} or (
            value.get("explicitly_unavailable") is True
        )
    if type(value) is list:
        return any(_has_explicit_unavailable_marker(item) for item in value)
    return value is True


def _reject_shallow_label_without_evidence_or_fix_path(
    finding: Mapping[str, Any],
    index: int,
) -> None:
    labels = (
        finding.get("label"),
        finding.get("diagnosed_failure_category"),
        finding.get("diagnostic_category"),
        finding.get("failure_category"),
        finding.get("source_bucket"),
    )
    if not any(_is_shallow_label(label) for label in labels):
        return
    if _has_evidence_or_unavailable_marker(finding) and _non_empty_string_or_none(
        finding.get("next_fix_path")
    ):
        return
    raise ValueError(
        "Historical optimization readiness rejects shallow optimization labels "
        f"without evidence and fix path at diagnostic_findings[{index}]"
    )


def _reject_fact_language_in_likely_causes(
    finding: Mapping[str, Any],
    index: int,
) -> None:
    candidates = finding.get("likely_cause_candidates", [])
    if type(candidates) is not list:
        return
    for candidate in candidates:
        if type(candidate) is not dict:
            continue
        label = str(candidate.get("label", "")).strip().lower()
        if label in {"fact", "root_cause", "confirmed"}:
            raise ValueError(
                "Historical optimization readiness requires likely causes to remain "
                f"candidate language at diagnostic_findings[{index}]"
            )


def _reject_forbidden_historical_optimization_fields(
    value: Any,
    path: tuple[str, ...],
) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.lower()
            if (
                normalized_key in _FORBIDDEN_HISTORICAL_OPTIMIZATION_FIELD_NAMES
                and not _is_allowed_boundary_field(normalized_key, path)
            ):
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden execution/trade field: {dotted_path}")
            _reject_forbidden_historical_optimization_fields(
                nested_value, (*path, key_text)
            )
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_forbidden_historical_optimization_fields(
                nested_value, (*path, str(index))
            )


def _is_allowed_boundary_field(normalized_key: str, path: tuple[str, ...]) -> bool:
    if not path or path[-1] != "no_trade_boundary":
        return False
    return normalized_key in {
        "broker_enabled",
        "orders_enabled",
        "account_sizing_enabled",
        "option_pnl_enabled",
        "live_trade_decision_enabled",
    }


def _is_shallow_label(value: Any) -> bool:
    if value is None:
        return False
    normalized = str(value).strip().lower().replace("-", "_")
    return normalized in _SHALLOW_OPTIMIZATION_LABELS


def _is_non_empty(value: Any) -> bool:
    if value is None:
        return False
    if type(value) is str:
        return bool(value.strip())
    return bool(value)


def _non_empty_string_or_none(value: Any) -> str | None:
    if type(value) is str and value.strip():
        return value
    return None
