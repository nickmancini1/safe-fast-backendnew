"""Local-only Day 60 outcome scoring contract validation.

This module validates caller-provided in-memory outcome-review rows only. It
does not fetch data, write files, start live data, emit alerts, call brokers,
or make trade decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.constants import (
    ACCEPTED_DIRECTIONS,
    ACCEPTED_SETUP_TYPES,
    ACCEPTED_STAGES,
    ACCEPTED_TRIGGER_STATUSES,
    FORBIDDEN_EXECUTION_FIELD_NAMES,
)


DAY60_OUTCOME_SCORING_CONTRACT_REQUIRED_FIELDS = (
    "outcome_row_id",
    "source_review_packet_id",
    "symbol",
    "timeframe",
    "setup_type",
    "direction",
    "detection_timestamp",
    "outcome_review_timestamp",
    "stage_at_detection",
    "trigger_status_at_detection",
    "trigger_reference",
    "invalidation_reference",
    "outcome_window",
    "outcome_status",
    "follow_through_status",
    "failure_status",
    "mfe",
    "mae",
    "time_to_follow_through",
    "time_to_failure",
    "stale_spent_outcome",
    "blocker_caution_outcome",
    "evidence_refs",
    "unavailable_fields",
    "no_hindsight_boundary",
    "diagnostics_placeholders",
    "no_trade_boundary",
    "watch_only",
)

DAY60_OUTCOME_SCORING_CONTRACT_REQUIRED_PROOF_FIELDS = (
    "outcome_status",
    "follow_through_status",
    "failure_status",
    "mfe",
    "mae",
    "time_to_follow_through",
    "time_to_failure",
    "stale_spent_outcome",
    "blocker_caution_outcome",
    "evidence_refs",
    "no_hindsight_boundary",
)

DAY60_OUTCOME_SCORING_CONTRACT_RESULT_FIELDS = (
    "watch_only",
    "outcome_scoring_contract_only",
    "rows_processed",
    "rows_accepted",
    "rows_rejected",
    "accepted_rows",
    "rejected_rows",
    "no_trade_boundary_preserved",
    "live_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

FABRICATED_PROOF_MARKERS = (
    "FABRICATED",
    "MADE_UP",
    "ASSUMED_WITHOUT_EVIDENCE",
    "INVENTED",
    "UNKNOWN_BUT_FILLED",
    "FAKE",
)

FORBIDDEN_DAY60_OUTCOME_FIELD_NAMES = (
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

_NON_PROOF_REQUIRED_FIELDS = tuple(
    field_name
    for field_name in DAY60_OUTCOME_SCORING_CONTRACT_REQUIRED_FIELDS
    if field_name not in DAY60_OUTCOME_SCORING_CONTRACT_REQUIRED_PROOF_FIELDS
)


def validate_day60_outcome_scoring_row(row: dict[str, Any]) -> dict[str, Any]:
    """Return a defensive copy of a valid Day 60 outcome scoring row."""
    if type(row) is not dict:
        raise TypeError("Day 60 outcome scoring row must be a dict")

    _reject_forbidden_day60_outcome_fields(row, path=())
    _reject_fabricated_proof_values(row, path=())

    missing_non_proof_fields = [
        field_name for field_name in _NON_PROOF_REQUIRED_FIELDS if field_name not in row
    ]
    if missing_non_proof_fields:
        raise ValueError(
            "Missing required Day 60 outcome scoring fields: "
            + ", ".join(missing_non_proof_fields)
        )

    unavailable_fields = row["unavailable_fields"]
    _validate_unavailable_fields(unavailable_fields)
    unavailable_field_names = _unavailable_field_names(unavailable_fields)

    missing_proof_fields = [
        field_name
        for field_name in DAY60_OUTCOME_SCORING_CONTRACT_REQUIRED_PROOF_FIELDS
        if field_name not in row
    ]
    missing_without_unavailable_marker = [
        field_name
        for field_name in missing_proof_fields
        if field_name not in unavailable_field_names
    ]
    if missing_without_unavailable_marker:
        raise ValueError(
            "Missing required Day 60 outcome scoring proof fields: "
            + ", ".join(missing_without_unavailable_marker)
        )

    _require_string(row, "outcome_row_id")
    _require_string(row, "source_review_packet_id")
    _require_string(row, "symbol")
    _require_string(row, "timeframe")
    _require_string(row, "setup_type")
    _require_string(row, "direction")
    _require_string(row, "detection_timestamp")
    _require_string(row, "outcome_review_timestamp")
    _require_string(row, "stage_at_detection")
    _require_string(row, "trigger_status_at_detection")

    if row["setup_type"] not in ACCEPTED_SETUP_TYPES:
        raise ValueError(f"Unsupported setup_type: {row['setup_type']}")
    if row["direction"] not in ACCEPTED_DIRECTIONS:
        raise ValueError(f"Unsupported direction: {row['direction']}")
    if row["stage_at_detection"] not in ACCEPTED_STAGES:
        raise ValueError(f"Unsupported stage_at_detection: {row['stage_at_detection']}")
    if row["trigger_status_at_detection"] not in ACCEPTED_TRIGGER_STATUSES:
        raise ValueError(
            "Unsupported trigger_status_at_detection: "
            f"{row['trigger_status_at_detection']}"
        )

    if row["watch_only"] is not True:
        raise ValueError(
            "Day 60 outcome scoring contract rows must preserve watch_only=True"
        )

    _validate_reference(row["trigger_reference"], "trigger_reference")
    _validate_reference(row["invalidation_reference"], "invalidation_reference")
    _validate_outcome_window(row["outcome_window"])
    _validate_diagnostics_placeholders(row["diagnostics_placeholders"])
    _validate_no_trade_boundary(row["no_trade_boundary"])

    if "evidence_refs" in row:
        _validate_evidence_refs(row["evidence_refs"])
    if "no_hindsight_boundary" in row:
        _validate_no_hindsight_boundary(row["no_hindsight_boundary"])

    for field_name in DAY60_OUTCOME_SCORING_CONTRACT_REQUIRED_PROOF_FIELDS:
        if field_name in row and field_name not in {"evidence_refs", "no_hindsight_boundary"}:
            _validate_proof_value(row[field_name], field_name, unavailable_field_names)

    return deepcopy(dict(row))


def validate_day60_outcome_scoring_batch(
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate in-memory outcome rows and return an in-memory summary."""
    if type(rows) is not list:
        raise TypeError("Day 60 outcome scoring batch must be a list")

    accepted_rows = []
    rejected_rows = []

    for index, row in enumerate(rows):
        row_id = _extract_outcome_row_id(row)
        try:
            accepted_rows.append(validate_day60_outcome_scoring_row(row))
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
        "outcome_scoring_contract_only": True,
        "rows_processed": len(rows),
        "rows_accepted": len(accepted_rows),
        "rows_rejected": len(rejected_rows),
        "accepted_rows": accepted_rows,
        "rejected_rows": rejected_rows,
        "no_trade_boundary_preserved": True,
        "live_data_started": False,
        "alerts_sent": False,
        "files_written": False,
        "broker_or_trade_behavior_enabled": False,
    }


def _require_string(row: Mapping[str, Any], field_name: str) -> None:
    if type(row[field_name]) is not str:
        raise TypeError(f"Day 60 outcome scoring {field_name} must be a string")
    if not row[field_name]:
        raise ValueError(f"Day 60 outcome scoring {field_name} must not be empty")


def _validate_reference(reference: Any, field_name: str) -> None:
    if type(reference) is not dict:
        raise TypeError(f"Day 60 outcome scoring {field_name} must be a dict")
    if not reference:
        raise ValueError(f"Day 60 outcome scoring {field_name} must not be empty")
    if reference.get("fabricated") is not False:
        raise ValueError(
            f"Day 60 outcome scoring {field_name} must set fabricated=False"
        )


def _validate_outcome_window(outcome_window: Any) -> None:
    if type(outcome_window) is not dict:
        raise TypeError("Day 60 outcome scoring outcome_window must be a dict")
    for field_name in ("start_timestamp", "end_timestamp"):
        if type(outcome_window.get(field_name)) is not str or not outcome_window.get(
            field_name
        ):
            raise ValueError(
                f"Day 60 outcome scoring outcome_window must include {field_name}"
            )
    if outcome_window.get("caller_provided") is not True:
        raise ValueError(
            "Day 60 outcome scoring outcome_window must set caller_provided=True"
        )


def _validate_diagnostics_placeholders(placeholders: Any) -> None:
    if type(placeholders) is not dict:
        raise TypeError("Day 60 outcome scoring diagnostics_placeholders must be a dict")


def _validate_evidence_refs(evidence_refs: Any) -> None:
    if type(evidence_refs) is not list:
        raise TypeError("Day 60 outcome scoring evidence_refs must be a list")
    if not evidence_refs:
        raise ValueError("Day 60 outcome scoring evidence_refs must be non-empty")
    for index, ref in enumerate(evidence_refs):
        if type(ref) is not str or not ref:
            raise TypeError(
                f"Day 60 outcome scoring evidence_refs[{index}] must be a string"
            )


def _validate_unavailable_fields(unavailable_fields: Any) -> None:
    if type(unavailable_fields) not in {list, dict}:
        raise TypeError(
            "Day 60 outcome scoring unavailable_fields must be a list or dict"
        )

    items = _iter_unavailable_items(unavailable_fields)
    for field_name, item in items:
        if field_name not in DAY60_OUTCOME_SCORING_CONTRACT_REQUIRED_PROOF_FIELDS:
            continue
        if type(field_name) is not str or not field_name:
            raise ValueError(
                "Day 60 outcome scoring unavailable_fields must name fields explicitly"
            )
        if type(item) is not dict:
            raise TypeError(
                f"Day 60 outcome scoring unavailable_fields[{field_name}] must be a dict"
            )
        status = item.get("status")
        if status not in {"unavailable", "unconfirmed"}:
            raise ValueError(
                f"Day 60 outcome scoring unavailable_fields[{field_name}] "
                "status must be unavailable or unconfirmed"
            )
        if type(item.get("reason")) is not str or not item.get("reason"):
            raise ValueError(
                f"Day 60 outcome scoring unavailable_fields[{field_name}] "
                "must include reason"
            )
        if item.get("fabricated") is not False:
            raise ValueError(
                f"Day 60 outcome scoring unavailable_fields[{field_name}] "
                "must set fabricated=False"
            )


def _unavailable_field_names(unavailable_fields: Any) -> set[str]:
    return {
        field_name
        for field_name, item in _iter_unavailable_items(unavailable_fields)
        if field_name in DAY60_OUTCOME_SCORING_CONTRACT_REQUIRED_PROOF_FIELDS
        and type(item) is dict
        and item.get("status") in {"unavailable", "unconfirmed"}
    }


def _iter_unavailable_items(unavailable_fields: Any) -> list[tuple[str, Any]]:
    if type(unavailable_fields) is dict:
        return [(str(field_name), item) for field_name, item in unavailable_fields.items()]

    items = []
    for index, item in enumerate(unavailable_fields):
        if type(item) is not dict:
            raise TypeError(
                f"Day 60 outcome scoring unavailable_fields[{index}] must be a dict"
            )
        field_name = item.get("field_name")
        if type(field_name) is not str or not field_name:
            raise ValueError(
                f"Day 60 outcome scoring unavailable_fields[{index}] "
                "must include field_name"
            )
        items.append((field_name, item))
    return items


def _validate_no_hindsight_boundary(boundary: Any) -> None:
    if type(boundary) is not dict:
        raise TypeError("Day 60 outcome scoring no_hindsight_boundary must be a dict")
    required_true_fields = (
        "evidence_available_at_or_before_review_timestamp",
        "future_evidence_not_used",
        "no_backfilled_outcome_labels",
    )
    for field_name in required_true_fields:
        if boundary.get(field_name) is not True:
            raise ValueError(
                f"Day 60 outcome scoring no_hindsight_boundary must set "
                f"{field_name}=True"
            )
    if boundary.get("review_timestamp_field") != "outcome_review_timestamp":
        raise ValueError(
            "Day 60 outcome scoring no_hindsight_boundary must reference "
            "outcome_review_timestamp"
        )


def _validate_no_trade_boundary(boundary: Any) -> None:
    if type(boundary) is not dict:
        raise TypeError("Day 60 outcome scoring no_trade_boundary must be a dict")
    required_true_fields = (
        "no_trade",
        "no_broker",
        "no_order",
        "no_account_sizing",
        "no_option_pnl",
        "no_live_trade_decision",
    )
    for field_name in required_true_fields:
        if boundary.get(field_name) is not True:
            raise ValueError(
                f"Day 60 outcome scoring no_trade_boundary must set {field_name}=True"
            )
    required_false_fields = (
        "broker_enabled",
        "orders_enabled",
        "account_sizing_enabled",
        "option_pnl_enabled",
        "live_trade_decision_enabled",
    )
    for field_name in required_false_fields:
        if boundary.get(field_name) is not False:
            raise ValueError(
                f"Day 60 outcome scoring no_trade_boundary must set {field_name}=False"
            )


def _validate_proof_value(
    value: Any,
    field_name: str,
    unavailable_field_names: set[str],
) -> None:
    if value is None and field_name not in unavailable_field_names:
        raise ValueError(
            f"Day 60 outcome scoring proof field {field_name} is unavailable but "
            "not explicitly preserved in unavailable_fields"
        )
    if value == "" and field_name not in unavailable_field_names:
        raise ValueError(
            f"Day 60 outcome scoring proof field {field_name} must not be empty"
        )
    if type(value) is dict and value.get("fabricated") is not False:
        raise ValueError(
            f"Day 60 outcome scoring proof field {field_name} must set "
            "fabricated=False when represented as a dict"
        )


def _reject_fabricated_proof_values(value: Any, path: tuple[str, ...]) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            if key_text.lower() == "fabricated" and nested_value is True:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Fabricated proof value rejected: {dotted_path}")
            _reject_fabricated_proof_values(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_fabricated_proof_values(nested_value, (*path, str(index)))
    elif isinstance(value, str):
        normalized_value = value.upper()
        for marker in FABRICATED_PROOF_MARKERS:
            if marker in normalized_value:
                dotted_path = ".".join(path) or "row"
                raise ValueError(
                    f"Fabricated proof marker rejected at {dotted_path}: {marker}"
                )


def _reject_forbidden_day60_outcome_fields(value: Any, path: tuple[str, ...]) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.lower()
            if normalized_key in FORBIDDEN_DAY60_OUTCOME_FIELD_NAMES:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden execution/trade field: {dotted_path}")
            _reject_forbidden_day60_outcome_fields(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_forbidden_day60_outcome_fields(nested_value, (*path, str(index)))


def _extract_outcome_row_id(row: Any) -> str:
    if isinstance(row, Mapping) and "outcome_row_id" in row:
        return str(row["outcome_row_id"])
    return "UNAVAILABLE"
