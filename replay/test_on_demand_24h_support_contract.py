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

tests = [
    (
        "continuation_allowed_when_24h_mixed_not_bearish",
        {
            "option_type": "C",
            "chart_check": {"latest_close": 103.0, "ema50_1h": 100.0},
            "trend_ctx": {"supportive": None},
            "room_ratio": 3.0,
            "room_pass": True,
            "wall_pass": True,
            "extension_state": {"state": "acceptable"},
            "candles": candles([101.0, 102.0, 102.8, 103.0]),
            "continuation_context": {
                "shelf_exists": True,
                "shelf_proven": True,
                "tradeable_now": False,
                "trigger_level": 103.5,
            },
        },
        "Continuation",
        True,
    ),
    (
        "clean_fast_break_allowed_even_if_24h_countertrend",
        {
            "option_type": "C",
            "chart_check": {"latest_close": 101.0, "ema50_1h": 100.0},
            "trend_ctx": {"supportive": False},
            "room_ratio": 3.0,
            "room_pass": True,
            "wall_pass": True,
            "extension_state": {"state": "acceptable"},
            "candles": candles([100.8, 100.9, 101.0]),
            "continuation_context": {},
        },
        "Clean Fast Break",
        True,
    ),
]

failures = []

for name, kwargs, expected_type, expected_allowed in tests:
    result = _setup_classifier(**kwargs)
    actual_type = result.get("setup_type")
    actual_allowed = result.get("allowed_setup")
    ok = actual_type == expected_type and actual_allowed == expected_allowed
    print(f"{name}: {'PASS' if ok else 'FAIL'} | got type={actual_type}, allowed={actual_allowed}")
    if not ok:
        failures.append(name)

if failures:
    print("24H CONTRACT FAILURES:", ", ".join(failures))
    raise SystemExit(2)

print("24H SUPPORT CONTRACT PASS")
