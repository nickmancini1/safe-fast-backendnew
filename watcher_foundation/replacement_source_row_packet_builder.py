"""SAFE-FAST replacement source row packet builder.

Pure local/in-memory builder only.
No file reads, no file writes, no live data, no broker/order/account/options/P&L,
no alerts, and no trade decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from .replacement_source_row_packet import (
    ALLOWED_CANDIDATES,
    validate_replacement_source_row_packet,
    validate_replacement_source_row_packet_batch,
)


OHLCV_ALIASES: dict[str, tuple[str, ...]] = {
    "open": ("open", "Open", "o"),
    "high": ("high", "High", "h"),
    "low": ("low", "Low", "l"),
    "close": ("close", "Close", "c"),
    "volume": ("volume", "Volume", "v"),
}

TIMESTAMP_KEYS: tuple[str, ...] = (
    "timestamp",
    "time",
    "datetime",
    "candle_time",
    "source_timestamp",
)


def _first_present(row: Mapping[str, Any], keys: Sequence[str]) -> Any:
    for key in keys:
        if key in row and row[key] is not None:
            return row[key]
    return None


def _coerce_number(value: Any) -> float | int | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return None
        try:
            as_float = float(stripped)
        except ValueError:
            return None
        if as_float.is_integer():
            return int(as_float)
        return as_float
    return None


def extract_setup_time_ohlcv(row: Mapping[str, Any]) -> dict[str, Any]:
    """Extract normalized OHLCV fields from one in-memory source row."""

    return {
        field: _coerce_number(_first_present(row, aliases))
        for field, aliases in OHLCV_ALIASES.items()
    }


def extract_setup_time_timestamp(row: Mapping[str, Any]) -> str | None:
    """Extract a setup-time timestamp from one in-memory source row."""

    value = _first_present(row, TIMESTAMP_KEYS)
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def build_replacement_source_row_packet_from_rows(
    *,
    candidate_id: str,
    source_rows: Sequence[Mapping[str, Any]],
    setup_time_row_index: int,
    source_file_reference: str,
    source_row_reference: str,
    source_window_start: str,
    source_window_end: str,
    trigger_candidate: float | int | None,
    trigger_basis: str,
    invalidation_candidate: float | int | None,
    invalidation_basis: str,
    freshness_final_signal_candidate: str,
    blocker_caution_status: str,
    unavailable_fields: Sequence[str] | None = None,
    after_setup_outcome_window_start: str,
    after_setup_outcome_window_end: str,
    no_hindsight_boundary: str = "setup-time row selected before terminal outcome review",
) -> dict[str, Any]:
    """Build and validate one replacement source row packet from in-memory rows."""

    if candidate_id not in ALLOWED_CANDIDATES:
        return {
            "candidate_id": candidate_id,
            "packet": None,
            "validation": {
                "candidate_id": candidate_id,
                "ready_for_acceptance_review": False,
                "decision": "missing_evidence_inconclusive",
                "rejected_reasons": ["unknown_candidate_id"],
            },
            "ready_for_acceptance_review": False,
            "decision": "missing_evidence_inconclusive",
            "watch_only": True,
            "no_trade_decision": True,
        }

    rows = list(source_rows)
    if setup_time_row_index < 0 or setup_time_row_index >= len(rows):
        packet = {
            "candidate_id": candidate_id,
            "symbol": ALLOWED_CANDIDATES[candidate_id][0],
            "setup_type": ALLOWED_CANDIDATES[candidate_id][1],
        }
        return {
            "candidate_id": candidate_id,
            "packet": packet,
            "validation": {
                "candidate_id": candidate_id,
                "ready_for_acceptance_review": False,
                "decision": "missing_evidence_inconclusive",
                "rejected_reasons": ["setup_time_row_index_out_of_range"],
            },
            "ready_for_acceptance_review": False,
            "decision": "missing_evidence_inconclusive",
            "watch_only": True,
            "no_trade_decision": True,
        }

    symbol, setup_type = ALLOWED_CANDIDATES[candidate_id]
    setup_row = deepcopy(dict(rows[setup_time_row_index]))
    timestamp = extract_setup_time_timestamp(setup_row)
    ohlcv = extract_setup_time_ohlcv(setup_row)

    packet = {
        "candidate_id": candidate_id,
        "symbol": symbol,
        "setup_type": setup_type,
        "timeframe": "1h_rth",
        "source_file_reference": source_file_reference,
        "source_row_reference": source_row_reference,
        "source_window_start": source_window_start,
        "source_window_end": source_window_end,
        "setup_time_candidate_row_timestamp": timestamp,
        "setup_time_candidate_row_ohlcv": ohlcv,
        "trigger_candidate": trigger_candidate,
        "trigger_basis": trigger_basis,
        "invalidation_candidate": invalidation_candidate,
        "invalidation_basis": invalidation_basis,
        "freshness_final_signal_candidate": freshness_final_signal_candidate,
        "blocker_caution_status": blocker_caution_status,
        "unavailable_fields": list(unavailable_fields or []),
        "no_hindsight_boundary": no_hindsight_boundary,
        "after_setup_outcome_window_start": after_setup_outcome_window_start,
        "after_setup_outcome_window_end": after_setup_outcome_window_end,
    }

    validation = validate_replacement_source_row_packet(packet)

    return {
        "candidate_id": candidate_id,
        "packet": packet,
        "validation": validation,
        "ready_for_acceptance_review": validation["ready_for_acceptance_review"],
        "decision": validation["decision"],
        "watch_only": True,
        "no_trade_decision": True,
    }


def build_replacement_source_row_packet_batch_from_rows(
    packet_requests: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Build and validate multiple source row packets from caller-provided rows."""

    built = [
        build_replacement_source_row_packet_from_rows(**dict(request))
        for request in packet_requests
    ]

    packets = [
        result["packet"]
        for result in built
        if isinstance(result.get("packet"), Mapping)
    ]

    batch_validation = validate_replacement_source_row_packet_batch(packets)

    return {
        "records_processed": len(built),
        "built_packets": built,
        "batch_validation": batch_validation,
        "ready_for_acceptance_review": sum(
            1 for result in built if result["ready_for_acceptance_review"]
        ),
        "missing_evidence_or_rejected": sum(
            1 for result in built if not result["ready_for_acceptance_review"]
        ),
        "watch_only": True,
        "no_trade_decision": True,
    }
