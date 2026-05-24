"""Focus ranking for local watch-only watcher candidates.

This module ranks caller-provided watcher state/card dictionaries only. It does
not fetch live data, run watcher loops, emit alerts, create runtime schema
files, write logs, or integrate with broker/account/order/option systems.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, is_dataclass
from typing import Any, Mapping, Sequence

from watcher_foundation.constants import (
    DISTANCE_TO_TRIGGER_UNCONFIRMED,
    EVIDENCE_ROWS_UNCONFIRMED,
    FRESHNESS_UNCONFIRMED,
    INVALIDATION_UNCONFIRMED,
    NEWS_UNCONFIRMED,
    SESSION_DATE_UNCONFIRMED,
    SOURCE_AS_OF_UNCONFIRMED,
    TRIGGER_LEVEL_UNCONFIRMED,
)
from watcher_foundation.models import reject_forbidden_execution_fields


FOCUS_RANK_BUCKETS = (
    "primary_focus",
    "secondary_watch",
    "watch_only_blocked",
    "stale_spent_context",
    "unavailable_unconfirmed",
)

CRITICAL_FOCUS_FIELDS = (
    "trigger_level_or_zone",
    "distance_to_trigger",
    "invalidation_level_or_condition",
    "source_as_of",
    "evidence_rows",
    "regular_session_date",
    "fresh_stale_spent_state",
)

UNCONFIRMED_VALUES = frozenset(
    {
        "",
        None,
        "UNCONFIRMED",
        TRIGGER_LEVEL_UNCONFIRMED,
        DISTANCE_TO_TRIGGER_UNCONFIRMED,
        INVALIDATION_UNCONFIRMED,
        SOURCE_AS_OF_UNCONFIRMED,
        EVIDENCE_ROWS_UNCONFIRMED,
        SESSION_DATE_UNCONFIRMED,
        FRESHNESS_UNCONFIRMED,
        NEWS_UNCONFIRMED,
        "unconfirmed",
    }
)


def rank_focus_candidates(
    candidates: Sequence[Mapping[str, Any] | Any],
    *,
    previous_primary_focus_candidate_id: str | None = None,
) -> dict[str, Any]:
    """Return a deterministic plain dict focus-ranking result."""

    normalized = [_normalize_candidate(candidate) for candidate in candidates]
    ranked = [_ranked_candidate(candidate) for candidate in normalized]
    ranked.sort(key=lambda candidate: candidate["focus_rank_score"])

    primary_focus_candidate_id = None
    for candidate in ranked:
        if candidate["focus_rank_bucket"] == "secondary_watch":
            candidate["focus_rank_bucket"] = "primary_focus"
            candidate["focus_rank_reason"] = _reason_text(candidate)
            primary_focus_candidate_id = candidate["candidate_id"]
            break

    best_candidate_changed = (
        previous_primary_focus_candidate_id is not None
        and previous_primary_focus_candidate_id != primary_focus_candidate_id
    )
    demotion_reason_codes: dict[str, list[str]] = {
        candidate["candidate_id"]: list(candidate["demotion_reason_codes"])
        for candidate in ranked
    }

    result = {
        "watch_only": True,
        "primary_focus_candidate_id": primary_focus_candidate_id,
        "best_candidate_changed": best_candidate_changed,
        "ranked_candidates": ranked,
        "demotion_reason_codes": demotion_reason_codes,
        "focus_rank_buckets": FOCUS_RANK_BUCKETS,
    }
    reject_forbidden_execution_fields(result)
    return result


def _normalize_candidate(candidate: Mapping[str, Any] | Any) -> dict[str, Any]:
    source = _to_plain_dict(candidate)
    reject_forbidden_execution_fields(source)
    _reject_watch_only_false(source)

    normalized = deepcopy(source)
    normalized["watch_only"] = True
    normalized["candidate_id"] = str(
        normalized.get("candidate_id")
        or normalized.get("deterministic_tie_breaker")
        or normalized.get("symbol")
        or "UNCONFIRMED"
    )
    normalized["setup_type"] = normalized.get("setup_type", "UNCONFIRMED")
    normalized["stage"] = normalized.get("stage", "unavailable/unconfirmed")
    normalized["trigger_status"] = normalized.get("trigger_status", "unconfirmed")
    normalized["fresh_stale_spent_state"] = normalized.get(
        "fresh_stale_spent_state",
        normalized.get("freshness_state", "unconfirmed"),
    )
    if normalized["fresh_stale_spent_state"] == FRESHNESS_UNCONFIRMED:
        normalized["fresh_stale_spent_state"] = "unconfirmed"
    normalized["trigger_level_or_zone"] = normalized.get(
        "trigger_level_or_zone",
        normalized.get("trigger_level", TRIGGER_LEVEL_UNCONFIRMED),
    )
    normalized["distance_to_trigger"] = normalized.get(
        "distance_to_trigger", DISTANCE_TO_TRIGGER_UNCONFIRMED
    )
    normalized["invalidation_level_or_condition"] = normalized.get(
        "invalidation_level_or_condition",
        normalized.get("invalidation", INVALIDATION_UNCONFIRMED),
    )
    normalized["source_as_of"] = normalized.get(
        "source_as_of", SOURCE_AS_OF_UNCONFIRMED
    )
    normalized["regular_session_date"] = normalized.get(
        "regular_session_date", normalized.get("session_date", SESSION_DATE_UNCONFIRMED)
    )
    normalized["evidence_rows"] = _as_list(
        normalized.get("evidence_rows", (EVIDENCE_ROWS_UNCONFIRMED,))
    )
    normalized["unavailable_fields"] = _as_list(
        normalized.get("unavailable_fields", ())
    )
    normalized["blockers"] = _as_list(normalized.get("blockers", ()))
    normalized["cautions"] = _as_list(normalized.get("cautions", ()))
    normalized["headline_news_status"] = (
        normalized.get("headline_news_status") or NEWS_UNCONFIRMED
    )
    normalized["evidence_quality"] = normalized.get(
        "evidence_quality", "unconfirmed"
    )
    return normalized


def _ranked_candidate(source: Mapping[str, Any]) -> dict[str, Any]:
    critical_unavailable = _critical_unavailable_fields(source)
    blocker_severity = _blocker_severity(source)
    caution_severity = _caution_severity(source)
    evidence_rank = _evidence_rank(source.get("evidence_quality"))
    unavailable_count = len(_as_list(source.get("unavailable_fields", ())))
    proximity_rank = _proximity_rank(source.get("distance_to_trigger"))
    stale_spent = _is_stale_spent(source)

    reason_codes: list[str] = []
    if blocker_severity >= 3:
        reason_codes.append("blocked_or_source_confirmed_news_block")
    if stale_spent:
        reason_codes.append("stale_spent_or_no_fresh_trigger")
    if critical_unavailable:
        reason_codes.append("critical_fields_unavailable")
    if evidence_rank >= 2:
        reason_codes.append("evidence_quality_poor")

    if blocker_severity >= 3:
        bucket = "watch_only_blocked"
    elif stale_spent:
        bucket = "stale_spent_context"
    elif critical_unavailable or evidence_rank >= 2:
        bucket = "unavailable_unconfirmed"
    else:
        bucket = "secondary_watch"

    rank_bucket_order = {
        "secondary_watch": 0,
        "watch_only_blocked": 1,
        "stale_spent_context": 2,
        "unavailable_unconfirmed": 3,
    }
    rank_tuple = (
        rank_bucket_order[bucket],
        0 if _is_current_lifecycle(source) else 1,
        _freshness_rank(source.get("fresh_stale_spent_state")),
        blocker_severity,
        caution_severity,
        evidence_rank,
        len(critical_unavailable),
        unavailable_count,
        proximity_rank,
        str(source.get("candidate_id", "UNCONFIRMED")),
    )

    ranked = deepcopy(dict(source))
    ranked.update(
        {
            "focus_rank_bucket": bucket,
            "focus_rank_reason": "",
            "focus_rank_score": rank_tuple,
            "demotion_reason_codes": reason_codes,
            "critical_unavailable_fields": critical_unavailable,
            "blocker_severity": blocker_severity,
            "caution_severity": caution_severity,
            "trigger_proximity_rank": proximity_rank,
            "watch_only": True,
        }
    )
    ranked["focus_rank_reason"] = _reason_text(ranked)
    return ranked


def _reason_text(candidate: Mapping[str, Any]) -> str:
    bucket = candidate["focus_rank_bucket"]
    codes = candidate.get("demotion_reason_codes") or []
    if bucket == "primary_focus":
        return "cleanest_current_candidate_after_no_trade_discipline"
    if bucket == "secondary_watch":
        return "current_watch_candidate_below_primary_focus"
    return ";".join(str(code) for code in codes) or bucket


def _to_plain_dict(value: Mapping[str, Any] | Any) -> dict[str, Any]:
    if hasattr(value, "to_dict"):
        return deepcopy(value.to_dict())
    if is_dataclass(value):
        return deepcopy(asdict(value))
    if isinstance(value, Mapping):
        return deepcopy(dict(value))
    raise TypeError("focus ranking candidates must be mappings or dict-like artifacts")


def _reject_watch_only_false(value: Any, path: tuple[str, ...] = ()) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            if key_text == "watch_only" and nested_value is not True:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Focus ranking must preserve watch_only=True: {dotted_path}")
            _reject_watch_only_false(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_watch_only_false(nested_value, (*path, str(index)))


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return deepcopy(value)
    if isinstance(value, tuple):
        return [deepcopy(item) for item in value]
    if isinstance(value, set):
        return sorted(deepcopy(value))
    return [deepcopy(value)]


def _is_unconfirmed(value: Any) -> bool:
    if isinstance(value, (list, tuple, set)):
        return not value or all(_is_unconfirmed(item) for item in value)
    if value in UNCONFIRMED_VALUES:
        return True
    if isinstance(value, str):
        return value.endswith("_UNCONFIRMED")
    return False


def _critical_unavailable_fields(source: Mapping[str, Any]) -> list[str]:
    unavailable = {str(field) for field in _as_list(source.get("unavailable_fields", ()))}
    missing: list[str] = []
    for field_name in CRITICAL_FOCUS_FIELDS:
        value = source.get(field_name)
        if field_name in unavailable or _is_unconfirmed(value):
            missing.append(field_name)
    return missing


def _blocker_severity(source: Mapping[str, Any]) -> int:
    severity = _max_severity(source.get("blockers", ()))
    if source.get("stage") == "blocked/no-trade":
        severity = max(severity, 3)
    if _source_confirmed_news_block(source):
        severity = max(severity, 3)
    return severity


def _caution_severity(source: Mapping[str, Any]) -> int:
    severity = _max_severity(source.get("cautions", ()))
    if _source_confirmed_news_caution(source):
        severity = max(severity, 1)
    return severity


def _max_severity(items: Any) -> int:
    severity = 0
    for item in _as_list(items):
        if isinstance(item, Mapping):
            value = str(item.get("severity", item.get("level", ""))).lower()
        else:
            value = str(item).lower()
        if value in {"block", "blocked", "hard_block", "news_block"}:
            severity = max(severity, 3)
        elif value in {"warning", "warn", "caution", "medium"}:
            severity = max(severity, 1)
        elif value and "block" in value:
            severity = max(severity, 3)
        elif value:
            severity = max(severity, 1)
    return severity


def _source_confirmed_news_block(source: Mapping[str, Any]) -> bool:
    return (
        source.get("headline_news_status") == "NEWS_BLOCK"
        and _source_confirmed_news(source)
    )


def _source_confirmed_news_caution(source: Mapping[str, Any]) -> bool:
    return (
        source.get("headline_news_status") == "NEWS_CAUTION"
        and _source_confirmed_news(source)
    )


def _source_confirmed_news(source: Mapping[str, Any]) -> bool:
    if source.get("headline_news_source_confirmed") is True:
        return True
    status = str(source.get("headline_news_source_status", "")).lower()
    return status in {"source_confirmed", "confirmed", "valid_source_confirmed"}


def _is_stale_spent(source: Mapping[str, Any]) -> bool:
    freshness = source.get("fresh_stale_spent_state")
    stale = (
        source.get("stage") == "stale/spent/no-fresh-trigger"
        or source.get("trigger_status") in {"stale", "spent", "no_valid_trigger"}
        or freshness in {"stale", "spent", "prior-session"}
    )
    accepted_fresh_path = (
        source.get("fresh_trigger_path_present") is True
        and freshness in {"fresh", "rebuilding"}
        and source.get("trigger_status") not in {"stale", "spent", "no_valid_trigger"}
    )
    return stale and not accepted_fresh_path


def _is_current_lifecycle(source: Mapping[str, Any]) -> bool:
    return source.get("stage") in {
        "forming/developing",
        "near-trigger",
        "pending_completed_candle_approval",
        "triggered_signal_stage",
        "rebuilding",
    }


def _freshness_rank(value: Any) -> int:
    return {
        "fresh": 0,
        "rebuilding": 1,
        "unconfirmed": 2,
        "prior-session": 3,
        "stale": 4,
        "spent": 5,
    }.get(str(value), 2)


def _evidence_rank(value: Any) -> int:
    return {
        "deterministic": 0,
        "partial": 1,
        "unconfirmed": 2,
        "missing": 3,
    }.get(str(value), 2)


def _proximity_rank(value: Any) -> int:
    if _is_unconfirmed(value):
        return 99
    if isinstance(value, (int, float)):
        return abs(float(value))
    text = str(value).lower()
    if text in {"at_trigger", "touching", "near", "near_trigger", "close"}:
        return 0
    if text in {"medium", "moderate"}:
        return 1
    if text in {"far", "not_near"}:
        return 2
    try:
        return abs(float(text.strip().rstrip("%")))
    except ValueError:
        return 50
