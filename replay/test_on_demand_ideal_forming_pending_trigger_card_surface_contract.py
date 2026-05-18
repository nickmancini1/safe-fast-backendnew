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
        "setup_type": "Ideal",
        "setup_eligible_now": False,
        "trend_label": "bullish",
        "latest_close": 100.18,
        "ema50_1h": 100.0,
    },
    trigger_state={
        "trigger_present": False,
        "structural_trigger_present": True,
        "completed_candle_trigger_present": False,
        "structure_ready": True,
        "trigger_level": 100.42,
        "trigger_style": "ideal_retest_recovery_pending_completed_1h_close",
        "why": "waiting_for_completed_breakout_close",
        "why_human": "Ideal retest/recovery path is forming; wait for a completed 1H trigger confirmation through 100.42.",
    },
    user_facing={
        "setup_state": "PENDING",
        "invalidation": "1H close back below EMA50 / retest base near 100.0 invalidates the Ideal recovery path.",
        "why": "Ideal retest/recovery path is forming; wait for a completed 1H trigger confirmation through 100.42.",
    },
    checklist_block={
        "effective_failed_items": ["completed_candle_confirmation"],
        "caution_items": ["soft_extension_caution"],
    },
)

print("trigger_card:", trigger_card)

failures = []
response_text = str(trigger_card.get("response_text") or "")
response_lower = response_text.lower()

if trigger_card.get("surface_type") != "trigger_card":
    failures.append("surface_type_should_be_trigger_card")
if trigger_card.get("setup_type") != "Ideal":
    failures.append("setup_type_should_be_ideal")
if "call" not in str(trigger_card.get("direction") or "").lower() and "bull" not in str(trigger_card.get("direction") or "").lower():
    failures.append("direction_should_surface_call_or_bullish_path")
if trigger_card.get("stage") != "PENDING":
    failures.append("stage_should_surface_pending_status")
if "forming" not in str(trigger_card.get("trigger_status") or "").lower() and "pending" not in str(trigger_card.get("trigger_status") or "").lower():
    failures.append("trigger_status_should_surface_forming_or_pending_state")
if trigger_card.get("trigger_level") != 100.42:
    failures.append("trigger_level_should_be_carried_from_engine_context")
if "100.42" not in str(trigger_card.get("trigger_zone") or ""):
    failures.append("trigger_zone_should_include_ideal_trigger_reference")
if "ideal" not in str(trigger_card.get("trigger_zone") or "").lower():
    failures.append("trigger_zone_should_name_ideal_path")
if "completed 1h" not in str(trigger_card.get("confirmation_rule") or "").lower():
    failures.append("confirmation_rule_should_name_completed_1h_close")
if "retest" not in str(trigger_card.get("confirmation_rule") or "").lower() and "recovery" not in str(trigger_card.get("confirmation_rule") or "").lower():
    failures.append("confirmation_rule_should_name_retest_or_recovery_path")
if "fresh" not in str(trigger_card.get("freshness_rule") or "").lower():
    failures.append("freshness_rule_should_surface_fresh_state_context")
if "ideal" not in str(trigger_card.get("freshness_rule") or "").lower():
    failures.append("freshness_rule_should_be_setup_specific")
if "completed 1h" not in str(trigger_card.get("next_condition") or "").lower():
    failures.append("next_condition_should_name_next_completed_1h_check")
if "retest" not in str(trigger_card.get("next_condition") or "").lower() and "recovery" not in str(trigger_card.get("next_condition") or "").lower():
    failures.append("next_condition_should_include_trigger_path_context")
if "EMA50" not in str(trigger_card.get("invalidation") or ""):
    failures.append("invalidation_should_surface_when_available")
if "completed_candle_confirmation" not in trigger_card.get("blockers", []):
    failures.append("blockers_should_connect_to_trigger_readiness")
if "soft_extension_caution" not in trigger_card.get("cautions", []):
    failures.append("cautions_should_connect_to_trigger_readiness")
if "blocked by" not in str(trigger_card.get("blocker_caution_relationship") or "").lower():
    failures.append("blocker_caution_relationship_should_be_explicit")

vague_only = (
    (
        "wait for confirmation" in response_lower
        or "recovery confirmation" in response_lower
    )
    and "ideal" not in response_lower
    and "retest" not in response_lower
    and "100.42" not in response_text
)
if vague_only:
    failures.append("response_text_should_not_be_vague_confirmation_only_language")

for expected in [
    "Setup: Ideal",
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
        "IDEAL FORMING PENDING TRIGGER CARD SURFACE CONTRACT FAILURES:",
        ", ".join(failures),
    )
    raise SystemExit(2)

print("IDEAL FORMING PENDING TRIGGER CARD SURFACE CONTRACT PASS")
