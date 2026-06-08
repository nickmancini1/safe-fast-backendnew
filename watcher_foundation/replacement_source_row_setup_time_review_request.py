"""Local in-memory setup-time review request packets for source rows.

No file reads, file writes, live data, network, subprocesses, broker/order/
account/options/P&L, alerts, or trade decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from .replacement_source_row_packet import ALLOWED_CANDIDATES


REPLACEMENT_SOURCE_ROW_SETUP_TIME_REVIEW_REQUEST_FIELDS = (
    "candidate_id",
    "symbol",
    "setup_type",
    "old_source_window_id",
    "old_source_sample_id",
    "source_file_label",
    "row_start",
    "row_end",
    "candidate_review_rows",
    "setup_time_review_request_status",
    "required_fields_to_complete",
    "setup_time_source_row_number",
    "setup_time_timestamp",
    "setup_time_row_ohlcv",
    "accepted_setup_identity",
    "accepted_final_verdict",
    "accepted_trigger_state",
    "accepted_numeric_trigger",
    "accepted_trigger_basis",
    "accepted_numeric_invalidation",
    "accepted_invalidation_basis",
    "accepted_freshness_final_signal_decision",
    "accepted_blocker_caution_decision",
    "no_hindsight_boundary_statement",
    "after_setup_outcome_window_start",
    "after_setup_outcome_window_end",
    "evidence_used",
    "missing_evidence",
    "rejected_reasons",
    "diagnosis",
    "likely_cause_candidate",
    "next_fix_path",
    "regression_needed",
    "lower_tier_handoff_summary",
    "watch_only",
    "no_trade_decision",
    "accepted_proof",
)

REQUIRED_FIELDS_TO_COMPLETE = (
    "setup_time_source_row_number",
    "setup_time_timestamp",
    "setup_time_row_ohlcv",
    "accepted_setup_identity",
    "accepted_final_verdict",
    "accepted_trigger_state",
    "accepted_numeric_trigger",
    "accepted_trigger_basis",
    "accepted_numeric_invalidation",
    "accepted_invalidation_basis",
    "accepted_freshness_final_signal_decision",
    "accepted_blocker_caution_decision",
    "no_hindsight_boundary_statement",
    "after_setup_outcome_window_start",
    "after_setup_outcome_window_end",
)

_ROW_PRESERVE_FIELDS = ("timestamp", "open", "high", "low", "close", "volume")

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


def build_replacement_source_row_setup_time_review_request(
    extracted_source_window: Mapping[str, Any],
    candidate_metadata: Mapping[str, Any] | None = None,
    *,
    candidate_row_numbers: Sequence[int] | None = None,
    candidate_row_start: int | None = None,
    candidate_row_end: int | None = None,
) -> dict[str, Any]:
    """Build one watch-only setup-time review request from extracted rows."""

    if not isinstance(extracted_source_window, Mapping):
        raise TypeError("Extracted source-window input must be a mapping")
    if candidate_metadata is not None and not isinstance(candidate_metadata, Mapping):
        raise TypeError("Candidate metadata must be a mapping when provided")

    extracted = deepcopy(dict(extracted_source_window))
    metadata = deepcopy(dict(candidate_metadata or {}))
    candidate_id = _text_or_none(metadata.get("candidate_id")) or _text_or_none(extracted.get("candidate_id"))
    expected = ALLOWED_CANDIDATES.get(candidate_id or "")
    symbol = _identity_value(metadata, extracted, "symbol", expected, 0)
    setup_type = _identity_value(metadata, extracted, "setup_type", expected, 1)
    old_source_window_id = _first_present(extracted, metadata, ("old_source_window_id", "source_window_id"))
    old_source_sample_id = _first_present(extracted, metadata, ("old_source_sample_id", "source_sample_id"))
    source_file_label = _first_present(extracted, metadata, ("source_file_label", "source_file_reference"))

    base_context = {
        "candidate_id": candidate_id,
        "symbol": symbol,
        "setup_type": setup_type,
        "old_source_window_id": old_source_window_id,
        "old_source_sample_id": old_source_sample_id,
        "source_file_label": source_file_label,
        "row_start": _first_present(extracted, metadata, ("row_start",)),
        "row_end": _first_present(extracted, metadata, ("row_end",)),
        "candidate_review_rows": [],
    }

    if expected is None:
        return _result(
            **base_context,
            setup_time_review_request_status="rejected",
            required_fields_to_complete=[],
            evidence_used=[],
            missing_evidence=["known replacement candidate id"],
            rejected_reasons=["unknown_candidate_id"],
            diagnosis="unknown replacement setup-time review request candidate id",
            likely_cause_candidate="candidate id is outside the replacement source row candidate set",
            next_fix_path="use one of the known local replacement source row candidate ids",
            regression_needed="preserve regression coverage for unknown setup-time review request rejection",
            lower_tier_handoff_summary="rejected before setup-time review request because candidate id is unknown",
        )

    identity_rejections = _identity_rejections(metadata, extracted, expected)
    if identity_rejections:
        return _result(
            **base_context,
            setup_time_review_request_status="rejected",
            required_fields_to_complete=[],
            evidence_used=[],
            missing_evidence=["valid candidate/symbol/setup-type combination"],
            rejected_reasons=identity_rejections,
            diagnosis="replacement setup-time review request failed candidate identity validation",
            likely_cause_candidate=", ".join(identity_rejections),
            next_fix_path="correct the candidate id, symbol, or setup type before building a review request",
            regression_needed="preserve regression coverage for invalid candidate identity combinations",
            lower_tier_handoff_summary="rejected setup-time review request requires identity correction",
        )

    forbidden_paths = _walk_forbidden_keys({"extracted_source_window": extracted, "candidate_metadata": metadata})
    if forbidden_paths:
        return _result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            setup_time_review_request_status="rejected",
            required_fields_to_complete=[],
            evidence_used=[],
            missing_evidence=[{"forbidden_paths": forbidden_paths}],
            rejected_reasons=["forbidden_live_or_broker_fields"],
            diagnosis="setup-time review request contains forbidden live, broker, account, options, or P&L fields",
            likely_cause_candidate=", ".join(forbidden_paths),
            next_fix_path="remove forbidden execution, broker, account, options, P&L, production, or secret fields",
            regression_needed="preserve regression coverage for forbidden setup-time review request fields",
            lower_tier_handoff_summary="rejected setup-time review request requires field cleanup",
        )

    rows = _source_rows(extracted)
    if not rows:
        return _result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            setup_time_review_request_status="rejected",
            required_fields_to_complete=[],
            evidence_used=[],
            missing_evidence=["extracted source rows"],
            rejected_reasons=["missing_extracted_rows"],
            diagnosis="setup-time review request requires caller-provided extracted source rows",
            likely_cause_candidate="source-window extraction output did not include rows",
            next_fix_path="supply extracted source-window rows in memory before building the review request",
            regression_needed="preserve regression coverage for missing extracted rows",
            lower_tier_handoff_summary="rejected until lower-tier extracted rows are supplied",
        )

    row_numbers = _row_numbers(rows)
    explicit_review_numbers = _candidate_review_numbers(
        metadata=metadata,
        candidate_row_numbers=candidate_row_numbers,
        candidate_row_start=candidate_row_start,
        candidate_row_end=candidate_row_end,
    )
    candidate_numbers = explicit_review_numbers if explicit_review_numbers is not None else row_numbers
    invalid_candidate_rows = _invalid_candidate_rows(candidate_numbers, row_numbers)
    if invalid_candidate_rows:
        return _result(
            **{
                **base_context,
                "symbol": expected[0],
                "setup_type": expected[1],
                "row_start": _row_start(base_context["row_start"], row_numbers),
                "row_end": _row_end(base_context["row_end"], row_numbers),
            },
            setup_time_review_request_status="rejected",
            required_fields_to_complete=[],
            evidence_used=_evidence_used(extracted, metadata, len(rows)),
            missing_evidence=["candidate row numbers inside extracted source rows"],
            rejected_reasons=["candidate_row_outside_extracted_range"],
            diagnosis="candidate setup-time review rows must be 1-based row numbers inside extracted source rows",
            likely_cause_candidate=", ".join(str(row_number) for row_number in invalid_candidate_rows),
            next_fix_path="choose candidate review rows from the extracted source rows",
            regression_needed="preserve regression coverage for candidate row bounds",
            lower_tier_handoff_summary="rejected until candidate review rows are inside extracted source rows",
        )

    candidate_review_rows = [
        _review_row(row)
        for row in rows
        if row.get("source_row_number") in set(candidate_numbers)
    ]
    return _result(
        **{
            **base_context,
            "symbol": expected[0],
            "setup_type": expected[1],
            "row_start": _row_start(base_context["row_start"], row_numbers),
            "row_end": _row_end(base_context["row_end"], row_numbers),
            "candidate_review_rows": candidate_review_rows,
        },
        setup_time_review_request_status="ready_for_setup_time_review_request",
        required_fields_to_complete=list(REQUIRED_FIELDS_TO_COMPLETE),
        evidence_used=_evidence_used(extracted, metadata, len(rows)),
        missing_evidence=list(REQUIRED_FIELDS_TO_COMPLETE),
        rejected_reasons=[],
        diagnosis="extracted source rows are ready for caller setup-time review field completion only",
        likely_cause_candidate=(
            "review request contains source rows but no accepted trigger, invalidation, freshness, blocker, "
            "no-hindsight, or terminal outcome proof"
        ),
        next_fix_path="complete setup-time review fields from exact accepted evidence before calling the setup-time gate",
        regression_needed="preserve coverage that request packets are not accepted proof",
        lower_tier_handoff_summary="review request packet only; use candidate_review_rows as watch-only source material",
    )


def build_replacement_source_row_setup_time_review_request_batch(
    requests: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Build setup-time review request packets for caller-provided inputs."""

    results = []
    for request in requests:
        extracted = request.get("extracted_source_window", request.get("extracted_rows_bundle", {}))
        metadata = request.get("candidate_metadata", {})
        results.append(
            build_replacement_source_row_setup_time_review_request(
                extracted,
                metadata,
                candidate_row_numbers=request.get("candidate_row_numbers"),
                candidate_row_start=request.get("candidate_row_start"),
                candidate_row_end=request.get("candidate_row_end"),
            )
        )
    return {
        "total": len(results),
        "ready_for_setup_time_review_request": sum(
            1
            for result in results
            if result["setup_time_review_request_status"] == "ready_for_setup_time_review_request"
        ),
        "rejected": sum(1 for result in results if result["setup_time_review_request_status"] == "rejected"),
        "accepted_proof_count": 0,
        "results": {str(result["candidate_id"]): deepcopy(result) for result in results},
        "watch_only": True,
        "no_trade_decision": True,
    }


def _result(
    *,
    candidate_id: Any,
    symbol: Any,
    setup_type: Any,
    old_source_window_id: Any,
    old_source_sample_id: Any,
    source_file_label: Any,
    row_start: Any,
    row_end: Any,
    candidate_review_rows: Sequence[Mapping[str, Any]],
    setup_time_review_request_status: str,
    required_fields_to_complete: Sequence[Any],
    evidence_used: Sequence[Any],
    missing_evidence: Sequence[Any],
    rejected_reasons: Sequence[Any],
    diagnosis: str,
    likely_cause_candidate: str,
    next_fix_path: str,
    regression_needed: str,
    lower_tier_handoff_summary: str,
) -> dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "symbol": symbol,
        "setup_type": setup_type,
        "old_source_window_id": old_source_window_id,
        "old_source_sample_id": old_source_sample_id,
        "source_file_label": source_file_label,
        "row_start": row_start,
        "row_end": row_end,
        "candidate_review_rows": deepcopy(list(candidate_review_rows)),
        "setup_time_review_request_status": setup_time_review_request_status,
        "required_fields_to_complete": deepcopy(list(required_fields_to_complete)),
        "setup_time_source_row_number": None,
        "setup_time_timestamp": None,
        "setup_time_row_ohlcv": None,
        "accepted_setup_identity": None,
        "accepted_final_verdict": None,
        "accepted_trigger_state": None,
        "accepted_numeric_trigger": None,
        "accepted_trigger_basis": None,
        "accepted_numeric_invalidation": None,
        "accepted_invalidation_basis": None,
        "accepted_freshness_final_signal_decision": None,
        "accepted_blocker_caution_decision": None,
        "no_hindsight_boundary_statement": None,
        "after_setup_outcome_window_start": None,
        "after_setup_outcome_window_end": None,
        "evidence_used": deepcopy(list(evidence_used)),
        "missing_evidence": deepcopy(list(missing_evidence)),
        "rejected_reasons": deepcopy(list(rejected_reasons)),
        "diagnosis": diagnosis,
        "likely_cause_candidate": likely_cause_candidate,
        "next_fix_path": next_fix_path,
        "regression_needed": regression_needed,
        "lower_tier_handoff_summary": lower_tier_handoff_summary,
        "watch_only": True,
        "no_trade_decision": True,
        "accepted_proof": False,
    }


def _source_rows(extracted: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = extracted.get("source_rows", extracted.get("extracted_source_rows", []))
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes, bytearray)):
        return []
    normalized = []
    for row in rows:
        if not isinstance(row, Mapping):
            continue
        copied = deepcopy(dict(row))
        source_row_number = copied.get("source_row_number")
        if isinstance(source_row_number, str) and source_row_number.strip().isdigit():
            copied["source_row_number"] = int(source_row_number.strip())
        normalized.append(copied)
    return normalized


def _row_numbers(rows: Sequence[Mapping[str, Any]]) -> list[int]:
    return [
        row["source_row_number"]
        for row in rows
        if isinstance(row.get("source_row_number"), int)
        and not isinstance(row.get("source_row_number"), bool)
        and row.get("source_row_number") >= 1
    ]


def _candidate_review_numbers(
    *,
    metadata: Mapping[str, Any],
    candidate_row_numbers: Sequence[int] | None,
    candidate_row_start: int | None,
    candidate_row_end: int | None,
) -> list[int] | None:
    numbers = candidate_row_numbers if candidate_row_numbers is not None else metadata.get("candidate_row_numbers")
    if numbers is not None:
        if not isinstance(numbers, Sequence) or isinstance(numbers, (str, bytes, bytearray)):
            return [-1]
        return [number if isinstance(number, int) and not isinstance(number, bool) else -1 for number in numbers]

    start = candidate_row_start if candidate_row_start is not None else metadata.get("candidate_row_start")
    end = candidate_row_end if candidate_row_end is not None else metadata.get("candidate_row_end")
    if start is None and end is None:
        return None
    if (
        isinstance(start, bool)
        or isinstance(end, bool)
        or not isinstance(start, int)
        or not isinstance(end, int)
        or start < 1
        or end < start
    ):
        return [-1]
    return list(range(start, end + 1))


def _invalid_candidate_rows(candidate_numbers: Sequence[int], extracted_numbers: Sequence[int]) -> list[int]:
    extracted_set = set(extracted_numbers)
    return [
        number
        for number in candidate_numbers
        if not isinstance(number, int) or isinstance(number, bool) or number < 1 or number not in extracted_set
    ]


def _review_row(row: Mapping[str, Any]) -> dict[str, Any]:
    result = deepcopy(dict(row))
    unavailable_fields = list(result.get("unavailable_fields", []))
    for field_name in _ROW_PRESERVE_FIELDS:
        if field_name not in result or result[field_name] in (None, ""):
            result[field_name] = "unavailable"
            if field_name not in unavailable_fields:
                unavailable_fields.append(field_name)
    result["unavailable_fields"] = unavailable_fields
    return result


def _evidence_used(extracted: Mapping[str, Any], metadata: Mapping[str, Any], rows_supplied: int) -> list[Any]:
    evidence = []
    for field_name in (
        "source_window_id",
        "old_source_window_id",
        "source_sample_id",
        "old_source_sample_id",
        "source_file_label",
        "source_file_reference",
    ):
        value = _first_present(extracted, metadata, (field_name,))
        if _is_present(value):
            evidence.append({field_name: deepcopy(value)})
    evidence.append({"extracted_source_rows": rows_supplied})
    return evidence


def _identity_value(
    metadata: Mapping[str, Any],
    extracted: Mapping[str, Any],
    field_name: str,
    expected: tuple[str, str] | None,
    expected_index: int,
) -> Any:
    if field_name in metadata:
        return deepcopy(metadata[field_name])
    if field_name in extracted:
        return deepcopy(extracted[field_name])
    if expected is not None:
        return expected[expected_index]
    return None


def _identity_rejections(
    metadata: Mapping[str, Any],
    extracted: Mapping[str, Any],
    expected: tuple[str, str],
) -> list[str]:
    rejected = []
    symbol = metadata.get("symbol", extracted.get("symbol"))
    setup_type = metadata.get("setup_type", extracted.get("setup_type"))
    if symbol is not None and symbol != expected[0]:
        rejected.append("symbol_does_not_match_candidate_id")
    if setup_type is not None and setup_type != expected[1]:
        rejected.append("setup_type_does_not_match_candidate_id")
    return rejected


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


def _first_present(
    first: Mapping[str, Any],
    second: Mapping[str, Any],
    keys: Sequence[str],
) -> Any:
    for mapping in (first, second):
        for key in keys:
            if key in mapping and _is_present(mapping[key]):
                return deepcopy(mapping[key])
    return None


def _row_start(value: Any, row_numbers: Sequence[int]) -> Any:
    return value if _is_present(value) else min(row_numbers)


def _row_end(value: Any, row_numbers: Sequence[int]) -> Any:
    return value if _is_present(value) else max(row_numbers)


def _is_present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, Mapping):
        return len(value) > 0
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return len(value) > 0
    return True


def _text_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
