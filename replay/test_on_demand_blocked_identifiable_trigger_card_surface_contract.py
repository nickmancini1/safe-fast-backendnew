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


collect_function_dependencies("_setup_classifier")
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

_setup_classifier = ns["_setup_classifier"]
_build_trigger_card_surface = ns["_build_trigger_card_surface"]


def candles(closes):
    return [
        {"open": c, "high": c + 0.2, "low": c - 0.2, "close": c}
        for c in closes
    ]


classifier_result = _setup_classifier(
    option_type="C",
    chart_check={"latest_close": 100.1, "ema50_1h": 100.0},
    trend_ctx={"supportive": True},
    room_ratio=3.0,
    room_pass=True,
    wall_pass=True,
    extension_state={"state": "acceptable"},
    candles=candles([100.0, 100.1, 100.0, 100.1]),
    continuation_context={},
)

print("classifier_result:", classifier_result)

trigger_card = _build_trigger_card_surface(
    option_type="C",
    structure_context={
        **classifier_result,
        "chop_risk": True,
        "noisy_chop_explicit": True,
        "trend_label": "bullish",
        "latest_close": 100.10,
        "ema50_1h": 100.0,
    },
    trigger_state={
        "trigger_present": False,
        "structural_trigger_present": True,
        "completed_candle_trigger_present": False,
        "structure_ready": False,
        "trigger_level": 100.42,
        "trigger_style": "ideal_retest_recovery_blocked_by_noisy_chop",
        "why": "noisy_chop",
        "why_human": "Ideal retest/recovery trigger path is identifiable but blocked by noisy chop; no ready trigger until structure cleans up and a completed 1H close confirms through 100.42.",
    },
    user_facing={
        "setup_state": "BLOCKED",
        "invalidation": "1H close back below EMA50 / retest base near 100.0 invalidates the Ideal recovery path.",
        "why": "Ideal retest/recovery path is blocked by noisy chop; wait for cleaner structure and a completed 1H trigger through 100.42.",
    },
    checklist_block={
        "effective_failed_items": ["noisy_chop"],
        "caution_items": ["room_caution"],
    },
)

print("trigger_card:", trigger_card)

failures = []
response_text = str(trigger_card.get("response_text") or "")
response_lower = response_text.lower()

if classifier_result.get("setup_type") != "Ideal":
    failures.append("blocked_classifier_should_preserve_ideal_setup_type")
if classifier_result.get("setup_eligible_now") is not False:
    failures.append("blocked_classifier_should_make_ideal_not_eligible_now")
if trigger_card.get("surface_type") != "trigger_card":
    failures.append("surface_type_should_be_trigger_card")
if trigger_card.get("setup_type") != "Ideal":
    failures.append("trigger_card_should_preserve_blocked_setup_identity")
if "clean fast break" in response_lower or "continuation" in response_lower:
    failures.append("response_text_should_not_relabel_blocked_ideal_setup")
if trigger_card.get("stage") != "BLOCKED":
    failures.append("stage_should_surface_blocked_status")
trigger_status_lower = str(trigger_card.get("trigger_status") or "").lower()
if "blocked" not in trigger_status_lower and "not ready" not in trigger_status_lower:
    failures.append("trigger_status_should_show_blocked_or_not_ready")
if "noisy chop" not in trigger_status_lower and "chop" not in trigger_status_lower:
    failures.append("trigger_status_should_name_blocker_context")
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
if "EMA50" not in str(trigger_card.get("invalidation") or ""):
    failures.append("invalidation_should_surface_when_available")
if "noisy_chop" not in trigger_card.get("blockers", []):
    failures.append("blockers_should_connect_chop_to_trigger_readiness")
if "room_caution" not in trigger_card.get("cautions", []):
    failures.append("cautions_should_connect_to_trigger_readiness")
relationship = str(trigger_card.get("blocker_caution_relationship") or "").lower()
if "blocked by" not in relationship or "noisy_chop" not in relationship:
    failures.append("blocker_caution_relationship_should_be_explicit")
if "fresh" not in str(trigger_card.get("freshness_rule") or "").lower():
    failures.append("freshness_rule_should_surface_fresh_state_context")
if "ideal" not in str(trigger_card.get("freshness_rule") or "").lower():
    failures.append("freshness_rule_should_be_setup_specific")
next_condition_lower = str(trigger_card.get("next_condition") or "").lower()
if "completed 1h" not in next_condition_lower:
    failures.append("next_condition_should_name_next_completed_1h_check")
if "ideal" not in next_condition_lower:
    failures.append("next_condition_should_keep_setup_context")
if "retest" not in next_condition_lower and "recovery" not in next_condition_lower:
    failures.append("next_condition_should_include_trigger_path_context")

vague_only = (
    "wait for confirmation" in response_lower
    and "ideal" not in response_lower
    and "retest" not in response_lower
    and "blocked" not in response_lower
    and "noisy_chop" not in response_lower
    and "chop" not in response_lower
    and "100.42" not in response_text
)
if vague_only:
    failures.append("response_text_should_not_be_vague_confirmation_only_language")

for expected in [
    "Setup: Ideal",
    "Direction:",
    "Stage: BLOCKED",
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
    "blocked by",
    "noisy_chop",
    "Ideal retest/recovery",
    "100.42",
]:
    if expected not in response_text:
        failures.append(f"response_text_missing_blocked_context_{expected}")

if failures:
    print(
        "BLOCKED IDENTIFIABLE TRIGGER CARD SURFACE CONTRACT FAILURES:",
        ", ".join(failures),
    )
    raise SystemExit(2)

print("BLOCKED IDENTIFIABLE TRIGGER CARD SURFACE CONTRACT PASS")
