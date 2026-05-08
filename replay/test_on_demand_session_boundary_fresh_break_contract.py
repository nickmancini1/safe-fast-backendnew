import ast
import copy
import json
import math
import re
from datetime import datetime, time, timedelta, timezone
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


for root_name in {
    "_build_continuation_window_context",
    "_build_trigger_state",
}:
    collect_function_dependencies(root_name)


NY_TZ_FIXED = timezone(timedelta(hours=-4), "EDT")


def ZoneInfo_stub(key):
    if key == "America/New_York":
        return NY_TZ_FIXED
    return timezone.utc


ns = {
    "Any": Any,
    "Dict": Dict,
    "List": List,
    "Optional": Optional,
    "datetime": datetime,
    "time": time,
    "timedelta": timedelta,
    "timezone": timezone,
    "ZoneInfo": ZoneInfo_stub,
    "Path": Path,
    "copy": copy,
    "json": json,
    "math": math,
    "re": re,
    "NY_TZ": NY_TZ_FIXED,
    "ALLOWED_SETUP_TYPES": {"Ideal", "Clean Fast Break", "Continuation"},
}

future_annotations = ast.ImportFrom(
    module="__future__",
    names=[ast.alias(name="annotations")],
    level=0,
)

for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in needed:
        mod = ast.Module(body=[future_annotations, node], type_ignores=[])
        ast.fix_missing_locations(mod)
        exec(compile(mod, filename="main.py", mode="exec"), ns)

_build_continuation_window_context = ns["_build_continuation_window_context"]
_build_trigger_state = ns["_build_trigger_state"]


def candle(time_iso, open_, high, low, close):
    return {
        "time_iso": time_iso,
        "open": open_,
        "high": high,
        "low": low,
        "close": close,
    }


def build_chart_check(candles):
    latest_close = candles[-1]["close"]
    return {
        "ok": True,
        "ema50_1h": 100.0,
        "latest_close": latest_close,
        "price_vs_ema50_1h": "above" if latest_close > 100.0 else "below",
        "recent_candles": candles,
    }


def continuation_context_for(candles):
    latest_close = candles[-1]["close"]
    return _build_continuation_window_context(
        option_type="C",
        candles=candles,
        latest_close=latest_close,
        ema50_1h=100.0,
        trend_supportive=True,
        room_pass=True,
        extension_blocks_now=False,
    )


def trigger_state_for(candles, continuation_context):
    chart_check = build_chart_check(candles)
    structure_context = {
        "setup_type": "Continuation",
        "setup_type_allowed": True,
        "allowed_setup": True,
        "setup_eligible_now": True,
        "continuation_context": continuation_context,
    }

    return _build_trigger_state(
        "C",
        {"is_open": True},
        {"fresh_entry_allowed": True},
        structure_context,
        chart_check,
    )


fresh_current_session_break_after_prior_session_break = [
    # Prior session: completed Continuation-style shelf and break.
    candle("2026-05-06T09:30:00-04:00", 99.80, 100.20, 99.70, 100.00),
    candle("2026-05-06T10:30:00-04:00", 100.00, 100.30, 99.90, 100.10),
    candle("2026-05-06T11:30:00-04:00", 100.35, 100.65, 100.25, 100.55),
    candle("2026-05-06T12:30:00-04:00", 100.50, 100.70, 100.35, 100.60),
    candle("2026-05-06T13:30:00-04:00", 100.55, 100.75, 100.45, 100.65),
    candle("2026-05-06T14:30:00-04:00", 100.65, 101.00, 100.60, 100.85),

    # Current session: new shelf and fresh current-session break.
    candle("2026-05-07T09:30:00-04:00", 100.65, 100.90, 100.55, 100.75),
    candle("2026-05-07T10:30:00-04:00", 100.95, 101.05, 100.85, 101.00),
    candle("2026-05-07T11:30:00-04:00", 101.00, 101.10, 100.90, 101.05),
    candle("2026-05-07T12:30:00-04:00", 101.05, 101.35, 101.00, 101.25),
    candle("2026-05-07T13:30:00-04:00", 101.25, 101.40, 101.15, 101.30),
]

continuation_context = continuation_context_for(fresh_current_session_break_after_prior_session_break)
trigger_state = trigger_state_for(
    fresh_current_session_break_after_prior_session_break,
    continuation_context,
)

compact_continuation = {
    "exact_reason": continuation_context.get("exact_reason"),
    "main_blocker": continuation_context.get("main_blocker"),
    "status_message": continuation_context.get("status_message"),
    "prior_completed_shelf_break_seen": continuation_context.get("prior_completed_shelf_break_seen"),
    "tradeable_now": continuation_context.get("tradeable_now"),
    "inside_tradeable_window": continuation_context.get("inside_tradeable_window"),
    "breakout_completed": continuation_context.get("breakout_completed"),
    "breakout_candle_time_iso": continuation_context.get("breakout_candle_time_iso"),
    "trigger_level": continuation_context.get("trigger_level"),
}

compact_trigger = {
    "structure_ready": trigger_state.get("structure_ready"),
    "trigger_present": trigger_state.get("trigger_present"),
    "completed_candle_trigger_present": trigger_state.get("completed_candle_trigger_present"),
    "why": trigger_state.get("why"),
    "trigger_style": trigger_state.get("trigger_style"),
    "trigger_level": trigger_state.get("trigger_level"),
}

print("fresh_current_session_break continuation:", compact_continuation)
print("fresh_current_session_break trigger_state:", compact_trigger)

failures = []

if continuation_context.get("prior_completed_shelf_break_seen") is True:
    failures.append("fresh_current_session_break_should_not_be_marked_prior_spent")

if continuation_context.get("exact_reason") != "tradeable":
    failures.append("fresh_current_session_break_should_remain_tradeable")

if continuation_context.get("tradeable_now") is not True:
    failures.append("fresh_current_session_break_tradeable_now_should_be_true")

if continuation_context.get("inside_tradeable_window") is not True:
    failures.append("fresh_current_session_break_inside_window_should_be_true")

message = str(continuation_context.get("status_message") or "").lower()
if "prior completed" in message or "no fresh continuation trigger" in message:
    failures.append("fresh_current_session_break_should_not_use_prior_spent_message")

if trigger_state.get("why") == "prior_completed_shelf_break_spent":
    failures.append("fresh_current_session_break_should_not_surface_prior_spent_trigger_reason")

if trigger_state.get("trigger_style") == "prior_session_completed_shelf_break_spent":
    failures.append("fresh_current_session_break_should_not_use_prior_spent_trigger_style")

if failures:
    print("SESSION BOUNDARY FRESH BREAK CONTRACT FAILURES:", ", ".join(failures))
    raise SystemExit(2)

print("SESSION BOUNDARY FRESH BREAK CONTRACT PASS")
