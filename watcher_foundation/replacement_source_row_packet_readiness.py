"""Local-only replacement source row packet readiness review.

This module accepts caller-provided in-memory replacement source row packets
or unavailable/template summaries and returns in-memory readiness summaries.
It does not read files, write files, call network services, start subprocesses,
touch brokers/accounts/options/P&L, emit alerts, or make trade decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from .replacement_source_row_packet import (
    ALLOWED_CANDIDATES,
    validate_replacement_source_row_packet,
)


REPLACEMENT_SOURCE_ROW_PACKET_READINESS_STATUSES = (
    "ready_for_acceptance_review",
    "missing_evidence_inconclusive",
    "rejected",
)

REPLACEMENT_SOURCE_ROW_PACKET_READINESS_RESULT_FIELDS = (
    "candidate_id",
    "symbol",
    "setup_type",
    "readiness_status",
    "setup_appeared",
    "what_happened_after",
    "evidence_used",
    "missing_evidence",
    "diagnosis",
    "likely_cause_candidate",
    "next_fix_path",
    "regression_needed",
    "lower_tier_handoff_summary",
    "watch_only",
    "no_trade_decision",
    "accepted_proof",
)

_TRIGGER_FIELDS = (
    "trigger_candidate",
    "trigger_basis",
)

_INVALIDATION_FIELDS = (
    "invalidation_candidate",
    "invalidation_basis",
)

_FRESHNESS_FIELDS = (
    "freshness_final_signal_candidate",
)


def review_replacement_source_row_packet_readiness(
    candidate_summary: Mapping[str, Any],
) -> dict[str, Any]:
    """Review one in-memory replacement source row packet or unavailable slot."""

    if not isinstance(candidate_summary, Mapping):
        raise TypeError("Replacement source row packet readiness input must be a mapping")

    input_copy = deepcopy(dict(candidate_summary))
    packet = _extract_packet(input_copy)
    candidate_id = _candidate_id(input_copy, packet)
    expected = ALLOWED_CANDIDATES.get(candidate_id or "")
    symbol = _identity_value(input_copy, packet, "symbol", expected, 0)
    setup_type = _identity_value(input_copy, packet, "setup_type", expected, 1)

    if expected is None:
        return _result(
            candidate_id=candidate_id,
            symbol=symbol,
            setup_type=setup_type,
            readiness_status="rejected",
            setup_appeared="unknown",
            what_happened_after="unknown candidate cannot be reviewed",
            evidence_used=[],
            missing_evidence=["known replacement candidate id"],
            diagnosis="unknown replacement source row candidate id",
            likely_cause_candidate="candidate id is outside the Day 36 replacement source row candidate set",
            next_fix_path="use one of the known local replacement source row candidate ids",
            regression_needed="add or preserve regression coverage for unknown candidate rejection",
            lower_tier_handoff_summary="rejected before packet readiness because candidate id is unknown",
        )

    if packet is None:
        missing_evidence = _unavailable_missing_evidence(input_copy)
        return _result(
            candidate_id=candidate_id,
            symbol=symbol,
            setup_type=setup_type,
            readiness_status="missing_evidence_inconclusive",
            setup_appeared="missing_evidence_inconclusive",
            what_happened_after="unavailable replacement source row slot; no accepted proof reviewed",
            evidence_used=_summary_evidence_used(input_copy),
            missing_evidence=missing_evidence,
            diagnosis="replacement source row evidence remains unavailable or template-only",
            likely_cause_candidate="source row packet evidence has not been collected for local review",
            next_fix_path="collect trigger, invalidation, freshness, source row, and after-setup evidence locally",
            regression_needed="preserve regression coverage that unavailable slots remain inconclusive",
            lower_tier_handoff_summary=(
                f"{symbol} {setup_type} requires lower-tier source row evidence collection: "
                + ", ".join(missing_evidence)
            ),
        )

    validation = validate_replacement_source_row_packet(packet)
    missing_evidence = _validation_missing_evidence(validation)
    rejected_reasons = validation.get("rejected_reasons", [])
    identity_rejected = any(
        reason in rejected_reasons
        for reason in (
            "unknown_candidate_id",
            "symbol_does_not_match_candidate_id",
            "setup_type_does_not_match_candidate_id",
            "forbidden_live_or_broker_fields",
        )
    )
    readiness_status = (
        "ready_for_acceptance_review"
        if validation["ready_for_acceptance_review"]
        else "rejected"
        if identity_rejected
        else "missing_evidence_inconclusive"
    )

    if readiness_status == "ready_for_acceptance_review":
        diagnosis = "valid local source row packet is ready for acceptance review only"
        likely_cause = "required setup-time and after-setup evidence fields are present"
        next_fix = "perform acceptance review without promoting accepted proof"
        regression = "preserve regression coverage that readiness is not accepted proof"
        handoff = "packet can be reviewed locally; accepted proof remains false"
    elif readiness_status == "rejected":
        diagnosis = "replacement source row packet failed identity or forbidden-field validation"
        likely_cause = ", ".join(rejected_reasons)
        next_fix = "correct candidate identity or remove forbidden live/trade fields before review"
        regression = "preserve regression coverage for rejected packet boundaries"
        handoff = "rejected packet requires lower-tier contract correction before review"
    else:
        diagnosis = "replacement source row packet is still missing required evidence"
        likely_cause = ", ".join(rejected_reasons) or "missing evidence"
        next_fix = "fill the missing source row packet evidence locally"
        regression = "preserve regression coverage for missing packet evidence"
        handoff = "blocked packet requires lower-tier evidence completion before review"

    return _result(
        candidate_id=validation["candidate_id"],
        symbol=validation["symbol"],
        setup_type=validation["setup_type"],
        readiness_status=readiness_status,
        setup_appeared=_setup_appeared(packet, validation),
        what_happened_after=_what_happened_after(packet, validation),
        evidence_used=_packet_evidence_used(packet),
        missing_evidence=missing_evidence,
        diagnosis=diagnosis,
        likely_cause_candidate=likely_cause,
        next_fix_path=next_fix,
        regression_needed=regression,
        lower_tier_handoff_summary=handoff,
        validation=validation,
    )


def review_replacement_source_row_packet_readiness_batch(
    candidate_summaries: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Review multiple replacement source row packets or unavailable slots."""

    results = [
        review_replacement_source_row_packet_readiness(candidate_summary)
        for candidate_summary in candidate_summaries
    ]

    return {
        "records_processed": len(results),
        "ready_for_acceptance_review": sum(
            1 for result in results if result["readiness_status"] == "ready_for_acceptance_review"
        ),
        "blocked_missing_evidence_inconclusive": sum(
            1 for result in results if result["readiness_status"] == "missing_evidence_inconclusive"
        ),
        "rejected": sum(
            1 for result in results if result["readiness_status"] == "rejected"
        ),
        "results": deepcopy(results),
        "watch_only": True,
        "no_trade_decision": True,
        "accepted_proof": False,
    }


def _extract_packet(candidate_summary: Mapping[str, Any]) -> Mapping[str, Any] | None:
    packet = candidate_summary.get("packet")
    if isinstance(packet, Mapping):
        return packet
    if packet is None and any(field in candidate_summary for field in ("template_status", "unavailable_status")):
        return None
    if packet is None and "ready_for_acceptance_review" in candidate_summary:
        return None
    if "candidate_id" in candidate_summary and "source_row_reference" in candidate_summary:
        return candidate_summary
    return None


def _candidate_id(
    candidate_summary: Mapping[str, Any],
    packet: Mapping[str, Any] | None,
) -> str | None:
    value = packet.get("candidate_id") if packet is not None else candidate_summary.get("candidate_id")
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _identity_value(
    candidate_summary: Mapping[str, Any],
    packet: Mapping[str, Any] | None,
    field_name: str,
    expected: tuple[str, str] | None,
    expected_index: int,
) -> Any:
    if packet is not None and field_name in packet:
        return deepcopy(packet[field_name])
    if field_name in candidate_summary:
        return deepcopy(candidate_summary[field_name])
    if expected is not None:
        return expected[expected_index]
    return None


def _unavailable_missing_evidence(candidate_summary: Mapping[str, Any]) -> list[str]:
    supplied = candidate_summary.get("missing_evidence")
    if isinstance(supplied, list) and supplied:
        return deepcopy(supplied)

    missing = [
        "source row packet",
        "setup-time source row",
        "after-setup outcome window",
    ]
    missing.extend(_missing_summary_family(candidate_summary, _TRIGGER_FIELDS, "trigger evidence"))
    missing.extend(_missing_summary_family(candidate_summary, _INVALIDATION_FIELDS, "invalidation evidence"))
    missing.extend(_missing_summary_family(candidate_summary, _FRESHNESS_FIELDS, "freshness/final-signal evidence"))
    return list(dict.fromkeys(missing))


def _missing_summary_family(
    candidate_summary: Mapping[str, Any],
    field_names: tuple[str, ...],
    label: str,
) -> list[str]:
    if any(candidate_summary.get(field_name) for field_name in field_names):
        return []
    return [label]


def _validation_missing_evidence(validation: Mapping[str, Any]) -> list[Any]:
    missing = []
    missing.extend(deepcopy(validation.get("missing_fields", [])))
    if validation.get("invalid_ohlcv_fields"):
        missing.append({"invalid_setup_time_ohlcv": deepcopy(validation["invalid_ohlcv_fields"])})
    if validation.get("timeline_errors"):
        missing.append({"timeline_errors": deepcopy(validation["timeline_errors"])})
    if validation.get("forbidden_paths"):
        missing.append({"forbidden_paths": deepcopy(validation["forbidden_paths"])})
    return missing


def _summary_evidence_used(candidate_summary: Mapping[str, Any]) -> list[Any]:
    evidence = []
    for field_name in ("template_status", "unavailable_status", "source_file_reference", "source_row_reference"):
        if candidate_summary.get(field_name):
            evidence.append({field_name: deepcopy(candidate_summary[field_name])})
    return evidence


def _packet_evidence_used(packet: Mapping[str, Any]) -> list[dict[str, Any]]:
    evidence_fields = (
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
        "after_setup_outcome_window_start",
        "after_setup_outcome_window_end",
    )
    return [
        {field_name: deepcopy(packet[field_name])}
        for field_name in evidence_fields
        if field_name in packet and packet[field_name] not in (None, "", [])
    ]


def _setup_appeared(packet: Mapping[str, Any], validation: Mapping[str, Any]) -> str:
    if validation["ready_for_acceptance_review"]:
        return "setup-time candidate row present"
    if validation.get("missing_fields"):
        return "missing_evidence_inconclusive"
    return str(packet.get("setup_appeared", "not accepted"))


def _what_happened_after(packet: Mapping[str, Any], validation: Mapping[str, Any]) -> str:
    if validation["ready_for_acceptance_review"]:
        return (
            "after-setup outcome window supplied from "
            f"{packet.get('after_setup_outcome_window_start')} to "
            f"{packet.get('after_setup_outcome_window_end')}"
        )
    return "after-setup outcome remains inconclusive until packet evidence is valid"


def _result(
    *,
    candidate_id: Any,
    symbol: Any,
    setup_type: Any,
    readiness_status: str,
    setup_appeared: Any,
    what_happened_after: Any,
    evidence_used: list[Any],
    missing_evidence: list[Any],
    diagnosis: str,
    likely_cause_candidate: str,
    next_fix_path: str,
    regression_needed: str,
    lower_tier_handoff_summary: str,
    validation: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    result = {
        "candidate_id": candidate_id,
        "symbol": symbol,
        "setup_type": setup_type,
        "readiness_status": readiness_status,
        "setup_appeared": setup_appeared,
        "what_happened_after": what_happened_after,
        "evidence_used": deepcopy(evidence_used),
        "missing_evidence": deepcopy(missing_evidence),
        "diagnosis": diagnosis,
        "likely_cause_candidate": likely_cause_candidate,
        "next_fix_path": next_fix_path,
        "regression_needed": regression_needed,
        "lower_tier_handoff_summary": lower_tier_handoff_summary,
        "watch_only": True,
        "no_trade_decision": True,
        "accepted_proof": False,
    }
    if validation is not None:
        result["validation"] = deepcopy(dict(validation))
    return result
