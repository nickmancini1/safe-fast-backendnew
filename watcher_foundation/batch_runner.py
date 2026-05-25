"""Local in-memory watcher batch runner.

This module runs caller-provided observation dictionaries through the existing
local watcher pipeline in order. It does not fetch live data, run loops,
schedule work, emit phone alerts, write persistent files, or create reports.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.models import reject_forbidden_execution_fields
from watcher_foundation.pipeline import run_local_watcher_pipeline


BATCH_RUNNER_RESULT_FIELDS = (
    "observations_processed",
    "final_state",
    "final_trigger_card",
    "final_diagnostics",
    "final_duplicate_suppression",
    "final_focus_ranking",
    "shadow_log_records",
    "alert_decisions",
    "watch_only",
    "no_trade_boundary",
)


def run_local_watcher_batch(
    observations: list[dict[str, Any]],
) -> dict[str, Any]:
    """Run local caller-provided observations through the watcher pipeline."""

    if not isinstance(observations, list):
        raise TypeError("observations must be a list of caller-provided dicts")

    previous_state: dict[str, Any] | None = None
    previous_suppression_state: dict[str, Any] | None = None
    previous_primary_focus_candidate_id: str | None = None
    final_result: dict[str, Any] | None = None
    shadow_log_records: list[dict[str, Any]] = []
    alert_decisions: list[str] = []

    for index, observation in enumerate(observations):
        if not isinstance(observation, dict):
            raise TypeError(f"observations[{index}] must be a caller-provided dict")
        observation_copy = deepcopy(dict(observation))
        _validate_observation(observation_copy)

        final_result = run_local_watcher_pipeline(
            observation_copy,
            previous_state=previous_state,
            previous_suppression_state=previous_suppression_state,
            previous_primary_focus_candidate_id=previous_primary_focus_candidate_id,
        )

        previous_state = deepcopy(final_result["state"])
        previous_suppression_state = deepcopy(final_result["duplicate_suppression"])
        previous_primary_focus_candidate_id = final_result["focus_ranking"][
            "primary_focus_candidate_id"
        ]
        shadow_log_records.append(deepcopy(final_result["shadow_log_record"]))
        alert_decisions.append(
            str(final_result["duplicate_suppression"]["alert_decision"])
        )

    result = _empty_result() if final_result is None else _summary_from_final_result(
        final_result,
        observations_processed=len(observations),
        shadow_log_records=shadow_log_records,
        alert_decisions=alert_decisions,
    )
    reject_forbidden_execution_fields(result)
    _reject_watch_only_false(result)
    return result


def _validate_observation(observation: Mapping[str, Any]) -> None:
    reject_forbidden_execution_fields(observation)
    _reject_watch_only_false(observation)


def _summary_from_final_result(
    final_result: Mapping[str, Any],
    *,
    observations_processed: int,
    shadow_log_records: list[dict[str, Any]],
    alert_decisions: list[str],
) -> dict[str, Any]:
    return {
        "observations_processed": observations_processed,
        "final_state": deepcopy(final_result["state"]),
        "final_trigger_card": deepcopy(final_result["trigger_card"]),
        "final_diagnostics": deepcopy(final_result["diagnostics"]),
        "final_duplicate_suppression": deepcopy(
            final_result["duplicate_suppression"]
        ),
        "final_focus_ranking": deepcopy(final_result["focus_ranking"]),
        "shadow_log_records": deepcopy(shadow_log_records),
        "alert_decisions": list(alert_decisions),
        "watch_only": True,
        "no_trade_boundary": deepcopy(final_result["no_trade_boundary"]),
    }


def _empty_result() -> dict[str, Any]:
    return {
        "observations_processed": 0,
        "final_state": {},
        "final_trigger_card": {},
        "final_diagnostics": {},
        "final_duplicate_suppression": {},
        "final_focus_ranking": {},
        "shadow_log_records": [],
        "alert_decisions": [],
        "watch_only": True,
        "no_trade_boundary": {
            "watch_only": True,
            "no_live_trade_approval": True,
            "trade_approval": False,
            "live_trade_approval": False,
            "shadow_signal_review_only": False,
            "no_trade_reason": "watch_only_empty_local_batch_no_trade",
        },
    }


def _reject_watch_only_false(value: Any, path: tuple[str, ...] = ()) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            if key_text == "watch_only" and nested_value is not True:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(
                    "Local watcher batch runner must preserve watch_only=True: "
                    f"{dotted_path}"
                )
            _reject_watch_only_false(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_watch_only_false(nested_value, (*path, str(index)))
