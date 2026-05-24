"""Pure Python models for the local watch-only watcher scaffold."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from watcher_foundation.constants import (
    ACCEPTED_DIRECTIONS,
    ACCEPTED_HEADLINE_NEWS_STATUSES,
    ACCEPTED_SETUP_TYPES,
    ACCEPTED_STAGES,
    ACCEPTED_TRIGGER_STATUSES,
    DEFAULT_UNAVAILABLE_FIELDS,
    DISTANCE_TO_TRIGGER_UNCONFIRMED,
    EVIDENCE_ROWS_UNCONFIRMED,
    FORBIDDEN_EXECUTION_FIELD_NAMES,
    FRESHNESS_UNCONFIRMED,
    INVALIDATION_UNCONFIRMED,
    NEWS_UNCONFIRMED,
    SOURCE_AS_OF_UNCONFIRMED,
    TRIGGER_LEVEL_UNCONFIRMED,
)


def reject_forbidden_execution_fields(payload: Mapping[str, Any]) -> None:
    """Reject broker/order/account/option/execution fields in scaffold payloads."""
    _reject_forbidden_execution_fields(payload, path=())


def _reject_forbidden_execution_fields(value: Any, path: tuple[str, ...]) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.lower()
            if normalized_key in FORBIDDEN_EXECUTION_FIELD_NAMES:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden execution/account/order field: {dotted_path}")
            _reject_forbidden_execution_fields(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_forbidden_execution_fields(nested_value, (*path, str(index)))


@dataclass(frozen=True)
class WatchOnlyCandidateState:
    """Normalized local state for one watch-only candidate.

    This is a projection scaffold only. It deliberately carries no live-data,
    broker, account, order, option, sizing, or execution behavior.
    """

    candidate_id: str = "UNCONFIRMED"
    symbol: str = "UNCONFIRMED"
    watch_session_id: str = "UNCONFIRMED"
    setup_type: str = "UNCONFIRMED"
    direction: str = "UNCONFIRMED"
    stage: str = "unavailable/unconfirmed"
    trigger_status: str = "unconfirmed"
    freshness_state: str = FRESHNESS_UNCONFIRMED
    trigger_level: str = TRIGGER_LEVEL_UNCONFIRMED
    distance_to_trigger: str = DISTANCE_TO_TRIGGER_UNCONFIRMED
    invalidation: str = INVALIDATION_UNCONFIRMED
    source_as_of: str = SOURCE_AS_OF_UNCONFIRMED
    evidence_rows: tuple[str, ...] = (EVIDENCE_ROWS_UNCONFIRMED,)
    unavailable_fields: tuple[str, ...] = field(default_factory=lambda: DEFAULT_UNAVAILABLE_FIELDS)
    headline_news_status: str = NEWS_UNCONFIRMED
    blockers: tuple[str, ...] = ()
    cautions: tuple[str, ...] = ()
    no_trade_reason: str = (
        "watch_only_unconfirmed_trigger_invalidation_source_or_evidence"
    )
    watch_only: bool = True

    def __post_init__(self) -> None:
        if self.setup_type not in ACCEPTED_SETUP_TYPES:
            raise ValueError(f"Unsupported setup_type: {self.setup_type}")
        if self.direction not in ACCEPTED_DIRECTIONS:
            raise ValueError(f"Unsupported direction: {self.direction}")
        if self.stage not in ACCEPTED_STAGES:
            raise ValueError(f"Unsupported stage: {self.stage}")
        if self.trigger_status not in ACCEPTED_TRIGGER_STATUSES:
            raise ValueError(f"Unsupported trigger_status: {self.trigger_status}")
        if self.headline_news_status not in ACCEPTED_HEADLINE_NEWS_STATUSES:
            raise ValueError(
                f"Unsupported headline_news_status: {self.headline_news_status}"
            )
        if self.watch_only is not True:
            raise ValueError("Watcher foundation candidates must remain watch_only=True")

    def to_dict(self) -> dict[str, Any]:
        """Return a plain dict for later card/log projection."""
        output = {
            "candidate_id": self.candidate_id,
            "symbol": self.symbol,
            "watch_session_id": self.watch_session_id,
            "setup_type": self.setup_type,
            "direction": self.direction,
            "stage": self.stage,
            "trigger_status": self.trigger_status,
            "freshness_state": self.freshness_state,
            "trigger_level": self.trigger_level,
            "distance_to_trigger": self.distance_to_trigger,
            "invalidation": self.invalidation,
            "source_as_of": self.source_as_of,
            "evidence_rows": list(self.evidence_rows),
            "unavailable_fields": list(self.unavailable_fields),
            "headline_news_status": self.headline_news_status,
            "blockers": list(self.blockers),
            "cautions": list(self.cautions),
            "no_trade_reason": self.no_trade_reason,
            "watch_only": self.watch_only,
        }
        reject_forbidden_execution_fields(output)
        return output
