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
    option_type="P",
    structure_context={
        "setup_type": "Continuation",
        "setup_eligible_now": False,
        "trend_label": "bearish",
        "latest_close": 99.70,
        "ema50_1h": 100.0,
        "continuation_context": {
            "shelf_exists": True,
            "shelf_proven": True,
            "reclaim_hold_proven": True,
            "exact_reason": "early",
            "main_blocker": "no_valid_trigger",
            "trigger_level": 99.50,
            "status_message": "Bearish Continuation shelf is forming; wait for a completed 1H close below the shelf low.",
        },
    },
    trigger_state={
        "trigger_present": False,
        "structural_trigger_present": True,
        "completed_candle_trigger_present": False,
        "structure_ready": True,
        "trigger_level": 99.50,
        "trigger_style": "first_close_below_shelf_low",
        "why": "waiting_for_completed_shelf_break_close",
        "why_human": "Put-side Continuation shelf path is forming; wait for a completed 1H close below 99.50.",
    },
    user_facing={
        "setup_state": "PENDING",
        "invalidation": "1H close back above the bearish shelf / EMA50 reclaim area invalidates the put-side Continuation path.",
        "why": "Put-side Continuation shelf path is forming; wait for a completed 1H close below 99.50.",
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
if trigger_card.get("setup_type") != "Continuation":
    failures.append("setup_type_should_be_continuation")
if "put" not in str(trigger_card.get("direction") or "").lower() and "bear" not in str(trigger_card.get("direction") or "").lower():
    failures.append("direction_should_surface_put_side_or_bearish_path")
if trigger_card.get("stage") != "PENDING":
    failures.append("stage_should_surface_pending_put_side_status")
if "forming" not in str(trigger_card.get("trigger_status") or "").lower() and "pending" not in str(trigger_card.get("trigger_status") or "").lower():
    failures.append("trigger_status_should_surface_put_side_forming_or_pending_state")
if trigger_card.get("trigger_style") != "first_close_below_shelf_low":
    failures.append("trigger_style_should_preserve_below_shelf_trigger_path")
if trigger_card.get("trigger_level") != 99.50:
    failures.append("trigger_level_should_be_carried_from_engine_context")
if "99.5" not in str(trigger_card.get("trigger_zone") or ""):
    failures.append("trigger_zone_should_include_below_trigger_reference")
if "shelf" not in str(trigger_card.get("trigger_zone") or "").lower():
    failures.append("trigger_zone_should_name_continuation_shelf_path")
if "completed 1h close below" not in str(trigger_card.get("confirmation_rule") or "").lower():
    failures.append("confirmation_rule_should_name_completed_1h_close_below")
if "put-side continuation" not in str(trigger_card.get("confirmation_rule") or "").lower():
    failures.append("confirmation_rule_should_name_put_side_continuation_path")
if "fresh" not in str(trigger_card.get("freshness_rule") or "").lower():
    failures.append("freshness_rule_should_surface_fresh_state_context")
if "completed 1h close below" not in str(trigger_card.get("next_condition") or "").lower():
    failures.append("next_condition_should_name_next_completed_1h_close_below")
if "shelf" not in str(trigger_card.get("next_condition") or "").lower():
    failures.append("next_condition_should_include_shelf_trigger_path_context")
if "above" not in str(trigger_card.get("invalidation") or "").lower():
    failures.append("invalidation_should_surface_put_side_failure_condition")
if "completed_candle_confirmation" not in trigger_card.get("blockers", []):
    failures.append("blockers_should_connect_to_trigger_readiness")
if "room_caution" not in trigger_card.get("cautions", []):
    failures.append("cautions_should_connect_to_trigger_readiness")
if "blocked by" not in str(trigger_card.get("blocker_caution_relationship") or "").lower():
    failures.append("blocker_caution_relationship_should_be_explicit")

call_side_terms = [
    "call-side",
    "upside",
    "close above the shelf high",
    "break above the trigger",
    "close above the trigger",
]
for term in call_side_terms:
    if term in response_lower:
        failures.append(f"response_text_should_not_use_call_side_language_{term.replace(' ', '_')}")

vague_only = (
    "wait for confirmation" in response_lower
    and "put" not in response_lower
    and "below" not in response_lower
    and "shelf" not in response_lower
    and "99.5" not in response_text
)
if vague_only:
    failures.append("response_text_should_not_be_vague_confirmation_only_language")

for expected in [
    "Setup: Continuation",
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

for expected in [
    "bearish / put-side",
    "completed 1H close below",
    "shelf trigger",
    "99.5",
]:
    if expected not in response_text:
        failures.append(f"response_text_missing_put_side_context_{expected}")

if failures:
    print(
        "PUT-SIDE TRIGGER CARD SURFACE CONTRACT FAILURES:",
        ", ".join(failures),
    )
    raise SystemExit(2)

print("PUT-SIDE TRIGGER CARD SURFACE CONTRACT PASS")
