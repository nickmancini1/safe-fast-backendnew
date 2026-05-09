import ast
from pathlib import Path
from typing import Any, Dict, List, Optional

source = Path("main.py").read_text(encoding="utf-8")
tree = ast.parse(source)

function_defs = {
    node.name: node
    for node in tree.body
    if isinstance(node, ast.FunctionDef)
}

needed = set()


def collect_function_dependencies(name):
    if name in needed or name not in function_defs:
        return
    needed.add(name)
    for child in ast.walk(function_defs[name]):
        if isinstance(child, ast.Call):
            func = child.func
            if isinstance(func, ast.Name) and func.id in function_defs:
                collect_function_dependencies(func.id)


collect_function_dependencies("_build_trigger_state")

ns = {
    "Any": Any,
    "Dict": Dict,
    "List": List,
    "Optional": Optional,
}

future_annotations = ast.ImportFrom(
    module="__future__",
    names=[ast.alias(name="annotations")],
    level=0,
)

for node in sorted(tree.body, key=lambda item: getattr(item, "lineno", 0)):
    if isinstance(node, ast.FunctionDef) and node.name in needed:
        mod = ast.Module(body=[future_annotations, node], type_ignores=[])
        ast.fix_missing_locations(mod)
        exec(compile(mod, filename="main.py", mode="exec"), ns)

_build_trigger_state = ns["_build_trigger_state"]


def candle(time_iso, close):
    return {
        "time_iso": time_iso,
        "open": close - 0.05,
        "high": close + 0.10,
        "low": close - 0.10,
        "close": close,
    }


def chart_check(completed_close, current_close):
    candles = [
        candle("2026-05-07T10:30:00-04:00", 100.10),
        candle("2026-05-07T11:30:00-04:00", completed_close),
        candle("2026-05-07T12:30:00-04:00", current_close),
    ]
    return {
        "ok": True,
        "recent_candles": candles,
        "latest_close": current_close,
        "ema50_1h": 100.0,
        "price_vs_ema50_1h": "above" if current_close > 100.0 else "below",
    }


def structure_context():
    continuation = {
        "shelf_exists": True,
        "shelf_proven": True,
        "reclaim_hold_proven": True,
        "exact_reason": "early",
        "main_blocker": "no_valid_trigger",
        "trigger_level": 100.50,
        "breakout_completed": True,
        "inside_tradeable_window": False,
        "current_break_is_first_completed_break": False,
        "current_breakout_without_completed_confirmation": True,
        "status_message": "Hold proven. Waiting for first completed shelf break.",
    }

    return {
        "setup_type": "Continuation",
        "setup_type_allowed": True,
        "allowed_setup": True,
        "setup_eligible_now": False,
        "wall_pass": True,
        "room_hard_fail": False,
        "room_pass": True,
        "noisy_chop_explicit": False,
        "chop_risk": False,
        "valid_post_impulse_shelf_not_chop": True,
        "hidden_left_cluster_found": False,
        "parabolic_exhaustion": False,
        "extension_blocks_now": True,
        "extension_soft_flag": True,
        "continuation_context": continuation,
    }


def assert_case(name, actual, expected):
    print(f"{name}: {actual}")
    failures = []
    for key, expected_value in expected.items():
        if actual.get(key) != expected_value:
            failures.append(f"{key}:expected_{expected_value}_got_{actual.get(key)}")
    return failures


soft_extension_pending = _build_trigger_state(
    "C",
    {"is_open": True},
    {"fresh_entry_allowed": True},
    structure_context(),
    chart_check(completed_close=100.40, current_close=100.80),
)

failures = [
    f"soft_extension_intrabar_break_pending_completed_approval:{item}"
    for item in assert_case(
        "soft_extension_intrabar_break_pending_completed_approval",
        {
            "trigger_present": soft_extension_pending.get("trigger_present"),
            "structural_trigger_present": soft_extension_pending.get("structural_trigger_present"),
            "completed_candle_trigger_present": soft_extension_pending.get("completed_candle_trigger_present"),
            "pending_completed_candle_approval": soft_extension_pending.get("pending_completed_candle_approval"),
            "structure_ready": soft_extension_pending.get("structure_ready"),
            "why": soft_extension_pending.get("why"),
        },
        {
            "trigger_present": False,
            "structural_trigger_present": False,
            "completed_candle_trigger_present": False,
            "pending_completed_candle_approval": True,
            "structure_ready": True,
            "why": "pending_completed_candle_approval",
        },
    )
]

if failures:
    print("SOFT-EXTENSION PENDING TRIGGER CONTRACT FAILURES:", ", ".join(failures))
    raise SystemExit(2)

print("SOFT-EXTENSION PENDING TRIGGER CONTRACT PASS")
