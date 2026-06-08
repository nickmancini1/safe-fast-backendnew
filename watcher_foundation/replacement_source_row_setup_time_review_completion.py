"""Local in-memory intake for completed setup-time review request packets.

No file reads, file writes, live data, network, subprocesses, broker/order/
account/options/P&L, alerts, or trade decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from .replacement_source_row_packet import ALLOWED_CANDIDATES
from .replacement_source_row_setup_time_review import (
    REQUIRED_SETUP_TIME_REVIEW_FIELDS,
    review_replacement_source_row_setup_time,
)


REPLACEMENT_SOURCE_ROW_SETUP_TIME_REVIEW_COMPLETION_RESULT_FIELDS = (
    "candidate_id",
    "symbol",
    "setup_type",
    "completion_status",
    "setup_time_review_status",
    "setup_time_source_row_number",
    "setup_time_timestamp",
    "completed_fields_used",
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

_ALLOWED_SAFETY_KEYS = {
    "no_trade_decision",
    "watch_only",
    "accepted_proof",
}


def complete_replacement_source_row_setup_time_review(
    request_packet: Mapping[str, Any] | None,
    completed_review_fields: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Intake one caller-completed setup-time review request packet."""

    if not isinstance(request_packet, Mapping) or not request_packet:
        return _result(
            candidate_id=_candidate_id_from(completed_review_fields),
            symbol=_value_from(completed_review_fields, "symbol"),
            setup_type=_value_from(completed_review_fields, "setup_type"),
            old_source_window_id=None,
            old_source_sample_id=None,
            source_file_label=None,
            completion_status="rejected",
            setup_time_review_status="rejected",
            setup_time_source_row_number=_value_from(completed_review_fields, "setup_time_source_row_number"),
            setup_time_timestamp=_value_from(completed_review_fields, "setup_time_timestamp"),
            completed_fields_used=[],
            missing_evidence=["setup-time review request packet"],
            rejected_reasons=["missing_request_packet"],
            diagnosis="completed setup-time review intake requires a caller-provided request packet",
            likely_cause_candidate="request packet was not supplied in memory",
            next_fix_path="supply a ready setup-time review request packet and completed review fields",
            regression_needed="preserve regression coverage for missing request packets",
            lower_tier_handoff_summary="rejected until the setup-time review request packet is supplied",
            packet_population_seed=None,
        )
    if completed_review_fields is not None and not isinstance(completed_review_fields, Mapping):
        raise TypeError("Completed review fields must be a mapping when provided")

    packet = deepcopy(dict(request_packet))
    completed = deepcopy(dict(completed_review_fields or {}))
    candidate_id = _text_or_none(packet.get("candidate_id")) or _text_or_none(completed.get("candidate_id"))
    expected = ALLOWED_CANDIDATES.get(candidate_id or "")
    symbol = completed.get("symbol", packet.get("symbol"))
    setup_type = completed.get("setup_type", packet.get("setup_type"))
    old_source_window_id = _first_present(packet, ("old_source_window_id", "source_window_id"))
    old_source_sample_id = _first_present(packet, ("old_source_sample_id", "source_sample_id"))
    source_file_label = _first_present(packet, ("source_file_label", "source_file_reference"))
    base_context = {
        "candidate_id": candidate_id,
        "symbol": symbol,
        "setup_type": setup_type,
        "old_source_window_id": old_source_window_id,
        "old_source_sample_id": old_source_sample_id,
        "source_file_label": source_file_label,
        "setup_time_source_row_number": completed.get("setup_time_source_row_number"),
        "setup_time_timestamp": completed.get("setup_time_timestamp"),
    }

    if expected is None:
        return _result(
            **base_context,
            completion_status="rejected",
            setup_time_review_status="rejected",
            completed_fields_used=_completed_fields_used(completed),
            missing_evidence=["known replacement candidate id"],
            rejected_reasons=["unknown_candidate_id"],
            diagnosis="unknown replacement setup-time review completion candidate id",
            likely_cause_candidate="candidate id is outside the replacement source row candidate set",
            next_fix_path="use one of the known local replacement source row candidate ids",
            regression_needed="preserve regression coverage for unknown completion candidate rejection",
            lower_tier_handoff_summary="rejected before completion intake because candidate id is unknown",
            packet_population_seed=None,
        )

    unavailable_packet = packet.get("setup_time_review_request_status") == "unavailable"
    if unavailable_packet:
        return _result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            completion_status="unavailable",
            setup_time_review_status="unavailable",
            completed_fields_used=_completed_fields_used(completed),
            missing_evidence=deepcopy(list(packet.get("missing_evidence", []))),
            rejected_reasons=[],
            diagnosis="setup-time review completion remains unavailable because the request packet is unavailable",
            likely_cause_candidate=str(packet.get("likely_cause_candidate") or "request packet is unavailable"),
            next_fix_path=str(packet.get("next_fix_path") or "supply an available setup-time review request packet"),
            regression_needed="preserve coverage that unavailable candidates stay unavailable",
            lower_tier_handoff_summary=str(
                packet.get("lower_tier_handoff_summary")
                or "no lower-tier setup-time completion work can begin until a request packet exists"
            ),
            packet_population_seed=None,
        )

    request_status = packet.get("setup_time_review_request_status")
    if request_status != "ready_for_setup_time_review_request":
        return _result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            completion_status="rejected",
            setup_time_review_status="rejected",
            completed_fields_used=_completed_fields_used(completed),
            missing_evidence=["ready_for_setup_time_review_request packet"],
            rejected_reasons=["request_packet_not_ready_for_setup_time_review_request"],
            diagnosis="setup-time review completion requires a ready setup-time review request packet",
            likely_cause_candidate=str(request_status),
            next_fix_path="complete only packets already marked ready_for_setup_time_review_request",
            regression_needed="preserve regression coverage for non-ready request packets",
            lower_tier_handoff_summary="rejected until request packet readiness is corrected",
            packet_population_seed=None,
        )

    rejected_reasons = _identity_rejections(packet, completed, expected)
    rejected_reasons.extend(_watch_flag_rejections(packet, completed))
    rejected_reasons.extend(_no_hindsight_rejections(completed))
    if rejected_reasons:
        return _result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            completion_status="rejected",
            setup_time_review_status="rejected",
            completed_fields_used=_completed_fields_used(completed),
            missing_evidence=["non-conflicting completed setup-time review fields"],
            rejected_reasons=rejected_reasons,
            diagnosis="setup-time review completion conflicts with the request packet or no-hindsight boundary",
            likely_cause_candidate=", ".join(rejected_reasons),
            next_fix_path="correct the completed candidate identity, watch flags, or no-hindsight boundary",
            regression_needed="preserve regression coverage for conflicting completion fields",
            lower_tier_handoff_summary="rejected until completion conflicts are corrected",
            packet_population_seed=None,
        )

    forbidden_paths = _walk_forbidden_keys({"request_packet": packet, "completed_review_fields": completed})
    if forbidden_paths:
        return _result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            completion_status="rejected",
            setup_time_review_status="rejected",
            completed_fields_used=_completed_fields_used(completed),
            missing_evidence=[{"forbidden_paths": forbidden_paths}],
            rejected_reasons=["forbidden_live_or_broker_fields"],
            diagnosis="setup-time review completion contains forbidden live, broker, account, options, or P&L fields",
            likely_cause_candidate=", ".join(forbidden_paths),
            next_fix_path="remove forbidden execution, broker, account, options, P&L, production, or secret fields",
            regression_needed="preserve regression coverage for forbidden completion fields",
            lower_tier_handoff_summary="rejected setup-time completion requires field cleanup",
            packet_population_seed=None,
        )

    candidate_review_rows = _candidate_review_rows(packet)
    if not candidate_review_rows:
        return _result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            completion_status="rejected",
            setup_time_review_status="rejected",
            completed_fields_used=_completed_fields_used(completed),
            missing_evidence=["candidate_review_rows"],
            rejected_reasons=["missing_candidate_review_rows"],
            diagnosis="setup-time review completion requires request candidate_review_rows",
            likely_cause_candidate="request packet did not include candidate review rows",
            next_fix_path="supply the original setup-time review request packet with candidate_review_rows",
            regression_needed="preserve regression coverage for missing candidate review rows",
            lower_tier_handoff_summary="rejected until request row material is supplied",
            packet_population_seed=None,
        )

    missing_fields = _missing_required_fields(completed)
    if missing_fields:
        return _result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            completion_status="blocked_missing_evidence",
            setup_time_review_status="blocked_missing_evidence",
            completed_fields_used=_completed_fields_used(completed),
            missing_evidence=missing_fields,
            rejected_reasons=[],
            diagnosis="setup-time review completion is missing required caller-provided evidence fields",
            likely_cause_candidate=", ".join(missing_fields),
            next_fix_path="provide the missing setup-time trigger, invalidation, freshness, blocker, and outcome fields",
            regression_needed="preserve regression coverage for missing completion fields",
            lower_tier_handoff_summary="blocked until required completed setup-time review fields are supplied",
            packet_population_seed=None,
        )

    setup_row_number = completed["setup_time_source_row_number"]
    candidate_row_numbers = _row_numbers(candidate_review_rows)
    if setup_row_number not in set(candidate_row_numbers):
        return _result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            completion_status="rejected",
            setup_time_review_status="rejected",
            completed_fields_used=_completed_fields_used(completed),
            missing_evidence=["setup-time row number inside request candidate_review_rows"],
            rejected_reasons=["setup_time_source_row_number_outside_candidate_review_rows"],
            diagnosis="completed setup-time row must be a 1-based source row inside request candidate_review_rows",
            likely_cause_candidate=str(setup_row_number),
            next_fix_path="choose a setup-time source row number from the request candidate_review_rows",
            regression_needed="preserve regression coverage for request row bounds",
            lower_tier_handoff_summary="rejected until setup-time row is inside request review rows",
            packet_population_seed=None,
        )

    gate_input = _gate_extracted_source_window(packet, candidate_review_rows, expected)
    gate_review = _gate_review_fields(packet, completed, expected)
    gate_result = review_replacement_source_row_setup_time(gate_input, gate_review)
    status = gate_result["setup_time_review_status"]
    return _result(
        **{
            **base_context,
            "symbol": expected[0],
            "setup_type": expected[1],
            "setup_time_source_row_number": completed["setup_time_source_row_number"],
            "setup_time_timestamp": completed["setup_time_timestamp"],
        },
        completion_status=status,
        setup_time_review_status=status,
        completed_fields_used=_completed_fields_used(completed),
        missing_evidence=gate_result["missing_evidence"],
        rejected_reasons=gate_result["rejected_reasons"],
        diagnosis=gate_result["diagnosis"],
        likely_cause_candidate=gate_result["likely_cause_candidate"],
        next_fix_path=gate_result["next_fix_path"],
        regression_needed=gate_result["regression_needed"],
        lower_tier_handoff_summary=gate_result["lower_tier_handoff_summary"],
        packet_population_seed=gate_result["packet_population_seed"],
    )


def complete_replacement_source_row_setup_time_review_batch(
    completions: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Intake caller-provided completed setup-time review request packets."""

    results = []
    for completion in completions:
        request_packet = completion.get("request_packet", completion.get("setup_time_review_request_packet"))
        completed_fields = completion.get("completed_review_fields", completion.get("setup_time_review_completion"))
        results.append(complete_replacement_source_row_setup_time_review(request_packet, completed_fields))

    return {
        "total": len(results),
        "ready_for_packet_build_review": sum(
            1 for result in results if result["completion_status"] == "ready_for_packet_build_review"
        ),
        "blocked_missing_evidence": sum(
            1 for result in results if result["completion_status"] == "blocked_missing_evidence"
        ),
        "rejected": sum(1 for result in results if result["completion_status"] == "rejected"),
        "unavailable": sum(1 for result in results if result["completion_status"] == "unavailable"),
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
    completion_status: str,
    setup_time_review_status: str,
    setup_time_source_row_number: Any,
    setup_time_timestamp: Any,
    completed_fields_used: Sequence[str],
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
        "source_file_label": source_file_label,
        "completion_status": completion_status,
        "setup_time_review_status": setup_time_review_status,
        "setup_time_source_row_number": setup_time_source_row_number,
        "setup_time_timestamp": setup_time_timestamp,
        "completed_fields_used": deepcopy(list(completed_fields_used)),
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


def _gate_extracted_source_window(
    packet: Mapping[str, Any],
    candidate_review_rows: Sequence[Mapping[str, Any]],
    expected: tuple[str, str],
) -> dict[str, Any]:
    return {
        "candidate_id": packet.get("candidate_id"),
        "symbol": expected[0],
        "setup_type": expected[1],
        "source_rows": deepcopy(list(candidate_review_rows)),
        "old_source_window_id": _first_present(packet, ("old_source_window_id", "source_window_id")),
        "old_source_sample_id": _first_present(packet, ("old_source_sample_id", "source_sample_id")),
        "source_file_label": _first_present(packet, ("source_file_label", "source_file_reference")),
        "source_file_reference": _first_present(packet, ("source_file_label", "source_file_reference")),
        "source_row_reference": _source_row_reference(packet, candidate_review_rows),
    }


def _gate_review_fields(
    packet: Mapping[str, Any],
    completed: Mapping[str, Any],
    expected: tuple[str, str],
) -> dict[str, Any]:
    result = {field: deepcopy(completed[field]) for field in REQUIRED_SETUP_TIME_REVIEW_FIELDS}
    result["candidate_id"] = packet.get("candidate_id")
    result["symbol"] = expected[0]
    result["setup_type"] = expected[1]
    return result


def _candidate_review_rows(packet: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = packet.get("candidate_review_rows")
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes, bytearray)):
        return []
    return [deepcopy(dict(row)) for row in rows if isinstance(row, Mapping)]


def _row_numbers(rows: Sequence[Mapping[str, Any]]) -> list[int]:
    numbers = []
    for row in rows:
        value = row.get("source_row_number")
        if isinstance(value, str) and value.strip().isdigit():
            value = int(value.strip())
        if isinstance(value, int) and not isinstance(value, bool) and value >= 1:
            numbers.append(value)
    return numbers


def _completed_fields_used(completed: Mapping[str, Any] | None) -> list[str]:
    if not isinstance(completed, Mapping):
        return []
    return [field for field in REQUIRED_SETUP_TIME_REVIEW_FIELDS if _is_present(completed.get(field))]


def _missing_required_fields(completed: Mapping[str, Any]) -> list[str]:
    return [field for field in REQUIRED_SETUP_TIME_REVIEW_FIELDS if not _is_present(completed.get(field))]


def _identity_rejections(
    packet: Mapping[str, Any],
    completed: Mapping[str, Any],
    expected: tuple[str, str],
) -> list[str]:
    rejected = []
    if packet.get("symbol") is not None and packet.get("symbol") != expected[0]:
        rejected.append("request_symbol_does_not_match_candidate_id")
    if packet.get("setup_type") is not None and packet.get("setup_type") != expected[1]:
        rejected.append("request_setup_type_does_not_match_candidate_id")
    if completed.get("candidate_id") is not None and completed.get("candidate_id") != packet.get("candidate_id"):
        rejected.append("completed_candidate_id_does_not_match_request_packet")
    if completed.get("symbol") is not None and completed.get("symbol") != expected[0]:
        rejected.append("symbol_does_not_match_candidate_id")
    if completed.get("setup_type") is not None and completed.get("setup_type") != expected[1]:
        rejected.append("setup_type_does_not_match_candidate_id")
    return rejected


def _watch_flag_rejections(packet: Mapping[str, Any], completed: Mapping[str, Any]) -> list[str]:
    rejected = []
    for field_name in ("watch_only", "no_trade_decision"):
        for source_name, source in (("request", packet), ("completed", completed)):
            if field_name in source and source[field_name] is not True:
                rejected.append(f"{source_name}_{field_name}_must_be_true")
    return rejected


def _no_hindsight_rejections(completed: Mapping[str, Any]) -> list[str]:
    statement = completed.get("no_hindsight_boundary_statement")
    if not isinstance(statement, str):
        return []
    lowered = statement.lower()
    conflict_markers = (
        "hindsight allowed",
        "uses hindsight",
        "use hindsight",
        "boundary violated",
        "not preserved",
        "after outcome",
    )
    if any(marker in lowered for marker in conflict_markers):
        return ["no_hindsight_boundary_conflict"]
    return []


def _source_row_reference(packet: Mapping[str, Any], rows: Sequence[Mapping[str, Any]]) -> str | None:
    explicit = _first_present(packet, ("source_row_reference",))
    if explicit is not None:
        return str(explicit)
    row_numbers = _row_numbers(rows)
    if row_numbers:
        return f"rows {min(row_numbers)}-{max(row_numbers)}"
    return None


def _walk_forbidden_keys(value: Any, path: str = "") -> list[str]:
    hits: list[str] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            key_text = str(key).lower()
            child_path = f"{path}.{key}" if path else str(key)
            if key_text not in _ALLOWED_SAFETY_KEYS and any(part in key_text for part in _FORBIDDEN_KEY_PARTS):
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


def _candidate_id_from(value: Any) -> str | None:
    if not isinstance(value, Mapping):
        return None
    return _text_or_none(value.get("candidate_id"))


def _value_from(value: Any, key: str) -> Any:
    if not isinstance(value, Mapping):
        return None
    return deepcopy(value.get(key))


def _text_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
