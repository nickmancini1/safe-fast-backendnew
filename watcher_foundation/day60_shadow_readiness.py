"""Local-only Day 60 diagnostics readiness evaluator.

This module accepts an in-memory Day 60 shadow review packet only and returns
an in-memory readiness summary. It does not fetch data, write files, start
loops, emit alerts, call brokers, or make trade decisions.
"""

from __future__ import annotations

from typing import Any, Mapping

from watcher_foundation.constants import FORBIDDEN_EXECUTION_FIELD_NAMES
from watcher_foundation.day60_shadow_review_packet import (
    DAY60_SHADOW_REVIEW_PACKET_DIAGNOSTIC_PLACEHOLDER_FIELDS,
    DAY60_SHADOW_REVIEW_PACKET_OUTCOME_PLACEHOLDER_FIELDS,
    DAY60_SHADOW_REVIEW_PACKET_RESULT_FIELDS,
    DAY60_SHADOW_REVIEW_PACKET_VIABILITY_PLACEHOLDER_FIELDS,
)


DAY60_SHADOW_READINESS_RESULT_FIELDS = (
    "watch_only",
    "readiness_evaluation_only",
    "review_packet_only",
    "diagnostic_placeholders_present",
    "outcome_scoring_placeholders_present",
    "viability_review_placeholders_present",
    "diagnostic_gaps",
    "missing_proof_fields",
    "ready_for_controlled_shadow_review",
    "ready_for_live_data",
    "ready_for_alerts",
    "ready_for_trading",
    "no_trade_boundary_preserved",
    "live_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

DAY60_SHADOW_READINESS_REQUIRED_PROOF_FIELDS = (
    "rows_processed",
    "rows_accepted",
    "rows_rejected",
    "accepted_rows",
    "rejected_rows",
    "session_metadata",
    "accepted_rows[].row_id",
    "accepted_rows[].watch_session_id",
    "accepted_rows[].symbol",
    "accepted_rows[].timestamp",
    "accepted_rows[].timeframe",
    "accepted_rows[].setup_type",
    "accepted_rows[].direction",
    "accepted_rows[].stage",
    "accepted_rows[].trigger_status",
    "accepted_rows[].trigger_card",
    "accepted_rows[].provenance",
    "accepted_rows[].diagnostics_placeholders",
    "accepted_rows[].unavailable_fields",
    "accepted_rows[].evidence_refs",
    "accepted_rows[].no_hindsight_boundary",
    "accepted_rows[].no_trade_boundary",
    "accepted_rows[].watch_only",
)

FORBIDDEN_DAY60_SHADOW_READINESS_FIELD_NAMES = (
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

_REQUIRED_TRUE_PACKET_FIELDS = (
    "watch_only",
    "review_packet_only",
    "dry_run_only",
    "no_trade_boundary_preserved",
)

_REQUIRED_FALSE_PACKET_FIELDS = (
    "live_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

_ACCEPTED_ROW_REQUIRED_PROOF_FIELDS = (
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


def evaluate_day60_shadow_readiness(review_packet: dict[str, Any]) -> dict[str, Any]:
    """Return an in-memory Day 60 diagnostics readiness summary."""
    if type(review_packet) is not dict:
        raise TypeError("Day 60 shadow readiness input must be a dict")

    _validate_required_packet_fields(review_packet)
    _reject_forbidden_day60_readiness_fields(review_packet, path=())
    _validate_packet_boundaries(review_packet)
    _validate_packet_counts_and_rows(review_packet)
    _validate_accepted_row_boundaries(review_packet["accepted_rows"])

    diagnostic_gaps: list[str] = []
    missing_proof_fields = _find_missing_proof_fields(review_packet)
    diagnostic_gaps.extend(
        f"missing_proof_field:{field_name}"
        for field_name in missing_proof_fields
    )

    diagnostic_placeholders_present = _collect_placeholder_gaps(
        review_packet,
        section_name="diagnostic_placeholders",
        required_fields=DAY60_SHADOW_REVIEW_PACKET_DIAGNOSTIC_PLACEHOLDER_FIELDS,
        diagnostic_gaps=diagnostic_gaps,
    )
    outcome_scoring_placeholders_present = _collect_placeholder_gaps(
        review_packet,
        section_name="outcome_scoring_placeholders",
        required_fields=DAY60_SHADOW_REVIEW_PACKET_OUTCOME_PLACEHOLDER_FIELDS,
        diagnostic_gaps=diagnostic_gaps,
    )
    viability_review_placeholders_present = _collect_placeholder_gaps(
        review_packet,
        section_name="viability_review_placeholders",
        required_fields=DAY60_SHADOW_REVIEW_PACKET_VIABILITY_PLACEHOLDER_FIELDS,
        diagnostic_gaps=diagnostic_gaps,
    )

    ready_for_controlled_shadow_review = not diagnostic_gaps

    return {
        "watch_only": True,
        "readiness_evaluation_only": True,
        "review_packet_only": True,
        "diagnostic_placeholders_present": diagnostic_placeholders_present,
        "outcome_scoring_placeholders_present": outcome_scoring_placeholders_present,
        "viability_review_placeholders_present": viability_review_placeholders_present,
        "diagnostic_gaps": diagnostic_gaps,
        "missing_proof_fields": missing_proof_fields,
        "ready_for_controlled_shadow_review": ready_for_controlled_shadow_review,
        "ready_for_live_data": False,
        "ready_for_alerts": False,
        "ready_for_trading": False,
        "no_trade_boundary_preserved": True,
        "live_data_started": False,
        "alerts_sent": False,
        "files_written": False,
        "broker_or_trade_behavior_enabled": False,
    }


def _validate_required_packet_fields(review_packet: Mapping[str, Any]) -> None:
    missing_fields = [
        field_name
        for field_name in DAY60_SHADOW_REVIEW_PACKET_RESULT_FIELDS
        if field_name not in review_packet
    ]
    if missing_fields:
        raise ValueError(
            "Missing required Day 60 shadow review packet fields: "
            + ", ".join(missing_fields)
        )

    unexpected_fields = [
        field_name
        for field_name in review_packet
        if field_name not in DAY60_SHADOW_REVIEW_PACKET_RESULT_FIELDS
    ]
    if unexpected_fields:
        raise ValueError(
            "Unexpected Day 60 shadow review packet fields: "
            + ", ".join(unexpected_fields)
        )


def _validate_packet_boundaries(review_packet: Mapping[str, Any]) -> None:
    for field_name in _REQUIRED_TRUE_PACKET_FIELDS:
        if review_packet[field_name] is not True:
            raise ValueError(
                f"Day 60 shadow review packet must preserve {field_name}=True"
            )
    for field_name in _REQUIRED_FALSE_PACKET_FIELDS:
        if review_packet[field_name] is not False:
            raise ValueError(
                f"Day 60 shadow review packet must preserve {field_name}=False"
            )


def _validate_packet_counts_and_rows(review_packet: Mapping[str, Any]) -> None:
    for field_name in ("rows_processed", "rows_accepted", "rows_rejected"):
        if type(review_packet[field_name]) is not int:
            raise TypeError(f"Day 60 shadow review packet {field_name} must be an int")
        if review_packet[field_name] < 0:
            raise ValueError(
                f"Day 60 shadow review packet {field_name} must be non-negative"
            )

    if type(review_packet["accepted_rows"]) is not list:
        raise TypeError("Day 60 shadow review packet accepted_rows must be a list")
    if type(review_packet["rejected_rows"]) is not list:
        raise TypeError("Day 60 shadow review packet rejected_rows must be a list")
    if type(review_packet["session_metadata"]) is not dict:
        raise TypeError("Day 60 shadow review packet session_metadata must be a dict")

    if review_packet["rows_accepted"] != len(review_packet["accepted_rows"]):
        raise ValueError(
            "Day 60 shadow review packet rows_accepted must match accepted_rows length"
        )
    if review_packet["rows_rejected"] != len(review_packet["rejected_rows"]):
        raise ValueError(
            "Day 60 shadow review packet rows_rejected must match rejected_rows length"
        )
    if review_packet["rows_processed"] != (
        review_packet["rows_accepted"] + review_packet["rows_rejected"]
    ):
        raise ValueError(
            "Day 60 shadow review packet rows_processed must equal accepted plus rejected rows"
        )


def _validate_accepted_row_boundaries(accepted_rows: list[Any]) -> None:
    required_true_no_trade_fields = (
        "no_trade",
        "no_broker",
        "no_order",
        "no_live_decision",
        "no_trade_decision",
        "no_option_pnl",
        "no_account_sizing",
    )

    for index, accepted_row in enumerate(accepted_rows):
        if type(accepted_row) is not dict:
            continue
        if "watch_only" in accepted_row and accepted_row["watch_only"] is not True:
            raise ValueError(
                f"Day 60 shadow review packet accepted_rows[{index}].watch_only=True"
            )

        provenance = accepted_row.get("provenance")
        if isinstance(provenance, Mapping):
            if provenance.get("live_data_fetch") is not False:
                raise ValueError(
                    "Day 60 shadow review packet "
                    f"accepted_rows[{index}].provenance.live_data_fetch=False"
                )
            if provenance.get("data_created_by_validator") is not False:
                raise ValueError(
                    "Day 60 shadow review packet "
                    f"accepted_rows[{index}].provenance.data_created_by_validator=False"
                )

        no_trade_boundary = accepted_row.get("no_trade_boundary")
        if isinstance(no_trade_boundary, Mapping):
            for field_name in required_true_no_trade_fields:
                if no_trade_boundary.get(field_name) is not True:
                    raise ValueError(
                        "Day 60 shadow review packet "
                        f"accepted_rows[{index}].no_trade_boundary.{field_name}=True"
                    )
            if no_trade_boundary.get("live_decision_allowed") is not False:
                raise ValueError(
                    "Day 60 shadow review packet "
                    f"accepted_rows[{index}].no_trade_boundary.live_decision_allowed=False"
                )


def _find_missing_proof_fields(review_packet: Mapping[str, Any]) -> list[str]:
    missing_fields = [
        field_name
        for field_name in (
            "rows_processed",
            "rows_accepted",
            "rows_rejected",
            "accepted_rows",
            "rejected_rows",
            "session_metadata",
        )
        if field_name not in review_packet
    ]

    for index, accepted_row in enumerate(review_packet["accepted_rows"]):
        if type(accepted_row) is not dict:
            missing_fields.append(f"accepted_rows[{index}]")
            continue
        for field_name in _ACCEPTED_ROW_REQUIRED_PROOF_FIELDS:
            if field_name not in accepted_row:
                missing_fields.append(f"accepted_rows[{index}].{field_name}")

    return missing_fields


def _collect_placeholder_gaps(
    review_packet: Mapping[str, Any],
    section_name: str,
    required_fields: tuple[str, ...],
    diagnostic_gaps: list[str],
) -> bool:
    section = review_packet[section_name]
    if type(section) is not dict:
        raise TypeError(f"Day 60 shadow review packet {section_name} must be a dict")

    section_present = True
    for field_name in required_fields:
        placeholder = section.get(field_name)
        if type(placeholder) is not dict:
            diagnostic_gaps.append(f"missing_{section_name}:{field_name}")
            section_present = False
            continue
        if placeholder.get("placeholder_preserved") is not True:
            diagnostic_gaps.append(
                f"{section_name}:{field_name}:placeholder_preserved_not_true"
            )
            section_present = False
        if placeholder.get("review_required_later") is not True:
            diagnostic_gaps.append(
                f"{section_name}:{field_name}:review_required_later_not_true"
            )
            section_present = False
        if placeholder.get("watch_only") is not True:
            diagnostic_gaps.append(f"{section_name}:{field_name}:watch_only_not_true")
            section_present = False
        if placeholder.get("no_trade_boundary_preserved") is not True:
            diagnostic_gaps.append(
                f"{section_name}:{field_name}:no_trade_boundary_preserved_not_true"
            )
            section_present = False

    return section_present


def _reject_forbidden_day60_readiness_fields(
    value: Any,
    path: tuple[str, ...],
) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.lower()
            if normalized_key in FORBIDDEN_DAY60_SHADOW_READINESS_FIELD_NAMES:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden execution/trade field: {dotted_path}")
            _reject_forbidden_day60_readiness_fields(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_forbidden_day60_readiness_fields(
                nested_value,
                (*path, str(index)),
            )
