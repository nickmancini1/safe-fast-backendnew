"""Local in-memory watcher replay/regression runner.

This module runs named caller-provided fixture cases through the existing local
watcher batch runner, then evaluates selected expected output fields. It does
not fetch live data, create loops, emit alerts, write files, or create reports.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from watcher_foundation.batch_runner import run_local_watcher_batch
from watcher_foundation.models import reject_forbidden_execution_fields


REPLAY_REGRESSION_RESULT_FIELDS = (
    "cases_processed",
    "cases_passed",
    "cases_failed",
    "case_results",
    "watch_only",
    "no_trade_boundary",
)

REPLAY_FORBIDDEN_TRADE_DECISION_FIELDS = frozenset(
    {
        "live_trade_decision",
        "live_trade_decisions",
        "trade_decision",
        "trade_decision_status",
        "trade_decisions",
    }
)


@dataclass(frozen=True)
class ReplayRegressionCase:
    """One local watch-only replay/regression fixture case."""

    name: str
    observations: Sequence[Mapping[str, Any]]
    expected_values: Mapping[str, Any] = field(default_factory=dict)
    expected_contains: Mapping[str, Sequence[Any]] = field(default_factory=dict)
    expected_absent_fields: Sequence[str] = field(default_factory=tuple)


def run_local_replay_regression(
    cases: Sequence[ReplayRegressionCase | Mapping[str, Any]],
) -> dict[str, Any]:
    """Run named local fixture cases and return in-memory regression results."""

    if not isinstance(cases, Sequence) or isinstance(cases, (str, bytes)):
        raise TypeError("cases must be a sequence of replay regression cases")

    case_results = [_run_case(_coerce_case(case)) for case in cases]
    cases_failed = sum(1 for result in case_results if not result["passed"])
    result = {
        "cases_processed": len(case_results),
        "cases_passed": len(case_results) - cases_failed,
        "cases_failed": cases_failed,
        "case_results": case_results,
        "watch_only": True,
        "no_trade_boundary": {
            "watch_only": True,
            "no_live_trade_approval": True,
            "trade_approval": False,
            "live_trade_approval": False,
            "no_trade_reason": "watch_only_local_replay_regression_no_trade",
        },
    }
    _validate_no_forbidden_outputs(result)
    _reject_watch_only_false(result)
    return result


def _coerce_case(case: ReplayRegressionCase | Mapping[str, Any]) -> ReplayRegressionCase:
    if isinstance(case, ReplayRegressionCase):
        return case
    if not isinstance(case, Mapping):
        raise TypeError("each replay regression case must be a case or mapping")
    return ReplayRegressionCase(
        name=str(case["name"]),
        observations=case["observations"],
        expected_values=case.get("expected_values", {}),
        expected_contains=case.get("expected_contains", {}),
        expected_absent_fields=case.get("expected_absent_fields", ()),
    )


def _run_case(case: ReplayRegressionCase) -> dict[str, Any]:
    if not case.name:
        raise ValueError("replay regression case name is required")
    observations = [deepcopy(dict(observation)) for observation in case.observations]
    for index, observation in enumerate(observations):
        if not isinstance(observation, dict):
            raise TypeError(f"{case.name}.observations[{index}] must be a mapping")
        _validate_no_forbidden_outputs(observation)
        _reject_watch_only_false(observation)

    batch_result = run_local_watcher_batch(observations)
    _validate_no_forbidden_outputs(batch_result)
    _reject_watch_only_false(batch_result)

    failures: list[dict[str, Any]] = []
    failures.extend(_expected_value_failures(batch_result, case.expected_values))
    failures.extend(_expected_contains_failures(batch_result, case.expected_contains))
    failures.extend(_expected_absent_failures(batch_result, case.expected_absent_fields))

    result = {
        "case_name": case.name,
        "passed": not failures,
        "failures": failures,
        "observations_processed": batch_result["observations_processed"],
        "result": deepcopy(batch_result),
        "watch_only": True,
        "no_trade_boundary": deepcopy(batch_result["no_trade_boundary"]),
    }
    _validate_no_forbidden_outputs(result)
    _reject_watch_only_false(result)
    return result


def _expected_value_failures(
    result: Mapping[str, Any],
    expected_values: Mapping[str, Any],
) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for path, expected in expected_values.items():
        actual = _resolve_path(result, str(path))
        if actual != expected:
            failures.append(
                {
                    "check": "expected_value",
                    "path": str(path),
                    "expected": deepcopy(expected),
                    "actual": deepcopy(actual),
                }
            )
    return failures


def _expected_contains_failures(
    result: Mapping[str, Any],
    expected_contains: Mapping[str, Sequence[Any]],
) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for path, expected_items in expected_contains.items():
        actual = _resolve_path(result, str(path))
        actual_values = actual if isinstance(actual, (list, tuple, set)) else (actual,)
        missing = [item for item in expected_items if item not in actual_values]
        if missing:
            failures.append(
                {
                    "check": "expected_contains",
                    "path": str(path),
                    "expected": list(deepcopy(expected_items)),
                    "actual": deepcopy(actual),
                    "missing": missing,
                }
            )
    return failures


def _expected_absent_failures(
    result: Mapping[str, Any],
    expected_absent_fields: Sequence[str],
) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for field_name in expected_absent_fields:
        paths = _find_key_paths(result, str(field_name))
        if paths:
            failures.append(
                {
                    "check": "expected_absent_field",
                    "field": str(field_name),
                    "paths": paths,
                }
            )
    return failures


def _resolve_path(source: Any, path: str) -> Any:
    current = source
    for part in path.split("."):
        if isinstance(current, Mapping):
            current = current.get(part)
        elif isinstance(current, (list, tuple)) and part.isdigit():
            index = int(part)
            current = current[index] if index < len(current) else None
        else:
            return None
    return current


def _find_key_paths(value: Any, field_name: str, path: tuple[str, ...] = ()) -> list[str]:
    matches: list[str] = []
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            nested_path = (*path, key_text)
            if key_text == field_name:
                matches.append(".".join(nested_path))
            matches.extend(_find_key_paths(nested_value, field_name, nested_path))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            matches.extend(_find_key_paths(nested_value, field_name, (*path, str(index))))
    return matches


def _validate_no_forbidden_outputs(value: Any) -> None:
    if isinstance(value, Mapping):
        reject_forbidden_execution_fields(value)
    _reject_forbidden_trade_decision_fields(value)


def _reject_forbidden_trade_decision_fields(
    value: Any,
    path: tuple[str, ...] = (),
) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            if key_text.lower() in REPLAY_FORBIDDEN_TRADE_DECISION_FIELDS:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden trade-decision field: {dotted_path}")
            _reject_forbidden_trade_decision_fields(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_forbidden_trade_decision_fields(nested_value, (*path, str(index)))


def _reject_watch_only_false(value: Any, path: tuple[str, ...] = ()) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            if key_text == "watch_only" and nested_value is not True:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(
                    "Local replay regression runner must preserve watch_only=True: "
                    f"{dotted_path}"
                )
            _reject_watch_only_false(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_watch_only_false(nested_value, (*path, str(index)))
