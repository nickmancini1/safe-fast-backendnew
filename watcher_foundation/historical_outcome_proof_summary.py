"""Local-only historical outcome proof summary evaluation.

This module accepts caller-provided in-memory historical outcome proof rows
only. It validates rows through the historical outcome proof preflight
validator and returns an in-memory summary without side effects.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.day60_outcome_scoring_summary import (
    DAY60_OUTCOME_REVIEW_BUCKETS,
    build_day60_outcome_scoring_summary,
)
from watcher_foundation.historical_outcome_proof_preflight import (
    validate_historical_outcome_proof_row,
)


HISTORICAL_OUTCOME_PROOF_SUMMARY_RESULT_FIELDS = (
    "watch_only",
    "historical_outcome_summary_only",
    "final_viability_proven",
    "rows_processed",
    "rows_accepted",
    "rows_rejected",
    "accepted_rows",
    "rejected_rows",
    "bucket_counts",
    "unavailable_evidence",
    "no_hindsight_boundary_preserved",
    "no_trade_boundary_preserved",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)


def build_historical_outcome_proof_summary(
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Return an in-memory historical outcome proof summary."""
    if type(rows) is not list:
        raise TypeError("Historical outcome proof summary rows must be a list")

    accepted_rows = []
    rejected_rows = []

    for index, row in enumerate(rows):
        row_id = _extract_outcome_row_id(row)
        try:
            accepted_rows.append(validate_historical_outcome_proof_row(row))
        except (TypeError, ValueError) as exc:
            rejected_rows.append(
                {
                    "index": index,
                    "row_id": row_id,
                    "reason": str(exc),
                }
            )

    scoring_summary = build_day60_outcome_scoring_summary(accepted_rows)
    summarized_accepted_rows = deepcopy(scoring_summary["accepted_rows"])

    return {
        "watch_only": True,
        "historical_outcome_summary_only": True,
        "final_viability_proven": False,
        "rows_processed": len(rows),
        "rows_accepted": len(summarized_accepted_rows),
        "rows_rejected": len(rejected_rows),
        "accepted_rows": summarized_accepted_rows,
        "rejected_rows": deepcopy(rejected_rows),
        "bucket_counts": _complete_bucket_counts(scoring_summary["bucket_counts"]),
        "unavailable_evidence": _summarize_unavailable_evidence(
            summarized_accepted_rows
        ),
        "no_hindsight_boundary_preserved": True,
        "no_trade_boundary_preserved": True,
        "live_data_started": False,
        "controlled_shadow_data_started": False,
        "alerts_sent": False,
        "files_written": False,
        "broker_or_trade_behavior_enabled": False,
    }


def _complete_bucket_counts(bucket_counts: Mapping[str, int]) -> dict[str, int]:
    complete_counts = {bucket: 0 for bucket in DAY60_OUTCOME_REVIEW_BUCKETS}
    for bucket, count in bucket_counts.items():
        complete_counts[str(bucket)] = count
    return complete_counts


def _summarize_unavailable_evidence(
    rows: list[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    unavailable_evidence = []
    for row in rows:
        row_id = _extract_outcome_row_id(row)
        for field_name, item in _iter_unavailable_items(row.get("unavailable_fields", [])):
            unavailable_evidence.append(
                {
                    "row_id": row_id,
                    "field_name": field_name,
                    "status": item.get("status"),
                    "reason": item.get("reason"),
                    "fabricated": item.get("fabricated"),
                    "missing_from_row": field_name not in row,
                }
            )
    return unavailable_evidence


def _iter_unavailable_items(unavailable_fields: Any) -> list[tuple[str, Mapping[str, Any]]]:
    if type(unavailable_fields) is dict:
        return [
            (str(field_name), item)
            for field_name, item in unavailable_fields.items()
            if type(item) is dict
        ]
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
