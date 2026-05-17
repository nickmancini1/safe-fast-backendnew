import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError


ROOT = Path(__file__).resolve().parent
OUTPUT_SCHEMA = ROOT / "schemas" / "chart_outcome_backtest_output_v1.schema.json"
SUMMARY_REPORT = ROOT / "reports" / "qqq_three_setup_chart_outcome_summary_v1.json"

SAMPLES: Tuple[Tuple[str, Path], ...] = (
    (
        "Ideal",
        ROOT / "reports" / "qqq_ideal_chart_outcome_result_v1.json",
    ),
    (
        "Clean Fast Break",
        ROOT / "reports" / "qqq_clean_fast_break_chart_outcome_result_v1.json",
    ),
    (
        "Continuation",
        ROOT / "reports" / "qqq_continuation_chart_outcome_result_v1.json",
    ),
)


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")


def _format_error(error: ValidationError) -> str:
    location = ".".join(str(part) for part in error.absolute_path)
    if not location:
        location = "<root>"
    return f"{location}: {error.message}"


def _validate_payload(name: str, payload: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [f"{name}: {_format_error(error)}" for error in sorted(validator.iter_errors(payload), key=str)]


def _count_terminal(results: List[Dict[str, Any]], terminal_type: str) -> int:
    return sum(1 for result in results if result["terminal_outcome_type"] == terminal_type)


def _classification_counts(results: List[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for result in results:
        classification = result["same_day_fast_swing_classification"]["hold_classification"]
        counts[classification] = counts.get(classification, 0) + 1
    return dict(sorted(counts.items()))


def _round4(value: float) -> float:
    return round(value, 4)


def _average(values: List[float]) -> float:
    if not values:
        return 0.0
    return _round4(sum(values) / len(values))


def _move_summary(result: Dict[str, Any], move_key: str, prefix: str) -> Dict[str, Any]:
    move = result[move_key]
    return {
        f"{prefix}_points": move[f"{prefix}_points"],
        f"{prefix}_percent": move[f"{prefix}_percent"],
        f"{prefix}_chart_r": move[f"{prefix}_chart_r"],
        f"{prefix}_timestamp": move[f"{prefix}_timestamp"],
        f"{prefix}_candle_index": move[f"{prefix}_candle_index"],
        f"{prefix}_candles_after_entry": move[f"{prefix}_candles_after_entry"],
        f"{prefix}_before_terminal_condition": move[f"{prefix}_before_terminal_condition"],
    }


def _family_summary(setup_family: str, result: Dict[str, Any], source_path: Path) -> Dict[str, Any]:
    likely_risk = result["likely_chart_risk"]
    classification = result["same_day_fast_swing_classification"]
    headline_gap = result["headline_gap_risk_context"]
    return {
        "setup_family": setup_family,
        "sample_count": 1,
        "candidate_id": result["candidate_id"],
        "source_result_file": str(source_path.relative_to(ROOT.parent)).replace("\\", "/"),
        "terminal_outcome_type": result["terminal_outcome_type"],
        "follow_through_count": 1 if result["terminal_outcome_type"] == "follow_through" else 0,
        "failure_count": 1 if result["terminal_outcome_type"] == "invalidated" else 0,
        "time_stop_count": 1 if result["terminal_outcome_type"] == "time_stop" else 0,
        "entry_invalidation_summary": {
            "source_signal_timestamp": result["source_signal_timestamp"],
            "entry_status": result["entry_status"],
            "entry_timestamp": result["entry_timestamp"],
            "entry_reference_price": result["entry_reference_price"],
            "invalidation_reference_price": likely_risk["invalidation_reference_price"],
            "likely_chart_risk_points": likely_risk["likely_chart_risk_points"],
            "likely_chart_risk_percent": likely_risk["likely_chart_risk_percent"],
            "likely_chart_risk_basis": likely_risk["likely_chart_risk_basis"],
        },
        "mfe_summary": _move_summary(result, "max_favorable_move", "mfe"),
        "mae_summary": _move_summary(result, "max_adverse_move", "mae"),
        "same_day_fast_swing_classification_summary": {
            "hold_classification": classification["hold_classification"],
            "same_session_terminal": classification["same_session_terminal"],
            "overnight_carried": classification["overnight_carried"],
            "sessions_held": classification["sessions_held"],
            "same_day_time_stop_applied": classification["same_day_time_stop_applied"],
            "fast_swing_time_stop_applied": classification["fast_swing_time_stop_applied"],
        },
        "headline_gap_risk_context_summary": {
            "macro_context_status": headline_gap["macro_context_status"],
            "iv_context_status": headline_gap["iv_context_status"],
            "event_context_status": headline_gap["event_context_status"],
            "headline_context_status": headline_gap["headline_context_status"],
            "gap_detected_from_chart": headline_gap["gap_detected_from_chart"],
            "gap_direction": headline_gap["gap_direction"],
            "gap_points": headline_gap["gap_points"],
            "gap_percent": headline_gap["gap_percent"],
            "gap_cause_known": headline_gap["gap_cause_known"],
            "gap_cause_source": headline_gap["gap_cause_source"],
        },
        "chart_only_boundary": {
            "chart_only": result["chart_only"],
            "full_risk_modeled": result["full_risk_modeled"],
            "option_pnl_modeled": result["option_pnl_modeled"],
            "account_sizing_modeled": result["account_sizing_modeled"],
            "broker_order_execution_modeled": result["broker_order_execution_modeled"],
        },
    }


def build_summary() -> Tuple[bool, List[str], Dict[str, Any]]:
    schema = _load_json(OUTPUT_SCHEMA)
    errors: List[str] = []
    loaded_samples: List[Tuple[str, Path, Dict[str, Any]]] = []

    for setup_family, result_path in SAMPLES:
        result = _load_json(result_path)
        errors.extend(_validate_payload(str(result_path.relative_to(ROOT.parent)), result, schema))
        loaded_samples.append((setup_family, result_path, result))

    for setup_family, result_path, result in loaded_samples:
        boundary_checks = {
            "chart_only": result.get("chart_only") is True,
            "full_risk_modeled": result.get("full_risk_modeled") is False,
            "option_pnl_modeled": result.get("option_pnl_modeled") is False,
            "account_sizing_modeled": result.get("account_sizing_modeled") is False,
            "broker_order_execution_modeled": result.get("broker_order_execution_modeled") is False,
        }
        failed = [name for name, passed in boundary_checks.items() if not passed]
        if failed:
            errors.append(f"{setup_family} {result_path.name}: boundary check failed for {', '.join(failed)}")

    if errors:
        return False, errors, {}

    results = [result for _, _, result in loaded_samples]
    family_summaries = [
        _family_summary(setup_family, result, result_path)
        for setup_family, result_path, result in loaded_samples
    ]
    mfe_points = [result["max_favorable_move"]["mfe_points"] for result in results]
    mfe_percent = [result["max_favorable_move"]["mfe_percent"] for result in results]
    mfe_chart_r = [result["max_favorable_move"]["mfe_chart_r"] for result in results]
    mae_points = [result["max_adverse_move"]["mae_points"] for result in results]
    mae_percent = [result["max_adverse_move"]["mae_percent"] for result in results]
    mae_chart_r = [result["max_adverse_move"]["mae_chart_r"] for result in results]

    summary: Dict[str, Any] = {
        "schema_version": "qqq_three_setup_chart_outcome_summary_v1",
        "summary_name": "QQQ three setup-family chart outcome summary v1",
        "baseline": "patch8",
        "source_result_schema": "chart_outcome_backtest_output_v1",
        "chart_only_3_sample_qqq_proof": True,
        "profitability_proof": False,
        "summary_boundary": {
            "chart_only": True,
            "sample_count": 3,
            "new_outcome_calculation_from_ohlcv_source_rows": False,
            "option_pnl_modeled": False,
            "account_sizing_modeled": False,
            "broker_order_execution_modeled": False,
            "watcher_output_included": False,
            "profitability_proof": False,
        },
        "samples_included": [
            {
                "setup_family": setup_family,
                "candidate_id": result["candidate_id"],
                "source_result_file": str(result_path.relative_to(ROOT.parent)).replace("\\", "/"),
            }
            for setup_family, result_path, result in loaded_samples
        ],
        "setup_families_included": [setup_family for setup_family, _, _ in loaded_samples],
        "aggregate_outcome_summary": {
            "total_samples": len(results),
            "follow_through_count": _count_terminal(results, "follow_through"),
            "failure_count": _count_terminal(results, "invalidated"),
            "time_stop_count": _count_terminal(results, "time_stop"),
            "failure_definition": "failure_count counts terminal_outcome_type == invalidated; no option, account, or broker failure is modeled.",
        },
        "aggregate_mfe_summary": {
            "average_mfe_points": _average(mfe_points),
            "average_mfe_percent": _average(mfe_percent),
            "average_mfe_chart_r": _average(mfe_chart_r),
            "max_mfe_points": max(mfe_points),
            "max_mfe_percent": max(mfe_percent),
            "max_mfe_chart_r": max(mfe_chart_r),
        },
        "aggregate_mae_summary": {
            "average_mae_points": _average(mae_points),
            "average_mae_percent": _average(mae_percent),
            "average_mae_chart_r": _average(mae_chart_r),
            "max_mae_points": max(mae_points),
            "max_mae_percent": max(mae_percent),
            "max_mae_chart_r": max(mae_chart_r),
        },
        "same_day_fast_swing_classification_summary": _classification_counts(results),
        "headline_gap_risk_context_summary": {
            "gap_detected_from_chart_count": sum(
                1 for result in results if result["headline_gap_risk_context"]["gap_detected_from_chart"]
            ),
            "gap_cause_known_count": sum(
                1 for result in results if result["headline_gap_risk_context"]["gap_cause_known"]
            ),
            "macro_context_status_counts": _status_counts(results, "macro_context_status"),
            "iv_context_status_counts": _status_counts(results, "iv_context_status"),
            "event_context_status_counts": _status_counts(results, "event_context_status"),
            "headline_context_status_counts": _status_counts(results, "headline_context_status"),
        },
        "by_setup_family": family_summaries,
        "validation_summary": {
            "source_result_files_validated_against_schema": True,
            "validated_schema_file": str(OUTPUT_SCHEMA.relative_to(ROOT.parent)).replace("\\", "/"),
            "validated_result_file_count": len(results),
        },
        "notes": (
            "Bounded aggregate reporting for the three validated QQQ setup-family chart-only "
            "outcome outputs. This is a 3-sample QQQ chart proof and not profitability proof. "
            "It reads only existing result files and does not calculate new outcomes from OHLCV source rows."
        ),
    }
    return True, [], summary


def _status_counts(results: List[Dict[str, Any]], status_key: str) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for result in results:
        status = result["headline_gap_risk_context"][status_key]
        counts[status] = counts.get(status, 0) + 1
    return dict(sorted(counts.items()))


def main() -> int:
    passed, errors, summary = build_summary()
    if not passed:
        print("FAIL aggregate chart outcome summary")
        for error in errors:
            print(f"- {error}")
        return 1

    _write_json(SUMMARY_REPORT, summary)
    print("PASS aggregate chart outcome summary")
    print("chart_only_3_sample_qqq_proof: true")
    print("profitability_proof: false")
    print("option_pnl_modeled: false")
    print("account_sizing_added: false")
    print("watcher_output_included: false")
    print(f"report: {SUMMARY_REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
