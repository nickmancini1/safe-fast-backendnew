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


def structure_context(continuation_overrides=None, structure_overrides=None):
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
        "current_breakout_without_completed_confirmation": False,
        "status_message": "Hold proven. Waiting for first completed shelf break.",
    }
    if continuation_overrides:
        continuation.update(continuation_overrides)

    structure = {
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
        "extension_blocks_now": False,
        "extension_soft_flag": False,
        "continuation_context": continuation,
    }
    if structure_overrides:
        structure.update(structure_overrides)
    return structure


def assert_case(name, actual, expected):
    print(f"{name}: {actual}")
    failures = []
    for key, expected_value in expected.items():
        if actual.get(key) != expected_value:
            failures.append(f"{key}:expected_{expected_value}_got_{actual.get(key)}")
    return failures


failures = []

intrabar_waiting = _build_trigger_state(
    "C",
    {"is_open": True},
    {"fresh_entry_allowed": True},
    structure_context(),
    chart_check(completed_close=100.40, current_close=100.80),
)
failures.extend(
    f"intrabar_raw_waits_completed_close:{item}"
    for item in assert_case(
        "intrabar_raw_waits_completed_close",
        {
            "trigger_present": intrabar_waiting.get("trigger_present"),
            "structural_trigger_present": intrabar_waiting.get("structural_trigger_present"),
            "completed_candle_trigger_present": intrabar_waiting.get("completed_candle_trigger_present"),
            "pending_completed_candle_approval": intrabar_waiting.get("pending_completed_candle_approval"),
            "why": intrabar_waiting.get("why"),
        },
        {
            "trigger_present": False,
            "structural_trigger_present": False,
            "completed_candle_trigger_present": False,
            "pending_completed_candle_approval": False,
            "why": "waiting_for_completed_shelf_break_close",
        },
    )
)

completed_market_closed = _build_trigger_state(
    "C",
    {"is_open": False},
    {"fresh_entry_allowed": False, "reason": "market_closed"},
    structure_context(
        continuation_overrides={
            "exact_reason": "tradeable",
            "main_blocker": None,
            "inside_tradeable_window": True,
            "current_break_is_first_completed_break": True,
            "status_message": "Tradeable now: reclaim hold is proven and the shelf break is in range.",
        }
    ),
    chart_check(completed_close=100.80, current_close=100.90),
)
failures.extend(
    f"completed_trigger_market_closed_not_live:{item}"
    for item in assert_case(
        "completed_trigger_market_closed_not_live",
        {
            "trigger_present": completed_market_closed.get("trigger_present"),
            "structural_trigger_present": completed_market_closed.get("structural_trigger_present"),
            "completed_candle_trigger_present": completed_market_closed.get("completed_candle_trigger_present"),
            "structure_ready": completed_market_closed.get("structure_ready"),
            "live_entry_requires_market_open": completed_market_closed.get("live_entry_requires_market_open"),
            "live_entry_waiting_on": completed_market_closed.get("live_entry_waiting_on"),
            "why": completed_market_closed.get("why"),
        },
        {
            "trigger_present": False,
            "structural_trigger_present": True,
            "completed_candle_trigger_present": False,
            "structure_ready": True,
            "live_entry_requires_market_open": True,
            "live_entry_waiting_on": "market_open",
            "why": "completed_candle_trigger_market_closed",
        },
    )
)

too_early_hold = _build_trigger_state(
    "C",
    {"is_open": True},
    {"fresh_entry_allowed": True},
    structure_context(
        continuation_overrides={
            "shelf_proven": False,
            "reclaim_hold_proven": False,
            "breakout_completed": False,
            "exact_reason": "early",
            "main_blocker": "no_proven_hold",
            "status_message": "Too early: hold is not proven yet.",
        }
    ),
    chart_check(completed_close=100.40, current_close=100.45),
)
failures.extend(
    f"too_early_hold_not_live:{item}"
    for item in assert_case(
        "too_early_hold_not_live",
        {
            "trigger_present": too_early_hold.get("trigger_present"),
            "structure_ready": too_early_hold.get("structure_ready"),
            "why": too_early_hold.get("why"),
        },
        {
            "trigger_present": False,
            "structure_ready": False,
            "why": "too_early_hold_not_proven",
        },
    )
)

if failures:
    print("TRIGGER STAGE CONTRACT FAILURES:", ", ".join(failures))
    raise SystemExit(2)

print("TRIGGER STAGE CONTRACT PASS")
