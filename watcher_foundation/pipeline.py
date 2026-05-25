"""Local watch-only watcher pipeline orchestration.

This module composes the existing watcher foundation helpers over
caller-provided dictionaries only. It does not fetch live data, run loops,
emit alerts, write persistent files, or integrate with execution systems.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from watcher_foundation.diagnostics import build_diagnostics
from watcher_foundation.duplicate_suppression import decide_duplicate_suppression
from watcher_foundation.focus_ranking import rank_focus_candidates
from watcher_foundation.headline_news import evaluate_headline_news_policy
from watcher_foundation.models import reject_forbidden_execution_fields
from watcher_foundation.shadow_log import create_shadow_log_record
from watcher_foundation.state_tracker import update_watcher_state
from watcher_foundation.trigger_card import project_trigger_card


PIPELINE_RESULT_FIELDS = (
    "state",
    "trigger_card",
    "diagnostics",
    "duplicate_suppression",
    "focus_ranking",
    "shadow_log_record",
    "watch_only",
    "no_trade_boundary",
)


def run_local_watcher_pipeline(
    observation: Mapping[str, Any],
    *,
    previous_state: Mapping[str, Any] | None = None,
    previous_suppression_state: Mapping[str, Any] | None = None,
    focus_candidates: Sequence[Mapping[str, Any]] | None = None,
    previous_primary_focus_candidate_id: str | None = None,
    headline_news_source: Mapping[str, Any] | None = None,
    event_at: str = "UNCONFIRMED",
) -> dict[str, Any]:
    """Return one local watch-only pipeline result from caller-provided dicts."""

    observation_copy = _copy_mapping("observation", observation)
    previous_state_copy = (
        _copy_mapping("previous_state", previous_state)
        if previous_state is not None
        else None
    )
    previous_suppression_copy = (
        _copy_mapping("previous_suppression_state", previous_suppression_state)
        if previous_suppression_state is not None
        else None
    )
    headline_source_copy = (
        _copy_mapping("headline_news_source", headline_news_source)
        if headline_news_source is not None
        else _headline_source_from_observation(observation_copy)
    )
    focus_candidate_copies = (
        [_copy_mapping("focus_candidate", candidate) for candidate in focus_candidates]
        if focus_candidates is not None
        else None
    )

    _validate_input_boundary(observation_copy)
    if previous_state_copy is not None:
        _validate_input_boundary(previous_state_copy)
    if previous_suppression_copy is not None:
        _validate_input_boundary(previous_suppression_copy)
    if headline_source_copy is not None:
        _validate_input_boundary(headline_source_copy)
    if focus_candidate_copies is not None:
        for candidate in focus_candidate_copies:
            _validate_input_boundary(candidate)

    tracked_state = update_watcher_state(previous_state_copy, observation_copy)
    state = tracked_state.to_dict()

    news_policy = evaluate_headline_news_policy(headline_source_copy)
    state = _apply_headline_news_policy(state, news_policy)

    trigger_card = project_trigger_card(state)
    diagnostics = build_diagnostics(trigger_card)
    duplicate_suppression = decide_duplicate_suppression(
        trigger_card, previous_suppression_copy
    )

    ranking_candidates = (
        [_apply_headline_news_policy(candidate, news_policy) for candidate in focus_candidate_copies]
        if focus_candidate_copies is not None
        else [state]
    )
    focus_ranking = rank_focus_candidates(
        ranking_candidates,
        previous_primary_focus_candidate_id=previous_primary_focus_candidate_id,
    )

    shadow_log_record = create_shadow_log_record(
        {
            "event_type": _shadow_log_event_type(duplicate_suppression),
            "event_at": event_at,
            "state_snapshot": state,
            "previous_state_snapshot": previous_state_copy or "UNCONFIRMED",
            "trigger_card_snapshot": trigger_card,
            "material_change_flags": duplicate_suppression["material_change_flags"]
            or state.get("material_change_flags", ("no_material_change",)),
            "suppression_fingerprint": duplicate_suppression[
                "suppression_fingerprint"
            ],
            "alert_decision": duplicate_suppression["alert_decision"],
            "evidence_refs": diagnostics.get("evidence_refs", ()),
            "unavailable_fields": trigger_card.get("unavailable_fields", ()),
            "watch_only": True,
        }
    )

    result = {
        "state": state,
        "trigger_card": trigger_card,
        "diagnostics": diagnostics,
        "duplicate_suppression": duplicate_suppression,
        "focus_ranking": focus_ranking,
        "shadow_log_record": shadow_log_record,
        "watch_only": True,
        "no_trade_boundary": _no_trade_boundary(state, trigger_card, diagnostics),
    }
    reject_forbidden_execution_fields(result)
    _reject_watch_only_false(result)
    return result


def _copy_mapping(name: str, value: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a caller-provided mapping")
    return deepcopy(dict(value))


def _validate_input_boundary(value: Mapping[str, Any]) -> None:
    reject_forbidden_execution_fields(value)
    _reject_watch_only_false(value)


def _reject_watch_only_false(value: Any, path: tuple[str, ...] = ()) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            if key_text == "watch_only" and nested_value is not True:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(
                    f"Local watcher pipeline must preserve watch_only=True: {dotted_path}"
                )
            _reject_watch_only_false(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_watch_only_false(nested_value, (*path, str(index)))


def _headline_source_from_observation(
    observation: Mapping[str, Any],
) -> dict[str, Any] | None:
    source = observation.get("headline_news_source")
    if source is None:
        source = observation.get("headline_news")
    if source is None:
        return None
    return _copy_mapping("headline_news_source", source)


def _apply_headline_news_policy(
    artifact: Mapping[str, Any],
    news_policy: Mapping[str, Any],
) -> dict[str, Any]:
    enriched = deepcopy(dict(artifact))
    enriched["headline_news_status"] = news_policy["headline_news_status"]
    enriched["headline_news_source_status"] = news_policy["headline_news_source_status"]
    enriched["headline_news_source_confirmed"] = news_policy[
        "headline_news_source_confirmed"
    ]
    enriched["news_evidence_refs"] = deepcopy(news_policy["evidence_refs"])
    enriched["news_policy_reason_codes"] = deepcopy(news_policy["policy_reason_codes"])
    enriched["unavailable_fields"] = _ordered_union(
        enriched.get("unavailable_fields", ()),
        news_policy.get("unavailable_fields", ()),
    )
    enriched["watch_only"] = True
    reject_forbidden_execution_fields(enriched)
    _reject_watch_only_false(enriched)
    return enriched


def _ordered_union(*values: Any) -> list[Any]:
    ordered: list[Any] = []
    for value in values:
        items = value if isinstance(value, (list, tuple)) else (value,)
        for item in items:
            if item not in ordered:
                ordered.append(deepcopy(item))
    return ordered


def _shadow_log_event_type(duplicate_suppression: Mapping[str, Any]) -> str:
    if duplicate_suppression.get("alert_decision") == "suppress_duplicate":
        return "suppressed_duplicate"
    return "state_observation"


def _no_trade_boundary(
    state: Mapping[str, Any],
    trigger_card: Mapping[str, Any],
    diagnostics: Mapping[str, Any],
) -> dict[str, Any]:
    stage = trigger_card.get("stage", state.get("stage"))
    return {
        "watch_only": True,
        "no_live_trade_approval": True,
        "trade_approval": False,
        "live_trade_approval": False,
        "shadow_signal_review_only": stage == "triggered_signal_stage",
        "no_trade_reason": diagnostics.get(
            "no_trade_reason", trigger_card.get("no_trade_reason", "")
        ),
    }
