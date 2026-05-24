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
from watcher_foundation.shadow_log import (
    ALLOWED_SHADOW_LOG_EVENT_TYPES,
    DEFAULT_REVIEW_LABEL,
    REQUIRED_SHADOW_LOG_FIELDS,
    SHADOW_LOG_SCHEMA_VERSION,
    append_shadow_log_line,
    create_shadow_log_record,
    serialize_shadow_log_line,
)
from watcher_foundation.trigger_card import (
    REQUIRED_TRIGGER_CARD_FIELDS,
    project_trigger_card,
)

__all__ = [
    "ACCEPTED_HEADLINE_NEWS_STATUSES",
    "ACCEPTED_SETUP_TYPES",
    "ACCEPTED_STAGES",
    "ACCEPTED_TRIGGER_STATUSES",
    "ALLOWED_SHADOW_LOG_EVENT_TYPES",
    "DEFAULT_REVIEW_LABEL",
    "EXPLICIT_UNCONFIRMED_MARKERS",
    "NEWS_UNCONFIRMED",
    "REQUIRED_SHADOW_LOG_FIELDS",
    "REQUIRED_TRIGGER_CARD_FIELDS",
    "SHADOW_LOG_SCHEMA_VERSION",
    "WatchOnlyCandidateState",
    "WatcherTrackedState",
    "append_shadow_log_line",
    "create_shadow_log_record",
    "project_trigger_card",
    "reject_forbidden_execution_fields",
    "serialize_shadow_log_line",
    "update_watcher_state",
]
