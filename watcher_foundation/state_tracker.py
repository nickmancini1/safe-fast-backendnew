"""Local watch-only watcher state tracking.

This module updates inert watcher state from caller-provided observations only.
It does not fetch live data, run loops, emit alerts, or integrate with broker,
account, order, option, deployment, or production systems.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from watcher_foundation.constants import (
    ACCEPTED_DIRECTIONS,
    ACCEPTED_EVIDENCE_QUALITIES,
    ACCEPTED_FRESH_STALE_SPENT_STATES,
    ACCEPTED_HEADLINE_NEWS_STATUSES,
    ACCEPTED_MATERIAL_CHANGE_FLAGS,
    ACCEPTED_SETUP_TYPES,
    ACCEPTED_STAGES,
    ACCEPTED_TRIGGER_STATUSES,
    CONFIRMATION_TIMEFRAME_RULE_UNCONFIRMED,
    DEFAULT_UNAVAILABLE_FIELDS,
    DISTANCE_TO_TRIGGER_UNCONFIRMED,
    EVIDENCE_ROWS_UNCONFIRMED,
    FRESHNESS_UNCONFIRMED,
    INVALIDATION_BUCKET_UNCONFIRMED,
    INVALIDATION_UNCONFIRMED,
    NEWS_UNCONFIRMED,
    PRIMARY_BLOCKER_UNCONFIRMED,
    SESSION_DATE_UNCONFIRMED,
    SOURCE_AS_OF_UNCONFIRMED,
    SOURCE_KIND_UNCONFIRMED,
    TRIGGER_LEVEL_UNCONFIRMED,
    TRIGGER_ZONE_UNCONFIRMED,
)
from watcher_foundation.models import (
    WatchOnlyCandidateState,
    reject_forbidden_execution_fields,
)


CRITICAL_AVAILABILITY_FIELDS = (
    "trigger_level_or_zone",
    "distance_to_trigger",
    "invalidation_level_or_condition",
    "source_as_of",
    "evidence_rows",
    "fresh_stale_spent_state",
    "regular_session_date",
)

UNCONFIRMED_VALUES = frozenset(
    {
        "UNCONFIRMED",
        TRIGGER_LEVEL_UNCONFIRMED,
        DISTANCE_TO_TRIGGER_UNCONFIRMED,
        INVALIDATION_UNCONFIRMED,
        SOURCE_AS_OF_UNCONFIRMED,
        EVIDENCE_ROWS_UNCONFIRMED,
        SESSION_DATE_UNCONFIRMED,
        FRESHNESS_UNCONFIRMED,
        NEWS_UNCONFIRMED,
        PRIMARY_BLOCKER_UNCONFIRMED,
        CONFIRMATION_TIMEFRAME_RULE_UNCONFIRMED,
        SOURCE_KIND_UNCONFIRMED,
    }
)


@dataclass(frozen=True)
class WatcherTrackedState:
    """Normalized state for one local watch-only watcher candidate."""

    candidate_id: str = "UNCONFIRMED"
    symbol: str = "UNCONFIRMED"
    watch_session_id: str = "UNCONFIRMED"
    setup_type: str = "UNCONFIRMED"
    direction: str = "UNCONFIRMED"
    regular_session_date: str = SESSION_DATE_UNCONFIRMED
    first_seen_at: str = "UNCONFIRMED"
    last_seen_at: str = "UNCONFIRMED"
    state_version: int = 1
    stage: str = "unavailable/unconfirmed"
    trigger_status: str = "unconfirmed"
    fresh_stale_spent_state: str = "unconfirmed"
    previous_stage: str = "unavailable/unconfirmed"
    previous_trigger_status: str = "unconfirmed"
    previous_fresh_stale_spent_state: str = "unconfirmed"
    trigger_level_or_zone: str = TRIGGER_LEVEL_UNCONFIRMED
    trigger_zone_bucket: str = TRIGGER_ZONE_UNCONFIRMED
    confirmation_timeframe_rule: str = CONFIRMATION_TIMEFRAME_RULE_UNCONFIRMED
    distance_to_trigger: str = DISTANCE_TO_TRIGGER_UNCONFIRMED
    invalidation_level_or_condition: str = INVALIDATION_UNCONFIRMED
    invalidation_bucket: str = INVALIDATION_BUCKET_UNCONFIRMED
    source_kind: str = SOURCE_KIND_UNCONFIRMED
    source_as_of: str = SOURCE_AS_OF_UNCONFIRMED
    evidence_rows: tuple[str, ...] = (EVIDENCE_ROWS_UNCONFIRMED,)
    evidence_quality: str = "unconfirmed"
    unavailable_fields: tuple[str, ...] = field(
        default_factory=lambda: DEFAULT_UNAVAILABLE_FIELDS
    )
    blockers: tuple[str, ...] = ()
    cautions: tuple[str, ...] = ()
    primary_blocker: str = PRIMARY_BLOCKER_UNCONFIRMED
    headline_news_status: str = NEWS_UNCONFIRMED
    no_trade_reason: str = (
        "watch_only_unconfirmed_trigger_invalidation_source_or_evidence"
    )
    watch_only: bool = True
    state_changed: bool = False
    state_change_reason_codes: tuple[str, ...] = ("no_material_change",)
    material_change_flags: tuple[str, ...] = ("no_material_change",)
    next_check_or_next_alert_condition: str = "UNCONFIRMED"
    trigger_path_identifier: str = "UNCONFIRMED"
    fresh_trigger_path_present: bool = False
    repeat_count: int = 0

    def __post_init__(self) -> None:
        if self.setup_type not in ACCEPTED_SETUP_TYPES:
            raise ValueError(f"Unsupported setup_type: {self.setup_type}")
        if self.direction not in ACCEPTED_DIRECTIONS:
            raise ValueError(f"Unsupported direction: {self.direction}")
        if self.stage not in ACCEPTED_STAGES:
            raise ValueError(f"Unsupported stage: {self.stage}")
        if self.trigger_status not in ACCEPTED_TRIGGER_STATUSES:
            raise ValueError(f"Unsupported trigger_status: {self.trigger_status}")
        if self.fresh_stale_spent_state not in ACCEPTED_FRESH_STALE_SPENT_STATES:
            raise ValueError(
                "Unsupported fresh_stale_spent_state: "
                f"{self.fresh_stale_spent_state}"
            )
        if self.evidence_quality not in ACCEPTED_EVIDENCE_QUALITIES:
            raise ValueError(f"Unsupported evidence_quality: {self.evidence_quality}")
        if self.headline_news_status not in ACCEPTED_HEADLINE_NEWS_STATUSES:
            raise ValueError(
                f"Unsupported headline_news_status: {self.headline_news_status}"
            )
        for flag in self.material_change_flags:
            if flag not in ACCEPTED_MATERIAL_CHANGE_FLAGS:
                raise ValueError(f"Unsupported material_change_flag: {flag}")
        if self.watch_only is not True:
            raise ValueError("Watcher tracked state must remain watch_only=True")
        reject_forbidden_execution_fields(self.to_dict(validate=False))

    def to_dict(self, *, validate: bool = True) -> dict[str, Any]:
        output = {
            "candidate_id": self.candidate_id,
            "symbol": self.symbol,
            "watch_session_id": self.watch_session_id,
            "setup_type": self.setup_type,
            "direction": self.direction,
            "regular_session_date": self.regular_session_date,
            "first_seen_at": self.first_seen_at,
            "last_seen_at": self.last_seen_at,
            "state_version": self.state_version,
            "stage": self.stage,
            "trigger_status": self.trigger_status,
            "fresh_stale_spent_state": self.fresh_stale_spent_state,
            "previous_stage": self.previous_stage,
            "previous_trigger_status": self.previous_trigger_status,
            "previous_fresh_stale_spent_state": (
                self.previous_fresh_stale_spent_state
            ),
            "trigger_level_or_zone": self.trigger_level_or_zone,
            "trigger_zone_bucket": self.trigger_zone_bucket,
            "confirmation_timeframe_rule": self.confirmation_timeframe_rule,
            "distance_to_trigger": self.distance_to_trigger,
            "invalidation_level_or_condition": (
                self.invalidation_level_or_condition
            ),
            "invalidation_bucket": self.invalidation_bucket,
            "source_kind": self.source_kind,
            "source_as_of": self.source_as_of,
            "evidence_rows": list(self.evidence_rows),
            "evidence_quality": self.evidence_quality,
            "unavailable_fields": list(self.unavailable_fields),
            "blockers": list(self.blockers),
            "cautions": list(self.cautions),
            "primary_blocker": self.primary_blocker,
            "headline_news_status": self.headline_news_status,
            "no_trade_reason": self.no_trade_reason,
            "watch_only": self.watch_only,
            "state_changed": self.state_changed,
            "state_change_reason_codes": list(self.state_change_reason_codes),
            "material_change_flags": list(self.material_change_flags),
            "next_check_or_next_alert_condition": (
                self.next_check_or_next_alert_condition
            ),
            "trigger_path_identifier": self.trigger_path_identifier,
            "fresh_trigger_path_present": self.fresh_trigger_path_present,
            "repeat_count": self.repeat_count,
        }
        if validate:
            reject_forbidden_execution_fields(output)
        return output


def update_watcher_state(
    previous_state: WatcherTrackedState | WatchOnlyCandidateState | Mapping[str, Any] | None,
    observation: WatcherTrackedState | WatchOnlyCandidateState | Mapping[str, Any],
) -> WatcherTrackedState:
    """Return updated watch-only state from previous state plus an observation."""

    previous = _coerce_state(previous_state) if previous_state is not None else None
    observed = _normalize_observation(observation)
    reject_forbidden_execution_fields(observed)

    if previous is None:
        state = _state_from_initial_observation(observed)
        reject_forbidden_execution_fields(state.to_dict())
        return state

    merged = _merge_with_previous(previous, observed)
    flags = _material_change_flags(previous, merged)
    material_change = flags != ("no_material_change",)

    merged.update(
        {
            "previous_stage": previous.stage,
            "previous_trigger_status": previous.trigger_status,
            "previous_fresh_stale_spent_state": previous.fresh_stale_spent_state,
            "state_version": previous.state_version + 1
            if material_change
            else previous.state_version,
            "state_changed": material_change,
            "state_change_reason_codes": flags,
            "material_change_flags": flags,
            "repeat_count": 0 if material_change else previous.repeat_count + 1,
            "watch_only": True,
        }
    )

    state = WatcherTrackedState(**merged)
    reject_forbidden_execution_fields(state.to_dict())
    return state


def _state_from_initial_observation(
    observation: Mapping[str, Any],
) -> WatcherTrackedState:
    values = WatcherTrackedState().to_dict()
    values.update(_supported_observation_values(observation))
    values["watch_only"] = True
    values["headline_news_status"] = values.get(
        "headline_news_status", NEWS_UNCONFIRMED
    ) or NEWS_UNCONFIRMED
    values["state_version"] = int(values.get("state_version") or 1)
    values["material_change_flags"] = tuple(values.get("material_change_flags") or ())
    if not values["material_change_flags"]:
        values["material_change_flags"] = ("no_material_change",)
    values["state_change_reason_codes"] = tuple(
        values.get("state_change_reason_codes") or values["material_change_flags"]
    )
    return WatcherTrackedState(**_constructor_values(values))


def _merge_with_previous(
    previous: WatcherTrackedState,
    observation: Mapping[str, Any],
) -> dict[str, Any]:
    merged = previous.to_dict()
    for key, value in _supported_observation_values(observation).items():
        if key in _identity_fields():
            continue
        if key in {
            "first_seen_at",
            "previous_stage",
            "previous_trigger_status",
            "previous_fresh_stale_spent_state",
            "state_version",
            "state_changed",
            "state_change_reason_codes",
            "material_change_flags",
            "repeat_count",
        }:
            continue
        merged[key] = value

    merged["watch_only"] = True
    merged["first_seen_at"] = previous.first_seen_at
    if "last_seen_at" not in observation:
        merged["last_seen_at"] = previous.last_seen_at
    merged["headline_news_status"] = (
        merged.get("headline_news_status") or NEWS_UNCONFIRMED
    )
    return _constructor_values(merged)


def _material_change_flags(
    previous: WatcherTrackedState,
    merged: Mapping[str, Any],
) -> tuple[str, ...]:
    flags: list[str] = []
    comparisons = (
        ("stage", "stage_changed"),
        ("trigger_status", "trigger_status_changed"),
        ("fresh_stale_spent_state", "freshness_changed"),
        ("primary_blocker", "primary_blocker_changed"),
        ("trigger_zone_bucket", "trigger_zone_changed"),
        ("trigger_level_or_zone", "trigger_zone_changed"),
        ("invalidation_bucket", "invalidation_changed"),
        ("invalidation_level_or_condition", "invalidation_changed"),
        ("evidence_quality", "evidence_quality_changed"),
    )
    previous_dict = previous.to_dict()
    for field_name, flag in comparisons:
        if previous_dict[field_name] != merged[field_name] and flag not in flags:
            flags.append(flag)

    availability_change = _critical_availability_change(previous_dict, merged)
    for flag in availability_change:
        if flag not in flags:
            flags.append(flag)

    return tuple(flags) if flags else ("no_material_change",)


def _critical_availability_change(
    previous: Mapping[str, Any],
    current: Mapping[str, Any],
) -> tuple[str, ...]:
    flags: list[str] = []
    for field_name in CRITICAL_AVAILABILITY_FIELDS:
        previous_available = _is_available(previous[field_name])
        current_available = _is_available(current[field_name])
        if not previous_available and current_available:
            flags.append("critical_field_became_available")
        elif previous_available and not current_available:
            flags.append("critical_field_became_unavailable")

    previous_unavailable = set(previous["unavailable_fields"])
    current_unavailable = set(current["unavailable_fields"])
    if len(current_unavailable) < len(previous_unavailable):
        flags.append("critical_field_became_available")
    elif len(current_unavailable) > len(previous_unavailable):
        flags.append("critical_field_became_unavailable")

    ordered: list[str] = []
    for flag in flags:
        if flag not in ordered:
            ordered.append(flag)
    return tuple(ordered)


def _is_available(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value not in UNCONFIRMED_VALUES and not value.endswith("_UNCONFIRMED")
    if isinstance(value, (list, tuple, set)):
        return bool(value) and any(_is_available(item) for item in value)
    return True


def _normalize_observation(
    observation: WatcherTrackedState | WatchOnlyCandidateState | Mapping[str, Any],
) -> dict[str, Any]:
    if isinstance(observation, WatcherTrackedState):
        return observation.to_dict()
    if isinstance(observation, WatchOnlyCandidateState):
        candidate = observation.to_dict()
        return {
            "candidate_id": candidate["candidate_id"],
            "symbol": candidate["symbol"],
            "watch_session_id": candidate["watch_session_id"],
            "setup_type": candidate["setup_type"],
            "direction": candidate["direction"],
            "stage": candidate["stage"],
            "trigger_status": candidate["trigger_status"],
            "fresh_stale_spent_state": _normalize_freshness(
                candidate["freshness_state"]
            ),
            "trigger_level_or_zone": candidate["trigger_level"],
            "distance_to_trigger": candidate["distance_to_trigger"],
            "invalidation_level_or_condition": candidate["invalidation"],
            "source_as_of": candidate["source_as_of"],
            "evidence_rows": candidate["evidence_rows"],
            "unavailable_fields": candidate["unavailable_fields"],
            "headline_news_status": candidate["headline_news_status"],
            "blockers": candidate["blockers"],
            "cautions": candidate["cautions"],
            "no_trade_reason": candidate["no_trade_reason"],
            "watch_only": candidate["watch_only"],
        }
    if isinstance(observation, Mapping):
        return dict(observation)
    raise TypeError("observation must be a watcher state, candidate state, or mapping")


def _coerce_state(
    state: WatcherTrackedState | WatchOnlyCandidateState | Mapping[str, Any],
) -> WatcherTrackedState:
    if isinstance(state, WatcherTrackedState):
        return state
    normalized = _normalize_observation(state)
    return _state_from_initial_observation(normalized)


def _supported_observation_values(observation: Mapping[str, Any]) -> dict[str, Any]:
    supported = set(WatcherTrackedState.__dataclass_fields__)
    values: dict[str, Any] = {}
    for key, value in observation.items():
        normalized_key = "fresh_stale_spent_state" if key == "freshness_state" else key
        if normalized_key not in supported:
            continue
        values[normalized_key] = _normalize_value(normalized_key, value)
    if values.get("watch_only") is not True and "watch_only" in values:
        raise ValueError("Watcher tracked observations must remain watch_only=True")
    return values


def _constructor_values(values: Mapping[str, Any]) -> dict[str, Any]:
    constructor_values = {}
    for key in WatcherTrackedState.__dataclass_fields__:
        value = values[key]
        constructor_values[key] = _normalize_value(key, value)
    return constructor_values


def _normalize_value(key: str, value: Any) -> Any:
    if key in {
        "evidence_rows",
        "unavailable_fields",
        "blockers",
        "cautions",
        "state_change_reason_codes",
        "material_change_flags",
    }:
        return tuple(value)
    if key == "fresh_stale_spent_state":
        return _normalize_freshness(str(value))
    return value


def _normalize_freshness(value: str) -> str:
    if value == FRESHNESS_UNCONFIRMED:
        return "unconfirmed"
    return value


def _identity_fields() -> frozenset[str]:
    return frozenset(
        {
            "candidate_id",
            "symbol",
            "watch_session_id",
            "setup_type",
            "direction",
            "regular_session_date",
        }
    )
