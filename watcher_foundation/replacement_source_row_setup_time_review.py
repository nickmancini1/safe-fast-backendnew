"""Local in-memory setup-time row review gate for replacement source rows.

No file reads, file writes, live data, network, subprocesses, broker/order/
account/options/P&L, alerts, or trade decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from .replacement_source_row_packet import ALLOWED_CANDIDATES


REPLACEMENT_SOURCE_ROW_SETUP_TIME_REVIEW_RESULT_FIELDS = (
    "candidate_id",
    "symbol",
    "setup_type",
    "old_source_window_id",
    "old_source_sample_id",
    "setup_time_review_status",
    "setup_time_source_row_number",
    "setup_time_timestamp",
    "evidence_used",
    "missing_evidence",
    "rejected_reasons",
    "diagnosis",
    "likely_cause_candidate",
    "next_fix_path",
    "regression_needed",
    "lower_tier_handoff_summary",
    "packet_population_seed",
    "watch_only",
    "no_trade_decision",
    "accepted_proof",
)

REQUIRED_SETUP_TIME_REVIEW_FIELDS = (
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

_OHLCV_FIELDS = ("open", "high", "low", "close", "volume")

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


def review_replacement_source_row_setup_time(
    extracted_source_window: Mapping[str, Any],
    setup_time_review: Mapping[str, Any],
) -> dict[str, Any]:
    """Review caller-provided extracted rows plus setup-time decisions."""

    if not isinstance(extracted_source_window, Mapping):
        raise TypeError("Extracted source-window input must be a mapping")
    if not isinstance(setup_time_review, Mapping):
        raise TypeError("Setup-time review input must be a mapping")

    extracted = deepcopy(dict(extracted_source_window))
    review = deepcopy(dict(setup_time_review))
    candidate_id = _text_or_none(review.get("candidate_id")) or _text_or_none(extracted.get("candidate_id"))
    expected = ALLOWED_CANDIDATES.get(candidate_id or "")
    symbol = _identity_value(review, extracted, "symbol", expected, 0)
    setup_type = _identity_value(review, extracted, "setup_type", expected, 1)
    old_source_window_id = _first_present(extracted, ("old_source_window_id", "source_window_id"))
    old_source_sample_id = _first_present(extracted, ("old_source_sample_id", "source_sample_id"))

    base_context = {
        "candidate_id": candidate_id,
        "symbol": symbol,
        "setup_type": setup_type,
        "old_source_window_id": old_source_window_id,
        "old_source_sample_id": old_source_sample_id,
        "setup_time_source_row_number": review.get("setup_time_source_row_number"),
        "setup_time_timestamp": review.get("setup_time_timestamp"),
    }

    if expected is None:
        return _result(
            **base_context,
            setup_time_review_status="rejected",
            evidence_used=[],
            missing_evidence=["known replacement candidate id"],
            rejected_reasons=["unknown_candidate_id"],
            diagnosis="unknown replacement setup-time review candidate id",
            likely_cause_candidate="candidate id is outside the replacement source row candidate set",
            next_fix_path="use one of the known local replacement source row candidate ids",
            regression_needed="preserve regression coverage for unknown setup-time review candidate rejection",
            lower_tier_handoff_summary="rejected before setup-time review because candidate id is unknown",
            packet_population_seed=None,
        )

    identity_rejections = _identity_rejections(review, extracted, expected)
    if identity_rejections:
        return _result(
            **base_context,
            setup_time_review_status="rejected",
            evidence_used=[],
            missing_evidence=["valid candidate/symbol/setup-type combination"],
            rejected_reasons=identity_rejections,
            diagnosis="replacement setup-time review failed candidate identity validation",
            likely_cause_candidate=", ".join(identity_rejections),
            next_fix_path="correct the candidate id, symbol, or setup type before setup-time row review",
            regression_needed="preserve regression coverage for invalid candidate identity combinations",
            lower_tier_handoff_summary="rejected setup-time review requires identity correction",
            packet_population_seed=None,
        )

    forbidden_paths = _walk_forbidden_keys({"extracted_source_window": extracted, "setup_time_review": review})
    if forbidden_paths:
        return _result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            setup_time_review_status="rejected",
            evidence_used=[],
            missing_evidence=[{"forbidden_paths": forbidden_paths}],
            rejected_reasons=["forbidden_live_or_broker_fields"],
            diagnosis="replacement setup-time review contains forbidden live, broker, account, options, or P&L fields",
            likely_cause_candidate=", ".join(forbidden_paths),
            next_fix_path="remove forbidden execution, broker, account, options, P&L, production, or secret fields",
            regression_needed="preserve regression coverage for forbidden setup-time review fields",
            lower_tier_handoff_summary="rejected setup-time review requires field cleanup",
            packet_population_seed=None,
        )

    rows = _source_rows(extracted)
    if not rows:
        return _result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            setup_time_review_status="rejected",
            evidence_used=[],
            missing_evidence=["extracted source rows"],
            rejected_reasons=["missing_extracted_rows"],
            diagnosis="setup-time row review requires caller-provided extracted source rows",
            likely_cause_candidate="source-window extraction output did not include rows",
            next_fix_path="supply extracted source-window rows in memory before setup-time review",
            regression_needed="preserve regression coverage for missing extracted rows",
            lower_tier_handoff_summary="rejected until lower-tier extracted rows are supplied",
            packet_population_seed=None,
        )

    missing_fields = _missing_required_fields(review)
    if missing_fields:
        return _result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            setup_time_review_status="blocked_missing_evidence",
            evidence_used=_evidence_used(extracted, review, rows),
            missing_evidence=missing_fields,
            rejected_reasons=["missing_required_setup_time_review_fields"],
            diagnosis="setup-time row review is missing required caller-provided evidence fields",
            likely_cause_candidate=", ".join(missing_fields),
            next_fix_path="provide the missing setup-time trigger, invalidation, freshness, blocker, and outcome fields",
            regression_needed="preserve regression coverage for missing setup-time review fields",
            lower_tier_handoff_summary="blocked until required setup-time review fields are supplied",
            packet_population_seed=None,
        )

    setup_row_number = review["setup_time_source_row_number"]
    if not _is_valid_row_number(setup_row_number):
        return _rejected_row_number(base_context, expected, "setup_time_source_row_number_invalid")

    setup_row = _row_for_source_number(rows, setup_row_number)
    if setup_row is None:
        return _rejected_row_number(base_context, expected, "setup_time_source_row_number_outside_extracted_rows")

    invalid_ohlcv = _invalid_ohlcv_fields(review["setup_time_row_ohlcv"])
    if invalid_ohlcv:
        return _result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            setup_time_review_status="rejected",
            evidence_used=_evidence_used(extracted, review, rows),
            missing_evidence=[{"invalid_setup_time_ohlcv": invalid_ohlcv}],
            rejected_reasons=["invalid_setup_time_ohlcv"],
            diagnosis="setup-time row OHLCV must contain numeric open, high, low, close, and volume fields",
            likely_cause_candidate=", ".join(invalid_ohlcv),
            next_fix_path="supply numeric setup-time OHLCV copied from the extracted source row",
            regression_needed="preserve regression coverage for invalid setup-time OHLCV",
            lower_tier_handoff_summary="rejected until setup-time OHLCV is corrected",
            packet_population_seed=None,
        )

    timeline_error = _timeline_error(review)
    if timeline_error:
        return _result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            setup_time_review_status="rejected",
            evidence_used=_evidence_used(extracted, review, rows),
            missing_evidence=[{"timeline_errors": [timeline_error]}],
            rejected_reasons=["after_setup_window_violates_no_hindsight_boundary"],
            diagnosis="after-setup outcome window must start after the setup-time row",
            likely_cause_candidate=timeline_error,
            next_fix_path="move the after-setup outcome window start after the setup-time row",
            regression_needed="preserve regression coverage for no-hindsight boundary violations",
            lower_tier_handoff_summary="rejected until after-setup window starts after setup-time evidence",
            packet_population_seed=None,
        )

    packet_population_seed = _packet_population_seed(extracted, review, rows, expected)
    return _result(
        **{
            **base_context,
            "symbol": expected[0],
            "setup_type": expected[1],
            "setup_time_source_row_number": setup_row_number,
            "setup_time_timestamp": review["setup_time_timestamp"],
        },
        setup_time_review_status="ready_for_packet_build_review",
        evidence_used=_evidence_used(extracted, review, rows),
        missing_evidence=[],
        rejected_reasons=[],
        diagnosis="setup-time row review fields are complete for packet-build review only",
        likely_cause_candidate="caller-provided setup-time identity, trigger, invalidation, freshness, blocker, and outcome fields are present",
        next_fix_path="send the packet population seed to packet-build review without accepting proof",
        regression_needed="preserve coverage that setup-time review readiness is not accepted proof",
        lower_tier_handoff_summary="ready for packet-build review only; accepted proof remains false",
        packet_population_seed=packet_population_seed,
    )


def review_replacement_source_row_setup_time_batch(
    review_requests: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Review a batch of caller-provided setup-time row review requests."""

    results = []
    for request in review_requests:
        extracted = request.get("extracted_source_window", request.get("extracted_rows_bundle", {}))
        review = request.get("setup_time_review", request.get("setup_time_review_fields", {}))
        results.append(review_replacement_source_row_setup_time(extracted, review))

    return {
        "total": len(results),
        "ready_for_packet_build_review": sum(
            1 for result in results if result["setup_time_review_status"] == "ready_for_packet_build_review"
        ),
        "blocked_missing_evidence": sum(
            1 for result in results if result["setup_time_review_status"] == "blocked_missing_evidence"
        ),
        "rejected": sum(1 for result in results if result["setup_time_review_status"] == "rejected"),
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
    setup_time_review_status: str,
    setup_time_source_row_number: Any,
    setup_time_timestamp: Any,
    evidence_used: Sequence[Any],
    missing_evidence: Sequence[Any],
    rejected_reasons: Sequence[Any],
    diagnosis: str,
    likely_cause_candidate: str,
    next_fix_path: str,
    regression_needed: str,
    lower_tier_handoff_summary: str,
    packet_population_seed: Mapping[str, Any] | None,
) -> dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "symbol": symbol,
        "setup_type": setup_type,
        "old_source_window_id": old_source_window_id,
        "old_source_sample_id": old_source_sample_id,
        "setup_time_review_status": setup_time_review_status,
        "setup_time_source_row_number": setup_time_source_row_number,
        "setup_time_timestamp": setup_time_timestamp,
        "evidence_used": deepcopy(list(evidence_used)),
        "missing_evidence": deepcopy(list(missing_evidence)),
        "rejected_reasons": deepcopy(list(rejected_reasons)),
        "diagnosis": diagnosis,
        "likely_cause_candidate": likely_cause_candidate,
        "next_fix_path": next_fix_path,
        "regression_needed": regression_needed,
        "lower_tier_handoff_summary": lower_tier_handoff_summary,
        "packet_population_seed": deepcopy(dict(packet_population_seed)) if packet_population_seed is not None else None,
        "watch_only": True,
        "no_trade_decision": True,
        "accepted_proof": False,
    }


def _packet_population_seed(
    extracted: Mapping[str, Any],
    review: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
    expected: tuple[str, str],
) -> dict[str, Any]:
    return {
        "candidate_id": review.get("candidate_id") or extracted.get("candidate_id"),
        "symbol": expected[0],
        "setup_type": expected[1],
        "source_rows": deepcopy(list(rows)),
        "setup_time_source_row_number": review["setup_time_source_row_number"],
        "setup_time_timestamp": review["setup_time_timestamp"],
        "setup_time_row_ohlcv": deepcopy(dict(review["setup_time_row_ohlcv"])),
        "source_file_reference": _first_present(extracted, ("source_file_reference", "source_file_label")),
        "source_row_reference": _first_present(extracted, ("source_row_reference",)),
        "old_source_window_id": _first_present(extracted, ("old_source_window_id", "source_window_id")),
        "old_source_sample_id": _first_present(extracted, ("old_source_sample_id", "source_sample_id")),
        "accepted_setup_identity": deepcopy(review["accepted_setup_identity"]),
        "accepted_final_verdict": deepcopy(review["accepted_final_verdict"]),
        "trigger_candidate": deepcopy(review["accepted_numeric_trigger"]),
        "trigger_basis": deepcopy(review["accepted_trigger_basis"]),
        "invalidation_candidate": deepcopy(review["accepted_numeric_invalidation"]),
        "invalidation_basis": deepcopy(review["accepted_invalidation_basis"]),
        "freshness_final_signal_candidate": deepcopy(review["accepted_freshness_final_signal_decision"]),
        "blocker_caution_status": deepcopy(review["accepted_blocker_caution_decision"]),
        "no_hindsight_boundary": deepcopy(review["no_hindsight_boundary_statement"]),
        "after_setup_outcome_window_start": deepcopy(review["after_setup_outcome_window_start"]),
        "after_setup_outcome_window_end": deepcopy(review["after_setup_outcome_window_end"]),
        "watch_only": True,
        "no_trade_decision": True,
        "accepted_proof": False,
    }


def _missing_required_fields(review: Mapping[str, Any]) -> list[str]:
    return [field for field in REQUIRED_SETUP_TIME_REVIEW_FIELDS if not _is_present(review.get(field))]


def _source_rows(extracted: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = extracted.get("source_rows", extracted.get("extracted_source_rows", []))
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes, bytearray)):
        return []
    return [deepcopy(dict(row)) for row in rows if isinstance(row, Mapping)]


def _row_for_source_number(rows: Sequence[Mapping[str, Any]], source_row_number: int) -> Mapping[str, Any] | None:
    for row in rows:
        if row.get("source_row_number") == source_row_number:
            return row
    return None


def _rejected_row_number(
    base_context: Mapping[str, Any],
    expected: tuple[str, str],
    reason: str,
) -> dict[str, Any]:
    return _result(
        **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
        setup_time_review_status="rejected",
        evidence_used=[],
        missing_evidence=["valid setup-time source row number inside extracted source rows"],
        rejected_reasons=[reason],
        diagnosis="setup-time source row number must be a 1-based row number inside the extracted source rows",
        likely_cause_candidate=reason,
        next_fix_path="choose a setup-time source row number from the extracted source rows",
        regression_needed="preserve regression coverage for setup-time row number bounds",
        lower_tier_handoff_summary="rejected until setup-time row number is inside extracted rows",
        packet_population_seed=None,
    )


def _timeline_error(review: Mapping[str, Any]) -> str | None:
    setup_row_number = review["setup_time_source_row_number"]
    outcome_start = review["after_setup_outcome_window_start"]
    outcome_end = review["after_setup_outcome_window_end"]
    outcome_start_number = _coerce_int(outcome_start)
    outcome_end_number = _coerce_int(outcome_end)
    if outcome_start_number is not None and outcome_start_number <= setup_row_number:
        return "after_setup_outcome_window_start must be greater than setup_time_source_row_number"
    if outcome_start_number is not None and outcome_end_number is not None and outcome_end_number <= outcome_start_number:
        return "after_setup_outcome_window_end must be greater than after_setup_outcome_window_start"

    setup_timestamp = str(review["setup_time_timestamp"])
    outcome_start_text = str(outcome_start)
    outcome_end_text = str(outcome_end)
    if outcome_start_number is None and outcome_start_text <= setup_timestamp:
        return "after_setup_outcome_window_start must be after setup_time_timestamp"
    if outcome_start_number is None and outcome_end_number is None and outcome_end_text <= outcome_start_text:
        return "after_setup_outcome_window_end must be after after_setup_outcome_window_start"
    return None


def _invalid_ohlcv_fields(value: Any) -> list[str]:
    if not isinstance(value, Mapping):
        return list(_OHLCV_FIELDS)
    invalid = []
    for field_name in _OHLCV_FIELDS:
        field_value = value.get(field_name)
        if not isinstance(field_value, (int, float)) or isinstance(field_value, bool):
            invalid.append(field_name)
    return invalid


def _evidence_used(
    extracted: Mapping[str, Any],
    review: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
) -> list[Any]:
    evidence = []
    for field_name in (
        "source_window_id",
        "old_source_window_id",
        "source_sample_id",
        "old_source_sample_id",
        "source_file_label",
        "source_file_reference",
    ):
        value = extracted.get(field_name)
        if _is_present(value):
            evidence.append({field_name: deepcopy(value)})
    evidence.append({"extracted_source_rows": len(rows)})
    for field_name in REQUIRED_SETUP_TIME_REVIEW_FIELDS:
        value = review.get(field_name)
        if _is_present(value):
            evidence.append({field_name: deepcopy(value)})
    return evidence


def _identity_value(
    review: Mapping[str, Any],
    extracted: Mapping[str, Any],
    field_name: str,
    expected: tuple[str, str] | None,
    expected_index: int,
) -> Any:
    if field_name in review:
        return deepcopy(review[field_name])
    if field_name in extracted:
        return deepcopy(extracted[field_name])
    if expected is not None:
        return expected[expected_index]
    return None


def _identity_rejections(
    review: Mapping[str, Any],
    extracted: Mapping[str, Any],
    expected: tuple[str, str],
) -> list[str]:
    rejected = []
    symbol = review.get("symbol", extracted.get("symbol"))
    setup_type = review.get("setup_type", extracted.get("setup_type"))
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


def _first_present(mapping: Mapping[str, Any], keys: Sequence[str]) -> Any:
    for key in keys:
        if key in mapping and _is_present(mapping[key]):
            return deepcopy(mapping[key])
    return None


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


def _is_valid_row_number(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 1


def _coerce_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.isdigit():
            return int(stripped)
    return None


def _text_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
