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


collect_function_dependencies("_build_trigger_card_surface")

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

_build_trigger_card_surface = ns["_build_trigger_card_surface"]

trigger_card = _build_trigger_card_surface(
    option_type="C",
    structure_context={
        "setup_type": "Clean Fast Break",
        "setup_eligible_now": False,
        "trend_label": "bullish",
        "latest_close": 101.05,
        "ema50_1h": 100.0,
    },
    trigger_state={
        "trigger_present": False,
        "structural_trigger_present": True,
        "completed_candle_trigger_present": False,
        "structure_ready": True,
        "trigger_level": 101.25,
        "trigger_style": "clean_fast_break_tight_pause_pending_completed_1h_close",
        "why": "waiting_for_completed_breakout_close",
        "why_human": "Clean Fast Break tight-pause path is forming; wait for a completed 1H break through 101.25.",
    },
    user_facing={
        "setup_state": "PENDING",
        "invalidation": "1H close back below the tight base near 100.80 invalidates the Clean Fast Break path.",
        "why": "Clean Fast Break tight-pause path is forming; wait for a completed 1H break through 101.25.",
    },
    checklist_block={
        "effective_failed_items": ["completed_candle_confirmation"],
        "caution_items": ["room_caution"],
    },
)

print("trigger_card:", trigger_card)

failures = []
response_text = str(trigger_card.get("response_text") or "")
response_lower = response_text.lower()

if trigger_card.get("surface_type") != "trigger_card":
    failures.append("surface_type_should_be_trigger_card")
if trigger_card.get("setup_type") != "Clean Fast Break":
    failures.append("setup_type_should_be_clean_fast_break")
if "call" not in str(trigger_card.get("direction") or "").lower() and "bull" not in str(trigger_card.get("direction") or "").lower():
    failures.append("direction_should_surface_call_or_bullish_path")
if trigger_card.get("stage") != "PENDING":
    failures.append("stage_should_surface_pending_status")
if "forming" not in str(trigger_card.get("trigger_status") or "").lower() and "pending" not in str(trigger_card.get("trigger_status") or "").lower():
    failures.append("trigger_status_should_surface_forming_or_pending_state")
if trigger_card.get("trigger_level") != 101.25:
    failures.append("trigger_level_should_be_carried_from_engine_context")
if "101.25" not in str(trigger_card.get("trigger_zone") or ""):
    failures.append("trigger_zone_should_include_clean_fast_break_trigger_reference")
if "clean fast break" not in str(trigger_card.get("trigger_zone") or "").lower():
    failures.append("trigger_zone_should_name_clean_fast_break_path")
if "tight" not in str(trigger_card.get("trigger_zone") or "").lower() and "base" not in str(trigger_card.get("trigger_zone") or "").lower():
    failures.append("trigger_zone_should_name_tight_pause_or_base_path")
if "completed 1h" not in str(trigger_card.get("confirmation_rule") or "").lower():
    failures.append("confirmation_rule_should_name_completed_1h_close")
if "clean fast break" not in str(trigger_card.get("confirmation_rule") or "").lower():
    failures.append("confirmation_rule_should_name_setup_type")
if "break" not in str(trigger_card.get("confirmation_rule") or "").lower():
    failures.append("confirmation_rule_should_name_break_path")
if "fresh" not in str(trigger_card.get("freshness_rule") or "").lower():
    failures.append("freshness_rule_should_surface_fresh_state_context")
if "clean fast break" not in str(trigger_card.get("freshness_rule") or "").lower():
    failures.append("freshness_rule_should_be_setup_specific")
if "completed 1h" not in str(trigger_card.get("next_condition") or "").lower():
    failures.append("next_condition_should_name_next_completed_1h_check")
if "clean fast break" not in str(trigger_card.get("next_condition") or "").lower():
    failures.append("next_condition_should_include_setup_context")
if "break" not in str(trigger_card.get("next_condition") or "").lower():
    failures.append("next_condition_should_include_trigger_path_context")
if "tight base" not in str(trigger_card.get("invalidation") or "").lower():
    failures.append("invalidation_should_surface_when_available")
if "completed_candle_confirmation" not in trigger_card.get("blockers", []):
    failures.append("blockers_should_connect_to_trigger_readiness")
if "room_caution" not in trigger_card.get("cautions", []):
    failures.append("cautions_should_connect_to_trigger_readiness")
if "blocked by" not in str(trigger_card.get("blocker_caution_relationship") or "").lower():
    failures.append("blocker_caution_relationship_should_be_explicit")

vague_only = (
    (
        "wait for confirmation" in response_lower
        or "break confirmation" in response_lower
    )
    and "clean fast break" not in response_lower
    and "tight" not in response_lower
    and "101.25" not in response_text
)
if vague_only:
    failures.append("response_text_should_not_be_vague_confirmation_only_language")

for expected in [
    "Setup: Clean Fast Break",
    "Direction:",
    "Stage: PENDING",
    "Trigger status:",
    "Trigger path:",
    "Confirmation rule:",
    "Freshness rule:",
    "Next condition:",
    "Invalidation:",
]:
    if expected not in response_text:
        failures.append(f"response_text_missing_{expected}")

if failures:
    print(
        "CLEAN FAST BREAK FORMING PENDING TRIGGER CARD SURFACE CONTRACT FAILURES:",
        ", ".join(failures),
    )
    raise SystemExit(2)

print("CLEAN FAST BREAK FORMING PENDING TRIGGER CARD SURFACE CONTRACT PASS")
