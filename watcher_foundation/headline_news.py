"""Headline/news policy placeholder for local watch-only watcher artifacts.

This module evaluates only caller-provided source payload dictionaries. It does
not fetch live data, read news, run watcher loops, emit alerts, create reports,
or integrate with broker/account/order/option systems.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.constants import (
    ACCEPTED_HEADLINE_NEWS_STATUSES,
    EVIDENCE_ROWS_UNCONFIRMED,
    NEWS_UNCONFIRMED,
    SOURCE_AS_OF_UNCONFIRMED,
)
from watcher_foundation.models import reject_forbidden_execution_fields


VALID_SOURCE_STATUSES = frozenset(
    {
        "confirmed",
        "source_confirmed",
        "valid_source_confirmed",
    }
)

REQUIRED_HEADLINE_NEWS_POLICY_FIELDS = (
    "headline_news_status",
    "source_status",
    "source_as_of",
    "evidence_refs",
    "unavailable_fields",
    "policy_reason_codes",
    "policy_explanation",
    "watch_only",
)


def evaluate_headline_news_policy(
    source_payload: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a plain dict headline/news policy result.

    Source-confirmed clear/caution/block statuses require a valid caller payload
    with a confirmed source status, source-as-of value, and evidence references.
    Invalid or incomplete source payloads fall back to NEWS_UNCONFIRMED.
    """

    if source_payload is None:
        return _unconfirmed_result(
            "source_missing",
            "No caller-provided headline/news source payload was supplied.",
        )
    if not isinstance(source_payload, Mapping):
        return _unconfirmed_result(
            "source_payload_invalid",
            "Caller-provided headline/news source payload was not a mapping.",
        )

    source = deepcopy(dict(source_payload))
    reject_forbidden_execution_fields(source)
    _reject_watch_only_false(source)

    if not source:
        return _unconfirmed_result(
            "source_payload_empty",
            "Caller-provided headline/news source payload was empty.",
        )

    status = source.get("headline_news_status", source.get("status"))
    source_status = source.get(
        "source_status",
        source.get("headline_news_source_status", "source_unconfirmed"),
    )
    source_as_of = source.get(
        "source_as_of",
        source.get("news_source_as_of", SOURCE_AS_OF_UNCONFIRMED),
    )
    evidence_refs = _as_list(
        source.get("evidence_refs", source.get("news_evidence_refs"))
    )
    unavailable_fields = _as_ordered_strings(source.get("unavailable_fields", ()))

    if status not in ACCEPTED_HEADLINE_NEWS_STATUSES:
        return _unconfirmed_result(
            "source_payload_invalid_status",
            "Caller-provided headline/news status was missing or unsupported.",
            source_status=source_status,
            source_as_of=source_as_of,
            evidence_refs=evidence_refs,
            unavailable_fields=unavailable_fields,
        )

    if not _confirmed_source_status(source_status):
        return _unconfirmed_result(
            "source_status_unconfirmed",
            "Caller-provided headline/news source was not source-confirmed.",
            source_status=source_status,
            source_as_of=source_as_of,
            evidence_refs=evidence_refs,
            unavailable_fields=unavailable_fields,
        )

    if not _available_text(source_as_of):
        return _unconfirmed_result(
            "source_as_of_missing",
            "Caller-provided headline/news source_as_of was unavailable.",
            source_status=source_status,
            source_as_of=source_as_of,
            evidence_refs=evidence_refs,
            unavailable_fields=_with_marker(
                unavailable_fields, SOURCE_AS_OF_UNCONFIRMED
            ),
        )

    if not _available_refs(evidence_refs):
        return _unconfirmed_result(
            "evidence_refs_missing",
            "Caller-provided headline/news evidence_refs were unavailable.",
            source_status=source_status,
            source_as_of=source_as_of,
            evidence_refs=evidence_refs or [EVIDENCE_ROWS_UNCONFIRMED],
            unavailable_fields=_with_marker(
                unavailable_fields, EVIDENCE_ROWS_UNCONFIRMED
            ),
        )

    result = {
        "headline_news_status": status,
        "source_status": str(source_status),
        "headline_news_source_status": str(source_status),
        "headline_news_source_confirmed": True,
        "source_as_of": str(source_as_of),
        "evidence_refs": deepcopy(evidence_refs),
        "unavailable_fields": unavailable_fields,
        "policy_reason_codes": [_accepted_reason_code(status)],
        "policy_explanation": _accepted_explanation(status),
        "watch_only": True,
        "news_blocker": status == "NEWS_BLOCK",
        "live_trade_approval": False,
        "trade_approval": False,
    }
    reject_forbidden_execution_fields(result)
    return result


def create_headline_news_policy(
    source_payload: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Compatibility alias for headline/news policy result creation."""

    return evaluate_headline_news_policy(source_payload)


def _unconfirmed_result(
    reason_code: str,
    explanation: str,
    *,
    source_status: Any = "source_unconfirmed",
    source_as_of: Any = SOURCE_AS_OF_UNCONFIRMED,
    evidence_refs: Any = None,
    unavailable_fields: Any = None,
) -> dict[str, Any]:
    refs = _as_list(evidence_refs)
    if not refs:
        refs = [EVIDENCE_ROWS_UNCONFIRMED]
    unavailable = _as_ordered_strings(unavailable_fields or ())
    unavailable = _with_marker(unavailable, NEWS_UNCONFIRMED)
    if not _available_text(source_as_of):
        unavailable = _with_marker(unavailable, SOURCE_AS_OF_UNCONFIRMED)
    if not _available_refs(refs):
        unavailable = _with_marker(unavailable, EVIDENCE_ROWS_UNCONFIRMED)

    result = {
        "headline_news_status": NEWS_UNCONFIRMED,
        "source_status": str(source_status),
        "headline_news_source_status": str(source_status),
        "headline_news_source_confirmed": False,
        "source_as_of": str(source_as_of),
        "evidence_refs": refs,
        "unavailable_fields": unavailable,
        "policy_reason_codes": [reason_code, "news_unconfirmed_default"],
        "policy_explanation": explanation
        + " NEWS_UNCONFIRMED is not a news blocker by itself.",
        "watch_only": True,
        "news_blocker": False,
        "live_trade_approval": False,
        "trade_approval": False,
    }
    reject_forbidden_execution_fields(result)
    return result


def _reject_watch_only_false(value: Any, path: tuple[str, ...] = ()) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            if key_text == "watch_only" and nested_value is not True:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(
                    "Headline/news policy must preserve watch_only=True: "
                    f"{dotted_path}"
                )
            _reject_watch_only_false(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_watch_only_false(nested_value, (*path, str(index)))


def _confirmed_source_status(value: Any) -> bool:
    return str(value).lower() in VALID_SOURCE_STATUSES


def _available_text(value: Any) -> bool:
    if value is None:
        return False
    text = str(value).strip()
    return bool(text) and text not in {
        "UNCONFIRMED",
        SOURCE_AS_OF_UNCONFIRMED,
    } and not text.endswith("_UNCONFIRMED")


def _available_refs(value: Any) -> bool:
    refs = _as_list(value)
    if not refs:
        return False
    return all(_available_text(ref) for ref in refs)


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return deepcopy(value)
    if isinstance(value, tuple):
        return [deepcopy(item) for item in value]
    return [deepcopy(value)]


def _as_ordered_strings(value: Any) -> list[str]:
    ordered: list[str] = []
    for item in _as_list(value):
        item_text = str(item)
        if item_text not in ordered:
            ordered.append(item_text)
    return ordered


def _with_marker(values: list[str], marker: str) -> list[str]:
    output = list(values)
    if marker not in output:
        output.append(marker)
    return output


def _accepted_reason_code(status: str) -> str:
    return {
        "NEWS_CLEAR": "news_clear_source_confirmed",
        "NEWS_CAUTION": "news_caution_source_confirmed",
        "NEWS_BLOCK": "news_block_source_confirmed",
        "NEWS_UNCONFIRMED": "news_unconfirmed_source_confirmed",
    }[status]


def _accepted_explanation(status: str) -> str:
    if status == "NEWS_CLEAR":
        return "Caller-provided source-confirmed headline/news status is NEWS_CLEAR."
    if status == "NEWS_CAUTION":
        return (
            "Caller-provided source-confirmed headline/news status is "
            "NEWS_CAUTION; this is context only and does not approve a trade."
        )
    if status == "NEWS_BLOCK":
        return (
            "Caller-provided source-confirmed headline/news status is NEWS_BLOCK; "
            "this preserves context/no-trade discipline and does not approve a trade."
        )
    return (
        "Caller-provided source-confirmed headline/news status is "
        "NEWS_UNCONFIRMED and is not a news blocker by itself."
    )
