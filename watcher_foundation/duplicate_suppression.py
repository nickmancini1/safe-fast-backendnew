"""Duplicate suppression decisions for local watch-only watcher artifacts.

This module compares caller-provided watcher state/card dictionaries only. It
does not fetch live data, run watcher loops, emit phone alerts, create runtime
schema files, write logs, or integrate with broker/account/order/option systems.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from dataclasses import asdict, is_dataclass
from typing import Any, Mapping

from watcher_foundation.constants import (
    INVALIDATION_BUCKET_UNCONFIRMED,
    NEWS_UNCONFIRMED,
    PRIMARY_BLOCKER_UNCONFIRMED,
    TRIGGER_ZONE_UNCONFIRMED,
)
from watcher_foundation.models import reject_forbidden_execution_fields


DUPLICATE_SUPPRESSION_FINGERPRINT_VERSION = "duplicate_suppression_v1"

DUPLICATE_SUPPRESSION_KEY_FIELD_NAMES = (
    "symbol",
    "setup_family",
    "direction",
    "stage",
    "trigger_status",
    "freshness_state",
    "primary_blocker",
    "trigger_zone_bucket",
    "invalidation_bucket",
)

MATERIAL_CHANGE_FLAGS_THAT_BREAK_SUPPRESSION = (
    "stage_changed",
    "trigger_status_changed",
    "freshness_changed",
    "primary_blocker_changed",
    "blocker_severity_changed",
    "caution_severity_changed",
    "trigger_zone_changed",
    "invalidation_changed",
    "evidence_quality_changed",
    "critical_field_became_available",
    "critical_field_became_unavailable",
    "session_boundary_changed",
    "best_candidate_changed",
    "trigger_path_changed",
    "source_confirmed_headline_news_status_changed",
)


def decide_duplicate_suppression(
    current: Mapping[str, Any] | Any,
    previous_suppression_state: Mapping[str, Any] | Any | None = None,
) -> dict[str, Any]:
    """Return a plain dict duplicate-suppression decision.

    The optional previous value is expected to be a prior decision object or a
    compatible suppression-state mapping. Inputs are copied before normalization.
    """

    current_source = _to_plain_dict(current)
    previous_source = (
        _to_plain_dict(previous_suppression_state)
        if previous_suppression_state is not None
        else None
    )

    reject_forbidden_execution_fields(current_source)
    if previous_source is not None:
        reject_forbidden_execution_fields(previous_source)
    _reject_watch_only_false(current_source)
    if previous_source is not None:
        _reject_watch_only_false(previous_source)

    current_source["headline_news_status"] = (
        current_source.get("headline_news_status") or NEWS_UNCONFIRMED
    )
    current_key_fields = build_duplicate_suppression_key_fields(current_source)
    current_material_fields = _material_review_fields(current_source)
    current_fingerprint = build_suppression_fingerprint(
        current_key_fields, current_material_fields
    )

    previous_key_fields = _previous_key_fields(previous_source)
    previous_material_fields = _previous_material_fields(previous_source)
    previous_fingerprint = _previous_fingerprint(previous_source)
    previous_repeat_count = int(previous_source.get("repeat_count", 0)) if previous_source else 0
    last_suppression_reason = (
        previous_source.get("suppression_reason") if previous_source else "none"
    )

    material_change_flags = _material_change_flags(
        current_source,
        current_key_fields,
        current_material_fields,
        previous_key_fields,
        previous_material_fields,
    )

    incomplete_projection = _is_incomplete_projection(current_source)
    is_duplicate = (
        previous_source is not None
        and previous_fingerprint == current_fingerprint
        and not material_change_flags
    )

    if is_duplicate:
        alert_decision = "suppress_duplicate"
        suppression_reason = "same_state_repeat_no_material_change"
        repeat_count = previous_repeat_count + 1
    elif incomplete_projection and previous_source is not None and not material_change_flags:
        alert_decision = "no_alert_incomplete_projection"
        suppression_reason = "incomplete_projection_no_material_change"
        repeat_count = previous_repeat_count + 1
    elif previous_source is None:
        alert_decision = "emit_material_change"
        suppression_reason = "new_state_observation"
        repeat_count = 0
    elif material_change_flags:
        alert_decision = "emit_material_change"
        suppression_reason = "material_change_breaks_suppression"
        repeat_count = 0
    else:
        alert_decision = "no_alert_no_material_change"
        suppression_reason = "fingerprint_changed_without_material_flag"
        repeat_count = previous_repeat_count

    decision = {
        "alert_decision": alert_decision,
        "suppression_reason": suppression_reason,
        "duplicate_suppression_key_fields": current_key_fields,
        "suppression_fingerprint": current_fingerprint,
        "repeat_count": repeat_count,
        "material_change_flags": material_change_flags,
        "last_suppression_reason": last_suppression_reason,
        "watch_only": True,
        "headline_news_status": current_source["headline_news_status"],
        "material_review_fields": current_material_fields,
    }
    reject_forbidden_execution_fields(decision)
    return decision


def build_duplicate_suppression_key_fields(source: Mapping[str, Any]) -> dict[str, Any]:
    """Build deterministic suppression key fields from normalized source input."""

    key_fields = source.get("duplicate_suppression_key_fields")
    if isinstance(key_fields, Mapping):
        return {
            "symbol": key_fields.get("symbol", source.get("symbol", "UNCONFIRMED")),
            "setup_family": key_fields.get(
                "setup_family", source.get("setup_type", "UNCONFIRMED")
            ),
            "direction": key_fields.get(
                "direction", source.get("direction", "UNCONFIRMED")
            ),
            "stage": key_fields.get(
                "stage", source.get("stage", "unavailable/unconfirmed")
            ),
            "trigger_status": key_fields.get(
                "trigger_status", source.get("trigger_status", "unconfirmed")
            ),
            "freshness_state": key_fields.get(
                "freshness_state",
                source.get(
                    "fresh_stale_spent_state",
                    source.get("freshness_state", "unconfirmed"),
                ),
            ),
            "primary_blocker": key_fields.get(
                "primary_blocker", _primary_blocker(source)
            ),
            "trigger_zone_bucket": key_fields.get(
                "trigger_zone_bucket", _trigger_zone_bucket(source)
            ),
            "invalidation_bucket": key_fields.get(
                "invalidation_bucket", _invalidation_bucket(source)
            ),
        }

    return {
        "symbol": source.get("symbol", "UNCONFIRMED"),
        "setup_family": source.get("setup_type", "UNCONFIRMED"),
        "direction": source.get("direction", "UNCONFIRMED"),
        "stage": source.get("stage", "unavailable/unconfirmed"),
        "trigger_status": source.get("trigger_status", "unconfirmed"),
        "freshness_state": source.get(
            "fresh_stale_spent_state", source.get("freshness_state", "unconfirmed")
        ),
        "primary_blocker": _primary_blocker(source),
        "trigger_zone_bucket": _trigger_zone_bucket(source),
        "invalidation_bucket": _invalidation_bucket(source),
    }


def build_suppression_fingerprint(
    key_fields: Mapping[str, Any], material_review_fields: Mapping[str, Any]
) -> str:
    """Return deterministic SHA-256 fingerprint for suppression equality."""

    payload = {
        "version": DUPLICATE_SUPPRESSION_FINGERPRINT_VERSION,
        "duplicate_suppression_key_fields": _json_compatible(key_fields),
        "material_review_fields": _json_compatible(material_review_fields),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _to_plain_dict(value: Mapping[str, Any] | Any) -> dict[str, Any]:
    if hasattr(value, "to_dict"):
        return deepcopy(value.to_dict())
    if is_dataclass(value):
        return deepcopy(asdict(value))
    if isinstance(value, Mapping):
        return deepcopy(dict(value))
    raise TypeError("duplicate suppression input must be a mapping or dict-like artifact")


def _reject_watch_only_false(value: Any, path: tuple[str, ...] = ()) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            if key_text == "watch_only" and nested_value is not True:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Duplicate suppression must preserve watch_only=True: {dotted_path}")
            _reject_watch_only_false(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_watch_only_false(nested_value, (*path, str(index)))


def _primary_blocker(source: Mapping[str, Any]) -> Any:
    if source.get("primary_blocker") is not None:
        return source["primary_blocker"]
    blockers = _as_list(source.get("blockers", ()))
    if blockers:
        first = blockers[0]
        if isinstance(first, Mapping):
            return first.get("reason_code", first.get("code", first))
        return first
    return PRIMARY_BLOCKER_UNCONFIRMED


def _trigger_zone_bucket(source: Mapping[str, Any]) -> Any:
    return source.get(
        "trigger_zone_bucket",
        source.get("trigger_level_or_zone", TRIGGER_ZONE_UNCONFIRMED),
    )


def _invalidation_bucket(source: Mapping[str, Any]) -> Any:
    return source.get(
        "invalidation_bucket",
        source.get("invalidation_level_or_condition", INVALIDATION_BUCKET_UNCONFIRMED),
    )


def _material_review_fields(source: Mapping[str, Any]) -> dict[str, Any]:
    headline_status = source.get("headline_news_status") or NEWS_UNCONFIRMED
    source_confirmed_news = _source_confirmed_news(source)

    fields = {
        "blocker_severity_summary": _severity_summary(source.get("blockers", ())),
        "caution_severity_summary": _severity_summary(source.get("cautions", ())),
        "trigger_path_identifier": source.get(
            "trigger_path_identifier",
            source.get("trigger_path_id", source.get("trigger_path", "UNCONFIRMED")),
        ),
        "fresh_trigger_path_present": bool(source.get("fresh_trigger_path_present", False)),
        "evidence_quality": source.get("evidence_quality", "unconfirmed"),
        "critical_unavailable_fields": sorted(
            str(field) for field in _as_list(source.get("unavailable_fields", ()))
        ),
        "session_boundary_state": source.get(
            "session_boundary_state",
            source.get("regular_session_date", source.get("session_boundary", "UNCONFIRMED")),
        ),
        "best_candidate_identity": source.get(
            "best_candidate_id",
            source.get("candidate_id", source.get("focus_rank_bucket", "UNCONFIRMED")),
        ),
        "best_candidate_ranking_inputs": _json_compatible(
            source.get("best_candidate_ranking_inputs", {})
        ),
        "source_as_of_bucket": source.get("source_as_of_bucket", source.get("source_as_of", "UNCONFIRMED")),
        "headline_news_status": headline_status if source_confirmed_news else NEWS_UNCONFIRMED,
        "headline_news_source_confirmed": source_confirmed_news,
    }
    return _json_compatible(fields)


def _severity_summary(items: Any) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for item in _as_list(items):
        if isinstance(item, Mapping):
            summary.append(
                {
                    "reason_code": item.get("reason_code", item.get("code", "UNCONFIRMED")),
                    "severity": item.get("severity", "UNCONFIRMED"),
                }
            )
        else:
            summary.append({"reason_code": item, "severity": "UNCONFIRMED"})
    return sorted(summary, key=lambda entry: json.dumps(entry, sort_keys=True))


def _source_confirmed_news(source: Mapping[str, Any]) -> bool:
    if source.get("headline_news_source_confirmed") is True:
        return True
    status = str(source.get("headline_news_source_status", "")).lower()
    return status in {"source_confirmed", "confirmed", "valid_source_confirmed"}


def _material_change_flags(
    current_source: Mapping[str, Any],
    current_key_fields: Mapping[str, Any],
    current_material_fields: Mapping[str, Any],
    previous_key_fields: Mapping[str, Any] | None,
    previous_material_fields: Mapping[str, Any] | None,
) -> list[str]:
    flags: list[str] = []
    for flag in _as_list(current_source.get("material_change_flags", ())):
        if flag in MATERIAL_CHANGE_FLAGS_THAT_BREAK_SUPPRESSION:
            flags.append(str(flag))

    if previous_key_fields is not None:
        _append_if_changed(flags, previous_key_fields, current_key_fields, "stage", "stage_changed")
        _append_if_changed(
            flags,
            previous_key_fields,
            current_key_fields,
            "trigger_status",
            "trigger_status_changed",
        )
        _append_if_changed(
            flags,
            previous_key_fields,
            current_key_fields,
            "freshness_state",
            "freshness_changed",
        )
        _append_if_changed(
            flags,
            previous_key_fields,
            current_key_fields,
            "primary_blocker",
            "primary_blocker_changed",
        )
        _append_if_changed(
            flags,
            previous_key_fields,
            current_key_fields,
            "trigger_zone_bucket",
            "trigger_zone_changed",
        )
        _append_if_changed(
            flags,
            previous_key_fields,
            current_key_fields,
            "invalidation_bucket",
            "invalidation_changed",
        )

    if previous_material_fields is not None:
        _append_if_changed(
            flags,
            previous_material_fields,
            current_material_fields,
            "blocker_severity_summary",
            "blocker_severity_changed",
        )
        _append_if_changed(
            flags,
            previous_material_fields,
            current_material_fields,
            "caution_severity_summary",
            "caution_severity_changed",
        )
        _append_if_changed(
            flags,
            previous_material_fields,
            current_material_fields,
            "evidence_quality",
            "evidence_quality_changed",
        )
        _append_availability_flags(flags, previous_material_fields, current_material_fields)
        _append_if_changed(
            flags,
            previous_material_fields,
            current_material_fields,
            "session_boundary_state",
            "session_boundary_changed",
        )
        _append_if_changed(
            flags,
            previous_material_fields,
            current_material_fields,
            "best_candidate_identity",
            "best_candidate_changed",
        )
        _append_if_changed(
            flags,
            previous_material_fields,
            current_material_fields,
            "best_candidate_ranking_inputs",
            "best_candidate_changed",
        )
        _append_if_changed(
            flags,
            previous_material_fields,
            current_material_fields,
            "trigger_path_identifier",
            "trigger_path_changed",
        )
        _append_if_changed(
            flags,
            previous_material_fields,
            current_material_fields,
            "fresh_trigger_path_present",
            "trigger_path_changed",
        )
        if (
            current_material_fields.get("headline_news_source_confirmed") is True
            and previous_material_fields.get("headline_news_status")
            != current_material_fields.get("headline_news_status")
        ):
            flags.append("source_confirmed_headline_news_status_changed")

    ordered: list[str] = []
    for flag in flags:
        if flag != "no_material_change" and flag not in ordered:
            ordered.append(flag)
    return ordered


def _append_if_changed(
    flags: list[str],
    previous: Mapping[str, Any],
    current: Mapping[str, Any],
    field_name: str,
    flag: str,
) -> None:
    if previous.get(field_name) != current.get(field_name):
        flags.append(flag)


def _append_availability_flags(
    flags: list[str],
    previous_material_fields: Mapping[str, Any],
    current_material_fields: Mapping[str, Any],
) -> None:
    previous_unavailable = set(previous_material_fields.get("critical_unavailable_fields", ()))
    current_unavailable = set(current_material_fields.get("critical_unavailable_fields", ()))
    if current_unavailable < previous_unavailable:
        flags.append("critical_field_became_available")
    if previous_unavailable < current_unavailable:
        flags.append("critical_field_became_unavailable")


def _previous_key_fields(previous_source: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if previous_source is None:
        return None
    key_fields = previous_source.get("duplicate_suppression_key_fields")
    if isinstance(key_fields, Mapping):
        return dict(key_fields)
    return build_duplicate_suppression_key_fields(previous_source)


def _previous_material_fields(previous_source: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if previous_source is None:
        return None
    material_fields = previous_source.get("material_review_fields")
    if isinstance(material_fields, Mapping):
        return dict(material_fields)
    return _material_review_fields(previous_source)


def _previous_fingerprint(previous_source: Mapping[str, Any] | None) -> str | None:
    if previous_source is None:
        return None
    fingerprint = previous_source.get("suppression_fingerprint")
    if fingerprint is not None:
        return str(fingerprint)
    key_fields = _previous_key_fields(previous_source)
    material_fields = _previous_material_fields(previous_source)
    return build_suppression_fingerprint(key_fields or {}, material_fields or {})


def _is_incomplete_projection(source: Mapping[str, Any]) -> bool:
    return source.get("trigger_card_projection_status") in {
        "incomplete",
        "INCOMPLETE",
        "no_alert_incomplete_projection",
    } or source.get("full_card_required_fields_status") in {"incomplete", "INCOMPLETE"}


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


def _json_compatible(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _json_compatible(nested) for key, nested in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_compatible(nested) for nested in value]
    if isinstance(value, set):
        return sorted(_json_compatible(nested) for nested in value)
    return deepcopy(value)
