import ast
from pathlib import Path
from typing import Any, Dict, List, Optional

source = Path("main.py").read_text(encoding="utf-8")
tree = ast.parse(source)

needed = {
    "_humanize_trigger_reason_key",
    "_humanize_reason_text",
    "_build_trigger_context_block",
}

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

humanize_trigger = ns["_humanize_trigger_reason_key"]
humanize_reason = ns["_humanize_reason_text"]
build_trigger_context = ns["_build_trigger_context_block"]

raw_reason = "prior_completed_shelf_break_spent"
expected_phrase = "no fresh trigger now"

trigger_state = {
    "trigger_present": False,
    "structural_trigger_present": False,
    "current_bar_trigger_present": False,
    "completed_candle_trigger_present": False,
    "structure_ready": False,
    "trigger_level": 100.55,
    "trigger_style": "prior_session_completed_shelf_break_spent",
    "why": raw_reason,
    "why_human": "Prior completed Continuation shelf break already happened; no fresh trigger now.",
}

live_map = {
    "trigger_scan": {
        "current_bar": {},
        "most_recent_completed_candle": {},
    }
}

human_trigger = humanize_trigger(raw_reason)
human_reason = humanize_reason(raw_reason)
trigger_context = build_trigger_context(trigger_state, live_map)

print("human_trigger:", human_trigger)
print("human_reason:", human_reason)
print("trigger_context:", trigger_context)

failures = []

if expected_phrase not in str(human_trigger or "").lower():
    failures.append("humanize_trigger_should_explain_no_fresh_trigger")

if expected_phrase not in str(human_reason or "").lower():
    failures.append("humanize_reason_should_explain_no_fresh_trigger")

context_human = (
    trigger_context.get("trigger_reason_human")
    or trigger_context.get("why_human")
    or ""
)

if expected_phrase not in str(context_human or "").lower():
    failures.append("trigger_context_should_surface_human_no_fresh_trigger_reason")

if trigger_context.get("trigger_reason") != raw_reason:
    failures.append("trigger_context_should_keep_raw_reason_key")

if failures:
    print("SESSION BOUNDARY SURFACE CONTRACT FAILURES:", ", ".join(failures))
    raise SystemExit(2)

print("SESSION BOUNDARY SURFACE CONTRACT PASS")
