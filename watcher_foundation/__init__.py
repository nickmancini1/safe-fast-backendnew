"""Local watch-only watcher foundation scaffold."""

from watcher_foundation.constants import (
    ACCEPTED_HEADLINE_NEWS_STATUSES,
    ACCEPTED_SETUP_TYPES,
    ACCEPTED_STAGES,
    ACCEPTED_TRIGGER_STATUSES,
    EXPLICIT_UNCONFIRMED_MARKERS,
    NEWS_UNCONFIRMED,
)
from watcher_foundation.models import (
    WatchOnlyCandidateState,
    reject_forbidden_execution_fields,
)
from watcher_foundation.state_tracker import WatcherTrackedState, update_watcher_state

__all__ = [
    "ACCEPTED_HEADLINE_NEWS_STATUSES",
    "ACCEPTED_SETUP_TYPES",
    "ACCEPTED_STAGES",
    "ACCEPTED_TRIGGER_STATUSES",
    "EXPLICIT_UNCONFIRMED_MARKERS",
    "NEWS_UNCONFIRMED",
    "WatchOnlyCandidateState",
    "WatcherTrackedState",
    "reject_forbidden_execution_fields",
    "update_watcher_state",
]
