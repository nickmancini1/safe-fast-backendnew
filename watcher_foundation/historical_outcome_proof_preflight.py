"""Local-only historical outcome proof preflight validation.

This module accepts caller-provided in-memory historical outcome proof rows
only. It does not fetch data, write files, start shadow/live workflows, emit
alerts, call subprocesses, touch brokers/accounts/options/P&L, or make trade
decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.day60_outcome_scoring_contract import (
    DAY60_OUTCOME_SCORING_CONTRACT_REQUIRED_FIELDS,
    FABRICATED_PROOF_MARKERS,
    FORBIDDEN_DAY60_OUTCOME_FIELD_NAMES,
    validate_day60_outcome_scoring_row,
)


HISTORICAL_OUTCOME_PROOF_PREFLIGHT_REQUIRED_FIELDS = (
    *DAY60_OUTCOME_SCORING_CONTRACT_REQUIRED_FIELDS,
    "historical_review_boundary",
)

HISTORICAL_OUTCOME_PROOF_PREFLIGHT_RESULT_FIELDS = (
    "watch_only",
    "historical_outcome_preflight_only",
    "rows_processed",
    "rows_accepted",
    "rows_rejected",
    "accepted_rows",
    "rejected_rows",
    "no_hindsight_boundary_preserved",
    "no_trade_boundary_preserved",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

FORBIDDEN_HISTORICAL_OUTCOME_PROOF_FIELD_NAMES = (
    FORBIDDEN_DAY60_OUTCOME_FIELD_NAMES
    | frozenset(
        {
            "options",
            "p/l",
            "p_l",
            "profit-and-loss",
            "trade-decision",
        }
    )
)


def validate_historical_outcome_proof_row(row: dict[str, Any]) -> dict[str, Any]:
    """Return a defensive copy of a valid historical outcome proof row."""
    if type(row) is not dict:
        raise TypeError("Historical outcome proof preflight row must be a dict")

    _reject_forbidden_historical_outcome_fields(row, path=())
    _reject_fabricated_historical_proof_values(row, path=())

    missing_fields = [
        field_name
        for field_name in HISTORICAL_OUTCOME_PROOF_PREFLIGHT_REQUIRED_FIELDS
        if field_name not in row
    ]
    if missing_fields:
        raise ValueError(
            "Missing required historical outcome proof preflight fields: "
            + ", ".join(missing_fields)
        )

    if row["watch_only"] is not True:
        raise ValueError(
            "Historical outcome proof preflight rows must preserve watch_only=True"
        )

    _validate_historical_review_boundary(row["historical_review_boundary"])
    _validate_no_hindsight_historical_boundary(row["no_hindsight_boundary"])
    _validate_explicit_historical_preflight_fields(row)

    return deepcopy(validate_day60_outcome_scoring_row(row))


def validate_historical_outcome_proof_batch(
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate historical proof rows and return an in-memory summary."""
    if type(rows) is not list:
        raise TypeError("Historical outcome proof preflight batch must be a list")

    accepted_rows = []
    rejected_rows = []

    for index, row in enumerate(rows):
        row_id = _extract_outcome_row_id(row)
        try:
            accepted_rows.append(validate_historical_outcome_proof_row(row))
        except (TypeError, ValueError) as exc:
            rejected_rows.append(
                {
                    "index": index,
                    "row_id": row_id,
                    "reason": str(exc),
                }
            )

    return {
        "watch_only": True,
        "historical_outcome_preflight_only": True,
        "rows_processed": len(rows),
        "rows_accepted": len(accepted_rows),
        "rows_rejected": len(rejected_rows),
        "accepted_rows": accepted_rows,
        "rejected_rows": rejected_rows,
        "no_hindsight_boundary_preserved": True,
        "no_trade_boundary_preserved": True,
        "live_data_started": False,
        "controlled_shadow_data_started": False,
        "alerts_sent": False,
        "files_written": False,
        "broker_or_trade_behavior_enabled": False,
    }


def _validate_historical_review_boundary(boundary: Any) -> None:
    if type(boundary) is not dict:
        raise TypeError(
            "Historical outcome proof preflight historical_review_boundary "
            "must be a dict"
        )

    required_true_fields = (
        "caller_provided",
        "historical_review_only",
        "no_live_data",
        "no_controlled_shadow_data",
        "no_generated_report",
    )
    for field_name in required_true_fields:
        if boundary.get(field_name) is not True:
            raise ValueError(
                "Historical outcome proof preflight historical_review_boundary "
                f"must set {field_name}=True"
            )


def _validate_no_hindsight_historical_boundary(boundary: Any) -> None:
    if type(boundary) is not dict:
        raise TypeError(
            "Historical outcome proof preflight no_hindsight_boundary must be a dict"
        )

    if boundary.get("evidence_available_at_or_before_review_timestamp") is not True:
        raise ValueError(
            "Historical outcome proof preflight no_hindsight_boundary must set "
            "evidence_available_at_or_before_review_timestamp=True"
        )
    if boundary.get("future_evidence_not_used") is not True:
        raise ValueError(
            "Historical outcome proof preflight no_hindsight_boundary must set "
            "future_evidence_not_used=True"
        )
    if boundary.get("review_timestamp_field") != "outcome_review_timestamp":
        raise ValueError(
            "Historical outcome proof preflight no_hindsight_boundary must reference "
            "outcome_review_timestamp"
        )
    if boundary.get("future_evidence_outside_declared_window_used") is True:
        raise ValueError(
            "Historical outcome proof preflight no_hindsight_boundary must not use "
            "future evidence outside the declared outcome_window"
        )
    if boundary.get("outcome_window_field") not in {None, "outcome_window"}:
        raise ValueError(
            "Historical outcome proof preflight no_hindsight_boundary must reference "
            "outcome_window when outcome_window_field is provided"
        )


def _validate_explicit_historical_preflight_fields(row: Mapping[str, Any]) -> None:
    for field_name in ("symbol", "setup_type", "timeframe"):
        if type(row[field_name]) is not str or not row[field_name]:
            raise ValueError(
                "Historical outcome proof preflight requires explicit "
                f"{field_name}"
            )

    for field_name in ("trigger_reference", "invalidation_reference", "outcome_window"):
        if type(row[field_name]) is not dict or not row[field_name]:
            raise ValueError(
                "Historical outcome proof preflight requires explicit "
                f"{field_name}"
            )

    if type(row["evidence_refs"]) is not list or not row["evidence_refs"]:
        raise ValueError(
            "Historical outcome proof preflight requires non-empty evidence_refs"
        )

    if type(row["unavailable_fields"]) not in {list, dict}:
        raise TypeError(
            "Historical outcome proof preflight unavailable_fields must be explicit"
        )


def _reject_fabricated_historical_proof_values(value: Any, path: tuple[str, ...]) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            if key_text.lower() == "fabricated" and nested_value is True:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Fabricated proof value rejected: {dotted_path}")
            _reject_fabricated_historical_proof_values(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_fabricated_historical_proof_values(
                nested_value, (*path, str(index))
            )
    elif isinstance(value, str):
        normalized_value = value.upper()
        for marker in FABRICATED_PROOF_MARKERS:
            if marker in normalized_value:
                dotted_path = ".".join(path) or "row"
                raise ValueError(
                    f"Fabricated proof marker rejected at {dotted_path}: {marker}"
                )


def _reject_forbidden_historical_outcome_fields(
    value: Any,
    path: tuple[str, ...],
) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.lower()
            if normalized_key in FORBIDDEN_HISTORICAL_OUTCOME_PROOF_FIELD_NAMES:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden execution/trade field: {dotted_path}")
            _reject_forbidden_historical_outcome_fields(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_forbidden_historical_outcome_fields(
                nested_value, (*path, str(index))
            )


def _extract_outcome_row_id(row: Any) -> str:
    if isinstance(row, Mapping) and "outcome_row_id" in row:
        return str(row["outcome_row_id"])
    return "UNAVAILABLE"
