"""SAFE-FAST replacement source row packet validation.

Pure local/in-memory validation only.
No live data, no broker/order/account/options/P&L, no alerts, no file writes.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence


ALLOWED_CANDIDATES: dict[str, tuple[str, str]] = {
    "IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001": ("IWM", "Continuation"),
    "IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002": ("IWM", "Continuation"),
    "GLD-REPLACEMENT-IDEAL-CANDIDATE-001": ("GLD", "Ideal"),
    "GLD-REPLACEMENT-IDEAL-CANDIDATE-002": ("GLD", "Ideal"),
}

REQUIRED_FIELDS: tuple[str, ...] = (
    "candidate_id",
    "symbol",
    "setup_type",
    "timeframe",
    "source_file_reference",
    "source_row_reference",
    "source_window_start",
    "source_window_end",
    "setup_time_candidate_row_timestamp",
    "setup_time_candidate_row_ohlcv",
    "trigger_candidate",
    "trigger_basis",
    "invalidation_candidate",
    "invalidation_basis",
    "freshness_final_signal_candidate",
    "blocker_caution_status",
    "unavailable_fields",
    "no_hindsight_boundary",
    "after_setup_outcome_window_start",
    "after_setup_outcome_window_end",
)

OHLCV_FIELDS: tuple[str, ...] = ("open", "high", "low", "close", "volume")

FORBIDDEN_KEY_PARTS: tuple[str, ...] = (
    "broker",
    "order",
    "account",
    "option_pnl",
    "options_pnl",
    "p&l",
    "pnl",
    "position_size",
    "account_size",
    "sizing",
    "live_trade",
    "trade_decision",
    "trade_approval",
    "execution",
    "fill_price",
    "real_money",
    "railway",
    "production",
    "secret",
    "credential",
    "token",
    "env",
)


def _is_present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return len(value) > 0
    if isinstance(value, Mapping):
        return len(value) > 0
    return True


def _walk_forbidden_keys(value: Any, path: str = "") -> list[str]:
    hits: list[str] = []

    if isinstance(value, Mapping):
        for key, child in value.items():
            key_text = str(key).lower()
            child_path = f"{path}.{key}" if path else str(key)
            if any(part in key_text for part in FORBIDDEN_KEY_PARTS):
                hits.append(child_path)
            hits.extend(_walk_forbidden_keys(child, child_path))
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, child in enumerate(value):
            hits.extend(_walk_forbidden_keys(child, f"{path}[{index}]"))

    return hits


def _missing_required_fields(packet: Mapping[str, Any]) -> list[str]:
    return [field for field in REQUIRED_FIELDS if not _is_present(packet.get(field))]


def _invalid_ohlcv_fields(packet: Mapping[str, Any]) -> list[str]:
    row = packet.get("setup_time_candidate_row_ohlcv")
    if not isinstance(row, Mapping):
        return list(OHLCV_FIELDS)

    bad: list[str] = []
    for field in OHLCV_FIELDS:
        value = row.get(field)
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            bad.append(field)
    return bad


def _timeline_errors(packet: Mapping[str, Any]) -> list[str]:
    setup_time = str(packet.get("setup_time_candidate_row_timestamp", ""))
    outcome_start = str(packet.get("after_setup_outcome_window_start", ""))
    outcome_end = str(packet.get("after_setup_outcome_window_end", ""))

    errors: list[str] = []
    if setup_time and outcome_start and outcome_start <= setup_time:
        errors.append("after_setup_outcome_window_start must be after setup_time_candidate_row_timestamp")
    if outcome_start and outcome_end and outcome_end <= outcome_start:
        errors.append("after_setup_outcome_window_end must be after after_setup_outcome_window_start")
    return errors


def validate_replacement_source_row_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    """Validate one replacement source row packet.

    Returns an in-memory summary only. The validator does not write files,
    fetch data, call network services, or make trade decisions.
    """

    candidate_id = str(packet.get("candidate_id", ""))
    missing_fields = _missing_required_fields(packet)
    forbidden_paths = _walk_forbidden_keys(packet)
    invalid_ohlcv_fields = _invalid_ohlcv_fields(packet)
    timeline_errors = _timeline_errors(packet)

    rejected_reasons: list[str] = []
    expected = ALLOWED_CANDIDATES.get(candidate_id)
    symbol = packet.get("symbol")
    setup_type = packet.get("setup_type")

    if expected is None:
        rejected_reasons.append("unknown_candidate_id")
    else:
        expected_symbol, expected_setup_type = expected
        if symbol != expected_symbol:
            rejected_reasons.append("symbol_does_not_match_candidate_id")
        if setup_type != expected_setup_type:
            rejected_reasons.append("setup_type_does_not_match_candidate_id")

    if missing_fields:
        rejected_reasons.append("missing_required_fields")
    if forbidden_paths:
        rejected_reasons.append("forbidden_live_or_broker_fields")
    if invalid_ohlcv_fields:
        rejected_reasons.append("invalid_setup_time_ohlcv")
    if timeline_errors:
        rejected_reasons.append("after_setup_window_violates_no_hindsight_boundary")

    ready = not rejected_reasons

    decision = "ready_for_acceptance_review" if ready else "missing_evidence_inconclusive"

    return {
        "candidate_id": candidate_id or None,
        "symbol": symbol,
        "setup_type": setup_type,
        "ready_for_acceptance_review": ready,
        "decision": decision,
        "missing_fields": missing_fields,
        "forbidden_paths": forbidden_paths,
        "invalid_ohlcv_fields": invalid_ohlcv_fields,
        "timeline_errors": timeline_errors,
        "rejected_reasons": rejected_reasons,
        "watch_only": True,
        "no_trade_decision": True,
        "input_copy": deepcopy(dict(packet)),
    }


def validate_replacement_source_row_packet_batch(
    packets: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Validate a batch of replacement source row packets in memory."""

    results = [validate_replacement_source_row_packet(packet) for packet in packets]
    ready = [result for result in results if result["ready_for_acceptance_review"]]
    not_ready = [result for result in results if not result["ready_for_acceptance_review"]]

    covered_ids = {str(result.get("candidate_id")) for result in results if result.get("candidate_id")}
    missing_candidate_ids = sorted(set(ALLOWED_CANDIDATES) - covered_ids)

    return {
        "records_processed": len(results),
        "ready_for_acceptance_review": len(ready),
        "missing_evidence_or_rejected": len(not_ready),
        "missing_candidate_ids": missing_candidate_ids,
        "results": results,
        "watch_only": True,
        "no_trade_decision": True,
    }
