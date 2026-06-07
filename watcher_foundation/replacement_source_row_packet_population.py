"""Local in-memory replacement source row packet population gate.

No file reads, file writes, live data, network, subprocesses, broker/order/
account/options/P&L, alerts, or trade decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from .replacement_source_row_packet import ALLOWED_CANDIDATES
from .replacement_source_row_packet_builder import (
    build_replacement_source_row_packet_from_rows,
)
from .replacement_source_row_packet_readiness import (
    review_replacement_source_row_packet_readiness,
)


REPLACEMENT_SOURCE_ROW_PACKET_POPULATION_RESULT_FIELDS = (
    "candidate_id",
    "symbol",
    "setup_type",
    "population_status",
    "readiness_status",
    "source_rows_supplied",
    "packet_built",
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

_BUILDER_REQUEST_FIELDS = (
    "candidate_id",
    "source_rows",
    "setup_time_row_index",
    "source_file_reference",
    "source_row_reference",
    "source_window_start",
    "source_window_end",
    "trigger_candidate",
    "trigger_basis",
    "invalidation_candidate",
    "invalidation_basis",
    "freshness_final_signal_candidate",
    "blocker_caution_status",
    "unavailable_fields",
    "after_setup_outcome_window_start",
    "after_setup_outcome_window_end",
    "no_hindsight_boundary",
)

_FORBIDDEN_REQUEST_KEY_PARTS = (
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


def populate_replacement_source_row_packet_request(
    candidate_request: Mapping[str, Any],
) -> dict[str, Any]:
    """Populate one caller-provided replacement source row packet request."""

    if not isinstance(candidate_request, Mapping):
        raise TypeError("Replacement source row packet population input must be a mapping")

    request = deepcopy(dict(candidate_request))
    candidate_id = _text_or_none(request.get("candidate_id"))
    expected = ALLOWED_CANDIDATES.get(candidate_id or "")
    symbol = _identity_value(request, "symbol", expected, 0)
    setup_type = _identity_value(request, "setup_type", expected, 1)

    if expected is None:
        return _result(
            candidate_id=candidate_id,
            symbol=symbol,
            setup_type=setup_type,
            population_status="rejected",
            readiness_status="rejected",
            source_rows_supplied=0,
            packet_built=False,
            evidence_used=[],
            missing_evidence=["known replacement candidate id"],
            rejected_reasons=["unknown_candidate_id"],
            diagnosis="unknown replacement source row candidate id",
            likely_cause_candidate="candidate id is outside the Day 36 replacement source row candidate set",
            next_fix_path="use one of the known local replacement source row candidate ids",
            regression_needed="preserve regression coverage for unknown candidate rejection",
            lower_tier_handoff_summary="rejected before packet population because candidate id is unknown",
        )

    identity_rejections = _identity_rejections(request, expected)
    if identity_rejections:
        return _result(
            candidate_id=candidate_id,
            symbol=symbol,
            setup_type=setup_type,
            population_status="rejected",
            readiness_status="rejected",
            source_rows_supplied=_source_rows_supplied(request),
            packet_built=False,
            evidence_used=[],
            missing_evidence=["valid candidate/symbol/setup-type combination"],
            rejected_reasons=identity_rejections,
            diagnosis="replacement source row request failed candidate identity validation",
            likely_cause_candidate=", ".join(identity_rejections),
            next_fix_path="correct the candidate id, symbol, or setup type before packet population",
            regression_needed="preserve regression coverage for invalid candidate identity combinations",
            lower_tier_handoff_summary="rejected request requires lower-tier identity correction before packet build",
        )

    forbidden_paths = _walk_forbidden_request_keys(request)
    if forbidden_paths:
        return _result(
            candidate_id=candidate_id,
            symbol=symbol,
            setup_type=setup_type,
            population_status="rejected",
            readiness_status="rejected",
            source_rows_supplied=_source_rows_supplied(request),
            packet_built=False,
            evidence_used=[],
            missing_evidence=[{"forbidden_paths": forbidden_paths}],
            rejected_reasons=["forbidden_live_or_broker_fields"],
            diagnosis="replacement source row request contains forbidden live, broker, account, options, or P&L fields",
            likely_cause_candidate=", ".join(forbidden_paths),
            next_fix_path="remove forbidden execution, broker, account, options, P&L, production, or secret fields",
            regression_needed="preserve regression coverage for forbidden population request fields",
            lower_tier_handoff_summary="rejected request requires lower-tier field cleanup before packet build",
        )

    if _source_rows_supplied(request) == 0:
        readiness = review_replacement_source_row_packet_readiness(
            {
                "candidate_id": candidate_id,
                "symbol": expected[0],
                "setup_type": expected[1],
                "unavailable_status": request.get("unavailable_status", "source_rows_missing"),
                "missing_evidence": request.get("missing_evidence", []),
            }
        )
        return _from_readiness(
            readiness,
            population_status="unavailable",
            source_rows_supplied=0,
            packet_built=False,
            rejected_reasons=[],
        )

    builder_request = {
        field_name: deepcopy(request[field_name])
        for field_name in _BUILDER_REQUEST_FIELDS
        if field_name in request
    }
    built = build_replacement_source_row_packet_from_rows(**builder_request)
    readiness = review_replacement_source_row_packet_readiness(built)
    readiness_status = readiness["readiness_status"]
    population_status = (
        "ready_for_packet_build_review"
        if readiness_status == "ready_for_acceptance_review"
        else "rejected"
        if readiness_status == "rejected"
        else "blocked_missing_evidence"
    )

    rejected_reasons = []
    validation = readiness.get("validation")
    if isinstance(validation, Mapping):
        rejected_reasons = deepcopy(validation.get("rejected_reasons", []))
    elif isinstance(built.get("validation"), Mapping):
        rejected_reasons = deepcopy(built["validation"].get("rejected_reasons", []))

    return _from_readiness(
        readiness,
        population_status=population_status,
        source_rows_supplied=_source_rows_supplied(request),
        packet_built=isinstance(built.get("packet"), Mapping),
        rejected_reasons=rejected_reasons,
    )


def populate_replacement_source_row_packet_batch(
    candidate_requests: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Populate a batch of caller-provided replacement source row requests."""

    results = [
        populate_replacement_source_row_packet_request(candidate_request)
        for candidate_request in candidate_requests
    ]

    by_candidate_id = {
        str(result["candidate_id"]): deepcopy(result)
        for result in results
    }

    return {
        "total": len(results),
        "ready_for_packet_build_review": sum(
            1 for result in results if result["population_status"] == "ready_for_packet_build_review"
        ),
        "blocked_missing_evidence": sum(
            1 for result in results if result["population_status"] == "blocked_missing_evidence"
        ),
        "rejected": sum(
            1 for result in results if result["population_status"] == "rejected"
        ),
        "unavailable": sum(
            1 for result in results if result["population_status"] == "unavailable"
        ),
        "accepted_proof_count": 0,
        "results": by_candidate_id,
        "watch_only": True,
        "no_trade_decision": True,
    }


def _from_readiness(
    readiness: Mapping[str, Any],
    *,
    population_status: str,
    source_rows_supplied: int,
    packet_built: bool,
    rejected_reasons: list[Any],
) -> dict[str, Any]:
    return _result(
        candidate_id=readiness.get("candidate_id"),
        symbol=readiness.get("symbol"),
        setup_type=readiness.get("setup_type"),
        population_status=population_status,
        readiness_status=readiness.get("readiness_status"),
        source_rows_supplied=source_rows_supplied,
        packet_built=packet_built,
        evidence_used=deepcopy(readiness.get("evidence_used", [])),
        missing_evidence=deepcopy(readiness.get("missing_evidence", [])),
        rejected_reasons=deepcopy(rejected_reasons),
        diagnosis=str(readiness.get("diagnosis", "")),
        likely_cause_candidate=str(readiness.get("likely_cause_candidate", "")),
        next_fix_path=str(readiness.get("next_fix_path", "")),
        regression_needed=str(readiness.get("regression_needed", "")),
        lower_tier_handoff_summary=str(readiness.get("lower_tier_handoff_summary", "")),
    )


def _result(
    *,
    candidate_id: Any,
    symbol: Any,
    setup_type: Any,
    population_status: str,
    readiness_status: str,
    source_rows_supplied: int,
    packet_built: bool,
    evidence_used: list[Any],
    missing_evidence: list[Any],
    rejected_reasons: list[Any],
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
        "population_status": population_status,
        "readiness_status": readiness_status,
        "source_rows_supplied": source_rows_supplied,
        "packet_built": packet_built,
        "evidence_used": deepcopy(evidence_used),
        "missing_evidence": deepcopy(missing_evidence),
        "rejected_reasons": deepcopy(rejected_reasons),
        "diagnosis": diagnosis,
        "likely_cause_candidate": likely_cause_candidate,
        "next_fix_path": next_fix_path,
        "regression_needed": regression_needed,
        "lower_tier_handoff_summary": lower_tier_handoff_summary,
        "watch_only": True,
        "no_trade_decision": True,
        "accepted_proof": False,
    }


def _source_rows_supplied(request: Mapping[str, Any]) -> int:
    rows = request.get("source_rows")
    if isinstance(rows, Sequence) and not isinstance(rows, (str, bytes, bytearray)):
        return len(rows)
    return 0


def _text_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _identity_value(
    request: Mapping[str, Any],
    field_name: str,
    expected: tuple[str, str] | None,
    expected_index: int,
) -> Any:
    if field_name in request:
        return deepcopy(request[field_name])
    if expected is not None:
        return expected[expected_index]
    return None


def _identity_rejections(
    request: Mapping[str, Any],
    expected: tuple[str, str],
) -> list[str]:
    rejected = []
    if "symbol" in request and request["symbol"] != expected[0]:
        rejected.append("symbol_does_not_match_candidate_id")
    if "setup_type" in request and request["setup_type"] != expected[1]:
        rejected.append("setup_type_does_not_match_candidate_id")
    return rejected


def _walk_forbidden_request_keys(value: Any, path: str = "") -> list[str]:
    hits: list[str] = []

    if isinstance(value, Mapping):
        for key, child in value.items():
            key_text = str(key).lower()
            child_path = f"{path}.{key}" if path else str(key)
            if any(part in key_text for part in _FORBIDDEN_REQUEST_KEY_PARTS):
                hits.append(child_path)
            hits.extend(_walk_forbidden_request_keys(child, child_path))
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, child in enumerate(value):
            hits.extend(_walk_forbidden_request_keys(child, f"{path}[{index}]"))

    return hits
