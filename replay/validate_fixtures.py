import json
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent
CASES_DIR = ROOT / "fixtures" / "cases"
EXPECTED_DIR = ROOT / "expected"

ALLOWED_SETUP_TYPES = {"IDEAL", "CLEAN_FAST_BREAK", "CONTINUATION"}


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _validate_case(case: Dict[str, Any]) -> List[str]:
    errs: List[str] = []
    for key in ["case_id", "setup_type_target", "payload"]:
        if key not in case:
            errs.append(f"missing required field '{key}'")
    if case.get("setup_type_target") not in ALLOWED_SETUP_TYPES:
        errs.append(f"invalid setup_type_target '{case.get('setup_type_target')}'")
    if not isinstance(case.get("payload"), dict):
        errs.append("payload must be an object")
    return errs


def _validate_expected(expected: Dict[str, Any]) -> List[str]:
    errs: List[str] = []
    if "case_id" not in expected:
        errs.append("missing required field 'case_id'")
    exp = expected.get("expected")
    if not isinstance(exp, dict):
        errs.append("missing required object 'expected'")
        return errs

    if exp.get("setup_type") not in ALLOWED_SETUP_TYPES:
        errs.append(f"invalid expected.setup_type '{exp.get('setup_type')}'")
    if not isinstance(exp.get("recognized"), bool):
        errs.append("expected.recognized must be boolean")
    if not isinstance(exp.get("min_confidence"), (int, float)):
        errs.append("expected.min_confidence must be numeric")

    assertions = expected.get("assertions")
    if not isinstance(assertions, list) or not assertions:
        errs.append("assertions must be a non-empty list")
    return errs


def validate_all() -> List[str]:
    errors: List[str] = []
    case_files = sorted(CASES_DIR.glob("*_case.json"))
    expected_files = sorted(EXPECTED_DIR.glob("*_expected.json"))

    expected_by_id: Dict[str, Dict[str, Any]] = {}
    for ep in expected_files:
        data = _load_json(ep)
        for e in _validate_expected(data):
            errors.append(f"{ep.name}: {e}")
        cid = data.get("case_id")
        if isinstance(cid, str):
            expected_by_id[cid] = data

    for cp in case_files:
        case = _load_json(cp)
        for e in _validate_case(case):
            errors.append(f"{cp.name}: {e}")
        cid = case.get("case_id")
        exp = expected_by_id.get(cid)
        if not exp:
            errors.append(f"{cp.name}: no expected file with matching case_id '{cid}'")
            continue
        if case.get("setup_type_target") != (exp.get("expected") or {}).get("setup_type"):
            errors.append(f"{cp.name}: setup_type_target does not match expected.setup_type")

    return errors


if __name__ == "__main__":
    errs = validate_all()
    if errs:
        print("Fixture validation failed:")
        for err in errs:
            print(f"- {err}")
        raise SystemExit(2)
    print("Fixture validation passed.")
