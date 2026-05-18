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
        "setup_type": "Continuation",
        "setup_eligible_now": False,
        "trend_label": "bullish",
        "latest_close": 100.56,
        "ema50_1h": 100.0,
        "continuation_context": {
            "shelf_exists": True,
            "shelf_proven": True,
            "reclaim_hold_proven": True,
            "exact_reason": "early",
            "main_blocker": "no_valid_trigger",
            "trigger_level": 100.50,
            "distance_current_to_shelf_high": 0.06,
            "distance_current_to_shelf_high_atr": 0.12,
            "atr_14_1h": 0.50,
            "status_message": "Current bar is above the shelf trigger; waiting for the completed 1H close.",
        },
    },
    trigger_state={
        "trigger_present": False,
        "structural_trigger_present": True,
        "completed_candle_trigger_present": False,
        "pending_completed_candle_approval": True,
        "structure_ready": True,
        "trigger_level": 100.50,
        "current_close": 100.56,
        "trigger_style": "first_close_above_shelf_high",
        "why": "waiting_for_completed_shelf_break_close",
        "why_human": "Continuation shelf trigger is arming: current price is through 100.50, but SAFE-FAST still needs a completed 1H close.",
    },
    user_facing={
        "setup_state": "PENDING",
        "invalidation": "1H close back below the shelf/reclaim area invalidates the Continuation path.",
        "why": "Continuation shelf trigger is arming; wait for a completed 1H close through 100.50.",
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
if "call" not in str(trigger_card.get("direction") or "").lower() and "bull" not in str(trigger_card.get("direction") or "").lower():
    failures.append("direction_should_surface_call_or_bullish_path")
if trigger_card.get("stage") != "PENDING":
    failures.append("stage_should_surface_pending_status")

trigger_status_lower = str(trigger_card.get("trigger_status") or "").lower()
if not any(term in trigger_status_lower for term in ["arming", "near", "approach", "pending"]):
    failures.append("trigger_status_should_surface_near_trigger_or_arming_state")
if trigger_card.get("trigger_level") != 100.50:
    failures.append("trigger_level_should_be_carried_from_engine_context")
if "100.5" not in str(trigger_card.get("trigger_zone") or ""):
    failures.append("trigger_zone_should_include_trigger_reference")
if "shelf" not in str(trigger_card.get("trigger_zone") or "").lower():
    failures.append("trigger_zone_should_name_continuation_shelf_path")
if "completed 1h close above" not in str(trigger_card.get("confirmation_rule") or "").lower():
    failures.append("confirmation_rule_should_name_completed_1h_close_above")

distance_text = str(trigger_card.get("current_distance_to_trigger") or "")
if "0.06" not in distance_text:
    failures.append("current_distance_to_trigger_should_surface_existing_distance")
if "above" not in distance_text.lower() and "through" not in distance_text.lower():
    failures.append("current_distance_to_trigger_should_name_side_of_trigger")

proximity_text = str(trigger_card.get("trigger_proximity") or "").lower()
if not any(term in proximity_text for term in ["near", "arming", "pending"]):
    failures.append("trigger_proximity_should_surface_near_trigger_context")
if "0.12 atr" not in proximity_text:
    failures.append("trigger_proximity_should_include_existing_atr_distance")

threshold_text = str(trigger_card.get("early_warning_threshold") or "").lower()
if "1.0 atr" not in threshold_text and "one atr" not in threshold_text:
    failures.append("early_warning_threshold_should_surface_existing_engine_window_when_available")

if "completed 1h" not in str(trigger_card.get("next_condition") or "").lower():
    failures.append("next_condition_should_name_next_completed_1h_check")
if "shelf" not in str(trigger_card.get("next_condition") or "").lower():
    failures.append("next_condition_should_include_shelf_trigger_path_context")
if "below" not in str(trigger_card.get("invalidation") or "").lower():
    failures.append("invalidation_should_surface_when_available")
if "completed_candle_confirmation" not in trigger_card.get("blockers", []):
    failures.append("blockers_should_connect_to_trigger_readiness")
if "room_caution" not in trigger_card.get("cautions", []):
    failures.append("cautions_should_connect_to_trigger_readiness")
if "blocked by" not in str(trigger_card.get("blocker_caution_relationship") or "").lower():
    failures.append("blocker_caution_relationship_should_be_explicit")

vague_only = (
    "wait for confirmation" in response_lower
    and "near" not in response_lower
    and "arming" not in response_lower
    and "shelf" not in response_lower
    and "100.5" not in response_text
    and "0.06" not in response_text
)
if vague_only:
    failures.append("response_text_should_not_be_vague_confirmation_only_language")

for expected in [
    "Setup: Continuation",
    "Direction:",
    "Stage: PENDING",
    "Trigger status:",
    "Trigger path:",
    "Current distance to trigger:",
    "Trigger proximity:",
    "Early-warning threshold:",
    "Confirmation rule:",
    "Freshness rule:",
    "Next condition:",
    "Invalidation:",
]:
    if expected not in response_text:
        failures.append(f"response_text_missing_{expected}")

for expected in [
    "arming",
    "100.5",
    "0.06",
    "0.12 ATR",
    "completed 1H close above",
]:
    if expected not in response_text:
        failures.append(f"response_text_missing_near_trigger_context_{expected}")

if failures:
    print(
        "NEAR TRIGGER EARLY WARNING TRIGGER CARD SURFACE CONTRACT FAILURES:",
        ", ".join(failures),
    )
    raise SystemExit(2)

print("NEAR TRIGGER EARLY WARNING TRIGGER CARD SURFACE CONTRACT PASS")
