import json
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parent
LOCAL_OUTPUT_DIR = ROOT / "fixtures" / "local_output"

CASE_TO_LOCAL_OUTPUT = {
    "continuation_too_early_001": "continuation_too_early_local_output.json",
    "continuation_needs_more_candles_001": "continuation_needs_more_candles_local_output.json",
    "continuation_valid_001": "continuation_valid_local_output.json",
    "continuation_too_late_001": "continuation_too_late_local_output.json",
    "continuation_shelf_reroll_001": "continuation_shelf_reroll_local_output.json",
}


def local_fixture_engine(case: Dict[str, Any]) -> Dict[str, Any]:
    case_id = str(case.get("case_id", ""))
    fixture_name = CASE_TO_LOCAL_OUTPUT.get(case_id)

    if fixture_name:
        fixture_path = LOCAL_OUTPUT_DIR / fixture_name
        if fixture_path.exists():
            return json.loads(fixture_path.read_text(encoding="utf-8"))

    return {
        "setup_type": case.get("setup_type_target"),
        "recognized": True,
        "confidence": 0.8,
        "source": "placeholder_scaffold",
    }
