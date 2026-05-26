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

SHADOW_REVIEW_WORKFLOW_SUMMARY_FIELDS = (
    "samples_processed",
    "samples_accepted",
    "samples_rejected",
    "rejected_samples",
    "label_counts",
    "setup_type_counts",
    "no_trade_boundary_preserved_count",
    "watch_only",
)

SHADOW_REVIEW_EXPORT_REQUIRED_FIELDS = (
    "export_id",
    "created_from",
    "schema_version",
    "samples",
    "label_counts",
    "setup_type_counts",
    "rejected_samples",
    "no_trade_boundary_summary",
    "reviewer_notes",
    "unavailable_fields",
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


def validate_shadow_review_export_shape(export: dict[str, Any]) -> dict[str, Any]:
    """Return a validated copy of one local in-memory shadow review export."""
    if type(export) is not dict:
        raise TypeError("shadow review export must be a dict")

    missing_fields = [
        field_name
        for field_name in SHADOW_REVIEW_EXPORT_REQUIRED_FIELDS
        if field_name not in export
    ]
    if missing_fields:
        raise ValueError(
            "Missing required shadow review export fields: "
            + ", ".join(missing_fields)
        )

    _reject_forbidden_shadow_review_fields(export, path=())

    if type(export["samples"]) is not list:
        raise TypeError("shadow review export samples must be a list")
    if type(export["label_counts"]) is not dict:
        raise TypeError("shadow review export label_counts must be a dict")
    if type(export["setup_type_counts"]) is not dict:
        raise TypeError("shadow review export setup_type_counts must be a dict")
    if type(export["rejected_samples"]) is not list:
        raise TypeError("shadow review export rejected_samples must be a list")
    if type(export["no_trade_boundary_summary"]) is not dict:
        raise TypeError(
            "shadow review export no_trade_boundary_summary must be a dict"
        )

    _require_export_watch_only_no_trade_boundary(
        export["no_trade_boundary_summary"]
    )

    return deepcopy(dict(export))


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


def run_local_shadow_review_label_workflow(
    samples: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate local in-memory samples and return a watch-only summary."""
    if type(samples) is not list:
        raise TypeError("shadow review workflow samples must be a list")

    label_counts = {label: 0 for label in ALLOWED_SHADOW_REVIEW_LABELS}
    setup_type_counts: dict[str, int] = {}
    rejected_samples = []
    no_trade_boundary_preserved_count = 0

    for sample in samples:
        sample_id = _extract_rejected_sample_id(sample)
        try:
            validated = validate_shadow_review_label(sample)
        except (TypeError, ValueError) as exc:
            rejected_samples.append(
                {
                    "sample_id": sample_id,
                    "reason": str(exc),
                }
            )
            continue

        reviewer_label = validated["reviewer_label"]
        setup_type = validated["setup_type"]
        label_counts[reviewer_label] += 1
        setup_type_counts[setup_type] = setup_type_counts.get(setup_type, 0) + 1
        if validated["no_trade_boundary_check"] is True:
            no_trade_boundary_preserved_count += 1

    samples_processed = len(samples)
    samples_rejected = len(rejected_samples)
    samples_accepted = samples_processed - samples_rejected

    return {
        "samples_processed": samples_processed,
        "samples_accepted": samples_accepted,
        "samples_rejected": samples_rejected,
        "rejected_samples": rejected_samples,
        "label_counts": label_counts,
        "setup_type_counts": setup_type_counts,
        "no_trade_boundary_preserved_count": no_trade_boundary_preserved_count,
        "watch_only": True,
    }


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


def _extract_rejected_sample_id(sample: Any) -> str:
    if isinstance(sample, Mapping) and "sample_id" in sample:
        return str(sample["sample_id"])
    return "UNAVAILABLE"


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


def _require_export_watch_only_no_trade_boundary(
    no_trade_boundary_summary: Mapping[str, Any]
) -> None:
    if no_trade_boundary_summary.get("watch_only") is not True:
        raise ValueError(
            "shadow review export must preserve watch_only boundary"
        )
    if no_trade_boundary_summary.get("no_trade_boundary_preserved") is not True:
        raise ValueError(
            "shadow review export must preserve no-trade boundary"
        )
