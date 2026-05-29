"""Day 60 shadow watcher input-contract preflight validation.

This module validates caller-provided in-memory dictionaries only. It does not
fetch data, create data, write files, run loops, emit alerts, call brokers, or
make live trade decisions.
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
from watcher_foundation.trigger_card import REQUIRED_TRIGGER_CARD_FIELDS


DAY60_SHADOW_CONTRACT_REQUIRED_FIELDS = (
    "row_id",
    "watch_session_id",
    "symbol",
    "timestamp",
    "timeframe",
    "setup_type",
    "direction",
    "stage",
    "trigger_status",
    "trigger_card",
    "provenance",
    "diagnostics_placeholders",
    "unavailable_fields",
    "evidence_refs",
    "no_hindsight_boundary",
    "no_trade_boundary",
    "watch_only",
)

DAY60_SHADOW_CONTRACT_TRIGGER_CARD_REQUIRED_FIELDS = REQUIRED_TRIGGER_CARD_FIELDS

DAY60_SHADOW_CONTRACT_DIAGNOSTIC_PLACEHOLDER_FIELDS = (
    "setup_identity",
    "lifecycle_stage",
    "trigger_status",
    "trigger_quality",
    "fresh_stale_spent_state",
    "duplicate_suppression",
    "focus_ranking",
    "headline_news",
    "unavailable_fields",
    "no_trade_boundary",
)

FORBIDDEN_DAY60_SHADOW_CONTRACT_FIELD_NAMES = (
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


def validate_day60_shadow_contract_row(row: dict[str, Any]) -> dict[str, Any]:
    """Return a defensive copy of a valid Day 60 shadow contract row."""
    if type(row) is not dict:
        raise TypeError("Day 60 shadow contract row must be a dict")

    missing_fields = [
        field_name
        for field_name in DAY60_SHADOW_CONTRACT_REQUIRED_FIELDS
        if field_name not in row
    ]
    if missing_fields:
        raise ValueError(
            "Missing required Day 60 shadow contract fields: "
            + ", ".join(missing_fields)
        )

    _reject_forbidden_day60_fields(row, path=())

    _require_string(row, "row_id")
    _require_string(row, "watch_session_id")
    _require_string(row, "symbol")
    _require_string(row, "timestamp")
    _require_string(row, "timeframe")
    _require_string(row, "setup_type")
    _require_string(row, "direction")
    _require_string(row, "stage")
    _require_string(row, "trigger_status")

    if row["setup_type"] not in ACCEPTED_SETUP_TYPES:
        raise ValueError(f"Unsupported setup_type: {row['setup_type']}")
    if row["direction"] not in ACCEPTED_DIRECTIONS:
        raise ValueError(f"Unsupported direction: {row['direction']}")
    if row["stage"] not in ACCEPTED_STAGES:
        raise ValueError(f"Unsupported stage: {row['stage']}")
    if row["trigger_status"] not in ACCEPTED_TRIGGER_STATUSES:
        raise ValueError(f"Unsupported trigger_status: {row['trigger_status']}")

    if row["watch_only"] is not True:
        raise ValueError("Day 60 shadow contract rows must preserve watch_only=True")

    _validate_trigger_card(row["trigger_card"])
    _validate_provenance(row["provenance"])
    _validate_diagnostics_placeholders(row["diagnostics_placeholders"])
    _validate_unavailable_fields(row["unavailable_fields"])
    _validate_evidence_refs(row["evidence_refs"])
    _validate_no_hindsight_boundary(row["no_hindsight_boundary"])
    _validate_no_trade_boundary(row["no_trade_boundary"])

    return deepcopy(dict(row))


def validate_day60_shadow_contract_batch(
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate in-memory rows and return an in-memory acceptance summary."""
    if type(rows) is not list:
        raise TypeError("Day 60 shadow contract batch must be a list")

    accepted_rows = []
    rejected_rows = []

    for index, row in enumerate(rows):
        row_id = _extract_row_id(row)
        try:
            accepted_rows.append(validate_day60_shadow_contract_row(row))
        except (TypeError, ValueError) as exc:
            rejected_rows.append(
                {
                    "index": index,
                    "row_id": row_id,
                    "reason": str(exc),
                }
            )

    return {
        "rows_processed": len(rows),
        "accepted_count": len(accepted_rows),
        "rejected_count": len(rejected_rows),
        "accepted_rows": accepted_rows,
        "rejected_rows": rejected_rows,
        "watch_only": True,
    }


def _require_string(row: Mapping[str, Any], field_name: str) -> None:
    if type(row[field_name]) is not str:
        raise TypeError(f"Day 60 shadow contract {field_name} must be a string")
    if not row[field_name]:
        raise ValueError(f"Day 60 shadow contract {field_name} must not be empty")


def _validate_trigger_card(trigger_card: Any) -> None:
    if type(trigger_card) is not dict:
        raise TypeError("Day 60 shadow contract trigger_card must be a dict")

    missing_fields = [
        field_name
        for field_name in DAY60_SHADOW_CONTRACT_TRIGGER_CARD_REQUIRED_FIELDS
        if field_name not in trigger_card
    ]
    if missing_fields:
        raise ValueError(
            "Missing required Day 60 trigger_card fields: "
            + ", ".join(missing_fields)
        )

    if trigger_card["watch_only"] is not True:
        raise ValueError("Day 60 trigger_card must preserve watch_only=True")
    if trigger_card["setup_type"] not in ACCEPTED_SETUP_TYPES:
        raise ValueError(f"Unsupported trigger_card setup_type: {trigger_card['setup_type']}")
    if trigger_card["direction"] not in ACCEPTED_DIRECTIONS:
        raise ValueError(f"Unsupported trigger_card direction: {trigger_card['direction']}")
    if trigger_card["stage"] not in ACCEPTED_STAGES:
        raise ValueError(f"Unsupported trigger_card stage: {trigger_card['stage']}")
    if trigger_card["trigger_status"] not in ACCEPTED_TRIGGER_STATUSES:
        raise ValueError(
            f"Unsupported trigger_card trigger_status: {trigger_card['trigger_status']}"
        )


def _validate_provenance(provenance: Any) -> None:
    if type(provenance) is not dict:
        raise TypeError("Day 60 shadow contract provenance must be a dict")
    if provenance.get("input_source") != "caller_provided_in_memory":
        raise ValueError(
            "Day 60 provenance must identify caller_provided_in_memory input"
        )
    if provenance.get("caller_provided") is not True:
        raise ValueError("Day 60 provenance must set caller_provided=True")
    if provenance.get("live_data_fetch") is not False:
        raise ValueError("Day 60 provenance must set live_data_fetch=False")
    if provenance.get("data_created_by_validator") is not False:
        raise ValueError(
            "Day 60 provenance must set data_created_by_validator=False"
        )


def _validate_diagnostics_placeholders(placeholders: Any) -> None:
    if type(placeholders) is not dict:
        raise TypeError(
            "Day 60 diagnostics_placeholders must be a dict"
        )

    missing_fields = [
        field_name
        for field_name in DAY60_SHADOW_CONTRACT_DIAGNOSTIC_PLACEHOLDER_FIELDS
        if field_name not in placeholders
    ]
    if missing_fields:
        raise ValueError(
            "Missing Day 60 diagnostics placeholder fields: "
            + ", ".join(missing_fields)
        )

    for field_name in DAY60_SHADOW_CONTRACT_DIAGNOSTIC_PLACEHOLDER_FIELDS:
        placeholder = placeholders[field_name]
        if type(placeholder) is not dict:
            raise TypeError(
                f"Day 60 diagnostics placeholder {field_name} must be a dict"
            )
        if placeholder.get("placeholder_preserved") is not True:
            raise ValueError(
                f"Day 60 diagnostics placeholder {field_name} must preserve "
                "placeholder_preserved=True"
            )
        if type(placeholder.get("status")) is not str:
            raise TypeError(
                f"Day 60 diagnostics placeholder {field_name} status must be a string"
            )


def _validate_unavailable_fields(unavailable_fields: Any) -> None:
    if type(unavailable_fields) is not list:
        raise TypeError("Day 60 unavailable_fields must be a list")
    if not unavailable_fields:
        raise ValueError(
            "Day 60 unavailable_fields must explicitly list unavailable semantics"
        )

    for index, item in enumerate(unavailable_fields):
        if type(item) is not dict:
            raise TypeError(f"Day 60 unavailable_fields[{index}] must be a dict")
        for field_name in ("field_name", "status", "reason"):
            if type(item.get(field_name)) is not str or not item.get(field_name):
                raise ValueError(
                    f"Day 60 unavailable_fields[{index}] must include {field_name}"
                )
        if item["status"] not in {"unavailable", "unconfirmed"}:
            raise ValueError(
                f"Day 60 unavailable_fields[{index}] status must be explicit"
            )
        if item.get("fabricated") is not False:
            raise ValueError(
                f"Day 60 unavailable_fields[{index}] must set fabricated=False"
            )


def _validate_evidence_refs(evidence_refs: Any) -> None:
    if type(evidence_refs) is not list:
        raise TypeError("Day 60 evidence_refs must be a list")
    for index, ref in enumerate(evidence_refs):
        if type(ref) is not str or not ref:
            raise TypeError(f"Day 60 evidence_refs[{index}] must be a string")


def _validate_no_hindsight_boundary(boundary: Any) -> None:
    if type(boundary) is not dict:
        raise TypeError("Day 60 no_hindsight_boundary must be a dict")
    required_true_fields = (
        "evidence_frozen_before_review",
        "future_rows_not_used_for_candidate",
        "no_backfilled_trigger_labels",
    )
    for field_name in required_true_fields:
        if boundary.get(field_name) is not True:
            raise ValueError(
                f"Day 60 no_hindsight_boundary must set {field_name}=True"
            )


def _validate_no_trade_boundary(boundary: Any) -> None:
    if type(boundary) is not dict:
        raise TypeError("Day 60 no_trade_boundary must be a dict")
    required_true_fields = (
        "no_trade",
        "no_broker",
        "no_order",
        "no_live_decision",
        "no_trade_decision",
        "no_option_pnl",
        "no_account_sizing",
    )
    for field_name in required_true_fields:
        if boundary.get(field_name) is not True:
            raise ValueError(
                f"Day 60 no_trade_boundary must set {field_name}=True"
            )
    if boundary.get("live_decision_allowed") is not False:
        raise ValueError(
            "Day 60 no_trade_boundary must set live_decision_allowed=False"
        )


def _reject_forbidden_day60_fields(value: Any, path: tuple[str, ...]) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.lower()
            if normalized_key in FORBIDDEN_DAY60_SHADOW_CONTRACT_FIELD_NAMES:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden execution/trade field: {dotted_path}")
            _reject_forbidden_day60_fields(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_forbidden_day60_fields(nested_value, (*path, str(index)))


def _extract_row_id(row: Any) -> str:
    if isinstance(row, Mapping) and "row_id" in row:
        return str(row["row_id"])
    return "UNAVAILABLE"
