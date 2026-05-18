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
    },
    trigger_state={
        "trigger_present": False,
        "structural_trigger_present": True,
        "completed_candle_trigger_present": False,
        "structure_ready": True,
        "trigger_level": None,
        "current_close": None,
        "trigger_style": None,
        "why": "trigger_card_inputs_unavailable",
        "why_human": "Ideal setup is identifiable, but trigger-card fields are unconfirmed because trigger inputs are unavailable.",
        "confirmation_rule_unavailable": True,
    },
    user_facing={
        "setup_state": "PENDING",
        "why": "Ideal setup is identifiable, but trigger-card fields are unconfirmed.",
    },
    checklist_block={
        "effective_failed_items": ["trigger_card_inputs_unavailable"],
        "caution_items": [],
    },
)

print("trigger_card:", trigger_card)

failures = []
response_text = str(trigger_card.get("response_text") or "")
response_lower = response_text.lower()


def has_unconfirmed_marker(value):
    value_lower = str(value or "").lower()
    return "unconfirmed" in value_lower or "unavailable" in value_lower


if trigger_card.get("surface_type") != "trigger_card":
    failures.append("surface_type_should_be_trigger_card")
if trigger_card.get("setup_type") != "Ideal":
    failures.append("setup_identity_should_survive_missing_trigger_card_fields")
if trigger_card.get("stage") != "PENDING":
    failures.append("stage_should_survive_missing_trigger_card_fields")
if "ideal" not in str(trigger_card.get("trigger_status") or "").lower():
    failures.append("trigger_status_should_preserve_identifiable_setup_context")
if "unconfirmed" not in str(trigger_card.get("trigger_status") or "").lower():
    failures.append("trigger_status_should_mark_missing_trigger_card_inputs_unconfirmed")

if trigger_card.get("trigger_level") is not None:
    failures.append("missing_trigger_level_should_not_be_fabricated")
if not has_unconfirmed_marker(trigger_card.get("trigger_zone")):
    failures.append("missing_trigger_zone_should_be_marked_unconfirmed_or_unavailable")
if not has_unconfirmed_marker(trigger_card.get("current_distance_to_trigger")):
    failures.append("missing_distance_should_be_marked_unconfirmed_or_unavailable")
if not has_unconfirmed_marker(trigger_card.get("trigger_proximity")):
    failures.append("missing_proximity_should_be_marked_unconfirmed_or_unavailable")
if not has_unconfirmed_marker(trigger_card.get("early_warning_threshold")):
    failures.append("missing_early_warning_threshold_should_be_marked_unconfirmed_or_unavailable")
if not has_unconfirmed_marker(trigger_card.get("invalidation")):
    failures.append("missing_invalidation_should_be_marked_unconfirmed_or_unavailable")
if not has_unconfirmed_marker(trigger_card.get("confirmation_rule")):
    failures.append("missing_candle_timeframe_rule_should_be_marked_unconfirmed_or_unavailable")
if "completed-candle/timeframe" not in str(trigger_card.get("confirmation_rule") or "").lower():
    failures.append("missing_candle_timeframe_rule_should_name_the_unavailable_rule")
if "trigger-card rule inputs are unconfirmed" not in str(trigger_card.get("next_condition") or "").lower():
    failures.append("next_condition_should_not_treat_unknown_trigger_rule_as_known")
if "trigger_card_inputs_unavailable" not in trigger_card.get("blockers", []):
    failures.append("blockers_should_connect_missing_inputs_to_trigger_readiness")

for expected in [
    "Setup: Ideal",
    "Stage: PENDING",
    "Trigger status:",
    "Trigger path:",
    "Current distance to trigger:",
    "Trigger proximity:",
    "Early-warning threshold:",
    "Confirmation rule:",
    "Next condition:",
    "Invalidation:",
]:
    if expected not in response_text:
        failures.append(f"response_text_missing_{expected}")

for expected in [
    "trigger level",
    "distance",
    "proximity",
    "completed-candle/timeframe",
    "invalidation",
]:
    if expected not in response_lower:
        failures.append(f"response_text_should_name_unconfirmed_field_{expected}")

if response_lower.count("unconfirmed") + response_lower.count("unavailable") < 5:
    failures.append("response_text_should_explicitly_mark_each_missing_trigger_card_field")

vague_only = (
    "wait for confirmation" in response_lower
    and "trigger level" not in response_lower
    and "distance" not in response_lower
    and "invalidation" not in response_lower
    and "completed-candle/timeframe" not in response_lower
)
if vague_only:
    failures.append("response_text_should_not_be_vague_confirmation_only_language")

fabricated_numbers = ["100.", "101.", "99.", "0.0", "1.0 atr"]
for fabricated in fabricated_numbers:
    if fabricated in response_lower:
        failures.append(f"response_text_should_not_fabricate_missing_value_{fabricated}")

if failures:
    print(
        "MISSING DATA UNCONFIRMED TRIGGER CARD SURFACE CONTRACT FAILURES:",
        ", ".join(failures),
    )
    raise SystemExit(2)

print("MISSING DATA UNCONFIRMED TRIGGER CARD SURFACE CONTRACT PASS")
