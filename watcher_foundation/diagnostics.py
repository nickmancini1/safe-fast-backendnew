"""Diagnostics explanations for local watch-only watcher artifacts.

This module explains caller-provided watcher state/card dictionaries only. It
does not fetch live data, run watcher loops, emit alerts, write logs, create
runtime schema files, or integrate with broker/account/order/option systems.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, is_dataclass
from typing import Any, Mapping

from watcher_foundation.constants import (
    CONFIRMATION_TIMEFRAME_RULE_UNCONFIRMED,
    DISTANCE_TO_TRIGGER_UNCONFIRMED,
    EVIDENCE_ROWS_UNCONFIRMED,
    FRESHNESS_UNCONFIRMED,
    INVALIDATION_UNCONFIRMED,
    NEWS_UNCONFIRMED,
    SESSION_DATE_UNCONFIRMED,
    SOURCE_AS_OF_UNCONFIRMED,
    TRIGGER_LEVEL_UNCONFIRMED,
)
from watcher_foundation.models import reject_forbidden_execution_fields


DIAGNOSTIC_REASON_CODE_GROUPS = (
    "setup_identity",
    "lifecycle_stage",
    "trigger_status",
    "blocker",
    "caution",
    "freshness",
    "stale_spent",
    "unavailable_field",
    "evidence_quality",
    "focus_ranking",
    "duplicate_suppression",
    "headline_news_status",
    "no_trade_boundary",
    "next_condition",
)

CRITICAL_DIAGNOSTIC_FIELDS = (
    "trigger_level_or_zone",
    "confirmation_timeframe_rule",
    "distance_to_trigger",
    "invalidation_level_or_condition",
    "source_as_of",
    "evidence_rows",
    "regular_session_date",
    "fresh_stale_spent_state",
    "headline_news_status",
)

UNCONFIRMED_VALUES = frozenset(
    {
        "",
        None,
        "UNCONFIRMED",
        TRIGGER_LEVEL_UNCONFIRMED,
        CONFIRMATION_TIMEFRAME_RULE_UNCONFIRMED,
        DISTANCE_TO_TRIGGER_UNCONFIRMED,
        INVALIDATION_UNCONFIRMED,
        SOURCE_AS_OF_UNCONFIRMED,
        EVIDENCE_ROWS_UNCONFIRMED,
        SESSION_DATE_UNCONFIRMED,
        FRESHNESS_UNCONFIRMED,
        NEWS_UNCONFIRMED,
        "unconfirmed",
    }
)

UNAVAILABLE_FIELD_REASON_CODES = {
    "trigger_level_or_zone": "unavailable_field.trigger_level_unconfirmed",
    "trigger_level": "unavailable_field.trigger_level_unconfirmed",
    TRIGGER_LEVEL_UNCONFIRMED: "unavailable_field.trigger_level_unconfirmed",
    "distance_to_trigger": "unavailable_field.distance_to_trigger_unconfirmed",
    DISTANCE_TO_TRIGGER_UNCONFIRMED: (
        "unavailable_field.distance_to_trigger_unconfirmed"
    ),
    "invalidation_level_or_condition": "unavailable_field.invalidation_unconfirmed",
    "invalidation": "unavailable_field.invalidation_unconfirmed",
    INVALIDATION_UNCONFIRMED: "unavailable_field.invalidation_unconfirmed",
    "source_as_of": "unavailable_field.source_as_of_unconfirmed",
    SOURCE_AS_OF_UNCONFIRMED: "unavailable_field.source_as_of_unconfirmed",
    "evidence_rows": "unavailable_field.evidence_rows_unconfirmed",
    EVIDENCE_ROWS_UNCONFIRMED: "unavailable_field.evidence_rows_unconfirmed",
    "regular_session_date": "unavailable_field.session_date_unconfirmed",
    "session_date": "unavailable_field.session_date_unconfirmed",
    SESSION_DATE_UNCONFIRMED: "unavailable_field.session_date_unconfirmed",
    "fresh_stale_spent_state": "unavailable_field.freshness_unconfirmed",
    "freshness_state": "unavailable_field.freshness_unconfirmed",
    FRESHNESS_UNCONFIRMED: "unavailable_field.freshness_unconfirmed",
    "headline_news_status": "unavailable_field.news_unconfirmed",
    NEWS_UNCONFIRMED: "unavailable_field.news_unconfirmed",
}


def build_diagnostics(
    artifact: Mapping[str, Any] | Any,
    *,
    focus_context: Mapping[str, Any] | Any | None = None,
    duplicate_suppression_context: Mapping[str, Any] | Any | None = None,
) -> dict[str, Any]:
    """Return a plain dict diagnostics result for one watch-only artifact."""

    source = _to_plain_dict(artifact)
    focus = _to_plain_dict(focus_context) if focus_context is not None else None
    suppression = (
        _to_plain_dict(duplicate_suppression_context)
        if duplicate_suppression_context is not None
        else None
    )

    reject_forbidden_execution_fields(source)
    _reject_watch_only_false(source)
    if focus is not None:
        reject_forbidden_execution_fields(focus)
        _reject_watch_only_false(focus)
    if suppression is not None:
        reject_forbidden_execution_fields(suppression)
        _reject_watch_only_false(suppression)

    normalized = _normalize_source(source)
    focus_reason = _focus_rank_reason(normalized, focus)
    suppression_reason = _suppression_reason(suppression)
    reason_codes = _reason_codes(normalized, focus, suppression)
    no_trade_reason = _no_trade_reason(normalized, reason_codes)

    result = {
        "diagnostic_reason_codes": reason_codes,
        "diagnostic_explanation": _diagnostic_explanation(
            normalized,
            no_trade_reason=no_trade_reason,
            focus_rank_reason=focus_reason,
            suppression_reason=suppression_reason,
        ),
        "diagnostic_scope": _diagnostic_scope(reason_codes),
        "evidence_refs": _evidence_refs(normalized),
        "unavailable_fields": _as_list(normalized.get("unavailable_fields", ())),
        "no_trade_reason": no_trade_reason,
        "next_check_or_next_alert_condition": normalized[
            "next_check_or_next_alert_condition"
        ],
        "focus_rank_reason": focus_reason,
        "suppression_reason": suppression_reason,
        "watch_only": True,
        "headline_news_status": normalized["headline_news_status"],
        "setup_type": normalized["setup_type"],
        "stage": normalized["stage"],
        "trigger_status": normalized["trigger_status"],
        "fresh_stale_spent_state": normalized["fresh_stale_spent_state"],
    }
    if "evidence_rows" in normalized:
        result["evidence_rows"] = _as_list(normalized["evidence_rows"])

    reject_forbidden_execution_fields(result)
    return result


def create_diagnostics(
    artifact: Mapping[str, Any] | Any,
    *,
    focus_context: Mapping[str, Any] | Any | None = None,
    duplicate_suppression_context: Mapping[str, Any] | Any | None = None,
) -> dict[str, Any]:
    """Compatibility alias for diagnostics result creation."""

    return build_diagnostics(
        artifact,
        focus_context=focus_context,
        duplicate_suppression_context=duplicate_suppression_context,
    )


def _to_plain_dict(value: Mapping[str, Any] | Any) -> dict[str, Any]:
    if hasattr(value, "to_dict"):
        return deepcopy(value.to_dict())
    if is_dataclass(value):
        return deepcopy(asdict(value))
    if isinstance(value, Mapping):
        return deepcopy(dict(value))
    raise TypeError("diagnostics input must be a mapping or dict-like artifact")


def _reject_watch_only_false(value: Any, path: tuple[str, ...] = ()) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            if key_text == "watch_only" and nested_value is not True:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(
                    f"Diagnostics must preserve watch_only=True: {dotted_path}"
                )
            _reject_watch_only_false(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_watch_only_false(nested_value, (*path, str(index)))


def _normalize_source(source: Mapping[str, Any]) -> dict[str, Any]:
    normalized = deepcopy(dict(source))
    normalized["watch_only"] = True
    normalized["setup_type"] = normalized.get("setup_type", "UNCONFIRMED")
    normalized["direction"] = normalized.get("direction", "UNCONFIRMED")
    normalized["stage"] = normalized.get("stage", "unavailable/unconfirmed")
    normalized["trigger_status"] = normalized.get("trigger_status", "unconfirmed")
    normalized["trigger_level_or_zone"] = normalized.get(
        "trigger_level_or_zone",
        normalized.get("trigger_level", TRIGGER_LEVEL_UNCONFIRMED),
    )
    normalized["confirmation_timeframe_rule"] = normalized.get(
        "confirmation_timeframe_rule", CONFIRMATION_TIMEFRAME_RULE_UNCONFIRMED
    )
    normalized["distance_to_trigger"] = normalized.get(
        "distance_to_trigger", DISTANCE_TO_TRIGGER_UNCONFIRMED
    )
    normalized["invalidation_level_or_condition"] = normalized.get(
        "invalidation_level_or_condition",
        normalized.get("invalidation", INVALIDATION_UNCONFIRMED),
    )
    normalized["source_as_of"] = normalized.get(
        "source_as_of", SOURCE_AS_OF_UNCONFIRMED
    )
    normalized["regular_session_date"] = normalized.get(
        "regular_session_date", normalized.get("session_date", SESSION_DATE_UNCONFIRMED)
    )
    normalized["evidence_rows"] = _as_list(
        normalized.get("evidence_rows", (EVIDENCE_ROWS_UNCONFIRMED,))
    )
    normalized["evidence_refs"] = _as_list(
        normalized.get("evidence_refs", normalized["evidence_rows"])
    )
    normalized["fresh_stale_spent_state"] = normalized.get(
        "fresh_stale_spent_state",
        normalized.get("freshness_state", "unconfirmed"),
    )
    if normalized["fresh_stale_spent_state"] == FRESHNESS_UNCONFIRMED:
        normalized["fresh_stale_spent_state"] = "unconfirmed"
    normalized["blockers"] = _as_list(normalized.get("blockers", ()))
    normalized["cautions"] = _as_list(normalized.get("cautions", ()))
    normalized["unavailable_fields"] = _as_list(
        normalized.get("unavailable_fields", ())
    )
    normalized["headline_news_status"] = (
        normalized.get("headline_news_status") or NEWS_UNCONFIRMED
    )
    normalized["evidence_quality"] = normalized.get("evidence_quality", "unconfirmed")
    normalized["no_trade_reason"] = normalized.get("no_trade_reason", "")
    normalized["next_check_or_next_alert_condition"] = normalized.get(
        "next_check_or_next_alert_condition", "UNCONFIRMED"
    )
    return normalized


def _reason_codes(
    source: Mapping[str, Any],
    focus: Mapping[str, Any] | None,
    suppression: Mapping[str, Any] | None,
) -> dict[str, list[str]]:
    codes = {group: [] for group in DIAGNOSTIC_REASON_CODE_GROUPS}

    _append(codes["setup_identity"], _setup_identity_code(source))
    _append(codes["lifecycle_stage"], _lifecycle_stage_code(source))
    _append(codes["trigger_status"], _trigger_status_code(source))
    _append(codes["blocker"], _blocker_codes(source))
    _append(codes["caution"], _caution_codes(source))
    _append(codes["freshness"], _freshness_code(source))
    _append(codes["stale_spent"], _stale_spent_codes(source))
    _append(codes["unavailable_field"], _unavailable_field_codes(source))
    _append(codes["evidence_quality"], _evidence_quality_code(source))
    _append(codes["focus_ranking"], _focus_ranking_codes(source, focus))
    _append(codes["duplicate_suppression"], _duplicate_suppression_codes(suppression))
    _append(codes["headline_news_status"], _headline_news_status_code(source))
    _append(codes["no_trade_boundary"], _no_trade_boundary_codes(source))
    _append(codes["next_condition"], _next_condition_codes(source, suppression))

    return codes


def _append(target: list[str], values: str | list[str]) -> None:
    if isinstance(values, str):
        values = [values]
    for value in values:
        if value and value not in target:
            target.append(value)


def _setup_identity_code(source: Mapping[str, Any]) -> str:
    setup_type = source["setup_type"]
    return {
        "Ideal": "setup_identity.confirmed_ideal",
        "Clean Fast Break": "setup_identity.confirmed_clean_fast_break",
        "Continuation": "setup_identity.confirmed_continuation",
    }.get(setup_type, "setup_identity.unconfirmed")


def _lifecycle_stage_code(source: Mapping[str, Any]) -> str:
    return {
        "forming/developing": "lifecycle_stage.forming_developing",
        "near-trigger": "lifecycle_stage.near_trigger",
        "pending_completed_candle_approval": (
            "lifecycle_stage.pending_completed_candle_approval"
        ),
        "triggered_signal_stage": (
            "lifecycle_stage.triggered_signal_stage_shadow_only"
        ),
        "blocked/no-trade": "lifecycle_stage.blocked_no_trade",
        "stale/spent/no-fresh-trigger": (
            "lifecycle_stage.stale_spent_no_fresh_trigger"
        ),
        "rebuilding": "lifecycle_stage.rebuilding",
    }.get(source["stage"], "lifecycle_stage.unavailable_unconfirmed")


def _trigger_status_code(source: Mapping[str, Any]) -> str:
    return {
        "no_valid_trigger": "trigger_status.no_valid_trigger",
        "waiting_for_trigger": "trigger_status.waiting_for_trigger",
        "near_trigger": "trigger_status.near_trigger",
        "pending_completed_candle": "trigger_status.pending_completed_candle",
        "triggered": "trigger_status.triggered_shadow_only",
        "failed_hold": "trigger_status.failed_hold",
        "stale": "trigger_status.stale",
        "spent": "trigger_status.spent",
    }.get(source["trigger_status"], "trigger_status.unconfirmed")


def _blocker_codes(source: Mapping[str, Any]) -> list[str]:
    codes: list[str] = []
    blockers = source["blockers"]
    if blockers or source.get("primary_blocker") not in {None, "", "UNCONFIRMED"}:
        codes.append("blocker.primary_blocker_active")
    else:
        codes.append("blocker.none_confirmed")
    missing = _critical_unavailable_fields(source)
    if "trigger_level_or_zone" in missing:
        codes.append("blocker.trigger_missing")
    if "invalidation_level_or_condition" in missing:
        codes.append("blocker.invalidation_missing")
    if "fresh_stale_spent_state" in missing:
        codes.append("blocker.freshness_missing")
    if "evidence_rows" in missing:
        codes.append("blocker.evidence_missing")
    if "source_as_of" in missing:
        codes.append("blocker.source_missing")
    if source["headline_news_status"] == "NEWS_BLOCK" and _source_confirmed_news(source):
        codes.append("blocker.news_source_confirmed_block")
    return codes


def _caution_codes(source: Mapping[str, Any]) -> list[str]:
    codes = ["caution.none_confirmed"] if not source["cautions"] else ["caution.context_risk"]
    if source["evidence_quality"] == "partial":
        codes.append("caution.evidence_partial")
    if _noncritical_unavailable_fields(source):
        codes.append("caution.unavailable_noncritical_field")
    if source["headline_news_status"] == "NEWS_CAUTION" and _source_confirmed_news(source):
        codes.append("caution.news_source_confirmed_caution")
    return codes


def _freshness_code(source: Mapping[str, Any]) -> str:
    freshness = source["fresh_stale_spent_state"]
    return {
        "fresh": "freshness.fresh_current_session",
        "prior-session": "freshness.prior_session",
        "rebuilding": "freshness.rebuilding",
    }.get(freshness, "freshness.unconfirmed")


def _stale_spent_codes(source: Mapping[str, Any]) -> list[str]:
    freshness = source["fresh_stale_spent_state"]
    if source["stage"] == "stale/spent/no-fresh-trigger" or source["trigger_status"] == "stale" or freshness == "stale":
        return ["stale_spent.stale_no_fresh_trigger"]
    if source["trigger_status"] == "spent" or freshness == "spent":
        return ["stale_spent.spent_no_fresh_trigger"]
    if freshness == "prior-session":
        return ["stale_spent.prior_session_no_fresh_trigger"]
    if freshness == "rebuilding":
        return ["stale_spent.rebuilding_required"]
    return []


def _unavailable_field_codes(source: Mapping[str, Any]) -> list[str]:
    codes: list[str] = []
    for field_name in _critical_unavailable_fields(source):
        _append(codes, UNAVAILABLE_FIELD_REASON_CODES.get(field_name, ""))
    for field in source["unavailable_fields"]:
        _append(codes, UNAVAILABLE_FIELD_REASON_CODES.get(str(field), ""))
    if source["headline_news_status"] == NEWS_UNCONFIRMED:
        _append(codes, "unavailable_field.news_unconfirmed")
    return codes


def _evidence_quality_code(source: Mapping[str, Any]) -> str:
    return {
        "deterministic": "evidence_quality.deterministic",
        "partial": "evidence_quality.partial",
        "missing": "evidence_quality.missing",
    }.get(source["evidence_quality"], "evidence_quality.unconfirmed")


def _focus_ranking_codes(
    source: Mapping[str, Any], focus: Mapping[str, Any] | None
) -> list[str]:
    if focus is None:
        return []
    bucket = _focus_rank_bucket(source, focus)
    codes = {
        "primary_focus": "focus_ranking.primary_focus_selected",
        "secondary_watch": "focus_ranking.secondary_watch",
        "watch_only_blocked": "focus_ranking.watch_only_blocked",
        "stale_spent_context": "focus_ranking.stale_spent_context",
        "unavailable_unconfirmed": "focus_ranking.unavailable_unconfirmed",
    }
    result = [codes.get(bucket, "focus_ranking.unavailable_unconfirmed")]
    for reason in _as_list(_focus_candidate(source, focus).get("demotion_reason_codes", ())):
        if "block" in str(reason):
            result.append("focus_ranking.demoted_by_blocker")
        elif "stale" in str(reason) or "fresh" in str(reason):
            result.append("focus_ranking.demoted_by_stale_spent")
        elif "evidence" in str(reason):
            result.append("focus_ranking.demoted_by_evidence")
        elif "unavailable" in str(reason) or "critical" in str(reason):
            result.append("focus_ranking.demoted_by_unavailable_fields")
    return result


def _duplicate_suppression_codes(suppression: Mapping[str, Any] | None) -> list[str]:
    if suppression is None:
        return []
    decision = suppression.get("alert_decision")
    reason = str(suppression.get("suppression_reason", ""))
    material_flags = _as_list(suppression.get("material_change_flags", ()))
    codes: list[str] = []
    if decision == "emit_material_change":
        codes.append("duplicate_suppression.emit_material_change")
    elif decision == "suppress_duplicate":
        codes.append("duplicate_suppression.suppress_same_state_repeat")
    elif decision == "no_alert_no_material_change" or "no_material_change" in reason:
        codes.append("duplicate_suppression.no_alert_no_material_change")
    for flag in material_flags:
        flag_text = str(flag)
        mapped = {
            "stage_changed": "duplicate_suppression.break_stage_changed",
            "trigger_status_changed": (
                "duplicate_suppression.break_trigger_status_changed"
            ),
            "freshness_changed": "duplicate_suppression.break_freshness_changed",
            "primary_blocker_changed": (
                "duplicate_suppression.break_blocker_changed"
            ),
            "evidence_quality_changed": (
                "duplicate_suppression.break_evidence_quality_changed"
            ),
            "critical_field_became_available": (
                "duplicate_suppression.break_unavailable_field_changed"
            ),
            "critical_field_became_unavailable": (
                "duplicate_suppression.break_unavailable_field_changed"
            ),
            "best_candidate_changed": "duplicate_suppression.break_focus_changed",
        }.get(flag_text)
        _append(codes, mapped or "")
    return codes


def _headline_news_status_code(source: Mapping[str, Any]) -> str:
    status = source["headline_news_status"]
    if status == "NEWS_CLEAR" and _source_confirmed_news(source):
        return "headline_news_status.news_clear_source_confirmed"
    if status == "NEWS_CAUTION" and _source_confirmed_news(source):
        return "headline_news_status.news_caution_source_confirmed"
    if status == "NEWS_BLOCK" and _source_confirmed_news(source):
        return "headline_news_status.news_block_source_confirmed"
    return "headline_news_status.news_unconfirmed"


def _no_trade_boundary_codes(source: Mapping[str, Any]) -> list[str]:
    codes = ["no_trade_boundary.watch_only", "no_trade_boundary.no_live_trade_approval"]
    if source["blockers"] or source["stage"] == "blocked/no-trade":
        codes.append("no_trade_boundary.blocker_active")
    if _stale_spent_codes(source):
        codes.append("no_trade_boundary.stale_spent")
    if _critical_unavailable_fields(source):
        codes.append("no_trade_boundary.unavailable_critical_field")
    if source["evidence_quality"] in {"unconfirmed", "missing"}:
        codes.append("no_trade_boundary.evidence_unconfirmed")
    if source["stage"] == "triggered_signal_stage":
        codes.append("no_trade_boundary.triggered_shadow_only")
    return codes


def _next_condition_codes(
    source: Mapping[str, Any], suppression: Mapping[str, Any] | None
) -> list[str]:
    codes: list[str] = []
    if _critical_unavailable_fields(source):
        codes.append("next_condition.resolve_unavailable_field")
    if source["trigger_status"] in {"no_valid_trigger", "unconfirmed"}:
        codes.append("next_condition.wait_for_defined_trigger")
    if source["trigger_status"] == "pending_completed_candle":
        codes.append("next_condition.wait_for_completed_candle_rule")
    if source["blockers"] or source["stage"] == "blocked/no-trade":
        codes.append("next_condition.resolve_blocker")
    if source["stage"] == "rebuilding" or _stale_spent_codes(source):
        codes.append("next_condition.wait_for_rebuilt_structure")
    if suppression and suppression.get("alert_decision") == "suppress_duplicate":
        codes.append("next_condition.no_repeat_alert_until_change")
    if not codes:
        codes.append("next_condition.new_material_change_required")
    return codes


def _no_trade_reason(
    source: Mapping[str, Any], reason_codes: Mapping[str, list[str]]
) -> str:
    if source.get("no_trade_reason"):
        return str(source["no_trade_reason"])
    if reason_codes["stale_spent"]:
        return "watch_only_no_fresh_trigger_no_trade"
    if source["stage"] == "triggered_signal_stage":
        return "triggered_for_shadow_signal_review_only_no_live_trade_approval"
    if reason_codes["unavailable_field"]:
        return "watch_only_unconfirmed_trigger_invalidation_source_or_evidence_no_trade"
    return "watch_only_no_live_trade_approval"


def _diagnostic_explanation(
    source: Mapping[str, Any],
    *,
    no_trade_reason: str,
    focus_rank_reason: str,
    suppression_reason: str,
) -> str:
    parts = [
        f"{source['symbol'] if source.get('symbol') else 'UNCONFIRMED'} is "
        f"{source['setup_type']} in stage {source['stage']} with trigger status "
        f"{source['trigger_status']}.",
    ]
    if source["stage"] == "triggered_signal_stage":
        parts.append(
            "triggered_signal_stage is shadow signal review only, not live trade approval."
        )
    if _stale_spent_codes(source):
        parts.append("The candidate has no fresh trigger and remains no-trade.")
    missing = _critical_unavailable_fields(source)
    if missing:
        parts.append(
            "Critical fields are unconfirmed: " + ", ".join(missing) + "."
        )
    if source["headline_news_status"] == NEWS_UNCONFIRMED:
        parts.append(
            "Headline/news status is NEWS_UNCONFIRMED and is not a news blocker by itself."
        )
    if no_trade_reason:
        parts.append(f"No-trade boundary: {no_trade_reason}.")
    if focus_rank_reason:
        parts.append(f"Focus ranking: {focus_rank_reason}.")
    if suppression_reason:
        parts.append(f"Duplicate suppression: {suppression_reason}.")
    next_condition = source["next_check_or_next_alert_condition"]
    if next_condition:
        parts.append(f"Next condition: {next_condition}.")
    return " ".join(parts)


def _diagnostic_scope(reason_codes: Mapping[str, list[str]]) -> list[str]:
    return [group for group, codes in reason_codes.items() if codes]


def _evidence_refs(source: Mapping[str, Any]) -> list[Any]:
    refs = _as_list(source.get("evidence_refs", ()))
    if refs:
        return refs
    return _as_list(source.get("evidence_rows", (EVIDENCE_ROWS_UNCONFIRMED,)))


def _focus_rank_reason(
    source: Mapping[str, Any], focus: Mapping[str, Any] | None
) -> str:
    if focus is None:
        return ""
    candidate = _focus_candidate(source, focus)
    if candidate.get("focus_rank_reason"):
        return str(candidate["focus_rank_reason"])
    if focus.get("focus_rank_reason"):
        return str(focus["focus_rank_reason"])
    return ""


def _focus_rank_bucket(source: Mapping[str, Any], focus: Mapping[str, Any]) -> str:
    candidate = _focus_candidate(source, focus)
    return str(candidate.get("focus_rank_bucket", focus.get("focus_rank_bucket", "")))


def _focus_candidate(source: Mapping[str, Any], focus: Mapping[str, Any]) -> dict[str, Any]:
    candidate_id = source.get("candidate_id")
    for candidate in _as_list(focus.get("ranked_candidates", ())):
        if isinstance(candidate, Mapping) and candidate.get("candidate_id") == candidate_id:
            return deepcopy(dict(candidate))
    return deepcopy(dict(focus))


def _suppression_reason(suppression: Mapping[str, Any] | None) -> str:
    if suppression is None:
        return ""
    return str(
        suppression.get("suppression_reason")
        or suppression.get("last_suppression_reason")
        or ""
    )


def _critical_unavailable_fields(source: Mapping[str, Any]) -> list[str]:
    unavailable = {str(field) for field in _as_list(source.get("unavailable_fields", ()))}
    missing: list[str] = []
    for field_name in CRITICAL_DIAGNOSTIC_FIELDS:
        if field_name in unavailable or _is_unconfirmed(source.get(field_name)):
            missing.append(field_name)
    return missing


def _noncritical_unavailable_fields(source: Mapping[str, Any]) -> list[str]:
    critical = set(_critical_unavailable_fields(source))
    return [
        str(field)
        for field in _as_list(source.get("unavailable_fields", ()))
        if str(field) not in critical
    ]


def _is_unconfirmed(value: Any) -> bool:
    if isinstance(value, (list, tuple, set)):
        return not value or all(_is_unconfirmed(item) for item in value)
    if value in UNCONFIRMED_VALUES:
        return True
    if isinstance(value, str):
        return value.endswith("_UNCONFIRMED")
    return False


def _source_confirmed_news(source: Mapping[str, Any]) -> bool:
    if source.get("headline_news_source_confirmed") is True:
        return True
    status = str(source.get("headline_news_source_status", "")).lower()
    return status in {"source_confirmed", "confirmed", "valid_source_confirmed"}


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
