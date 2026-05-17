import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent

INPUT_SCHEMA = ROOT / "schemas" / "chart_outcome_backtest_input_v1.schema.json"
OUTPUT_SCHEMA = ROOT / "schemas" / "chart_outcome_backtest_output_v1.schema.json"
INPUT_FIXTURE = ROOT / "fixtures" / "qqq_clean_fast_break_chart_outcome_input_v1.json"
EXPECTED_OUTPUT_FIXTURE = (
    ROOT / "fixtures" / "qqq_clean_fast_break_chart_outcome_expected_output_v1.json"
)
REPORT_PATH = ROOT / "reports" / "qqq_clean_fast_break_chart_outcome_result_v1.json"


@dataclass(frozen=True)
class BacktestResult:
    passed: bool
    errors: List[str]
    report_path: Path
    output_schema_valid: bool


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


def _repo_path(path_text: str) -> Path:
    return REPO_ROOT / path_text


def _read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if stripped:
                yield json.loads(stripped)


def _load_csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _to_float(value: Any) -> Optional[float]:
    if isinstance(value, bool) or value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _round4(value: float) -> float:
    return round(value, 4)


def _session_date(timestamp: str) -> Optional[str]:
    if "T" not in timestamp:
        return None
    return timestamp.split("T", 1)[0]


def _source_csv_path(symbol: str) -> Path:
    return (
        REPO_ROOT
        / "historical_signal_replay"
        / "source_data"
        / "incoming"
        / f"first_real_historical_replay_v1_{symbol}_source.csv"
    )


def _validate_source_artifacts(candidate: Dict[str, Any]) -> List[str]:
    errors: List[str] = []

    for key in ("source_replay_fixture", "source_signal_log", "source_summary"):
        artifact = candidate[key]
        artifact_path = _repo_path(artifact["path"])
        if artifact["status"] == "available" and not artifact_path.exists():
            errors.append(f"{key}: declared available artifact is missing: {artifact['path']}")

    signal_log_path = _repo_path(candidate["source_signal_log"]["path"])
    if signal_log_path.exists():
        matching_rows = [
            row
            for row in _read_jsonl(signal_log_path)
            if row.get("timestamp") == candidate["source_signal_timestamp"]
            and row.get("stage") == candidate["source_row_name"]
        ]
        if not matching_rows:
            errors.append("source_signal_log: no row matches source timestamp and row name")
        else:
            source_row = matching_rows[0]
            expected_fields = {
                "symbol": candidate["symbol"],
                "setup_type": candidate["setup_family"],
                "final_verdict": "TRADE",
                "trigger_state": "triggered",
            }
            for field, expected in expected_fields.items():
                actual = source_row.get(field)
                if actual != expected:
                    errors.append(
                        f"source_signal_log: expected {field}={expected!r}, got {actual!r}"
                    )

    source_csv_path = _source_csv_path(candidate["symbol"])
    if not source_csv_path.exists():
        errors.append(f"source_csv: missing {source_csv_path.relative_to(REPO_ROOT)}")
    else:
        csv_rows = _load_csv_rows(source_csv_path)
        source_timestamps = {row.get("timestamp") for row in csv_rows}
        required_timestamps = {
            candidate["source_signal_timestamp"],
            candidate["lookahead_window"]["start_timestamp"],
            candidate["lookahead_window"]["end_timestamp"],
        }
        required_timestamps.update(candle["timestamp"] for candle in candidate["source_candle_window"])
        for timestamp in sorted(ts for ts in required_timestamps if ts):
            if timestamp not in source_timestamps:
                errors.append(f"source_csv: missing required timestamp {timestamp}")

        mismatched_rows = [
            row
            for row in csv_rows
            if row.get("timestamp") in required_timestamps
            and (
                row.get("symbol") != candidate["symbol"]
                or row.get("timeframe") != candidate["timeframe"]
                or row.get("regular_session") != "true"
            )
        ]
        if mismatched_rows:
            errors.append(
                f"source_csv: required rows must be {candidate['symbol']} "
                "1h_rth regular-session candles"
            )

    return errors


def _load_matching_signal_row(candidate: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], List[str]]:
    errors: List[str] = []
    signal_log_path = _repo_path(candidate["source_signal_log"]["path"])
    matching_rows = [
        row
        for row in _read_jsonl(signal_log_path)
        if row.get("timestamp") == candidate["source_signal_timestamp"]
        and row.get("stage") == candidate["source_row_name"]
    ]
    if not matching_rows:
        return None, ["source_signal_log: no eligible source row found for candidate"]

    row = matching_rows[0]
    required_values = {
        "symbol": candidate["symbol"],
        "setup_type": candidate["setup_family"],
        "final_verdict": "TRADE",
        "current_state": "signal",
        "trigger_state": "triggered",
        "primary_blocker": None,
    }
    for field, expected in required_values.items():
        actual = row.get(field)
        if actual != expected:
            errors.append(f"eligible signal row: expected {field}={expected!r}, got {actual!r}")

    if _to_float(row.get("trigger_level")) is None:
        errors.append("eligible signal row: trigger_level is missing or non-numeric")
    if _to_float(row.get("invalidation")) is None:
        errors.append("eligible signal row: invalidation is missing or non-numeric")

    selected_setup = row.get("winner_selection_result", {}).get("selected_setup_type")
    if selected_setup != candidate["setup_family"]:
        errors.append(
            "eligible signal row: winner_selection_result.selected_setup_type "
            f"expected {candidate['setup_family']!r}, got {selected_setup!r}"
        )

    return row, errors


def _load_real_window_candles(candidate: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[str]]:
    errors: List[str] = []
    source_rows = _load_csv_rows(_source_csv_path(candidate["symbol"]))
    start_timestamp = candidate["source_signal_timestamp"]
    end_timestamp = candidate["lookahead_window"]["end_timestamp"]
    source_rows = [
        row
        for row in source_rows
        if row.get("symbol") == candidate["symbol"]
        and row.get("timeframe") == candidate["timeframe"]
        and row.get("regular_session") == "true"
        and start_timestamp <= row.get("timestamp", "") <= end_timestamp
    ]
    if not source_rows:
        return [], ["source_csv: no real source OHLCV rows found for candidate window"]

    candles: List[Dict[str, Any]] = []
    for row in source_rows:
        numeric_values = {
            key: _to_float(row.get(key))
            for key in ("open", "high", "low", "close", "volume")
        }
        missing = [key for key, value in numeric_values.items() if value is None]
        if missing:
            errors.append(
                f"source_csv: row {row.get('timestamp')} has missing/non-numeric fields: "
                + ", ".join(missing)
            )
            continue
        candles.append(
            {
                "timestamp": row["timestamp"],
                "open": numeric_values["open"],
                "high": numeric_values["high"],
                "low": numeric_values["low"],
                "close": numeric_values["close"],
                "volume": numeric_values["volume"],
                "session_date": row.get("session_date") or _session_date(row["timestamp"]),
            }
        )

    return candles, errors


def _terminal_classification(
    terminal_outcome_type: str,
    entry_date: str,
    terminal_date: str,
    sessions_held: int,
) -> Dict[str, Any]:
    same_session = entry_date == terminal_date
    if terminal_outcome_type == "follow_through":
        hold_classification = "same_day" if same_session else "fast_swing"
    elif terminal_outcome_type == "invalidated":
        hold_classification = "invalidated_same_day" if same_session else "invalidated_fast_swing"
    else:
        hold_classification = "time_stop_same_day" if same_session else "time_stop_fast_swing"

    return {
        "hold_classification": hold_classification,
        "entry_session_date": entry_date,
        "terminal_session_date": terminal_date,
        "same_session_terminal": same_session,
        "overnight_carried": not same_session,
        "sessions_held": sessions_held,
        "same_day_time_stop_applied": hold_classification == "time_stop_same_day",
        "fast_swing_time_stop_applied": hold_classification == "time_stop_fast_swing",
    }


def _known_unavailable_context() -> Dict[str, bool]:
    return {
        "context_24h_daily_unavailable_or_unconfirmed": True,
        "macro_context_unavailable_or_unconfirmed": True,
        "iv_context_unavailable_or_unconfirmed": True,
        "event_context_unavailable_or_unconfirmed": True,
        "headline_context_unavailable_or_unconfirmed": True,
        "option_chain_unavailable_by_design": True,
        "account_context_unavailable_by_design": True,
        "broker_execution_unavailable_by_design": True,
    }


def _build_real_chart_report(candidate: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], List[str]]:
    errors: List[str] = []
    source_row, source_row_errors = _load_matching_signal_row(candidate)
    errors.extend(source_row_errors)
    candles, candle_errors = _load_real_window_candles(candidate)
    errors.extend(candle_errors)
    if errors:
        return None, errors
    if source_row is None:
        return None, ["source_signal_log: source row unavailable"]

    entry_timestamp = candidate["lookahead_window"]["start_timestamp"]
    entry_index = next(
        (index for index, candle in enumerate(candles) if candle["timestamp"] == entry_timestamp),
        None,
    )
    if entry_index is None:
        return None, [f"entry: next eligible candle missing from real source CSV: {entry_timestamp}"]

    entry_candle = candles[entry_index]
    entry_reference_price = entry_candle["open"]
    invalidation_reference_price = _to_float(source_row.get("invalidation"))
    follow_threshold = _to_float(candidate["follow_through_condition"]["follow_through_threshold"])
    max_hold_candles = int(candidate["time_stop_condition"]["max_hold_candles"])
    if invalidation_reference_price is None:
        return None, ["invalidation: missing numeric invalidation in eligible signal row"]
    if follow_threshold is None:
        return None, ["follow_through: missing numeric follow-through threshold in input fixture"]

    direction = candidate["direction"]
    is_bullish = direction in {"CALL", "LONG", "BULLISH"}
    if not is_bullish:
        return None, [
            f"direction: chart outcome v1 supports bullish chart samples only, got {direction!r}"
        ]

    scan_candles = candles[entry_index : entry_index + max_hold_candles]
    if len(scan_candles) < max_hold_candles:
        return None, ["time_stop: insufficient real source lookahead rows to complete hold window"]

    terminal_index = None
    terminal_outcome_type = None
    terminal_reference_price = None
    terminal_reason = None
    follow_level = entry_reference_price + follow_threshold

    for index, candle in enumerate(scan_candles, start=entry_index):
        invalidation_hit = candle["low"] <= invalidation_reference_price
        follow_through_hit = candle["high"] >= follow_level
        if invalidation_hit:
            terminal_index = index
            terminal_outcome_type = "invalidated"
            terminal_reference_price = candle["low"]
            terminal_reason = (
                f"Real chart calculation: {candle['timestamp']} low {candle['low']} touched/crossed "
                f"copied invalidation {invalidation_reference_price} before follow-through or time stop."
            )
            break
        if follow_through_hit:
            terminal_index = index
            terminal_outcome_type = "follow_through"
            terminal_reference_price = candle["high"]
            terminal_reason = (
                f"Real chart calculation: next eligible candle open entry {entry_reference_price} plus "
                f"{follow_threshold} point favorable touch threshold was reached by "
                f"{candle['timestamp']} high {candle['high']}."
            )
            break

    if terminal_index is None:
        terminal_index = entry_index + max_hold_candles - 1
        terminal_outcome_type = "time_stop"
        terminal_reference_price = candles[terminal_index]["close"]
        terminal_reason = (
            "Real chart calculation: neither follow-through nor invalidation was reached before "
            "the predeclared maximum hold candle window."
        )

    terminal_candle = candles[terminal_index]
    measured_candles = candles[entry_index : terminal_index + 1]
    mfe_candle = max(measured_candles, key=lambda candle: candle["high"])
    mae_candle = min(measured_candles, key=lambda candle: candle["low"])
    mfe_points = _round4(mfe_candle["high"] - entry_reference_price)
    mae_points = _round4(entry_reference_price - mae_candle["low"])
    risk_points = _round4(abs(entry_reference_price - invalidation_reference_price))
    risk_percent = _round4((risk_points / entry_reference_price) * 100)
    sessions = sorted({candle["session_date"] for candle in measured_candles})
    sessions_held = len(sessions)
    entry_date = entry_candle["session_date"]
    terminal_date = terminal_candle["session_date"]

    terminal_candle_reference = {
        "timestamp": terminal_candle["timestamp"],
        "open": terminal_candle["open"],
        "high": terminal_candle["high"],
        "low": terminal_candle["low"],
        "close": terminal_candle["close"],
        "volume": terminal_candle["volume"],
    }

    report = {
        "schema_version": "chart_outcome_backtest_output_v1",
        "candidate_id": candidate["candidate_id"],
        "chart_only": True,
        "source_signal_timestamp": candidate["source_signal_timestamp"],
        "entry_status": "entry_reached",
        "entry_timestamp": entry_timestamp,
        "entry_reference_price": entry_reference_price,
        "terminal_outcome_type": terminal_outcome_type,
        "terminal_timestamp": terminal_candle["timestamp"],
        "terminal_reference_price": terminal_reference_price,
        "terminal_reason": terminal_reason,
        "terminal_candle_reference": terminal_candle_reference,
        "holding_period_candles": terminal_index - entry_index + 1,
        "holding_period_sessions": sessions_held,
        "same_day_fast_swing_classification": _terminal_classification(
            terminal_outcome_type,
            entry_date,
            terminal_date,
            sessions_held,
        ),
        "max_favorable_move": {
            "mfe_points": mfe_points,
            "mfe_percent": _round4((mfe_points / entry_reference_price) * 100),
            "mfe_chart_r": _round4(mfe_points / risk_points) if risk_points else None,
            "mfe_timestamp": mfe_candle["timestamp"],
            "mfe_candle_index": candles.index(mfe_candle),
            "mfe_candles_after_entry": candles.index(mfe_candle) - entry_index,
            "mfe_before_terminal_condition": True,
        },
        "max_adverse_move": {
            "mae_points": mae_points,
            "mae_percent": _round4((mae_points / entry_reference_price) * 100),
            "mae_chart_r": _round4(mae_points / risk_points) if risk_points else None,
            "mae_timestamp": mae_candle["timestamp"],
            "mae_candle_index": candles.index(mae_candle),
            "mae_candles_after_entry": candles.index(mae_candle) - entry_index,
            "mae_before_terminal_condition": True,
        },
        "chart_r_multiple": _round4(mfe_points / risk_points) if risk_points else None,
        "likely_chart_risk": {
            "entry_reference_price": entry_reference_price,
            "invalidation_reference_price": invalidation_reference_price,
            "likely_chart_risk_points": risk_points,
            "likely_chart_risk_percent": risk_percent,
            "likely_chart_risk_basis": (
                "Underlying-chart distance from calculated next eligible candle open entry "
                "to copied replay invalidation level."
            ),
            "full_risk_note": (
                "Full risk is not modeled. This output excludes option debit, spread pricing, "
                "slippage, liquidity, assignment, account drawdown, and broker execution."
            ),
        },
        "full_risk_modeled": False,
        "option_pnl_modeled": False,
        "account_sizing_modeled": False,
        "broker_order_execution_modeled": False,
        "headline_gap_risk_context": candidate["available_context"]["headline_gap_risk_context"],
        "no_hindsight_audit": {
            "rules_defined_before_future_scan": True,
            "setup_identity_not_recomputed_from_future_candles": True,
            "future_candles_used_only_for_outcome_measurement": True,
            "first_terminal_condition_stops_scan": True,
            "source_end_unresolved_when_needed": True,
            "manual_override_used": False,
            "manual_override_reason": None,
        },
        "known_unavailable_context": _known_unavailable_context(),
        "notes": (
            f"Real chart-only outcome calculation for {candidate['symbol']} "
            f"{candidate['setup_family']} sample {candidate['candidate_id']}. "
            "Uses real source OHLCV rows only, preserves unavailable headline/gap-risk context, "
            "does not model option P&L, does not add account sizing, and does not start watcher work."
        ),
    }
    return report, []


def run_chart_outcome_backtest() -> BacktestResult:
    input_schema = _load_json(INPUT_SCHEMA)
    output_schema = _load_json(OUTPUT_SCHEMA)
    candidate = _load_json(INPUT_FIXTURE)
    expected_output = _load_json(EXPECTED_OUTPUT_FIXTURE)

    errors: List[str] = []
    errors.extend(_validate_payload("input fixture", candidate, input_schema))
    errors.extend(_validate_payload("expected output fixture", expected_output, output_schema))

    if not errors:
        errors.extend(_validate_source_artifacts(candidate))

    report = None
    if not errors:
        report, calculation_errors = _build_real_chart_report(candidate)
        errors.extend(calculation_errors)

    if report is None:
        report = expected_output

    report_errors = _validate_payload("scaffold report", report, output_schema)
    errors.extend(report_errors)

    if errors:
        return BacktestResult(
            passed=False,
            errors=errors,
            report_path=REPORT_PATH,
            output_schema_valid=not report_errors,
        )

    _write_json(REPORT_PATH, report)
    return BacktestResult(
        passed=True,
        errors=[],
        report_path=REPORT_PATH,
        output_schema_valid=True,
    )


def run_scaffold() -> BacktestResult:
    return run_chart_outcome_backtest()
