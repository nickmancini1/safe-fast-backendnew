import ast
from pathlib import Path
from typing import Any, Dict, List, Optional

source = Path("main.py").read_text(encoding="utf-8")
tree = ast.parse(source)

needed = {
    "_to_float",
    "_build_checklist_block",
    "_is_allowed_setup_type_name",
    "_continuation_family_detected",
}

ns = {
    "Any": Any,
    "Dict": Dict,
    "List": List,
    "Optional": Optional,
    "ALLOWED_SETUP_TYPES": {"Ideal", "Clean Fast Break", "Continuation"},
}

for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in needed:
        mod = ast.Module(body=[node], type_ignores=[])
        ast.fix_missing_locations(mod)
        exec(compile(mod, filename="main.py", mode="exec"), ns)


class Req:
    open_positions = 0


def build_checklist(wall_thesis_fit_status):
    return ns["_build_checklist_block"](
        request=Req(),
        market_context={"is_open": True},
        time_day_gate={"fresh_entry_allowed": True},
        structure_context={
            "setup_type": "Ideal",
            "setup_type_allowed": True,
            "allowed_setup": True,
            "twentyfour_hour_supportive": True,
            "chop_risk": False,
            "noisy_chop_explicit": False,
            "room_quality": "pass",
            "room_hard_fail": False,
            "room_pass": True,
            "first_wall": 105.0,
            "extension_blocks_now": False,
            "extension_soft_flag": False,
            "extension_material": False,
            "ath_open_air_blocks_now": False,
        },
        chart_check={"ema50_1h": 100.0, "price_vs_ema50_1h": "above"},
        primary_candidate={"fits_risk_budget": True},
        liquidity_context={"liquidity_pass": True},
        trigger_state={"trigger_present": True},
        wall_thesis_fit_context={"wall_thesis_fit_status": wall_thesis_fit_status},
    )


failures = []

pass_checklist = build_checklist("pass")
print("pass failed_items:", pass_checklist.get("failed_items"))
print("pass global_gate_failures:", pass_checklist.get("global_gate_failures"))
print("pass effective_decision_blockers_priority:", pass_checklist.get("effective_decision_blockers_priority"))
print("pass live_entry_now_available:", pass_checklist.get("live_entry_now_available"))

if pass_checklist.get("global_gate_failures"):
    failures.append("pass_status_should_not_create_global_gate_failure")

if pass_checklist.get("effective_failed_items"):
    failures.append("pass_status_should_not_create_effective_failed_item")

if pass_checklist.get("live_entry_now_available") is not True:
    failures.append("pass_status_should_allow_live_entry_when_other_gates_pass")

fail_checklist = build_checklist("fail")
failed_items = fail_checklist.get("failed_items") or []
effective_failed_items = fail_checklist.get("effective_failed_items") or []
global_gate_failures = fail_checklist.get("global_gate_failures") or []
effective_priority = fail_checklist.get("effective_decision_blockers_priority") or []

print("fail failed_items:", failed_items)
print("fail global_gate_failures:", global_gate_failures)
print("fail effective_failed_items:", effective_failed_items)
print("fail effective_decision_blockers_priority:", effective_priority)
print("fail live_entry_now_available:", fail_checklist.get("live_entry_now_available"))

if "wall_thesis_fit" in failed_items:
    failures.append("wall_thesis_fit_should_remain_global_gate_not_base_failed_item")

if "wall_thesis_fit" not in global_gate_failures:
    failures.append("wall_thesis_fit_fail_should_create_global_gate_failure")

if "wall_thesis_fit" not in effective_failed_items:
    failures.append("wall_thesis_fit_fail_should_create_effective_failed_item")

if not effective_priority or effective_priority[0] != "wall_thesis_fit":
    failures.append("wall_thesis_fit_should_be_first_effective_blocker")

if fail_checklist.get("live_entry_now_available") is not False:
    failures.append("wall_thesis_fit_fail_should_block_live_entry")

if failures:
    print("WALL THESIS FIT CONTRACT FAILURES:", ", ".join(failures))
    raise SystemExit(2)

print("WALL THESIS FIT CONTRACT PASS")
