"""Local in-memory source-window extraction for replacement source rows.

No file reads, file writes, live data, network, subprocesses, broker/order/
account/options/P&L, alerts, or trade decisions.
"""

from __future__ import annotations

import csv
from copy import deepcopy
from io import StringIO
from typing import Any, Mapping, Sequence

from .replacement_source_row_csv_intake import intake_replacement_source_row_csv_text
from .replacement_source_row_packet import ALLOWED_CANDIDATES


REPLACEMENT_SOURCE_ROW_WINDOW_EXTRACTOR_RESULT_FIELDS = (
    "candidate_id",
    "symbol",
    "setup_type",
    "source_window_id",
    "source_sample_id",
    "source_file_label",
    "row_start",
    "row_end",
    "rows_extracted",
    "source_rows",
    "csv_text_for_extracted_rows",
    "population_request_seed",
    "evidence_used",
    "missing_evidence",
    "rejected_reasons",
    "diagnosis",
    "next_fix_path",
    "watch_only",
    "no_trade_decision",
    "accepted_proof",
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


def extract_replacement_source_row_window(
    *,
    candidate_id: str,
    csv_text: str,
    row_start: int | None,
    row_end: int | None,
    symbol: str | None = None,
    setup_type: str | None = None,
    source_window_id: str | None = None,
    source_sample_id: str | None = None,
    source_file_label: str | None = None,
    source_metadata: Mapping[str, Any] | None = None,
    unavailable_fields: Sequence[str] | None = None,
    setup_time_source_row_number: int | None = None,
    **metadata: Any,
) -> dict[str, Any]:
    """Extract a 1-based inclusive source row window from caller CSV text."""

    metadata_copy = _combine_metadata(source_metadata, metadata)
    expected = ALLOWED_CANDIDATES.get(str(candidate_id))
    result_symbol = symbol if symbol is not None else expected[0] if expected else None
    result_setup_type = setup_type if setup_type is not None else expected[1] if expected else None
    base_context = {
        "candidate_id": candidate_id,
        "symbol": result_symbol,
        "setup_type": result_setup_type,
        "source_window_id": source_window_id or metadata_copy.get("source_window_id"),
        "source_sample_id": source_sample_id or metadata_copy.get("source_sample_id"),
        "source_file_label": source_file_label or metadata_copy.get("source_file_label"),
        "row_start": row_start,
        "row_end": row_end,
    }

    if expected is None:
        return _base_result(
            **base_context,
            source_rows=[],
            csv_text_for_extracted_rows="",
            population_request_seed=None,
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
            **{**base_context, "symbol": result_symbol, "setup_type": result_setup_type},
            source_rows=[],
            csv_text_for_extracted_rows="",
            population_request_seed=None,
            evidence_used=[],
            missing_evidence=["valid candidate/symbol/setup-type combination"],
            rejected_reasons=identity_rejections,
            diagnosis="replacement source row window extraction failed candidate identity validation",
            next_fix_path="correct the candidate id, symbol, or setup type before extraction",
        )

    parsed = _parse_csv_text(csv_text)
    if parsed["rejected_reasons"]:
        return _base_result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            source_rows=[],
            csv_text_for_extracted_rows="",
            population_request_seed=None,
            evidence_used=[],
            missing_evidence=parsed["missing_evidence"],
            rejected_reasons=parsed["rejected_reasons"],
            diagnosis=parsed["diagnosis"],
            next_fix_path=parsed["next_fix_path"],
        )

    range_rejection = _validate_row_range(row_start, row_end, len(parsed["rows"]))
    if range_rejection:
        return _base_result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            source_rows=[],
            csv_text_for_extracted_rows="",
            population_request_seed=None,
            evidence_used=[],
            missing_evidence=range_rejection["missing_evidence"],
            rejected_reasons=range_rejection["rejected_reasons"],
            diagnosis=range_rejection["diagnosis"],
            next_fix_path=range_rejection["next_fix_path"],
        )

    assert row_start is not None
    assert row_end is not None
    extracted_rows = [
        {
            **deepcopy(row),
            "source_row_number": source_row_number,
        }
        for source_row_number, row in enumerate(
            parsed["rows"][row_start - 1 : row_end],
            start=row_start,
        )
    ]
    extraction_metadata = _extraction_metadata(
        metadata_copy=metadata_copy,
        candidate_id=candidate_id,
        source_window_id=base_context["source_window_id"],
        source_sample_id=base_context["source_sample_id"],
        source_file_label=base_context["source_file_label"],
        row_start=row_start,
        row_end=row_end,
    )
    forbidden_paths = _walk_forbidden_keys(
        {
            "rows": extracted_rows,
            "metadata": extraction_metadata,
        }
    )
    if forbidden_paths:
        return _base_result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            source_rows=extracted_rows,
            csv_text_for_extracted_rows="",
            population_request_seed=None,
            evidence_used=[],
            missing_evidence=[{"forbidden_paths": forbidden_paths}],
            rejected_reasons=["forbidden_live_or_broker_fields"],
            diagnosis="replacement source row window contains forbidden live, broker, account, options, or P&L fields",
            next_fix_path="remove forbidden execution, broker, account, options, P&L, production, or secret fields",
        )

    extracted_csv_text = _csv_text_from_rows(parsed["fieldnames"], extracted_rows)
    setup_time_index = _setup_time_index(
        row_start=row_start,
        row_end=row_end,
        rows_extracted=len(extracted_rows),
        setup_time_source_row_number=setup_time_source_row_number
        or metadata_copy.pop("setup_time_source_row_number", None)
        or metadata_copy.pop("setup_time_row_number", None),
    )
    if isinstance(setup_time_index, dict):
        return _base_result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            source_rows=extracted_rows,
            csv_text_for_extracted_rows=extracted_csv_text,
            population_request_seed=None,
            evidence_used=[],
            missing_evidence=setup_time_index["missing_evidence"],
            rejected_reasons=setup_time_index["rejected_reasons"],
            diagnosis=setup_time_index["diagnosis"],
            next_fix_path=setup_time_index["next_fix_path"],
        )

    intake = intake_replacement_source_row_csv_text(
        candidate_id=candidate_id,
        csv_text=extracted_csv_text,
        symbol=expected[0],
        setup_type=expected[1],
        setup_time_row_index=setup_time_index,
        unavailable_fields=unavailable_fields,
        source_metadata=extraction_metadata,
    )
    return _base_result(
        **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
        source_rows=_coerce_source_row_numbers(intake["normalized_rows"]),
        csv_text_for_extracted_rows=extracted_csv_text,
        population_request_seed=intake["population_request"],
        evidence_used=intake["evidence_used"],
        missing_evidence=intake["missing_evidence"],
        rejected_reasons=intake["rejected_reasons"],
        diagnosis=intake["diagnosis"],
        next_fix_path=intake["next_fix_path"],
        extra={
            "population_status": intake.get("population_status"),
            "readiness_status": intake.get("readiness_status"),
            "packet_built": intake.get("packet_built"),
        },
    )


def _parse_csv_text(csv_text: str) -> dict[str, Any]:
    if not isinstance(csv_text, str) or not csv_text.strip():
        return {
            "rows": [],
            "fieldnames": [],
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
            "fieldnames": [],
            "missing_evidence": ["well-formed CSV text"],
            "rejected_reasons": ["malformed_csv_text"],
            "diagnosis": "replacement source row CSV text is malformed",
            "next_fix_path": "supply well-formed in-memory CSV text with a header row",
        }

    if not rows:
        return {
            "rows": [],
            "fieldnames": reader.fieldnames,
            "missing_evidence": ["CSV data rows"],
            "rejected_reasons": ["empty_csv_text"],
            "diagnosis": "replacement source row CSV text has no data rows",
            "next_fix_path": "supply local exported 1H RTH CSV rows in memory",
        }

    if any(None in row for row in rows):
        return {
            "rows": [],
            "fieldnames": [],
            "missing_evidence": ["well-formed CSV text"],
            "rejected_reasons": ["malformed_csv_text"],
            "diagnosis": "replacement source row CSV text has rows that do not match the header",
            "next_fix_path": "supply well-formed in-memory CSV text with consistent columns",
        }

    return {
        "rows": rows,
        "fieldnames": list(reader.fieldnames),
        "missing_evidence": [],
        "rejected_reasons": [],
        "diagnosis": "",
        "next_fix_path": "",
    }


def _validate_row_range(row_start: int | None, row_end: int | None, row_count: int) -> dict[str, Any] | None:
    if row_start is None or row_end is None:
        return {
            "missing_evidence": ["row range"],
            "rejected_reasons": ["missing_row_range"],
            "diagnosis": "replacement source row window extraction requires 1-based row_start and row_end",
            "next_fix_path": "supply a bounded 1-based inclusive source row range",
        }
    if (
        isinstance(row_start, bool)
        or isinstance(row_end, bool)
        or not isinstance(row_start, int)
        or not isinstance(row_end, int)
        or row_start < 1
        or row_end < row_start
        or row_end > row_count
    ):
        return {
            "missing_evidence": ["valid in-range 1-based row range"],
            "rejected_reasons": ["row_range_out_of_range"],
            "diagnosis": "replacement source row window range is outside the supplied CSV rows",
            "next_fix_path": "supply row_start and row_end within the caller-provided CSV data rows",
        }
    return None


def _setup_time_index(
    *,
    row_start: int,
    row_end: int,
    rows_extracted: int,
    setup_time_source_row_number: Any,
) -> int | dict[str, Any]:
    if setup_time_source_row_number is None:
        return rows_extracted - 1
    if (
        isinstance(setup_time_source_row_number, bool)
        or not isinstance(setup_time_source_row_number, int)
        or setup_time_source_row_number < row_start
        or setup_time_source_row_number > row_end
    ):
        return {
            "missing_evidence": ["valid setup-time source row number"],
            "rejected_reasons": ["setup_time_row_number_out_of_range"],
            "diagnosis": "setup-time source row number must fall within the extracted row window",
            "next_fix_path": "supply a 1-based setup-time source row number inside row_start and row_end",
        }
    return setup_time_source_row_number - row_start


def _extraction_metadata(
    *,
    metadata_copy: Mapping[str, Any],
    candidate_id: str,
    source_window_id: Any,
    source_sample_id: Any,
    source_file_label: Any,
    row_start: int,
    row_end: int,
) -> dict[str, Any]:
    result = deepcopy(dict(metadata_copy))
    result["candidate_id"] = candidate_id
    result["source_window_id"] = source_window_id
    result["source_sample_id"] = source_sample_id
    result["source_file_label"] = source_file_label
    result.setdefault("source_file_reference", source_file_label)
    result.setdefault("source_row_reference", f"rows {row_start}-{row_end}")
    result.setdefault("source_window_start", result.get("source_window_start"))
    result.setdefault("source_window_end", result.get("source_window_end"))
    return result


def _combine_metadata(
    source_metadata: Mapping[str, Any] | None,
    metadata: Mapping[str, Any],
) -> dict[str, Any]:
    combined = deepcopy(dict(source_metadata or {}))
    for key, value in metadata.items():
        combined[key] = deepcopy(value)
    return combined


def _csv_text_from_rows(fieldnames: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> str:
    output = StringIO()
    fields = list(fieldnames)
    if "source_row_number" not in fields:
        fields.append("source_row_number")
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow(deepcopy(dict(row)))
    return output.getvalue().rstrip("\n")


def _coerce_source_row_numbers(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    coerced = [deepcopy(dict(row)) for row in rows]
    for row in coerced:
        value = row.get("source_row_number")
        if isinstance(value, str) and value.strip().isdigit():
            row["source_row_number"] = int(value.strip())
    return coerced


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
    source_window_id: Any,
    source_sample_id: Any,
    source_file_label: Any,
    row_start: Any,
    row_end: Any,
    source_rows: Sequence[Mapping[str, Any]],
    csv_text_for_extracted_rows: str,
    population_request_seed: Mapping[str, Any] | None,
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
        "source_window_id": source_window_id,
        "source_sample_id": source_sample_id,
        "source_file_label": source_file_label,
        "row_start": row_start,
        "row_end": row_end,
        "rows_extracted": len(source_rows),
        "source_rows": deepcopy(list(source_rows)),
        "csv_text_for_extracted_rows": csv_text_for_extracted_rows,
        "population_request_seed": deepcopy(dict(population_request_seed))
        if population_request_seed is not None
        else None,
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
