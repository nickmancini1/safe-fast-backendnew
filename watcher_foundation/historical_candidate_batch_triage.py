"""Local in-memory batch triage for historical setup candidates.

No file reads, file writes, live data, network, subprocesses, broker/order/
account/options/P&L, alerts, or trade decisions.
"""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from typing import Any, Mapping, Sequence


ALLOWED_HISTORICAL_CANDIDATE_SYMBOLS = ("SPY", "QQQ", "IWM", "GLD")
ALLOWED_HISTORICAL_CANDIDATE_SETUP_TYPES = ("Ideal", "Clean Fast Break", "Continuation")

HISTORICAL_CANDIDATE_TRIAGE_STATUSES = (
    "ready_for_deeper_review",
    "blocked_missing_evidence",
    "reject_not_clean_enough",
    "unavailable",
    "invalid_input",
)

HISTORICAL_CANDIDATE_BATCH_TRIAGE_RESULT_FIELDS = (
    "total_candidates",
    "status_counts",
    "symbol_counts",
    "setup_type_counts",
    "pair_counts",
    "ready_candidates",
    "blocked_candidates",
    "rejected_candidates",
    "unavailable_candidates",
    "invalid_candidates",
    "missing_evidence_summary",
    "fastest_next_actions",
    "tiny_sample_warning",
    "accepted_proof_count",
    "profitability_claimed",
    "watch_only",
    "no_trade_decision",
)

DEFAULT_MINIMUM_SAMPLE_SIZE = 20

_REQUIRED_READY_FIELDS = (
    "has_setup_time_row",
    "has_trigger",
    "has_invalidation",
    "has_freshness",
    "has_blocker_review",
    "has_no_hindsight_boundary",
    "has_after_setup_outcome_window",
)

_FIELD_MISSING_EVIDENCE_LABELS = {
    "has_setup_time_row": "setup_time_row",
    "has_trigger": "trigger",
    "has_invalidation": "invalidation",
    "has_freshness": "freshness",
    "has_blocker_review": "blocker_review",
    "has_terminal_outcome": "terminal_outcome",
    "has_no_hindsight_boundary": "no_hindsight_boundary",
    "has_after_setup_outcome_window": "after_setup_outcome_window",
}

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

_ALLOWED_SAFETY_KEYS = frozenset({"watch_only", "no_trade_decision", "profitability_claimed", "accepted_proof"})


def triage_historical_candidate_batch(
    candidates: Sequence[Mapping[str, Any]],
    *,
    minimum_sample_size: int = DEFAULT_MINIMUM_SAMPLE_SIZE,
    terminal_outcome_required: bool = True,
) -> dict[str, Any]:
    """Triage caller-provided historical candidates into local review buckets."""

    if not isinstance(candidates, Sequence) or isinstance(candidates, (str, bytes, bytearray)):
        raise TypeError("Historical candidates must be a sequence of mappings")
    if not isinstance(minimum_sample_size, int) or isinstance(minimum_sample_size, bool) or minimum_sample_size < 0:
        raise ValueError("minimum_sample_size must be a non-negative integer")

    triaged_candidates = [
        _triage_candidate(candidate, index, terminal_outcome_required=terminal_outcome_required)
        for index, candidate in enumerate(candidates)
    ]

    status_counts = Counter(candidate["triage_status"] for candidate in triaged_candidates)
    symbol_counts = Counter(
        candidate["symbol"]
        for candidate in triaged_candidates
        if candidate["symbol"] in ALLOWED_HISTORICAL_CANDIDATE_SYMBOLS
    )
    setup_type_counts = Counter(
        candidate["setup_type"]
        for candidate in triaged_candidates
        if candidate["setup_type"] in ALLOWED_HISTORICAL_CANDIDATE_SETUP_TYPES
    )
    pair_counts = Counter(
        f"{candidate['symbol']}|{candidate['setup_type']}"
        for candidate in triaged_candidates
        if candidate["symbol"] in ALLOWED_HISTORICAL_CANDIDATE_SYMBOLS
        and candidate["setup_type"] in ALLOWED_HISTORICAL_CANDIDATE_SETUP_TYPES
    )
    missing_summary = Counter(
        _missing_summary_key(evidence)
        for candidate in triaged_candidates
        for evidence in candidate["missing_evidence"]
    )

    result = {
        "total_candidates": len(triaged_candidates),
        "status_counts": _ordered_counts(status_counts, HISTORICAL_CANDIDATE_TRIAGE_STATUSES),
        "symbol_counts": _ordered_counts(symbol_counts, ALLOWED_HISTORICAL_CANDIDATE_SYMBOLS),
        "setup_type_counts": _ordered_counts(setup_type_counts, ALLOWED_HISTORICAL_CANDIDATE_SETUP_TYPES),
        "pair_counts": dict(sorted(pair_counts.items())),
        "ready_candidates": _candidates_with_status(triaged_candidates, "ready_for_deeper_review"),
        "blocked_candidates": _candidates_with_status(triaged_candidates, "blocked_missing_evidence"),
        "rejected_candidates": _candidates_with_status(triaged_candidates, "reject_not_clean_enough"),
        "unavailable_candidates": _candidates_with_status(triaged_candidates, "unavailable"),
        "invalid_candidates": _candidates_with_status(triaged_candidates, "invalid_input"),
        "missing_evidence_summary": dict(sorted(missing_summary.items())),
        "fastest_next_actions": [
            {
                "candidate_id": candidate["candidate_id"],
                "triage_status": candidate["triage_status"],
                "next_action": candidate["fastest_next_action"],
            }
            for candidate in triaged_candidates
        ],
        "tiny_sample_warning": _tiny_sample_warning(len(triaged_candidates), minimum_sample_size),
        "accepted_proof_count": 0,
        "profitability_claimed": False,
        "watch_only": True,
        "no_trade_decision": True,
    }
    return deepcopy(result)


def _triage_candidate(
    candidate: Mapping[str, Any],
    index: int,
    *,
    terminal_outcome_required: bool,
) -> dict[str, Any]:
    if not isinstance(candidate, Mapping):
        return _candidate_result(
            candidate_id=f"invalid_candidate_{index}",
            symbol=None,
            setup_type=None,
            source_window_id=None,
            row_count=None,
            triage_status="invalid_input",
            evidence_used=[],
            missing_evidence=["candidate_mapping"],
            invalid_reasons=["candidate_is_not_mapping"],
            fastest_next_action="collect missing fields",
        )

    candidate_copy = deepcopy(dict(candidate))
    candidate_id = _present_or_default(candidate_copy.get("candidate_id"), f"candidate_{index}")
    symbol = candidate_copy.get("symbol")
    setup_type = candidate_copy.get("setup_type")
    evidence_used = _list_value(candidate_copy.get("evidence_used"))
    missing_evidence = _list_value(candidate_copy.get("missing_evidence"))
    source_window_id = candidate_copy.get("source_window_id")
    row_count = candidate_copy.get("row_count")

    invalid_reasons: list[str] = []
    forbidden_paths = _walk_forbidden_keys(candidate_copy)
    if forbidden_paths:
        invalid_reasons.append("forbidden_live_broker_order_account_options_or_pnl_fields")
        missing_evidence.append({"forbidden_paths": forbidden_paths})
    if symbol not in ALLOWED_HISTORICAL_CANDIDATE_SYMBOLS:
        invalid_reasons.append("unknown_symbol")
        missing_evidence.append("allowed_symbol")
    if setup_type not in ALLOWED_HISTORICAL_CANDIDATE_SETUP_TYPES:
        invalid_reasons.append("unknown_setup_type")
        missing_evidence.append("allowed_setup_type")

    if invalid_reasons:
        return _candidate_result(
            candidate_id=candidate_id,
            symbol=symbol,
            setup_type=setup_type,
            source_window_id=source_window_id,
            row_count=row_count,
            triage_status="invalid_input",
            evidence_used=evidence_used,
            missing_evidence=missing_evidence,
            invalid_reasons=invalid_reasons,
            fastest_next_action=_invalid_next_action(invalid_reasons),
        )

    requested_status = candidate_copy.get("triage_status", candidate_copy.get("status"))
    if requested_status == "unavailable":
        return _candidate_result(
            candidate_id=candidate_id,
            symbol=symbol,
            setup_type=setup_type,
            source_window_id=source_window_id,
            row_count=row_count,
            triage_status="unavailable",
            evidence_used=evidence_used,
            missing_evidence=missing_evidence or ["candidate_material_unavailable"],
            invalid_reasons=[],
            fastest_next_action="find cleaner replacement",
        )
    if requested_status == "reject_not_clean_enough":
        return _candidate_result(
            candidate_id=candidate_id,
            symbol=symbol,
            setup_type=setup_type,
            source_window_id=source_window_id,
            row_count=row_count,
            triage_status="reject_not_clean_enough",
            evidence_used=evidence_used,
            missing_evidence=missing_evidence,
            invalid_reasons=[],
            fastest_next_action="reject/drop candidate",
        )

    required_fields = list(_REQUIRED_READY_FIELDS)
    if terminal_outcome_required:
        required_fields.append("has_terminal_outcome")
    field_missing = [
        _FIELD_MISSING_EVIDENCE_LABELS[field_name]
        for field_name in required_fields
        if candidate_copy.get(field_name) is not True
    ]
    missing_evidence.extend(label for label in field_missing if label not in missing_evidence)

    if field_missing:
        return _candidate_result(
            candidate_id=candidate_id,
            symbol=symbol,
            setup_type=setup_type,
            source_window_id=source_window_id,
            row_count=row_count,
            triage_status="blocked_missing_evidence",
            evidence_used=evidence_used,
            missing_evidence=missing_evidence,
            invalid_reasons=[],
            fastest_next_action="collect missing fields",
        )

    return _candidate_result(
        candidate_id=candidate_id,
        symbol=symbol,
        setup_type=setup_type,
        source_window_id=source_window_id,
        row_count=row_count,
        triage_status="ready_for_deeper_review",
        evidence_used=evidence_used,
        missing_evidence=[],
        invalid_reasons=[],
        fastest_next_action="move to deeper review",
    )


def _candidate_result(
    *,
    candidate_id: Any,
    symbol: Any,
    setup_type: Any,
    source_window_id: Any,
    row_count: Any,
    triage_status: str,
    evidence_used: Sequence[Any],
    missing_evidence: Sequence[Any],
    invalid_reasons: Sequence[str],
    fastest_next_action: str,
) -> dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "symbol": symbol,
        "setup_type": setup_type,
        "source_window_id": source_window_id,
        "row_count": row_count,
        "triage_status": triage_status,
        "evidence_used": deepcopy(list(evidence_used)),
        "missing_evidence": deepcopy(list(missing_evidence)),
        "invalid_reasons": list(invalid_reasons),
        "fastest_next_action": fastest_next_action,
        "accepted_proof": False,
        "profitability_claimed": False,
        "watch_only": True,
        "no_trade_decision": True,
    }


def _candidates_with_status(candidates: Sequence[Mapping[str, Any]], status: str) -> list[dict[str, Any]]:
    return [deepcopy(dict(candidate)) for candidate in candidates if candidate["triage_status"] == status]


def _ordered_counts(counts: Counter, ordered_keys: Sequence[str]) -> dict[str, int]:
    result = {key: counts.get(key, 0) for key in ordered_keys}
    for key in sorted(set(counts) - set(ordered_keys)):
        result[key] = counts[key]
    return result


def _tiny_sample_warning(total_candidates: int, minimum_sample_size: int) -> str | None:
    if total_candidates < minimum_sample_size:
        return f"tiny_sample_risk: total_candidates {total_candidates} below minimum_sample_size {minimum_sample_size}"
    return None


def _invalid_next_action(invalid_reasons: Sequence[str]) -> str:
    if "forbidden_live_broker_order_account_options_or_pnl_fields" in invalid_reasons:
        return "reject/drop candidate"
    return "collect missing fields"


def _list_value(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return deepcopy(value)
    if isinstance(value, tuple):
        return deepcopy(list(value))
    return [deepcopy(value)]


def _missing_summary_key(value: Any) -> str:
    if isinstance(value, Mapping) and "forbidden_paths" in value:
        return "forbidden_paths"
    return str(value)


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


def _present_or_default(value: Any, default: str) -> Any:
    if value is None:
        return default
    if isinstance(value, str) and not value.strip():
        return default
    return deepcopy(value)
