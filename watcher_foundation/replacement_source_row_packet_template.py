"""SAFE-FAST replacement source row packet template builder.

Pure local/in-memory helper only.
No live data, no broker/order/account/options/P&L, no alerts, no file writes.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from .replacement_source_row_packet import (
    ALLOWED_CANDIDATES,
    REQUIRED_FIELDS,
    validate_replacement_source_row_packet,
    validate_replacement_source_row_packet_batch,
)


PLACEHOLDER = "TO_COLLECT"


def build_replacement_source_row_packet_template(candidate_id: str) -> dict[str, Any]:
    """Build one incomplete packet template for a known replacement candidate."""

    expected = ALLOWED_CANDIDATES.get(candidate_id)
    if expected is None:
        return {
            "candidate_id": candidate_id,
            "template_status": "unknown_candidate_id",
            "ready_for_acceptance_review": False,
            "decision": "missing_evidence_inconclusive",
            "missing_fields": list(REQUIRED_FIELDS),
            "watch_only": True,
            "no_trade_decision": True,
        }

    symbol, setup_type = expected

    packet: dict[str, Any] = {
        "candidate_id": candidate_id,
        "symbol": symbol,
        "setup_type": setup_type,
        "timeframe": "1h_rth",
        "source_file_reference": PLACEHOLDER,
        "source_row_reference": PLACEHOLDER,
        "source_window_start": PLACEHOLDER,
        "source_window_end": PLACEHOLDER,
        "setup_time_candidate_row_timestamp": PLACEHOLDER,
        "setup_time_candidate_row_ohlcv": {
            "open": None,
            "high": None,
            "low": None,
            "close": None,
            "volume": None,
        },
        "trigger_candidate": None,
        "trigger_basis": PLACEHOLDER,
        "invalidation_candidate": None,
        "invalidation_basis": PLACEHOLDER,
        "freshness_final_signal_candidate": PLACEHOLDER,
        "blocker_caution_status": PLACEHOLDER,
        "unavailable_fields": ["TO_COLLECT"],
        "no_hindsight_boundary": "setup-time row must be selected before terminal outcome review",
        "after_setup_outcome_window_start": PLACEHOLDER,
        "after_setup_outcome_window_end": PLACEHOLDER,
    }

    validation = validate_replacement_source_row_packet(packet)

    return {
        "template_status": "source_rows_required",
        "packet": packet,
        "validation": validation,
        "ready_for_acceptance_review": validation["ready_for_acceptance_review"],
        "decision": validation["decision"],
        "missing_fields": validation["missing_fields"],
        "watch_only": True,
        "no_trade_decision": True,
    }


def build_all_replacement_source_row_packet_templates() -> dict[str, Any]:
    """Build incomplete templates for all replacement candidates."""

    templates = [
        build_replacement_source_row_packet_template(candidate_id)
        for candidate_id in sorted(ALLOWED_CANDIDATES)
    ]

    packet_inputs = [
        deepcopy(template["packet"])
        for template in templates
        if "packet" in template
    ]
    batch_validation = validate_replacement_source_row_packet_batch(packet_inputs)

    return {
        "template_count": len(templates),
        "templates": templates,
        "batch_validation": batch_validation,
        "ready_for_acceptance_review": batch_validation["ready_for_acceptance_review"],
        "missing_evidence_or_rejected": batch_validation["missing_evidence_or_rejected"],
        "watch_only": True,
        "no_trade_decision": True,
    }


def classify_source_row_packet(candidate_packet: Mapping[str, Any]) -> dict[str, Any]:
    """Classify one caller-provided packet without mutating it."""

    validation = validate_replacement_source_row_packet(candidate_packet)
    if validation["ready_for_acceptance_review"]:
        classification = "ready_for_acceptance_review"
    elif validation["rejected_reasons"]:
        classification = "missing_evidence_inconclusive"
    else:
        classification = "missing_evidence_inconclusive"

    return {
        "candidate_id": validation["candidate_id"],
        "classification": classification,
        "validation": validation,
        "watch_only": True,
        "no_trade_decision": True,
        "input_copy": deepcopy(dict(candidate_packet)),
    }
