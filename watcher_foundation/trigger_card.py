"""Trigger-card projection for local watch-only watcher state.

This module projects caller-provided watcher foundation state into an inert
plain dict review artifact. It does not fetch live data, run loops, emit
alerts, create reports, or integrate with broker/account/order/option systems.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, is_dataclass
from typing import Any, Mapping

from watcher_foundation.constants import (
    CONFIRMATION_TIMEFRAME_RULE_UNCONFIRMED,
    DISTANCE_TO_TRIGGER_UNCONFIRMED,
    EVIDENCE_ROWS_UNCONFIRMED,
    INVALIDATION_UNCONFIRMED,
    NEWS_UNCONFIRMED,
    SOURCE_AS_OF_UNCONFIRMED,
    TRIGGER_LEVEL_UNCONFIRMED,
)
from watcher_foundation.models import (
    WatchOnlyCandidateState,
    reject_forbidden_execution_fields,
)
from watcher_foundation.state_tracker import WatcherTrackedState


REQUIRED_TRIGGER_CARD_FIELDS = (
    "symbol",
    "setup_type",
    "direction",
    "stage",
    "trigger_status",
    "trigger_level_or_zone",
    "confirmation_timeframe_rule",
    "distance_to_trigger",
    "invalidation_level_or_condition",
    "fresh_stale_spent_state",
    "next_check_or_next_alert_condition",
    "blockers",
    "cautions",
    "unavailable_fields",
    "source_as_of",
    "evidence_rows",
    "headline_news_status",
    "diagnostic_reason_codes",
    "no_trade_reason",
    "duplicate_suppression_key_fields",
    "best_candidate_ranking_inputs",
    "watch_only",
)

CRITICAL_TRIGGER_CARD_FIELDS = (
    "trigger_level_or_zone",
    "confirmation_timeframe_rule",
    "distance_to_trigger",
    "invalidation_level_or_condition",
    "fresh_stale_spent_state",
    "source_as_of",
    "evidence_rows",
)

UNCONFIRMED_VALUES = frozenset(
    {
        "",
        None,
        "UNCONFIRMED",
        TRIGGER_LEVEL_UNCONFIRMED,
        CONFIRMATION_TIMEFRAME_RULE_UNCONFIRMED,
        DISTANCE_TO_TRIGGER_UNCONFIRMED,
        INVALIDATION_UNCONFIRMED,
        SOURCE_AS_OF_UNCONFIRMED,
        EVIDENCE_ROWS_UNCONFIRMED,
        NEWS_UNCONFIRMED,
        "FRESHNESS_UNCONFIRMED",
        "unconfirmed",
    }
)


def project_trigger_card(
    state: WatcherTrackedState | WatchOnlyCandidateState | Mapping[str, Any],
) -> dict[str, Any]:
    """Return a plain dict trigger-card projection from watch-only state."""

    source = _normalize_source(state)
    reject_forbidden_execution_fields(source)

    if source.get("watch_only") is False:
        raise ValueError("Trigger-card projection must preserve watch_only=True")

    card = {
        "symbol": source.get("symbol", "UNCONFIRMED"),
        "setup_type": source.get("setup_type", "UNCONFIRMED"),
        "direction": source.get("direction", "UNCONFIRMED"),
        "stage": source.get("stage", "unavailable/unconfirmed"),
        "trigger_status": source.get("trigger_status", "unconfirmed"),
        "trigger_level_or_zone": source.get(
            "trigger_level_or_zone",
            source.get("trigger_level", TRIGGER_LEVEL_UNCONFIRMED),
        ),
        "confirmation_timeframe_rule": source.get(
            "confirmation_timeframe_rule", CONFIRMATION_TIMEFRAME_RULE_UNCONFIRMED
        ),
        "distance_to_trigger": source.get(
            "distance_to_trigger", DISTANCE_TO_TRIGGER_UNCONFIRMED
        ),
        "invalidation_level_or_condition": source.get(
            "invalidation_level_or_condition",
            source.get("invalidation", INVALIDATION_UNCONFIRMED),
        ),
        "fresh_stale_spent_state": source.get(
            "fresh_stale_spent_state",
            source.get("freshness_state", "unconfirmed"),
        ),
        "next_check_or_next_alert_condition": source.get(
            "next_check_or_next_alert_condition", "UNCONFIRMED"
        ),
        "blockers": _as_list(source.get("blockers", ())),
        "cautions": _as_list(source.get("cautions", ())),
        "unavailable_fields": _as_list(source.get("unavailable_fields", ())),
        "source_as_of": source.get("source_as_of", SOURCE_AS_OF_UNCONFIRMED),
        "evidence_rows": _as_list(
            source.get("evidence_rows", (EVIDENCE_ROWS_UNCONFIRMED,))
        ),
        "headline_news_status": source.get("headline_news_status")
        or NEWS_UNCONFIRMED,
        "headline_news_source_status": source.get(
            "headline_news_source_status", "source_unconfirmed"
        ),
        "headline_news_source_confirmed": bool(
            source.get("headline_news_source_confirmed", False)
        ),
        "news_evidence_refs": _as_list(source.get("news_evidence_refs", ())),
        "news_policy_reason_codes": _as_list(
            source.get("news_policy_reason_codes", ())
        ),
        "diagnostic_reason_codes": _diagnostic_reason_codes(source),
        "no_trade_reason": _no_trade_reason(source),
        "duplicate_suppression_key_fields": _duplicate_suppression_key_fields(source),
        "best_candidate_ranking_inputs": _best_candidate_ranking_inputs(source),
        "watch_only": True,
    }

    if "evidence_refs" in source:
        card["evidence_refs"] = _as_list(source["evidence_refs"])
    if "trigger_path_identifier" in source:
        card["trigger_path_identifier"] = source["trigger_path_identifier"]
    if "fresh_trigger_path_present" in source:
        card["fresh_trigger_path_present"] = bool(source["fresh_trigger_path_present"])

    _preserve_no_trade_boundaries(card)
    reject_forbidden_execution_fields(card)
    return card


def _normalize_source(
    state: WatcherTrackedState | WatchOnlyCandidateState | Mapping[str, Any],
) -> dict[str, Any]:
    if isinstance(state, WatcherTrackedState):
        return deepcopy(state.to_dict())
    if isinstance(state, WatchOnlyCandidateState):
        return deepcopy(state.to_dict())
    if isinstance(state, Mapping):
        return deepcopy(dict(state))
    if is_dataclass(state):
        return deepcopy(asdict(state))
    raise TypeError("state must be a watcher state, candidate state, or mapping")


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return deepcopy(value)
    if isinstance(value, tuple):
        return [deepcopy(item) for item in value]
    return [deepcopy(value)]


def _diagnostic_reason_codes(source: Mapping[str, Any]) -> list[Any]:
    if "diagnostic_reason_codes" in source:
        return _as_list(source["diagnostic_reason_codes"])
    if "state_change_reason_codes" in source:
        return _as_list(source["state_change_reason_codes"])
    if "material_change_flags" in source:
        return _as_list(source["material_change_flags"])
    return []


def _no_trade_reason(source: Mapping[str, Any]) -> str:
    reason = str(
        source.get("no_trade_reason")
        or "watch_only_unconfirmed_trigger_invalidation_source_or_evidence_no_trade"
    )
    return reason


def _preserve_no_trade_boundaries(card: dict[str, Any]) -> None:
    reason = card["no_trade_reason"]
    if _has_unavailable_critical_fields(card) and "no_trade" not in reason:
        reason = f"{reason}; no_trade_until_critical_fields_confirmed"

    if card["stage"] == "triggered_signal_stage":
        if "shadow" not in reason.lower():
            reason = f"{reason}; shadow_signal_review_only"
        if "live trade approval" not in reason.lower():
            reason = f"{reason}; no_live_trade_approval"

    stale_or_spent = (
        card["stage"] == "stale/spent/no-fresh-trigger"
        or card["trigger_status"] in {"stale", "spent", "no_valid_trigger"}
        or card["fresh_stale_spent_state"] in {"stale", "spent"}
    )
    if stale_or_spent and "no fresh trigger" not in reason.lower():
        reason = f"{reason}; no fresh trigger; no-trade"

    card["no_trade_reason"] = reason


def _has_unavailable_critical_fields(card: Mapping[str, Any]) -> bool:
    unavailable_fields = set(str(field) for field in card["unavailable_fields"])
    for field_name in CRITICAL_TRIGGER_CARD_FIELDS:
        value = card[field_name]
        if field_name in unavailable_fields or _is_unconfirmed(value):
            return True
    return False


def _is_unconfirmed(value: Any) -> bool:
    if isinstance(value, (list, tuple, set)):
        return not value or all(_is_unconfirmed(item) for item in value)
    if value in UNCONFIRMED_VALUES:
        return True
    if isinstance(value, str):
        return value.endswith("_UNCONFIRMED")
    return False


def _duplicate_suppression_key_fields(source: Mapping[str, Any]) -> dict[str, Any]:
    primary_blocker = source.get("primary_blocker")
    if primary_blocker is None:
        blockers = _as_list(source.get("blockers", ()))
        primary_blocker = blockers[0] if blockers else "PRIMARY_BLOCKER_UNCONFIRMED"

    return {
        "symbol": source.get("symbol", "UNCONFIRMED"),
        "setup_family": source.get("setup_type", "UNCONFIRMED"),
        "direction": source.get("direction", "UNCONFIRMED"),
        "stage": source.get("stage", "unavailable/unconfirmed"),
        "trigger_status": source.get("trigger_status", "unconfirmed"),
        "freshness_state": source.get(
            "fresh_stale_spent_state",
            source.get("freshness_state", "unconfirmed"),
        ),
        "primary_blocker": primary_blocker,
        "trigger_zone_bucket": source.get(
            "trigger_zone_bucket",
            source.get("trigger_level_or_zone", TRIGGER_LEVEL_UNCONFIRMED),
        ),
        "invalidation_bucket": source.get(
            "invalidation_bucket",
            source.get("invalidation_level_or_condition", INVALIDATION_UNCONFIRMED),
        ),
    }


def _best_candidate_ranking_inputs(source: Mapping[str, Any]) -> dict[str, Any]:
    blockers = _as_list(source.get("blockers", ()))
    cautions = _as_list(source.get("cautions", ()))
    return {
        "eligibility_stage": source.get("stage", "unavailable/unconfirmed"),
        "freshness": source.get(
            "fresh_stale_spent_state",
            source.get("freshness_state", "unconfirmed"),
        ),
        "setup_type": source.get("setup_type", "UNCONFIRMED"),
        "trigger_proximity": source.get(
            "distance_to_trigger", DISTANCE_TO_TRIGGER_UNCONFIRMED
        ),
        "blocker_count": len(blockers),
        "caution_count": len(cautions),
        "headline_news_status": source.get("headline_news_status")
        or NEWS_UNCONFIRMED,
        "evidence_quality": source.get("evidence_quality", "unconfirmed"),
        "deterministic_tie_breaker": source.get(
            "candidate_id", source.get("symbol", "UNCONFIRMED")
        ),
    }
