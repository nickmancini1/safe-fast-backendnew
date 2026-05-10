import ast
from pathlib import Path
from typing import Any, Dict, List, Optional

source = Path("main.py").read_text(encoding="utf-8")
tree = ast.parse(source)

needed = {"_to_float", "_is_chop", "_continuation_family_detected", "_setup_classifier"}
ns = {
    "Any": Any,
    "Dict": Dict,
    "List": List,
    "Optional": Optional,
}

for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in needed:
        mod = ast.Module(body=[node], type_ignores=[])
        ast.fix_missing_locations(mod)
        exec(compile(mod, filename="main.py", mode="exec"), ns)

_setup_classifier = ns["_setup_classifier"]


def candles(closes):
    return [
        {"open": c, "high": c + 0.2, "low": c - 0.2, "close": c}
        for c in closes
    ]


result = _setup_classifier(
    option_type="C",
    chart_check={"latest_close": 101.0, "ema50_1h": 100.0},
    trend_ctx={"supportive": True},
    room_ratio=3.0,
    room_pass=True,
    wall_pass=True,
    extension_state={"state": "acceptable"},
    candles=candles([100.9, 101.0, 100.9, 101.0]),
    continuation_context={},
)

expected = {
    "setup_type": "Clean Fast Break",
    "allowed_setup": True,
    "setup_type_allowed": True,
    "setup_eligible_now": False,
}

failures = []
for key, expected_value in expected.items():
    actual = result.get(key)
    if actual != expected_value:
        failures.append(f"{key}: expected {expected_value!r}, got {actual!r}")

if failures:
    print("CLEAN FAST BREAK CHOP IDENTITY CONTRACT FAIL")
    print("result:", result)
    for failure in failures:
        print(failure)
    raise SystemExit(2)

print("CLEAN FAST BREAK CHOP IDENTITY CONTRACT PASS")
