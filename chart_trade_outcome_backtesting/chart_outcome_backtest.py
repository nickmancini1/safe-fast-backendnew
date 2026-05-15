import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent

INPUT_SCHEMA = ROOT / "schemas" / "chart_outcome_backtest_input_v1.schema.json"
OUTPUT_SCHEMA = ROOT / "schemas" / "chart_outcome_backtest_output_v1.schema.json"
INPUT_FIXTURE = ROOT / "fixtures" / "first_spy_continuation_chart_outcome_input_v1.json"
EXPECTED_OUTPUT_FIXTURE = (
    ROOT / "fixtures" / "first_spy_continuation_chart_outcome_expected_output_v1.json"
)
REPORT_PATH = ROOT / "reports" / "first_spy_continuation_chart_outcome_result_v1.json"


@dataclass(frozen=True)
class ScaffoldResult:
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

    source_csv_path = REPO_ROOT / "historical_signal_replay" / "source_data" / "incoming" / "first_real_historical_replay_v1_SPY_source.csv"
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
            errors.append("source_csv: required rows must be SPY 1h_rth regular-session candles")

    return errors


def _build_scaffold_report(expected_output: Dict[str, Any]) -> Dict[str, Any]:
    report = dict(expected_output)
    report["notes"] = (
        "Scaffold/sample runner report only. This file copies the schema-valid expected "
        "output fixture as a v1 scaffold target; it is not full backtest proof, does not "
        "calculate real profitability, does not model option P&L, does not add account "
        "sizing, and does not start watcher implementation."
    )
    return report


def run_scaffold() -> ScaffoldResult:
    input_schema = _load_json(INPUT_SCHEMA)
    output_schema = _load_json(OUTPUT_SCHEMA)
    candidate = _load_json(INPUT_FIXTURE)
    expected_output = _load_json(EXPECTED_OUTPUT_FIXTURE)

    errors: List[str] = []
    errors.extend(_validate_payload("input fixture", candidate, input_schema))
    errors.extend(_validate_payload("expected output fixture", expected_output, output_schema))

    if not errors:
        errors.extend(_validate_source_artifacts(candidate))

    report = _build_scaffold_report(expected_output)
    report_errors = _validate_payload("scaffold report", report, output_schema)
    errors.extend(report_errors)

    if errors:
        return ScaffoldResult(
            passed=False,
            errors=errors,
            report_path=REPORT_PATH,
            output_schema_valid=not report_errors,
        )

    _write_json(REPORT_PATH, report)
    return ScaffoldResult(
        passed=True,
        errors=[],
        report_path=REPORT_PATH,
        output_schema_valid=True,
    )
