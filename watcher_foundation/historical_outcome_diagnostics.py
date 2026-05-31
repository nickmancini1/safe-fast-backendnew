"""Local-only historical outcome diagnostics evaluation.

This module accepts the in-memory historical outcome proof summary only and
returns an in-memory diagnostics summary without side effects.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.historical_outcome_proof_summary import (
    HISTORICAL_OUTCOME_PROOF_SUMMARY_RESULT_FIELDS,
)


HISTORICAL_OUTCOME_DIAGNOSTIC_FAILURE_CATEGORIES = (
    "setup_recognition_review",
    "stage_transition_review",
    "trigger_card_review",
    "trigger_level_or_zone_review",
    "invalidation_review",
    "fresh_stale_spent_review",
    "blocker_caution_review",
    "duplicate_suppression_review",
    "ranking_focus_review",
    "session_boundary_review",
    "data_quality_or_missing_evidence",
    "market_context_review",
    "outcome_scoring_review",
    "review_logging_review",
    "user_facing_workflow_review",
)

HISTORICAL_OUTCOME_DIAGNOSTIC_FIX_PATHS = {
    "setup_recognition_review": "review setup-recognition evidence and fixture coverage",
    "stage_transition_review": "review stage-transition evidence and state history",
    "trigger_card_review": "review trigger-card field completeness and evidence references",
    "trigger_level_or_zone_review": "review trigger level or zone evidence before any rule change",
    "invalidation_review": "review invalidation evidence before any rule change",
    "fresh_stale_spent_review": "review freshness, stale, and spent-state evidence",
    "blocker_caution_review": "review blocker and caution evidence against outcome evidence",
    "duplicate_suppression_review": "review duplicate-suppression evidence and material-change markers",
    "ranking_focus_review": "review focus-ranking evidence and missed-priority cases",
    "session_boundary_review": "review session-boundary and outcome-window evidence",
    "data_quality_or_missing_evidence": "collect or preserve missing source-backed historical outcome evidence",
    "market_context_review": "review available market-context evidence without inventing missing context",
    "outcome_scoring_review": "review historical outcome scoring labels, windows, and terminal evidence",
    "review_logging_review": "review rejected row logging, reasons, and review packet traceability",
    "user_facing_workflow_review": "review user-facing historical review workflow evidence and handoff clarity",
}

HISTORICAL_OUTCOME_DIAGNOSTICS_RESULT_FIELDS = (
    "watch_only",
    "historical_outcome_diagnostics_only",
    "optimization_started",
    "rows_processed",
    "rows_accepted",
    "rows_rejected",
    "diagnostic_findings",
    "diagnostic_gap_counts",
    "likely_cause_candidates",
    "next_fix_paths",
    "unavailable_evidence",
    "rejected_rows",
    "no_hindsight_boundary_preserved",
    "no_trade_boundary_preserved",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

_SUMMARY_REQUIRED_FIELDS = set(HISTORICAL_OUTCOME_PROOF_SUMMARY_RESULT_FIELDS)

_EXPECTED_TRUE_BOUNDARY_FIELDS = (
    "watch_only",
    "historical_outcome_summary_only",
    "no_hindsight_boundary_preserved",
    "no_trade_boundary_preserved",
)

_EXPECTED_FALSE_BOUNDARY_FIELDS = (
    "final_viability_proven",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

_FORBIDDEN_HISTORICAL_DIAGNOSTIC_FIELD_NAMES = frozenset(
    {
        "account",
        "account_size",
        "account_sizing",
        "account_sizing_enabled",
        "approved_trade",
        "approved_trades",
        "auto_trade",
        "auto_trading",
        "broker",
        "broker_call",
        "broker_enabled",
        "broker_order",
        "buy",
        "contracts",
        "execute_order",
        "live_trade",
        "live_trade_approval",
        "live_trade_decision",
        "live_trade_decision_enabled",
        "option",
        "option_pnl",
        "option_pnl_enabled",
        "options",
        "order",
        "orders",
        "orders_enabled",
        "p&l",
        "p_and_l",
        "p_l",
        "pl",
        "position",
        "position_size",
        "sell",
        "trade",
        "trade_approval",
        "trade_decision",
        "trade_decisions",
        "trade-decision",
    }
)

_BUCKET_TO_CATEGORY = {
    "failed_trigger": "trigger_level_or_zone_review",
    "stale_spent": "fresh_stale_spent_review",
    "blocked_incorrectly": "blocker_caution_review",
    "inconclusive": "outcome_scoring_review",
    "partial_follow_through": "outcome_scoring_review",
    "unavailable_evidence": "data_quality_or_missing_evidence",
}

_BUCKET_TO_CANDIDATE = {
    "failed_trigger": "candidate: trigger level or zone evidence may need review",
    "stale_spent": "candidate: freshness, stale, or spent-state evidence may need review",
    "blocked_incorrectly": "candidate: blocker or caution handling may need review",
    "inconclusive": "candidate: historical outcome scoring evidence may be incomplete or inconclusive",
    "partial_follow_through": "candidate: historical follow-through scoring may need more outcome evidence",
    "unavailable_evidence": "candidate: missing or unavailable evidence may limit historical diagnostics",
}


def evaluate_historical_outcome_diagnostics(
    historical_summary: dict[str, Any],
) -> dict[str, Any]:
    """Return an in-memory historical outcome diagnostics summary."""
    if type(historical_summary) is not dict:
        raise TypeError(
            "Historical outcome diagnostics historical_summary must be a dict"
        )

    _validate_historical_summary(historical_summary)

    diagnostic_findings = []
    unavailable_evidence = _collect_summary_unavailable_evidence(historical_summary)

    for row in historical_summary["accepted_rows"]:
        diagnostic_findings.extend(_diagnostic_findings_for_row(row))

    if historical_summary["unavailable_evidence"]:
        diagnostic_findings.append(
            _summary_unavailable_evidence_finding(
                historical_summary["unavailable_evidence"]
            )
        )

    if historical_summary["rejected_rows"]:
        diagnostic_findings.append(
            _rejected_rows_finding(historical_summary["rejected_rows"])
        )

    diagnostic_gap_counts = {
        category: 0 for category in HISTORICAL_OUTCOME_DIAGNOSTIC_FAILURE_CATEGORIES
    }
    likely_cause_candidates = []
    next_fix_paths = {}
    for finding in diagnostic_findings:
        category = finding["diagnostic_category"]
        diagnostic_gap_counts[category] += 1
        likely_cause_candidates.extend(deepcopy(finding["likely_cause_candidates"]))
        next_fix_paths[category] = HISTORICAL_OUTCOME_DIAGNOSTIC_FIX_PATHS[category]

    return {
        "watch_only": True,
        "historical_outcome_diagnostics_only": True,
        "optimization_started": False,
        "rows_processed": historical_summary["rows_processed"],
        "rows_accepted": historical_summary["rows_accepted"],
        "rows_rejected": historical_summary["rows_rejected"],
        "diagnostic_findings": deepcopy(diagnostic_findings),
        "diagnostic_gap_counts": diagnostic_gap_counts,
        "likely_cause_candidates": likely_cause_candidates,
        "next_fix_paths": next_fix_paths,
        "unavailable_evidence": unavailable_evidence,
        "rejected_rows": deepcopy(historical_summary["rejected_rows"]),
        "no_hindsight_boundary_preserved": True,
        "no_trade_boundary_preserved": True,
        "live_data_started": False,
        "controlled_shadow_data_started": False,
        "alerts_sent": False,
        "files_written": False,
        "broker_or_trade_behavior_enabled": False,
    }


def _validate_historical_summary(historical_summary: Mapping[str, Any]) -> None:
    _reject_forbidden_historical_diagnostic_fields(historical_summary, path=())

    missing_fields = [
        field_name
        for field_name in HISTORICAL_OUTCOME_PROOF_SUMMARY_RESULT_FIELDS
        if field_name not in historical_summary
    ]
    if missing_fields:
        raise ValueError(
            "Missing required historical outcome proof summary fields: "
            + ", ".join(missing_fields)
        )

    if historical_summary.get("optimization_started") is True:
        raise ValueError("Historical outcome diagnostics must not start optimization")

    for field_name in _EXPECTED_TRUE_BOUNDARY_FIELDS:
        if historical_summary[field_name] is not True:
            raise ValueError(
                f"Historical outcome diagnostics requires {field_name}=True"
            )
    for field_name in _EXPECTED_FALSE_BOUNDARY_FIELDS:
        if historical_summary[field_name] is not False:
            raise ValueError(
                f"Historical outcome diagnostics requires {field_name}=False"
            )

    if type(historical_summary["accepted_rows"]) is not list:
        raise TypeError("Historical outcome diagnostics accepted_rows must be a list")
    if type(historical_summary["rejected_rows"]) is not list:
        raise TypeError("Historical outcome diagnostics rejected_rows must be a list")
    if type(historical_summary["unavailable_evidence"]) is not list:
        raise TypeError(
            "Historical outcome diagnostics unavailable_evidence must be a list"
        )
    if type(historical_summary["bucket_counts"]) is not dict:
        raise TypeError("Historical outcome diagnostics bucket_counts must be a dict")

    for index, row in enumerate(historical_summary["accepted_rows"]):
        _validate_accepted_row_boundaries(row, index)


def _validate_accepted_row_boundaries(row: Any, index: int) -> None:
    if type(row) is not dict:
        return
    if row.get("watch_only") is not True:
        raise ValueError(
            f"Historical outcome diagnostics accepted_rows[{index}] must preserve "
            "watch_only=True"
        )

    no_trade_boundary = row.get("no_trade_boundary")
    if no_trade_boundary is not None:
        _validate_no_trade_boundary(no_trade_boundary, index)

    no_hindsight_boundary = row.get("no_hindsight_boundary")
    if no_hindsight_boundary is not None:
        _validate_no_hindsight_boundary(no_hindsight_boundary, index)


def _validate_no_trade_boundary(boundary: Any, index: int) -> None:
    if type(boundary) is not dict:
        raise TypeError(
            f"Historical outcome diagnostics accepted_rows[{index}]."
            "no_trade_boundary must be a dict"
        )
    for field_name in (
        "no_trade",
        "no_broker",
        "no_order",
        "no_account_sizing",
        "no_option_pnl",
        "no_live_trade_decision",
    ):
        if boundary.get(field_name) is not True:
            raise ValueError(
                f"Historical outcome diagnostics accepted_rows[{index}]."
                f"no_trade_boundary must set {field_name}=True"
            )
    for field_name in (
        "broker_enabled",
        "orders_enabled",
        "account_sizing_enabled",
        "option_pnl_enabled",
        "live_trade_decision_enabled",
    ):
        if boundary.get(field_name) is not False:
            raise ValueError(
                f"Historical outcome diagnostics accepted_rows[{index}]."
                f"no_trade_boundary must set {field_name}=False"
            )


def _validate_no_hindsight_boundary(boundary: Any, index: int) -> None:
    if type(boundary) is not dict:
        raise TypeError(
            f"Historical outcome diagnostics accepted_rows[{index}]."
            "no_hindsight_boundary must be a dict"
        )
    for field_name in (
        "evidence_available_at_or_before_review_timestamp",
        "future_evidence_not_used",
        "no_backfilled_outcome_labels",
    ):
        if boundary.get(field_name) is not True:
            raise ValueError(
                f"Historical outcome diagnostics accepted_rows[{index}]."
                f"no_hindsight_boundary must set {field_name}=True"
            )


def _diagnostic_findings_for_row(row: Any) -> list[dict[str, Any]]:
    if type(row) is not dict:
        return [
            _build_finding(
                category="data_quality_or_missing_evidence",
                source_bucket="unavailable_evidence",
                row=row,
                evidence_used=[],
                unavailable_items=[
                    {
                        "field_name": "accepted_rows[]",
                        "status": "unavailable",
                        "reason": "accepted row is not a dict",
                    }
                ],
                likely_cause_text="candidate: accepted row shape may need review",
            )
        ]

    review_bucket = row.get("review_bucket")
    if review_bucket in {"strong_follow_through", "blocked_correctly"}:
        return []

    category = _BUCKET_TO_CATEGORY.get(review_bucket)
    if category is None:
        return [
            _build_finding(
                category="outcome_scoring_review",
                source_bucket=review_bucket,
                row=row,
                evidence_used=_evidence_used(row),
                unavailable_items=_row_unavailable_items(row),
                likely_cause_text=(
                    "candidate: unmapped historical outcome bucket may need scoring review"
                ),
            )
        ]

    return [
        _build_finding(
            category=category,
            source_bucket=review_bucket,
            row=row,
            evidence_used=_evidence_used(row),
            unavailable_items=_row_unavailable_items(row),
            likely_cause_text=_BUCKET_TO_CANDIDATE[review_bucket],
        )
    ]


def _summary_unavailable_evidence_finding(
    unavailable_evidence: list[Any],
) -> dict[str, Any]:
    return {
        "diagnostic_category": "data_quality_or_missing_evidence",
        "source_bucket": "unavailable_evidence",
        "row_id": "SUMMARY",
        "affected_setup_type": _unavailable_field("setup_type", "summary-level finding"),
        "affected_symbol": _unavailable_field("symbol", "summary-level finding"),
        "affected_stage": _unavailable_field("stage_at_detection", "summary-level finding"),
        "trigger_invalidation_freshness_relationship": _unavailable_relationship(),
        "evidence_used": [],
        "unavailable_evidence": deepcopy(unavailable_evidence),
        "likely_cause_candidates": [
            {
                "label": "candidate",
                "candidate": "candidate: unavailable historical evidence may limit diagnostics",
                "evidence_basis": deepcopy(unavailable_evidence),
            }
        ],
        "next_fix_path": HISTORICAL_OUTCOME_DIAGNOSTIC_FIX_PATHS[
            "data_quality_or_missing_evidence"
        ],
    }


def _rejected_rows_finding(rejected_rows: list[Any]) -> dict[str, Any]:
    return {
        "diagnostic_category": "review_logging_review",
        "source_bucket": "rejected_rows",
        "row_id": "SUMMARY",
        "affected_setup_type": _unavailable_field("setup_type", "rejected row summary"),
        "affected_symbol": _unavailable_field("symbol", "rejected row summary"),
        "affected_stage": _unavailable_field("stage_at_detection", "rejected row summary"),
        "trigger_invalidation_freshness_relationship": _unavailable_relationship(),
        "evidence_used": deepcopy(rejected_rows),
        "unavailable_evidence": [],
        "likely_cause_candidates": [
            {
                "label": "candidate",
                "candidate": "candidate: rejected row reasons may need review",
                "evidence_basis": deepcopy(rejected_rows),
            }
        ],
        "next_fix_path": HISTORICAL_OUTCOME_DIAGNOSTIC_FIX_PATHS[
            "review_logging_review"
        ],
    }


def _build_finding(
    *,
    category: str,
    source_bucket: Any,
    row: Any,
    evidence_used: list[Any],
    unavailable_items: list[Any],
    likely_cause_text: str,
) -> dict[str, Any]:
    row_mapping = row if type(row) is dict else {}
    return {
        "diagnostic_category": category,
        "source_bucket": source_bucket,
        "row_id": row_mapping.get("outcome_row_id", "UNAVAILABLE"),
        "affected_setup_type": _available_or_unavailable(row_mapping, "setup_type"),
        "affected_symbol": _available_or_unavailable(row_mapping, "symbol"),
        "affected_stage": _available_or_unavailable(row_mapping, "stage_at_detection"),
        "trigger_invalidation_freshness_relationship": {
            "trigger_reference": _available_or_unavailable(
                row_mapping, "trigger_reference"
            ),
            "trigger_status_at_detection": _available_or_unavailable(
                row_mapping, "trigger_status_at_detection"
            ),
            "invalidation_reference": _available_or_unavailable(
                row_mapping, "invalidation_reference"
            ),
            "stale_spent_outcome": _available_or_unavailable(
                row_mapping, "stale_spent_outcome"
            ),
        },
        "evidence_used": deepcopy(evidence_used),
        "unavailable_evidence": deepcopy(unavailable_items),
        "likely_cause_candidates": [
            {
                "label": "candidate",
                "candidate": likely_cause_text,
                "evidence_basis": {
                    "review_bucket": source_bucket,
                    "evidence_used": deepcopy(evidence_used),
                    "unavailable_evidence": deepcopy(unavailable_items),
                },
            }
        ],
        "next_fix_path": HISTORICAL_OUTCOME_DIAGNOSTIC_FIX_PATHS[category],
    }


def _evidence_used(row: Mapping[str, Any]) -> list[Any]:
    evidence_refs = row.get("evidence_refs")
    if type(evidence_refs) is list:
        return deepcopy(evidence_refs)
    return []


def _row_unavailable_items(row: Mapping[str, Any]) -> list[Any]:
    unavailable_items = []
    unavailable_fields = row.get("unavailable_fields")
    if type(unavailable_fields) is list:
        unavailable_items.extend(deepcopy(unavailable_fields))
    elif type(unavailable_fields) is dict:
        for field_name, item in unavailable_fields.items():
            copied_item = deepcopy(item) if type(item) is dict else {"value": item}
            copied_item["field_name"] = str(field_name)
            unavailable_items.append(copied_item)

    if not _evidence_used(row):
        unavailable_items.append(
            {
                "field_name": "evidence_refs",
                "status": "unavailable",
                "reason": "no evidence_refs were present for this diagnostic finding",
            }
        )
    return unavailable_items


def _collect_summary_unavailable_evidence(
    historical_summary: Mapping[str, Any],
) -> list[Any]:
    unavailable_evidence = deepcopy(historical_summary["unavailable_evidence"])
    for row in historical_summary["accepted_rows"]:
        if type(row) is dict:
            unavailable_evidence.extend(_row_unavailable_items(row))
    return unavailable_evidence


def _available_or_unavailable(row: Mapping[str, Any], field_name: str) -> Any:
    if field_name in row:
        return deepcopy(row[field_name])
    return _unavailable_field(field_name, "field not present in accepted row")


def _unavailable_field(field_name: str, reason: str) -> dict[str, str]:
    return {
        "field_name": field_name,
        "status": "unavailable",
        "reason": reason,
    }


def _unavailable_relationship() -> dict[str, Any]:
    return {
        "trigger_reference": _unavailable_field("trigger_reference", "not available"),
        "trigger_status_at_detection": _unavailable_field(
            "trigger_status_at_detection", "not available"
        ),
        "invalidation_reference": _unavailable_field(
            "invalidation_reference", "not available"
        ),
        "stale_spent_outcome": _unavailable_field(
            "stale_spent_outcome", "not available"
        ),
    }


def _reject_forbidden_historical_diagnostic_fields(
    value: Any,
    path: tuple[str, ...],
) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.lower()
            if (
                normalized_key in _FORBIDDEN_HISTORICAL_DIAGNOSTIC_FIELD_NAMES
                and normalized_key not in _SUMMARY_REQUIRED_FIELDS
                and not _is_preserved_no_trade_boundary_field(normalized_key, path)
            ):
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden execution/trade field: {dotted_path}")
            _reject_forbidden_historical_diagnostic_fields(
                nested_value, (*path, key_text)
            )
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_forbidden_historical_diagnostic_fields(
                nested_value, (*path, str(index))
            )


def _is_preserved_no_trade_boundary_field(
    normalized_key: str,
    path: tuple[str, ...],
) -> bool:
    if not path or path[-1] != "no_trade_boundary":
        return False
    return normalized_key in {
        "broker_enabled",
        "orders_enabled",
        "account_sizing_enabled",
        "option_pnl_enabled",
        "live_trade_decision_enabled",
    }
