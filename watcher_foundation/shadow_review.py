"""Local shadow review label validation.

This module validates caller-provided in-memory review dictionaries only. It
does not read live data, create files, emit alerts, or wire review labels into
production behavior.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.constants import FORBIDDEN_EXECUTION_FIELD_NAMES


ALLOWED_SHADOW_REVIEW_LABELS = (
    "valid_watch_candidate",
    "invalid_watch_candidate",
    "needs_more_evidence",
    "stale_or_spent",
    "duplicate_suppressed",
    "winner_correct",
    "winner_questionable",
    "no_trade_boundary_preserved",
)

REQUIRED_SHADOW_REVIEW_FIELDS = (
    "sample_id",
    "setup_type",
    "stage",
    "trigger_status",
    "headline_news_status",
    "duplicate_suppression_status",
    "focus_winner_status",
    "diagnostics_summary",
    "reviewer_label",
    "reviewer_notes",
    "no_trade_boundary_check",
)

FORBIDDEN_SHADOW_REVIEW_FIELD_NAMES = FORBIDDEN_EXECUTION_FIELD_NAMES | frozenset(
    {
        "approved_trade",
        "approved_trades",
        "live_trade_approval",
        "p_and_l",
        "p&l",
        "pl",
        "trade",
        "trade_approval",
        "trade_decision",
        "trade_decisions",
    }
)


def validate_shadow_review_label(sample: dict[str, Any]) -> dict[str, Any]:
    """Return a validated copy of one local watch-only shadow review label."""
    if type(sample) is not dict:
        raise TypeError("shadow review sample must be a dict")

    missing_fields = [
        field_name
        for field_name in REQUIRED_SHADOW_REVIEW_FIELDS
        if field_name not in sample
    ]
    if missing_fields:
        raise ValueError(
            "Missing required shadow review fields: " + ", ".join(missing_fields)
        )

    _reject_forbidden_shadow_review_fields(sample, path=())

    reviewer_label = sample["reviewer_label"]
    if reviewer_label not in ALLOWED_SHADOW_REVIEW_LABELS:
        raise ValueError(f"Unsupported reviewer_label: {reviewer_label}")

    if sample["no_trade_boundary_check"] is not True:
        raise ValueError("no_trade_boundary_check must be true")

    _require_local_watch_only_wording(sample)

    return deepcopy(dict(sample))


def _reject_forbidden_shadow_review_fields(
    value: Any, path: tuple[str, ...]
) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.lower()
            if normalized_key in FORBIDDEN_SHADOW_REVIEW_FIELD_NAMES:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden execution/trade field: {dotted_path}")
            _reject_forbidden_shadow_review_fields(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_forbidden_shadow_review_fields(nested_value, (*path, str(index)))


def _require_local_watch_only_wording(sample: Mapping[str, Any]) -> None:
    wording = " ".join(
        str(sample[field_name]).lower()
        for field_name in ("diagnostics_summary", "reviewer_notes")
    )
    has_local = "local" in wording
    has_watch_only = "watch-only" in wording or "watch_only" in wording
    if not has_local or not has_watch_only:
        raise ValueError(
            "shadow review wording must preserve local and watch-only boundaries"
        )
