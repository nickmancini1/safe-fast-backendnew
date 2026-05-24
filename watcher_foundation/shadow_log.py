"""Append-only shadow-log helpers for local watch-only watcher review.

This module creates inert JSON-compatible records from caller-provided watcher
state/card artifacts. It does not fetch live data, run watcher loops, emit phone
alerts, create runtime schema files, write repo logs, or integrate with broker,
account, order, option, deployment, or production systems.
"""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import asdict, is_dataclass
from typing import Any, Mapping, TextIO

from watcher_foundation.constants import (
    DEFAULT_UNAVAILABLE_FIELDS,
    NEWS_UNCONFIRMED,
    SOURCE_AS_OF_UNCONFIRMED,
)
from watcher_foundation.models import reject_forbidden_execution_fields


SHADOW_LOG_SCHEMA_VERSION = "shadow_log_v1"
DEFAULT_REVIEW_LABEL = "UNREVIEWED"

ALLOWED_SHADOW_LOG_EVENT_TYPES = (
    "state_observation",
    "lifecycle_transition",
    "trigger_card_snapshot",
    "alert_decision",
    "suppressed_duplicate",
    "blocker_caution_change",
    "unavailable_field_change",
    "evidence_quality_change",
    "best_candidate_snapshot",
    "manual_review_label",
    "shadow_review_summary",
)

REQUIRED_SHADOW_LOG_FIELDS = (
    "schema_version",
    "log_record_id",
    "event_type",
    "event_at",
    "source_as_of",
    "watch_session_id",
    "candidate_id",
    "symbol",
    "setup_type",
    "direction",
    "state_version",
    "state_snapshot",
    "previous_state_snapshot",
    "trigger_card_snapshot",
    "material_change_flags",
    "suppression_fingerprint",
    "alert_decision",
    "evidence_refs",
    "unavailable_fields",
    "review_label",
    "review_notes",
    "watch_only",
)


def create_shadow_log_record(
    record_input: Mapping[str, Any] | None = None,
    **overrides: Any,
) -> dict[str, Any]:
    """Return a JSON-compatible local shadow-log record dict.

    Caller input is copied and validated. Missing fields are explicit
    unconfirmed/review defaults so unavailable facts are not invented.
    """

    source: dict[str, Any] = {}
    if record_input is not None:
        source.update(_to_plain_dict(record_input))
    source.update(overrides)

    reject_forbidden_execution_fields(source)
    _reject_watch_only_false(source)

    state_snapshot = _snapshot(source.get("state_snapshot", {}))
    previous_state_snapshot = _snapshot(
        source.get("previous_state_snapshot", "UNCONFIRMED")
    )
    trigger_card_snapshot = _snapshot(source.get("trigger_card_snapshot", {}))

    for snapshot in (state_snapshot, previous_state_snapshot, trigger_card_snapshot):
        reject_forbidden_execution_fields(snapshot)
        _reject_watch_only_false(snapshot)

    event_type = source.get("event_type", "state_observation")
    if event_type not in ALLOWED_SHADOW_LOG_EVENT_TYPES:
        raise ValueError(f"Unsupported shadow-log event_type: {event_type}")

    record = {
        "schema_version": source.get(
            "schema_version", SHADOW_LOG_SCHEMA_VERSION
        ),
        "log_record_id": source.get("log_record_id", "UNCONFIRMED"),
        "event_type": event_type,
        "event_at": source.get("event_at", "UNCONFIRMED"),
        "source_as_of": source.get(
            "source_as_of",
            _first_available(
                state_snapshot,
                trigger_card_snapshot,
                "source_as_of",
                default=SOURCE_AS_OF_UNCONFIRMED,
            ),
        ),
        "watch_session_id": source.get(
            "watch_session_id",
            _first_available(state_snapshot, trigger_card_snapshot, "watch_session_id"),
        ),
        "candidate_id": source.get(
            "candidate_id",
            _first_available(state_snapshot, trigger_card_snapshot, "candidate_id"),
        ),
        "symbol": source.get(
            "symbol", _first_available(state_snapshot, trigger_card_snapshot, "symbol")
        ),
        "setup_type": source.get(
            "setup_type",
            _first_available(state_snapshot, trigger_card_snapshot, "setup_type"),
        ),
        "direction": source.get(
            "direction",
            _first_available(state_snapshot, trigger_card_snapshot, "direction"),
        ),
        "state_version": source.get(
            "state_version",
            _first_available(state_snapshot, trigger_card_snapshot, "state_version"),
        ),
        "state_snapshot": state_snapshot,
        "previous_state_snapshot": previous_state_snapshot,
        "trigger_card_snapshot": trigger_card_snapshot,
        "material_change_flags": _as_json_list(
            source.get(
                "material_change_flags",
                _first_available(
                    state_snapshot,
                    trigger_card_snapshot,
                    "material_change_flags",
                    default=("no_material_change",),
                ),
            )
        ),
        "suppression_fingerprint": source.get(
            "suppression_fingerprint",
            _first_available(
                state_snapshot,
                trigger_card_snapshot,
                "suppression_fingerprint",
            ),
        ),
        "alert_decision": source.get("alert_decision", "no_alert_watch_only"),
        "evidence_refs": _as_json_list(source.get("evidence_refs", ())),
        "unavailable_fields": _as_json_list(
            source.get(
                "unavailable_fields",
                _first_available(
                    state_snapshot,
                    trigger_card_snapshot,
                    "unavailable_fields",
                    default=DEFAULT_UNAVAILABLE_FIELDS,
                ),
            )
        ),
        "review_label": source.get("review_label", DEFAULT_REVIEW_LABEL),
        "review_notes": source.get("review_notes", ""),
        "watch_only": source.get("watch_only", True),
    }

    _preserve_news_unconfirmed(record)
    reject_forbidden_execution_fields(record)
    _reject_watch_only_false(record)
    _assert_json_compatible(record)
    return record


def serialize_shadow_log_line(record: Mapping[str, Any]) -> str:
    """Serialize one record as exactly one JSONL line."""

    record_dict = create_shadow_log_record(record)
    return json.dumps(record_dict, sort_keys=True, separators=(",", ":")) + "\n"


def append_shadow_log_line(file_like: TextIO, record: Mapping[str, Any]) -> None:
    """Append one serialized shadow-log line to an already-open file-like object."""

    file_like.write(serialize_shadow_log_line(record))


def _to_plain_dict(value: Any) -> dict[str, Any]:
    if hasattr(value, "to_dict"):
        return deepcopy(value.to_dict())
    if is_dataclass(value):
        return deepcopy(asdict(value))
    if isinstance(value, Mapping):
        return deepcopy(dict(value))
    raise TypeError("record_input must be a mapping or dict-like watcher artifact")


def _snapshot(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return deepcopy(value.to_dict())
    if is_dataclass(value):
        return _json_compatible(deepcopy(asdict(value)))
    return _json_compatible(deepcopy(value))


def _json_compatible(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _json_compatible(nested) for key, nested in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_compatible(nested) for nested in value]
    return value


def _as_json_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return _json_compatible(value)
    if isinstance(value, tuple):
        return _json_compatible(list(value))
    return [_json_compatible(value)]


def _first_available(
    first: Any,
    second: Any,
    field_name: str,
    *,
    default: Any = "UNCONFIRMED",
) -> Any:
    for snapshot in (first, second):
        if isinstance(snapshot, Mapping) and field_name in snapshot:
            value = snapshot[field_name]
            if value is not None:
                return deepcopy(value)
    return deepcopy(default)


def _reject_watch_only_false(value: Any, path: tuple[str, ...] = ()) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            if key_text == "watch_only" and nested_value is not True:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Shadow-log records must remain watch_only=True: {dotted_path}")
            _reject_watch_only_false(nested_value, (*path, key_text))
    elif isinstance(value, list):
        for index, nested_value in enumerate(value):
            _reject_watch_only_false(nested_value, (*path, str(index)))


def _preserve_news_unconfirmed(record: dict[str, Any]) -> None:
    for snapshot_name in ("state_snapshot", "trigger_card_snapshot"):
        snapshot = record[snapshot_name]
        if isinstance(snapshot, dict) and not snapshot.get("headline_news_status"):
            snapshot["headline_news_status"] = NEWS_UNCONFIRMED


def _assert_json_compatible(record: Mapping[str, Any]) -> None:
    try:
        json.dumps(record)
    except (TypeError, ValueError) as exc:
        raise ValueError("Shadow-log record must be JSON-compatible") from exc
