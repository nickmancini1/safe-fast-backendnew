"""Local-only Day 60 shadow session dry-run adapter.

This module accepts caller-provided in-memory contract rows only. It validates
them through the Day 60 shadow contract validator and returns an in-memory
summary without live data, file, alert, broker, or trade behavior.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from watcher_foundation.day60_shadow_contract import (
    validate_day60_shadow_contract_batch,
    validate_day60_shadow_contract_row,
)


DAY60_SHADOW_SESSION_RESULT_FIELDS = (
    "watch_only",
    "dry_run_only",
    "rows_processed",
    "rows_accepted",
    "rows_rejected",
    "accepted_rows",
    "rejected_rows",
    "session_metadata",
    "no_trade_boundary_preserved",
    "live_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)


def run_day60_shadow_session_dry_run(
    rows: list[dict[str, Any]],
    session_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate caller-provided rows and return a dry-run session summary."""
    if type(rows) is not list:
        raise TypeError("Day 60 shadow session rows must be a list")
    if session_metadata is not None and type(session_metadata) is not dict:
        raise TypeError("Day 60 shadow session metadata must be a dict")

    batch_result = validate_day60_shadow_contract_batch(rows)

    # Re-run row validation for accepted rows so the session adapter explicitly
    # depends on the public row and batch validators without changing behavior.
    accepted_rows = [
        validate_day60_shadow_contract_row(row)
        for row in batch_result["accepted_rows"]
    ]

    return {
        "watch_only": True,
        "dry_run_only": True,
        "rows_processed": batch_result["rows_processed"],
        "rows_accepted": batch_result["accepted_count"],
        "rows_rejected": batch_result["rejected_count"],
        "accepted_rows": accepted_rows,
        "rejected_rows": deepcopy(batch_result["rejected_rows"]),
        "session_metadata": deepcopy(session_metadata) if session_metadata else {},
        "no_trade_boundary_preserved": True,
        "live_data_started": False,
        "alerts_sent": False,
        "files_written": False,
        "broker_or_trade_behavior_enabled": False,
    }
