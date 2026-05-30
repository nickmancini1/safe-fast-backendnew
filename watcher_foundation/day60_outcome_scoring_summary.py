"""Local-only Day 60 outcome scoring summary evaluation.

This module accepts caller-provided in-memory outcome-review rows only. It
validates them through the Day 60 outcome scoring contract validator and
returns an in-memory summary without side effects.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.day60_outcome_scoring_contract import (
    DAY60_OUTCOME_SCORING_CONTRACT_REQUIRED_PROOF_FIELDS,
    validate_day60_outcome_scoring_row,
)


DAY60_OUTCOME_REVIEW_BUCKETS = (
    "strong_follow_through",
    "partial_follow_through",
    "failed_trigger",
    "stale_spent",
    "blocked_correctly",
    "blocked_incorrectly",
    "inconclusive",
    "unavailable_evidence",
)

DAY60_OUTCOME_SCORING_SUMMARY_RESULT_FIELDS = (
    "watch_only",
    "outcome_scoring_summary_only",
    "rows_processed",
    "rows_accepted",
    "rows_rejected",
    "accepted_rows",
    "rejected_rows",
    "bucket_counts",
    "unavailable_outcome_fields",
    "no_hindsight_boundary_preserved",
    "no_trade_boundary_preserved",
    "live_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)


def build_day60_outcome_scoring_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Return an in-memory Day 60 outcome scoring summary."""
    if type(rows) is not list:
        raise TypeError("Day 60 outcome scoring summary rows must be a list")

    accepted_rows = []
    rejected_rows = []
    bucket_counts = {bucket: 0 for bucket in DAY60_OUTCOME_REVIEW_BUCKETS}
    unavailable_outcome_fields = []

    for index, row in enumerate(rows):
        row_id = _extract_outcome_row_id(row)
        try:
            accepted_row = validate_day60_outcome_scoring_row(row)
        except (TypeError, ValueError) as exc:
            rejected_rows.append(
                {
                    "index": index,
                    "row_id": row_id,
                    "reason": str(exc),
                }
            )
            continue

        review_bucket = _classify_review_bucket(accepted_row)
        accepted_copy = deepcopy(accepted_row)
        accepted_copy["review_bucket"] = review_bucket
        accepted_rows.append(accepted_copy)
        bucket_counts[review_bucket] += 1
        unavailable_outcome_fields.extend(
            _summarize_unavailable_outcome_fields(accepted_row, row_id)
        )

    return {
        "watch_only": True,
        "outcome_scoring_summary_only": True,
        "rows_processed": len(rows),
        "rows_accepted": len(accepted_rows),
        "rows_rejected": len(rejected_rows),
        "accepted_rows": accepted_rows,
        "rejected_rows": rejected_rows,
        "bucket_counts": bucket_counts,
        "unavailable_outcome_fields": unavailable_outcome_fields,
        "no_hindsight_boundary_preserved": True,
        "no_trade_boundary_preserved": True,
        "live_data_started": False,
        "alerts_sent": False,
        "files_written": False,
        "broker_or_trade_behavior_enabled": False,
    }


def _classify_review_bucket(row: Mapping[str, Any]) -> str:
    unavailable_field_names = _unavailable_field_names(row.get("unavailable_fields", []))
    missing_proof_fields = {
        field_name
        for field_name in DAY60_OUTCOME_SCORING_CONTRACT_REQUIRED_PROOF_FIELDS
        if field_name not in row
    }
    if "evidence_refs" in unavailable_field_names or (
        unavailable_field_names | missing_proof_fields
    ):
        return "unavailable_evidence"

    outcome_status = _normalized(row.get("outcome_status"))
    failure_status = _normalized(row.get("failure_status"))
    stale_spent_outcome = _normalized(row.get("stale_spent_outcome"))
    blocker_caution_outcome = _normalized(row.get("blocker_caution_outcome"))

    if "strong" in outcome_status and "follow" in outcome_status:
        return "strong_follow_through"
    if "partial" in outcome_status and "follow" in outcome_status:
        return "partial_follow_through"
    if "failed" in failure_status and "trigger" in failure_status:
        return "failed_trigger"
    if "stale" in stale_spent_outcome or "spent" in stale_spent_outcome:
        return "stale_spent"
    if "correct" in blocker_caution_outcome and "incorrect" not in blocker_caution_outcome:
        return "blocked_correctly"
    if "incorrect" in blocker_caution_outcome:
        return "blocked_incorrectly"
    return "inconclusive"


def _summarize_unavailable_outcome_fields(
    row: Mapping[str, Any],
    row_id: str,
) -> list[dict[str, Any]]:
    unavailable_items = []
    for field_name, item in _iter_unavailable_items(row.get("unavailable_fields", [])):
        if field_name not in DAY60_OUTCOME_SCORING_CONTRACT_REQUIRED_PROOF_FIELDS:
            continue
        unavailable_items.append(
            {
                "row_id": row_id,
                "field_name": field_name,
                "status": item.get("status"),
                "reason": item.get("reason"),
                "fabricated": item.get("fabricated"),
                "missing_from_row": field_name not in row,
            }
        )
    return unavailable_items


def _unavailable_field_names(unavailable_fields: Any) -> set[str]:
    return {
        field_name
        for field_name, item in _iter_unavailable_items(unavailable_fields)
        if field_name in DAY60_OUTCOME_SCORING_CONTRACT_REQUIRED_PROOF_FIELDS
        and type(item) is dict
        and item.get("status") in {"unavailable", "unconfirmed"}
    }


def _iter_unavailable_items(unavailable_fields: Any) -> list[tuple[str, Any]]:
    if type(unavailable_fields) is dict:
        return [(str(field_name), item) for field_name, item in unavailable_fields.items()]
    if type(unavailable_fields) is not list:
        return []

    items = []
    for item in unavailable_fields:
        if type(item) is not dict:
            continue
        field_name = item.get("field_name")
        if type(field_name) is str and field_name:
            items.append((field_name, item))
    return items


def _extract_outcome_row_id(row: Any) -> str:
    if isinstance(row, Mapping) and "outcome_row_id" in row:
        return str(row["outcome_row_id"])
    return "UNAVAILABLE"


def _normalized(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower().replace("-", "_").replace(" ", "_")
