import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError


ROOT = Path(__file__).resolve().parent

INPUT_SCHEMA = ROOT / "schemas" / "chart_outcome_backtest_input_v1.schema.json"
OUTPUT_SCHEMA = ROOT / "schemas" / "chart_outcome_backtest_output_v1.schema.json"

INPUT_FIXTURE = ROOT / "fixtures" / "first_spy_continuation_chart_outcome_input_v1.json"
EXPECTED_OUTPUT_FIXTURE = (
    ROOT / "fixtures" / "first_spy_continuation_chart_outcome_expected_output_v1.json"
)


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _format_error(error: ValidationError) -> str:
    location = ".".join(str(part) for part in error.absolute_path)
    if not location:
        location = "<root>"
    return f"{location}: {error.message}"


def _validate_fixture(name: str, fixture_path: Path, schema_path: Path) -> List[str]:
    fixture = _load_json(fixture_path)
    schema = _load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [f"{name}: {_format_error(error)}" for error in sorted(validator.iter_errors(fixture), key=str)]


def validate_all() -> Tuple[bool, List[str]]:
    errors: List[str] = []
    errors.extend(_validate_fixture("input fixture", INPUT_FIXTURE, INPUT_SCHEMA))
    errors.extend(
        _validate_fixture("expected output fixture", EXPECTED_OUTPUT_FIXTURE, OUTPUT_SCHEMA)
    )
    return not errors, errors


if __name__ == "__main__":
    passed, validation_errors = validate_all()
    if passed:
        print("PASS chart outcome fixture schema validation")
        raise SystemExit(0)

    print("FAIL chart outcome fixture schema validation")
    for validation_error in validation_errors:
        print(f"- {validation_error}")
    raise SystemExit(1)
