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
        "continuation_context": {
            "shelf_exists": True,
            "shelf_proven": True,
            "reclaim_hold_proven": True,
            "exact_reason": "spent",
            "main_blocker": "prior_completed_shelf_break_spent",
            "prior_completed_shelf_break_seen": True,
            "prior_completed_shelf_break_trigger_level": 100.55,
            "trigger_level": 100.55,
            "status_message": "Prior completed Continuation shelf break already happened; no fresh trigger now.",
        },
    },
    trigger_state={
        "trigger_present": False,
        "structural_trigger_present": False,
        "completed_candle_trigger_present": False,
        "structure_ready": False,
        "trigger_level": 100.55,
        "trigger_style": "prior_session_completed_shelf_break_spent",
        "why": "prior_completed_shelf_break_spent",
        "why_human": "Prior completed Continuation shelf break already happened; no fresh trigger now.",
    },
    user_facing={
        "setup_state": "NO TRADE",
        "invalidation": "1H close beyond EMA50 against thesis. Current EMA50_1h anchor: 100.0.",
        "why": "Prior completed Continuation shelf break already happened; no fresh trigger now.",
    },
    checklist_block={
        "effective_failed_items": ["fresh_entry_allowed", "prior_completed_shelf_break_spent"],
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
if trigger_card.get("stage") != "NO TRADE":
    failures.append("stage_should_surface_stale_spent_no_trade_status")
if "already happened" not in str(trigger_card.get("trigger_status") or "").lower():
    failures.append("trigger_status_should_explain_spent_prior_break")
if trigger_card.get("trigger_level") != 100.55:
    failures.append("trigger_level_should_be_carried_from_engine_context")
if "100.55" not in str(trigger_card.get("trigger_zone") or ""):
    failures.append("trigger_zone_should_include_trigger_reference")
if "completed 1h close" not in str(trigger_card.get("confirmation_rule") or "").lower():
    failures.append("confirmation_rule_should_name_completed_1h_close")
if "no fresh trigger" not in str(trigger_card.get("freshness_rule") or "").lower():
    failures.append("freshness_rule_should_explain_no_fresh_trigger")
if "new continuation shelf" not in str(trigger_card.get("next_condition") or "").lower():
    failures.append("next_condition_should_require_new_shelf")
if "EMA50" not in str(trigger_card.get("invalidation") or ""):
    failures.append("invalidation_should_surface_when_available")
if "prior_completed_shelf_break_spent" not in trigger_card.get("blockers", []):
    failures.append("blockers_should_connect_to_trigger_readiness")
if "room_caution" not in trigger_card.get("cautions", []):
    failures.append("cautions_should_connect_to_trigger_readiness")
if "blocked by" not in str(trigger_card.get("blocker_caution_relationship") or "").lower():
    failures.append("blocker_caution_relationship_should_be_explicit")

vague_only = (
    "wait for confirmation" in response_lower
    and "shelf" not in response_lower
    and "trigger" not in response_lower
    and "100.55" not in response_text
)
if vague_only:
    failures.append("response_text_should_not_be_vague_confirmation_only_language")

for expected in [
    "Setup: Continuation",
    "Stage: NO TRADE",
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
        "CONTINUATION STALE SPENT TRIGGER CARD SURFACE CONTRACT FAILURES:",
        ", ".join(failures),
    )
    raise SystemExit(2)

print("CONTINUATION STALE SPENT TRIGGER CARD SURFACE CONTRACT PASS")
