"""Local-only Day 60 shadow review/diagnostics packet builder.

This module accepts an in-memory Day 60 shadow session dry-run result only and
returns an in-memory review packet. It does not fetch data, write files, start
loops, emit alerts, call brokers, or make trade decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.constants import FORBIDDEN_EXECUTION_FIELD_NAMES
from watcher_foundation.day60_shadow_session import DAY60_SHADOW_SESSION_RESULT_FIELDS


DAY60_SHADOW_REVIEW_PACKET_RESULT_FIELDS = (
    "watch_only",
    "review_packet_only",
    "dry_run_only",
    "rows_processed",
    "rows_accepted",
    "rows_rejected",
    "accepted_rows",
    "rejected_rows",
    "session_metadata",
    "diagnostic_placeholders",
    "outcome_scoring_placeholders",
    "viability_review_placeholders",
    "no_trade_boundary_preserved",
    "live_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

DAY60_SHADOW_REVIEW_PACKET_DIAGNOSTIC_PLACEHOLDER_FIELDS = (
    "setup_identity_review",
    "lifecycle_stage_review",
    "trigger_status_review",
    "trigger_quality_review",
    "fresh_stale_spent_review",
    "duplicate_suppression_review",
    "focus_ranking_review",
    "headline_news_review",
    "unavailable_fields_review",
    "boundary_review",
)

DAY60_SHADOW_REVIEW_PACKET_OUTCOME_PLACEHOLDER_FIELDS = (
    "future_outcome_window",
    "future_mfe_mae",
    "future_terminal_state",
    "future_same_day_fast_swing",
    "future_no_hindsight_outcome_review",
)

DAY60_SHADOW_REVIEW_PACKET_VIABILITY_PLACEHOLDER_FIELDS = (
    "review_readiness",
    "controlled_shadow_data_readiness",
    "diagnostics_usefulness",
    "day60_viability",
    "live_readiness_boundary",
)

FORBIDDEN_DAY60_SHADOW_REVIEW_PACKET_FIELD_NAMES = (
    FORBIDDEN_EXECUTION_FIELD_NAMES
    | frozenset(
        {
            "approved_trade",
            "approved_trades",
            "auto_trade",
            "auto_trading",
            "broker_call",
            "broker_order",
            "live_trade",
            "live_trade_approval",
            "p_and_l",
            "p&l",
            "pl",
            "trade",
            "trade_approval",
            "trade_decision",
            "trade_decisions",
        }
    )
)

_REQUIRED_TRUE_DRY_RUN_FIELDS = (
    "watch_only",
    "dry_run_only",
    "no_trade_boundary_preserved",
)

_REQUIRED_FALSE_DRY_RUN_FIELDS = (
    "live_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)


def build_day60_shadow_review_packet(dry_run_result: dict[str, Any]) -> dict[str, Any]:
    """Return an in-memory review packet for a valid dry-run adapter result."""
    if type(dry_run_result) is not dict:
        raise TypeError("Day 60 shadow review packet input must be a dict")

    missing_fields = [
        field_name
        for field_name in DAY60_SHADOW_SESSION_RESULT_FIELDS
        if field_name not in dry_run_result
    ]
    if missing_fields:
        raise ValueError(
            "Missing required Day 60 shadow dry-run result fields: "
            + ", ".join(missing_fields)
        )
    unexpected_fields = [
        field_name
        for field_name in dry_run_result
        if field_name not in DAY60_SHADOW_SESSION_RESULT_FIELDS
    ]
    if unexpected_fields:
        raise ValueError(
            "Unexpected Day 60 shadow dry-run result fields: "
            + ", ".join(unexpected_fields)
        )

    _reject_forbidden_day60_review_packet_fields(dry_run_result, path=())
    _validate_dry_run_boundaries(dry_run_result)
    _validate_dry_run_counts_and_rows(dry_run_result)

    return {
        "watch_only": True,
        "review_packet_only": True,
        "dry_run_only": True,
        "rows_processed": dry_run_result["rows_processed"],
        "rows_accepted": dry_run_result["rows_accepted"],
        "rows_rejected": dry_run_result["rows_rejected"],
        "accepted_rows": deepcopy(dry_run_result["accepted_rows"]),
        "rejected_rows": deepcopy(dry_run_result["rejected_rows"]),
        "session_metadata": deepcopy(dry_run_result["session_metadata"]),
        "diagnostic_placeholders": _build_placeholder_section(
            DAY60_SHADOW_REVIEW_PACKET_DIAGNOSTIC_PLACEHOLDER_FIELDS,
            "placeholder_only_future_review_ready_diagnostic",
        ),
        "outcome_scoring_placeholders": _build_placeholder_section(
            DAY60_SHADOW_REVIEW_PACKET_OUTCOME_PLACEHOLDER_FIELDS,
            "placeholder_only_future_outcome_scoring",
        ),
        "viability_review_placeholders": _build_placeholder_section(
            DAY60_SHADOW_REVIEW_PACKET_VIABILITY_PLACEHOLDER_FIELDS,
            "placeholder_only_future_viability_review",
        ),
        "no_trade_boundary_preserved": True,
        "live_data_started": False,
        "alerts_sent": False,
        "files_written": False,
        "broker_or_trade_behavior_enabled": False,
    }


def _validate_dry_run_boundaries(dry_run_result: Mapping[str, Any]) -> None:
    for field_name in _REQUIRED_TRUE_DRY_RUN_FIELDS:
        if dry_run_result[field_name] is not True:
            raise ValueError(
                f"Day 60 shadow dry-run result must preserve {field_name}=True"
            )
    for field_name in _REQUIRED_FALSE_DRY_RUN_FIELDS:
        if dry_run_result[field_name] is not False:
            raise ValueError(
                f"Day 60 shadow dry-run result must preserve {field_name}=False"
            )


def _validate_dry_run_counts_and_rows(dry_run_result: Mapping[str, Any]) -> None:
    for field_name in ("rows_processed", "rows_accepted", "rows_rejected"):
        if type(dry_run_result[field_name]) is not int:
            raise TypeError(f"Day 60 shadow dry-run {field_name} must be an int")
        if dry_run_result[field_name] < 0:
            raise ValueError(f"Day 60 shadow dry-run {field_name} must be non-negative")

    if type(dry_run_result["accepted_rows"]) is not list:
        raise TypeError("Day 60 shadow dry-run accepted_rows must be a list")
    if type(dry_run_result["rejected_rows"]) is not list:
        raise TypeError("Day 60 shadow dry-run rejected_rows must be a list")
    if type(dry_run_result["session_metadata"]) is not dict:
        raise TypeError("Day 60 shadow dry-run session_metadata must be a dict")

    if dry_run_result["rows_accepted"] != len(dry_run_result["accepted_rows"]):
        raise ValueError(
            "Day 60 shadow dry-run rows_accepted must match accepted_rows length"
        )
    if dry_run_result["rows_rejected"] != len(dry_run_result["rejected_rows"]):
        raise ValueError(
            "Day 60 shadow dry-run rows_rejected must match rejected_rows length"
        )
    if dry_run_result["rows_processed"] != (
        dry_run_result["rows_accepted"] + dry_run_result["rows_rejected"]
    ):
        raise ValueError(
            "Day 60 shadow dry-run rows_processed must equal accepted plus rejected rows"
        )


def _build_placeholder_section(
    field_names: tuple[str, ...],
    status: str,
) -> dict[str, dict[str, Any]]:
    return {
        field_name: {
            "status": status,
            "placeholder_preserved": True,
            "review_required_later": True,
            "watch_only": True,
            "no_trade_boundary_preserved": True,
        }
        for field_name in field_names
    }


def _reject_forbidden_day60_review_packet_fields(
    value: Any,
    path: tuple[str, ...],
) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.lower()
            if normalized_key in FORBIDDEN_DAY60_SHADOW_REVIEW_PACKET_FIELD_NAMES:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden execution/trade field: {dotted_path}")
            _reject_forbidden_day60_review_packet_fields(
                nested_value,
                (*path, key_text),
            )
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_forbidden_day60_review_packet_fields(
                nested_value,
                (*path, str(index)),
            )
