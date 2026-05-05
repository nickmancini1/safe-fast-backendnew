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
        "ideal_label_survives_wall_block",
        {
            "option_type": "C",
            "chart_check": {"latest_close": 100.1, "ema50_1h": 100.0},
            "trend_ctx": {"supportive": True},
            "room_ratio": 3.0,
            "room_pass": True,
            "wall_pass": False,
            "extension_state": {"state": "acceptable"},
            "candles": candles([99.8, 100.0, 100.1, 100.1]),
            "continuation_context": {},
        },
        "Ideal",
        False,
    ),
    (
        "ideal_label_survives_room_block",
        {
            "option_type": "C",
            "chart_check": {"latest_close": 100.1, "ema50_1h": 100.0},
            "trend_ctx": {"supportive": True},
            "room_ratio": 3.0,
            "room_pass": False,
            "wall_pass": True,
            "extension_state": {"state": "acceptable"},
            "candles": candles([99.8, 100.0, 100.1, 100.1]),
            "continuation_context": {},
        },
        "Ideal",
        False,
    ),
    (
        "ideal_label_survives_extension_block",
        {
            "option_type": "C",
            "chart_check": {"latest_close": 100.1, "ema50_1h": 100.0},
            "trend_ctx": {"supportive": True},
            "room_ratio": 3.0,
            "room_pass": True,
            "wall_pass": True,
            "extension_state": {"state": "extended"},
            "candles": candles([99.8, 100.0, 100.1, 100.1]),
            "continuation_context": {},
        },
        "Ideal",
        False,
    ),
    (
        "clean_fast_break_label_survives_room_block",
        {
            "option_type": "C",
            "chart_check": {"latest_close": 101.0, "ema50_1h": 100.0},
            "trend_ctx": {"supportive": True},
            "room_ratio": 1.0,
            "room_pass": False,
            "wall_pass": True,
            "extension_state": {"state": "acceptable"},
            "candles": candles([100.8, 100.9, 101.0]),
            "continuation_context": {},
        },
        "Clean Fast Break",
        False,
    ),
    (
        "clean_fast_break_label_survives_wall_block",
        {
            "option_type": "C",
            "chart_check": {"latest_close": 101.0, "ema50_1h": 100.0},
            "trend_ctx": {"supportive": True},
            "room_ratio": 3.0,
            "room_pass": True,
            "wall_pass": False,
            "extension_state": {"state": "acceptable"},
            "candles": candles([100.8, 100.9, 101.0]),
            "continuation_context": {},
        },
        "Clean Fast Break",
        False,
    ),
    (
        "clean_fast_break_label_survives_extension_block",
        {
            "option_type": "C",
            "chart_check": {"latest_close": 101.0, "ema50_1h": 100.0},
            "trend_ctx": {"supportive": True},
            "room_ratio": 3.0,
            "room_pass": True,
            "wall_pass": True,
            "extension_state": {"state": "extended"},
            "candles": candles([100.8, 100.9, 101.0]),
            "continuation_context": {},
        },
        "Clean Fast Break",
        False,
    ),
    (
        "continuation_developing_label_survives_not_tradeable",
        {
            "option_type": "C",
            "chart_check": {"latest_close": 103.0, "ema50_1h": 100.0},
            "trend_ctx": {"supportive": True},
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
        False,
    ),
]

failures = []

for name, kwargs, expected_type, expected_eligible in tests:
    result = _setup_classifier(**kwargs)
    actual_type = result.get("setup_type")
    actual_eligible = result.get("setup_eligible_now")
    ok = actual_type == expected_type and actual_eligible == expected_eligible
    print(f"{name}: {'PASS' if ok else 'FAIL'} | got type={actual_type}, eligible={actual_eligible}")
    if not ok:
        failures.append(name)

if failures:
    print("CLASSIFIER CONTRACT FAILURES:", ", ".join(failures))
    raise SystemExit(2)

print("CLASSIFIER CONTRACT PASS")
