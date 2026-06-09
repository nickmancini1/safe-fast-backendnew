"""Local in-memory setup-time review completion draft builder.

No file reads, file writes, live data, network, subprocesses, broker/order/
account/options/P&L, alerts, or trade decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from .replacement_source_row_packet import ALLOWED_CANDIDATES
from .replacement_source_row_setup_time_review import REQUIRED_SETUP_TIME_REVIEW_FIELDS


REPLACEMENT_SOURCE_ROW_SETUP_TIME_REVIEW_COMPLETION_DRAFT_FIELDS = (
    "candidate_id",
    "symbol",
    "setup_type",
    "completion_draft_status",
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
    "completed_fields_used",
    "missing_evidence",
    "rejected_reasons",
    "diagnosis",
    "likely_cause_candidate",
    "next_fix_path",
    "regression_needed",
    "lower_tier_handoff_summary",
    "completion_payload",
    "watch_only",
    "no_trade_decision",
    "accepted_proof",
)

REQUIRED_COMPLETION_CHOICES = (
    "setup_time_source_row_number",
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

_ALLOWED_SAFETY_KEYS = {"watch_only", "no_trade_decision", "accepted_proof"}


def build_replacement_source_row_setup_time_review_completion_draft(
    row_context_packet: Mapping[str, Any] | None,
    reviewer_completion_choices: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Build one completion draft from row-context rows and reviewer choices."""

    if row_context_packet is not None and not isinstance(row_context_packet, Mapping):
        raise TypeError("Row-context packet must be a mapping when provided")
    if reviewer_completion_choices is not None and not isinstance(reviewer_completion_choices, Mapping):
        raise TypeError("Reviewer completion choices must be a mapping when provided")

    packet = deepcopy(dict(row_context_packet or {}))
    choices = deepcopy(dict(reviewer_completion_choices or {}))
    candidate_id = _text_or_none(packet.get("candidate_id")) or _text_or_none(choices.get("candidate_id"))
    expected = ALLOWED_CANDIDATES.get(candidate_id or "")
    symbol = choices.get("symbol", packet.get("symbol"))
    setup_type = choices.get("setup_type", packet.get("setup_type"))
    base_context = _base_context(packet, choices, candidate_id, symbol, setup_type)

    if not packet:
        return _result(
            **base_context,
            completion_draft_status="rejected",
            completed_fields_used=_completed_fields_used(choices),
            missing_evidence=["row-context packet"],
            rejected_reasons=["missing_row_context_packet"],
            diagnosis="setup-time review completion draft requires a caller-provided row-context packet",
            likely_cause_candidate="row-context packet was not supplied in memory",
            next_fix_path="supply a row-context packet and reviewer completion choices",
            regression_needed="preserve coverage for missing row-context packets",
            lower_tier_handoff_summary="rejected until row-context packet is supplied",
            completion_payload=None,
        )

    if expected is None:
        return _result(
            **base_context,
            completion_draft_status="rejected",
            completed_fields_used=_completed_fields_used(choices),
            missing_evidence=["known replacement candidate id"],
            rejected_reasons=["unknown_candidate_id"],
            diagnosis="unknown replacement setup-time review completion draft candidate id",
            likely_cause_candidate="candidate id is outside the replacement source row candidate set",
            next_fix_path="use one of the known local replacement source row candidate ids",
            regression_needed="preserve coverage for unknown completion draft candidate rejection",
            lower_tier_handoff_summary="rejected before draft build because candidate id is unknown",
            completion_payload=None,
        )

    if _is_unavailable_packet(packet):
        return _result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            completion_draft_status="unavailable",
            completed_fields_used=_completed_fields_used(choices),
            missing_evidence=deepcopy(list(packet.get("missing_evidence", ["row-context packet unavailable"]))),
            rejected_reasons=[],
            diagnosis="setup-time review completion draft remains unavailable because the row-context packet is unavailable",
            likely_cause_candidate=str(packet.get("likely_cause_candidate") or "row-context packet is unavailable"),
            next_fix_path=str(packet.get("next_fix_path") or "supply an available row-context packet"),
            regression_needed="preserve coverage that unavailable row-context packets stay unavailable",
            lower_tier_handoff_summary=str(
                packet.get("lower_tier_handoff_summary")
                or "no completion draft can be built until row-context evidence exists"
            ),
            completion_payload=None,
        )

    rejected_reasons = _identity_rejections(packet, choices, expected)
    rejected_reasons.extend(_watch_flag_rejections(packet, choices))
    rejected_reasons.extend(_no_hindsight_rejections(choices))
    forbidden_paths = _walk_forbidden_keys({"row_context_packet": packet, "reviewer_completion_choices": choices})
    if forbidden_paths:
        rejected_reasons.append("forbidden_live_or_broker_fields")

    if rejected_reasons:
        missing = ["non-conflicting row-context packet and completion choices"]
        if forbidden_paths:
            missing = [{"forbidden_paths": forbidden_paths}]
        return _result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            completion_draft_status="rejected",
            completed_fields_used=_completed_fields_used(choices),
            missing_evidence=missing,
            rejected_reasons=rejected_reasons,
            diagnosis="setup-time review completion draft conflicts with identity, safety, or no-hindsight boundaries",
            likely_cause_candidate=", ".join(rejected_reasons),
            next_fix_path="correct candidate identity, watch flags, forbidden fields, or no-hindsight boundary",
            regression_needed="preserve coverage for rejected completion draft conflicts",
            lower_tier_handoff_summary="rejected until draft conflicts are corrected",
            completion_payload=None,
        )

    rows = _row_context_rows(packet)
    if not rows:
        return _result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            completion_draft_status="rejected",
            completed_fields_used=_completed_fields_used(choices),
            missing_evidence=["row-context rows"],
            rejected_reasons=["missing_row_context_rows"],
            diagnosis="setup-time review completion draft requires caller-provided row-context rows",
            likely_cause_candidate="row-context packet did not include usable rows",
            next_fix_path="supply row-context rows in memory before building a completion draft",
            regression_needed="preserve coverage for missing row-context rows",
            lower_tier_handoff_summary="rejected until row-context rows are supplied",
            completion_payload=None,
        )

    missing_choices = _missing_required_choices(choices)
    if missing_choices:
        return _result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            completion_draft_status="blocked_missing_evidence",
            completed_fields_used=_completed_fields_used(choices),
            missing_evidence=missing_choices,
            rejected_reasons=[],
            diagnosis="setup-time review completion draft is missing required caller-provided choices",
            likely_cause_candidate=", ".join(missing_choices),
            next_fix_path="provide the missing setup-time completion choices before draft readiness",
            regression_needed="preserve coverage for missing completion draft choices",
            lower_tier_handoff_summary="blocked until required reviewer completion choices are supplied",
            completion_payload=None,
        )

    setup_row_number = _coerce_int(choices["setup_time_source_row_number"])
    if setup_row_number is None or setup_row_number < 1:
        return _row_rejection(base_context, expected, choices, "setup_time_source_row_number_invalid")

    setup_row = _row_for_source_number(rows, setup_row_number)
    if setup_row is None:
        return _row_rejection(
            base_context,
            expected,
            choices,
            "setup_time_source_row_number_outside_row_context_rows",
        )

    timeline_error = _timeline_error(setup_row_number, choices)
    if timeline_error:
        return _result(
            **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
            completion_draft_status="rejected",
            completed_fields_used=_completed_fields_used(choices),
            missing_evidence=[{"timeline_errors": [timeline_error]}],
            rejected_reasons=["after_setup_window_violates_no_hindsight_boundary"],
            diagnosis="after-setup outcome window must start after the setup-time source row",
            likely_cause_candidate=timeline_error,
            next_fix_path="move the after-setup outcome window start after the setup-time row",
            regression_needed="preserve coverage for no-hindsight boundary violations",
            lower_tier_handoff_summary="rejected until after-setup window starts after setup-time evidence",
            completion_payload=None,
        )

    setup_time_timestamp = setup_row.get("timestamp")
    setup_time_row_ohlcv = _row_ohlcv(setup_row)
    completed_fields = _completed_review_fields(choices, expected, setup_time_timestamp, setup_time_row_ohlcv)
    request_packet = _request_packet(packet, rows, expected)
    completion_payload = {
        "request_packet": request_packet,
        "completed_review_fields": completed_fields,
    }
    return _result(
        **{
            **base_context,
            "symbol": expected[0],
            "setup_type": expected[1],
            "setup_time_source_row_number": setup_row_number,
            "setup_time_timestamp": setup_time_timestamp,
            "setup_time_row_ohlcv": setup_time_row_ohlcv,
        },
        completion_draft_status="completion_draft_ready",
        completed_fields_used=_completed_fields_used(completed_fields),
        missing_evidence=[],
        rejected_reasons=[],
        diagnosis="setup-time review completion draft is ready for completion intake only",
        likely_cause_candidate="caller selected row-context row and supplied completion choices",
        next_fix_path="send completion_payload to the setup-time review completion intake helper without accepting proof",
        regression_needed="preserve coverage that completion drafts are not accepted proof",
        lower_tier_handoff_summary="completion draft ready only; accepted proof remains false",
        completion_payload=completion_payload,
    )


def build_replacement_source_row_setup_time_review_completion_draft_batch(
    draft_requests: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Build completion drafts for caller-provided row-context packet inputs."""

    results = []
    for draft_request in draft_requests:
        row_context_packet = draft_request.get("row_context_packet", draft_request.get("request_packet"))
        choices = draft_request.get("reviewer_completion_choices", draft_request.get("completed_review_fields"))
        results.append(build_replacement_source_row_setup_time_review_completion_draft(row_context_packet, choices))

    return {
        "total": len(results),
        "completion_draft_ready": sum(
            1 for result in results if result["completion_draft_status"] == "completion_draft_ready"
        ),
        "blocked_missing_evidence": sum(
            1 for result in results if result["completion_draft_status"] == "blocked_missing_evidence"
        ),
        "rejected": sum(1 for result in results if result["completion_draft_status"] == "rejected"),
        "unavailable": sum(1 for result in results if result["completion_draft_status"] == "unavailable"),
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
    completion_draft_status: str,
    setup_time_source_row_number: Any,
    setup_time_timestamp: Any,
    setup_time_row_ohlcv: Any,
    accepted_setup_identity: Any,
    accepted_final_verdict: Any,
    accepted_trigger_state: Any,
    accepted_numeric_trigger: Any,
    accepted_trigger_basis: Any,
    accepted_numeric_invalidation: Any,
    accepted_invalidation_basis: Any,
    accepted_freshness_final_signal_decision: Any,
    accepted_blocker_caution_decision: Any,
    no_hindsight_boundary_statement: Any,
    after_setup_outcome_window_start: Any,
    after_setup_outcome_window_end: Any,
    completed_fields_used: Sequence[Any],
    missing_evidence: Sequence[Any],
    rejected_reasons: Sequence[Any],
    diagnosis: str,
    likely_cause_candidate: str,
    next_fix_path: str,
    regression_needed: str,
    lower_tier_handoff_summary: str,
    completion_payload: Mapping[str, Any] | None,
) -> dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "symbol": symbol,
        "setup_type": setup_type,
        "old_source_window_id": old_source_window_id,
        "old_source_sample_id": old_source_sample_id,
        "source_file_label": source_file_label,
        "completion_draft_status": completion_draft_status,
        "setup_time_source_row_number": setup_time_source_row_number,
        "setup_time_timestamp": setup_time_timestamp,
        "setup_time_row_ohlcv": deepcopy(setup_time_row_ohlcv),
        "accepted_setup_identity": deepcopy(accepted_setup_identity),
        "accepted_final_verdict": deepcopy(accepted_final_verdict),
        "accepted_trigger_state": deepcopy(accepted_trigger_state),
        "accepted_numeric_trigger": deepcopy(accepted_numeric_trigger),
        "accepted_trigger_basis": deepcopy(accepted_trigger_basis),
        "accepted_numeric_invalidation": deepcopy(accepted_numeric_invalidation),
        "accepted_invalidation_basis": deepcopy(accepted_invalidation_basis),
        "accepted_freshness_final_signal_decision": deepcopy(accepted_freshness_final_signal_decision),
        "accepted_blocker_caution_decision": deepcopy(accepted_blocker_caution_decision),
        "no_hindsight_boundary_statement": deepcopy(no_hindsight_boundary_statement),
        "after_setup_outcome_window_start": deepcopy(after_setup_outcome_window_start),
        "after_setup_outcome_window_end": deepcopy(after_setup_outcome_window_end),
        "completed_fields_used": deepcopy(list(completed_fields_used)),
        "missing_evidence": deepcopy(list(missing_evidence)),
        "rejected_reasons": deepcopy(list(rejected_reasons)),
        "diagnosis": diagnosis,
        "likely_cause_candidate": likely_cause_candidate,
        "next_fix_path": next_fix_path,
        "regression_needed": regression_needed,
        "lower_tier_handoff_summary": lower_tier_handoff_summary,
        "completion_payload": deepcopy(dict(completion_payload)) if completion_payload is not None else None,
        "watch_only": True,
        "no_trade_decision": True,
        "accepted_proof": False,
    }


def _base_context(
    packet: Mapping[str, Any],
    choices: Mapping[str, Any],
    candidate_id: Any,
    symbol: Any,
    setup_type: Any,
) -> dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "symbol": symbol,
        "setup_type": setup_type,
        "old_source_window_id": _first_present(packet, ("old_source_window_id", "source_window_id")),
        "old_source_sample_id": _first_present(packet, ("old_source_sample_id", "source_sample_id")),
        "source_file_label": _first_present(packet, ("source_file_label", "source_file_reference")),
        "setup_time_source_row_number": choices.get("setup_time_source_row_number"),
        "setup_time_timestamp": None,
        "setup_time_row_ohlcv": None,
        "accepted_setup_identity": choices.get("accepted_setup_identity"),
        "accepted_final_verdict": choices.get("accepted_final_verdict"),
        "accepted_trigger_state": choices.get("accepted_trigger_state"),
        "accepted_numeric_trigger": choices.get("accepted_numeric_trigger"),
        "accepted_trigger_basis": choices.get("accepted_trigger_basis"),
        "accepted_numeric_invalidation": choices.get("accepted_numeric_invalidation"),
        "accepted_invalidation_basis": choices.get("accepted_invalidation_basis"),
        "accepted_freshness_final_signal_decision": choices.get("accepted_freshness_final_signal_decision"),
        "accepted_blocker_caution_decision": choices.get("accepted_blocker_caution_decision"),
        "no_hindsight_boundary_statement": choices.get("no_hindsight_boundary_statement"),
        "after_setup_outcome_window_start": choices.get("after_setup_outcome_window_start"),
        "after_setup_outcome_window_end": choices.get("after_setup_outcome_window_end"),
    }


def _request_packet(packet: Mapping[str, Any], rows: Sequence[Mapping[str, Any]], expected: tuple[str, str]) -> dict[str, Any]:
    return {
        "candidate_id": packet.get("candidate_id"),
        "symbol": expected[0],
        "setup_type": expected[1],
        "old_source_window_id": _first_present(packet, ("old_source_window_id", "source_window_id")),
        "old_source_sample_id": _first_present(packet, ("old_source_sample_id", "source_sample_id")),
        "source_file_label": _first_present(packet, ("source_file_label", "source_file_reference")),
        "row_start": _first_present(packet, ("row_start",)),
        "row_end": _first_present(packet, ("row_end",)),
        "candidate_review_rows": deepcopy(list(rows)),
        "setup_time_review_request_status": "ready_for_setup_time_review_request",
        "watch_only": True,
        "no_trade_decision": True,
        "accepted_proof": False,
    }


def _completed_review_fields(
    choices: Mapping[str, Any],
    expected: tuple[str, str],
    setup_time_timestamp: Any,
    setup_time_row_ohlcv: Mapping[str, Any],
) -> dict[str, Any]:
    completed = {field: deepcopy(choices[field]) for field in REQUIRED_COMPLETION_CHOICES}
    completed["candidate_id"] = choices.get("candidate_id")
    completed["symbol"] = expected[0]
    completed["setup_type"] = expected[1]
    completed["setup_time_timestamp"] = deepcopy(setup_time_timestamp)
    completed["setup_time_row_ohlcv"] = deepcopy(dict(setup_time_row_ohlcv))
    completed["accepted_proof"] = False
    return completed


def _is_unavailable_packet(packet: Mapping[str, Any]) -> bool:
    unavailable_statuses = {
        "unavailable",
        "UNAVAILABLE",
    }
    status_keys = (
        "row_context_packet_status",
        "setup_time_review_request_status",
        "completion_status",
        "setup_time_review_row_context_status",
    )
    return any(packet.get(key) in unavailable_statuses for key in status_keys)


def _row_context_rows(packet: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = packet.get("row_context_rows", packet.get("candidate_review_rows", packet.get("source_rows", [])))
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes, bytearray)):
        return []
    normalized = []
    for row in rows:
        if not isinstance(row, Mapping):
            continue
        copied = deepcopy(dict(row))
        row_number = copied.get("source_row_number")
        if isinstance(row_number, str) and row_number.strip().isdigit():
            copied["source_row_number"] = int(row_number.strip())
        normalized.append(copied)
    return normalized


def _row_for_source_number(rows: Sequence[Mapping[str, Any]], source_row_number: int) -> Mapping[str, Any] | None:
    for row in rows:
        if row.get("source_row_number") == source_row_number:
            return row
    return None


def _row_ohlcv(row: Mapping[str, Any]) -> dict[str, Any]:
    return {field: deepcopy(row.get(field)) for field in _OHLCV_FIELDS}


def _row_rejection(
    base_context: Mapping[str, Any],
    expected: tuple[str, str],
    choices: Mapping[str, Any],
    reason: str,
) -> dict[str, Any]:
    return _result(
        **{**base_context, "symbol": expected[0], "setup_type": expected[1]},
        completion_draft_status="rejected",
        completed_fields_used=_completed_fields_used(choices),
        missing_evidence=["setup-time row number inside row-context rows"],
        rejected_reasons=[reason],
        diagnosis="setup-time source row number must be a 1-based source row inside the row-context rows",
        likely_cause_candidate=str(choices.get("setup_time_source_row_number")),
        next_fix_path="choose a setup-time source row number from the row-context packet rows",
        regression_needed="preserve coverage for row-context row bounds",
        lower_tier_handoff_summary="rejected until setup-time row is inside row-context rows",
        completion_payload=None,
    )


def _missing_required_choices(choices: Mapping[str, Any]) -> list[str]:
    return [field for field in REQUIRED_COMPLETION_CHOICES if not _is_present(choices.get(field))]


def _completed_fields_used(choices: Mapping[str, Any] | None) -> list[str]:
    if not isinstance(choices, Mapping):
        return []
    return [field for field in REQUIRED_SETUP_TIME_REVIEW_FIELDS if _is_present(choices.get(field))]


def _identity_rejections(packet: Mapping[str, Any], choices: Mapping[str, Any], expected: tuple[str, str]) -> list[str]:
    rejected = []
    if packet.get("symbol") is not None and packet.get("symbol") != expected[0]:
        rejected.append("row_context_symbol_does_not_match_candidate_id")
    if packet.get("setup_type") is not None and packet.get("setup_type") != expected[1]:
        rejected.append("row_context_setup_type_does_not_match_candidate_id")
    if choices.get("candidate_id") is not None and choices.get("candidate_id") != packet.get("candidate_id"):
        rejected.append("completed_candidate_id_does_not_match_row_context_packet")
    if choices.get("symbol") is not None and choices.get("symbol") != expected[0]:
        rejected.append("symbol_does_not_match_candidate_id")
    if choices.get("setup_type") is not None and choices.get("setup_type") != expected[1]:
        rejected.append("setup_type_does_not_match_candidate_id")
    return rejected


def _watch_flag_rejections(packet: Mapping[str, Any], choices: Mapping[str, Any]) -> list[str]:
    rejected = []
    for field_name in ("watch_only", "no_trade_decision"):
        for source_name, source in (("row_context", packet), ("completed", choices)):
            if field_name in source and source[field_name] is not True:
                rejected.append(f"{source_name}_{field_name}_must_be_true")
    return rejected


def _no_hindsight_rejections(choices: Mapping[str, Any]) -> list[str]:
    statement = choices.get("no_hindsight_boundary_statement")
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


def _timeline_error(setup_row_number: int, choices: Mapping[str, Any]) -> str | None:
    outcome_start = _coerce_int(choices.get("after_setup_outcome_window_start"))
    outcome_end = _coerce_int(choices.get("after_setup_outcome_window_end"))
    if outcome_start is not None and outcome_start <= setup_row_number:
        return "after_setup_outcome_window_start must be greater than setup_time_source_row_number"
    if outcome_start is not None and outcome_end is not None and outcome_end <= outcome_start:
        return "after_setup_outcome_window_end must be greater than after_setup_outcome_window_start"
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
        return bool(value.strip()) and value.strip().upper() != "UNAVAILABLE"
    if isinstance(value, Mapping):
        return len(value) > 0
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return len(value) > 0
    return True


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
