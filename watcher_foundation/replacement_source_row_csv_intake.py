"""Local in-memory CSV intake for replacement source row packet requests.

No file reads, file writes, live data, network, subprocesses, broker/order/
account/options/P&L, alerts, or trade decisions.
"""

from __future__ import annotations

import csv
from copy import deepcopy
from io import StringIO
from typing import Any, Mapping, Sequence

from .replacement_source_row_packet import ALLOWED_CANDIDATES
from .replacement_source_row_packet_population import (
    populate_replacement_source_row_packet_request,
)


REPLACEMENT_SOURCE_ROW_CSV_INTAKE_RESULT_FIELDS = (
    "candidate_id",
    "symbol",
    "setup_type",
    "source_rows_supplied",
    "parsed_rows",
    "normalized_rows",
    "population_request",
    "evidence_used",
    "missing_evidence",
    "rejected_reasons",
    "diagnosis",
    "next_fix_path",
    "watch_only",
    "no_trade_decision",
    "accepted_proof",
)

_TIMESTAMP_ALIASES = (
    "timestamp",
    "time",
    "datetime",
    "date_time",
    "Date Time",
    "candle_time",
    "source_timestamp",
)

_OHLCV_ALIASES: dict[str, tuple[str, ...]] = {
    "open": ("open", "Open", "o", "O"),
    "high": ("high", "High", "h", "H"),
    "low": ("low", "Low", "l", "L"),
    "close": ("close", "Close", "c", "C", "last", "Last"),
    "volume": ("volume", "Volume", "vol", "Vol", "v", "V"),
}

_REQUEST_ALIASES: dict[str, tuple[str, ...]] = {
    "trigger_candidate": ("trigger_candidate", "trigger", "trigger_level"),
    "trigger_basis": ("trigger_basis", "trigger_reason"),
    "invalidation_candidate": ("invalidation_candidate", "invalidation", "invalidation_level"),
    "invalidation_basis": ("invalidation_basis", "invalidation_reason"),
    "freshness_final_signal_candidate": (
        "freshness_final_signal_candidate",
        "freshness",
        "final_signal",
        "freshness_status",
    ),
    "blocker_caution_status": (
        "blocker_caution_status",
        "blocker_status",
        "caution_status",
    ),
}

_METADATA_FIELDS = (
    "source_file_reference",
    "source_row_reference",
    "source_window_start",
    "source_window_end",
    "after_setup_outcome_window_start",
    "after_setup_outcome_window_end",
    "no_hindsight_boundary",
)

_FORBIDDEN_KEY_PARTS = (
    "broker",
    "order",
    "account",
    "option",
    "options",
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


def intake_replacement_source_row_csv_text(
    *,
    candidate_id: str,
    csv_text: str,
    symbol: str | None = None,
    setup_type: str | None = None,
    setup_time_row_index: int | None = None,
    unavailable_fields: Sequence[str] | None = None,
    source_metadata: Mapping[str, Any] | None = None,
    **metadata: Any,
) -> dict[str, Any]:
    """Parse caller-provided CSV text into a replacement packet population request."""

    parsed = _parse_csv_text(csv_text)
    if parsed["rejected_reasons"]:
        return _base_result(
            candidate_id=candidate_id,
            symbol=symbol,
            setup_type=setup_type,
            parsed_rows=[],
            normalized_rows=[],
            population_request=None,
            evidence_used=[],
            missing_evidence=parsed["missing_evidence"],
            rejected_reasons=parsed["rejected_reasons"],
            diagnosis=parsed["diagnosis"],
            next_fix_path=parsed["next_fix_path"],
        )

    return intake_replacement_source_row_dicts(
        candidate_id=candidate_id,
        row_dicts=parsed["rows"],
        symbol=symbol,
        setup_type=setup_type,
        setup_time_row_index=setup_time_row_index,
        unavailable_fields=unavailable_fields,
        source_metadata=source_metadata,
        parsed_rows=parsed["rows"],
        **metadata,
    )


def intake_replacement_source_row_dicts(
    *,
    candidate_id: str,
    row_dicts: Sequence[Mapping[str, Any]],
    symbol: str | None = None,
    setup_type: str | None = None,
    setup_time_row_index: int | None = None,
    unavailable_fields: Sequence[str] | None = None,
    source_metadata: Mapping[str, Any] | None = None,
    parsed_rows: Sequence[Mapping[str, Any]] | None = None,
    **metadata: Any,
) -> dict[str, Any]:
    """Normalize caller-provided row dicts into a population request."""

    rows = [deepcopy(dict(row)) for row in row_dicts]
    parsed_copy = [deepcopy(dict(row)) for row in (parsed_rows if parsed_rows is not None else rows)]
    expected = ALLOWED_CANDIDATES.get(str(candidate_id))
    result_symbol = symbol if symbol is not None else expected[0] if expected else None
    result_setup_type = setup_type if setup_type is not None else expected[1] if expected else None

    if expected is None:
        return _base_result(
            candidate_id=candidate_id,
            symbol=result_symbol,
            setup_type=result_setup_type,
            parsed_rows=parsed_copy,
            normalized_rows=[],
            population_request=None,
            evidence_used=[],
            missing_evidence=["known replacement candidate id"],
            rejected_reasons=["unknown_candidate_id"],
            diagnosis="unknown replacement source row candidate id",
            next_fix_path="use one of the known local replacement source row candidate ids",
        )

    identity_rejections = []
    if symbol is not None and symbol != expected[0]:
        identity_rejections.append("symbol_does_not_match_candidate_id")
    if setup_type is not None and setup_type != expected[1]:
        identity_rejections.append("setup_type_does_not_match_candidate_id")
    if identity_rejections:
        return _base_result(
            candidate_id=candidate_id,
            symbol=result_symbol,
            setup_type=result_setup_type,
            parsed_rows=parsed_copy,
            normalized_rows=[],
            population_request=None,
            evidence_used=[],
            missing_evidence=["valid candidate/symbol/setup-type combination"],
            rejected_reasons=identity_rejections,
            diagnosis="replacement source row CSV intake failed candidate identity validation",
            next_fix_path="correct the candidate id, symbol, or setup type before packet population",
        )

    if not rows:
        return _base_result(
            candidate_id=candidate_id,
            symbol=expected[0],
            setup_type=expected[1],
            parsed_rows=parsed_copy,
            normalized_rows=[],
            population_request=None,
            evidence_used=[],
            missing_evidence=["source rows"],
            rejected_reasons=["empty_source_rows"],
            diagnosis="replacement source row CSV intake requires at least one source row",
            next_fix_path="supply local exported 1H RTH rows in memory",
        )

    normalized_rows = [_normalize_row(row) for row in rows]
    setup_index = setup_time_row_index if setup_time_row_index is not None else len(normalized_rows) - 1
    request_metadata = _combine_metadata(source_metadata, metadata)
    unavailable = list(deepcopy(unavailable_fields or request_metadata.pop("unavailable_fields", [])))

    population_request = {
        "candidate_id": candidate_id,
        "symbol": expected[0],
        "setup_type": expected[1],
        "source_rows": deepcopy(normalized_rows),
        "setup_time_row_index": setup_index,
        "source_file_reference": _metadata_value(request_metadata, "source_file_reference"),
        "source_row_reference": _metadata_value(request_metadata, "source_row_reference"),
        "source_window_start": _metadata_value(request_metadata, "source_window_start"),
        "source_window_end": _metadata_value(request_metadata, "source_window_end"),
        "trigger_candidate": _candidate_value(normalized_rows, request_metadata, "trigger_candidate"),
        "trigger_basis": _candidate_value(normalized_rows, request_metadata, "trigger_basis"),
        "invalidation_candidate": _candidate_value(normalized_rows, request_metadata, "invalidation_candidate"),
        "invalidation_basis": _candidate_value(normalized_rows, request_metadata, "invalidation_basis"),
        "freshness_final_signal_candidate": _candidate_value(
            normalized_rows,
            request_metadata,
            "freshness_final_signal_candidate",
        ),
        "blocker_caution_status": _candidate_value(normalized_rows, request_metadata, "blocker_caution_status"),
        "unavailable_fields": unavailable,
        "after_setup_outcome_window_start": _metadata_value(
            request_metadata,
            "after_setup_outcome_window_start",
        ),
        "after_setup_outcome_window_end": _metadata_value(
            request_metadata,
            "after_setup_outcome_window_end",
        ),
        "no_hindsight_boundary": request_metadata.get(
            "no_hindsight_boundary",
            "setup-time row selected before terminal outcome review",
        ),
    }

    for key, value in request_metadata.items():
        if key not in population_request:
            population_request[key] = deepcopy(value)

    forbidden_paths = _walk_forbidden_keys(
        {
            "rows": normalized_rows,
            "metadata": request_metadata,
        }
    )
    if forbidden_paths:
        population_request["forbidden_paths_surfaced"] = forbidden_paths

    population = populate_replacement_source_row_packet_request(population_request)
    return _base_result(
        candidate_id=population["candidate_id"],
        symbol=population["symbol"],
        setup_type=population["setup_type"],
        parsed_rows=parsed_copy,
        normalized_rows=normalized_rows,
        population_request=population_request,
        evidence_used=population["evidence_used"],
        missing_evidence=population["missing_evidence"],
        rejected_reasons=population["rejected_reasons"],
        diagnosis=population["diagnosis"],
        next_fix_path=population["next_fix_path"],
        extra={
            "population_status": population["population_status"],
            "readiness_status": population["readiness_status"],
            "packet_built": population["packet_built"],
        },
    )


def _parse_csv_text(csv_text: str) -> dict[str, Any]:
    if not isinstance(csv_text, str) or not csv_text.strip():
        return {
            "rows": [],
            "missing_evidence": ["csv text"],
            "rejected_reasons": ["empty_csv_text"],
            "diagnosis": "replacement source row CSV text is empty",
            "next_fix_path": "supply caller-provided in-memory CSV text",
        }

    try:
        reader = csv.DictReader(StringIO(csv_text), strict=True)
        if not reader.fieldnames or any(field is None or not field.strip() for field in reader.fieldnames):
            raise csv.Error("missing or blank CSV header")
        rows = [dict(row) for row in reader]
    except csv.Error:
        return {
            "rows": [],
            "missing_evidence": ["well-formed CSV text"],
            "rejected_reasons": ["malformed_csv_text"],
            "diagnosis": "replacement source row CSV text is malformed",
            "next_fix_path": "supply well-formed in-memory CSV text with a header row",
        }

    if not rows:
        return {
            "rows": [],
            "missing_evidence": ["CSV data rows"],
            "rejected_reasons": ["empty_csv_text"],
            "diagnosis": "replacement source row CSV text has no data rows",
            "next_fix_path": "supply local exported 1H RTH CSV rows in memory",
        }

    if any(None in row for row in rows):
        return {
            "rows": [],
            "missing_evidence": ["well-formed CSV text"],
            "rejected_reasons": ["malformed_csv_text"],
            "diagnosis": "replacement source row CSV text has rows that do not match the header",
            "next_fix_path": "supply well-formed in-memory CSV text with consistent columns",
        }

    return {
        "rows": rows,
        "missing_evidence": [],
        "rejected_reasons": [],
        "diagnosis": "",
        "next_fix_path": "",
    }


def _normalize_row(row: Mapping[str, Any]) -> dict[str, Any]:
    normalized = deepcopy(dict(row))
    timestamp = _first_present(row, _TIMESTAMP_ALIASES)
    if timestamp is not None:
        normalized["timestamp"] = _text_or_none(timestamp)
    for field_name, aliases in _OHLCV_ALIASES.items():
        normalized[field_name] = _number_or_none(_first_present(row, aliases))
    return normalized


def _combine_metadata(
    source_metadata: Mapping[str, Any] | None,
    metadata: Mapping[str, Any],
) -> dict[str, Any]:
    combined = deepcopy(dict(source_metadata or {}))
    for key, value in metadata.items():
        combined[key] = deepcopy(value)
    return combined


def _metadata_value(metadata: Mapping[str, Any], field_name: str) -> Any:
    if field_name in metadata:
        return deepcopy(metadata[field_name])
    return None


def _candidate_value(
    normalized_rows: Sequence[Mapping[str, Any]],
    metadata: Mapping[str, Any],
    field_name: str,
) -> Any:
    if field_name in metadata:
        return deepcopy(metadata[field_name])
    aliases = _REQUEST_ALIASES[field_name]
    for row in reversed(normalized_rows):
        value = _first_present(row, aliases)
        if value not in (None, ""):
            return _number_or_text(value)
    return None


def _first_present(row: Mapping[str, Any], keys: Sequence[str]) -> Any:
    for key in keys:
        if key in row and row[key] is not None:
            return row[key]
    return None


def _text_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _number_or_none(value: Any) -> float | int | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return None
        try:
            parsed = float(stripped)
        except ValueError:
            return None
        if parsed.is_integer():
            return int(parsed)
        return parsed
    return None


def _number_or_text(value: Any) -> Any:
    parsed = _number_or_none(value)
    if parsed is not None:
        return parsed
    return _text_or_none(value)


def _walk_forbidden_keys(value: Any, path: str = "") -> list[str]:
    hits: list[str] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            key_text = str(key).lower()
            child_path = f"{path}.{key}" if path else str(key)
            if any(part in key_text for part in _FORBIDDEN_KEY_PARTS):
                hits.append(child_path)
            hits.extend(_walk_forbidden_keys(child, child_path))
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, child in enumerate(value):
            hits.extend(_walk_forbidden_keys(child, f"{path}[{index}]"))
    return hits


def _base_result(
    *,
    candidate_id: Any,
    symbol: Any,
    setup_type: Any,
    parsed_rows: Sequence[Mapping[str, Any]],
    normalized_rows: Sequence[Mapping[str, Any]],
    population_request: Mapping[str, Any] | None,
    evidence_used: Sequence[Any],
    missing_evidence: Sequence[Any],
    rejected_reasons: Sequence[Any],
    diagnosis: str,
    next_fix_path: str,
    extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    result = {
        "candidate_id": candidate_id,
        "symbol": symbol,
        "setup_type": setup_type,
        "source_rows_supplied": len(parsed_rows),
        "parsed_rows": deepcopy(list(parsed_rows)),
        "normalized_rows": deepcopy(list(normalized_rows)),
        "population_request": deepcopy(dict(population_request)) if population_request is not None else None,
        "evidence_used": deepcopy(list(evidence_used)),
        "missing_evidence": deepcopy(list(missing_evidence)),
        "rejected_reasons": deepcopy(list(rejected_reasons)),
        "diagnosis": diagnosis,
        "next_fix_path": next_fix_path,
        "watch_only": True,
        "no_trade_decision": True,
        "accepted_proof": False,
    }
    if extra:
        result.update(deepcopy(dict(extra)))
    return result
