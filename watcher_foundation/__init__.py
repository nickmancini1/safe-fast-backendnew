"""Local watch-only watcher foundation scaffold."""

from watcher_foundation.constants import (
    ACCEPTED_HEADLINE_NEWS_STATUSES,
    ACCEPTED_SETUP_TYPES,
    ACCEPTED_STAGES,
    ACCEPTED_TRIGGER_STATUSES,
    EXPLICIT_UNCONFIRMED_MARKERS,
    NEWS_UNCONFIRMED,
)
from watcher_foundation.diagnostics import (
    DIAGNOSTIC_REASON_CODE_GROUPS,
    build_diagnostics,
    create_diagnostics,
)
from watcher_foundation.duplicate_suppression import (
    DUPLICATE_SUPPRESSION_FINGERPRINT_VERSION,
    DUPLICATE_SUPPRESSION_KEY_FIELD_NAMES,
    MATERIAL_CHANGE_FLAGS_THAT_BREAK_SUPPRESSION,
    build_duplicate_suppression_key_fields,
    build_suppression_fingerprint,
    decide_duplicate_suppression,
)
from watcher_foundation.focus_ranking import FOCUS_RANK_BUCKETS, rank_focus_candidates
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
    "DIAGNOSTIC_REASON_CODE_GROUPS",
    "DUPLICATE_SUPPRESSION_FINGERPRINT_VERSION",
    "DUPLICATE_SUPPRESSION_KEY_FIELD_NAMES",
    "EXPLICIT_UNCONFIRMED_MARKERS",
    "FOCUS_RANK_BUCKETS",
    "MATERIAL_CHANGE_FLAGS_THAT_BREAK_SUPPRESSION",
    "NEWS_UNCONFIRMED",
    "REQUIRED_SHADOW_LOG_FIELDS",
    "REQUIRED_TRIGGER_CARD_FIELDS",
    "SHADOW_LOG_SCHEMA_VERSION",
    "WatchOnlyCandidateState",
    "WatcherTrackedState",
    "append_shadow_log_line",
    "build_diagnostics",
    "build_duplicate_suppression_key_fields",
    "build_suppression_fingerprint",
    "create_diagnostics",
    "create_shadow_log_record",
    "decide_duplicate_suppression",
    "project_trigger_card",
    "rank_focus_candidates",
    "reject_forbidden_execution_fields",
    "serialize_shadow_log_line",
    "update_watcher_state",
]
