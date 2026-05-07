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


def build_checklist(room_quality, room_hard_fail, room_pass, first_wall):
    return ns["_build_checklist_block"](
        request=Req(),
        market_context={"is_open": True},
        time_day_gate={"fresh_entry_allowed": True},
        structure_context={
            "setup_type": "Ideal",
            "setup_type_allowed": True,
            "twentyfour_hour_supportive": True,
            "chop_risk": False,
            "noisy_chop_explicit": False,
            "room_quality": room_quality,
            "room_hard_fail": room_hard_fail,
            "room_pass": room_pass,
            "first_wall": first_wall,
            "extension_blocks_now": False,
            "extension_soft_flag": False,
            "extension_material": False,
            "ath_open_air_blocks_now": False,
        },
        chart_check={"ema50_1h": 100.0, "price_vs_ema50_1h": "above"},
        primary_candidate={"fits_risk_budget": True},
        liquidity_context={"liquidity_pass": True},
        trigger_state={"trigger_present": True},
        wall_thesis_fit_context={"wall_thesis_fit_status": "pass"},
    )


failures = []

# Workable/tight room must be caution only, not a hard blocker.
caution_checklist = build_checklist(
    room_quality="caution",
    room_hard_fail=False,
    room_pass=True,
    first_wall=105.0,
)

caution_failed = caution_checklist.get("failed_items", [])
caution_items = caution_checklist.get("caution_items", [])

print("caution failed_items:", caution_failed)
print("caution caution_items:", caution_items)

if "clear_room" in caution_failed:
    failures.append("workable_room_should_not_hard_fail")

if "room_caution" not in caution_items:
    failures.append("workable_room_caution_not_surfaced")

# Cramped room / first wall too close must hard-fail as clear_room.
cramped_checklist = build_checklist(
    room_quality="fail",
    room_hard_fail=True,
    room_pass=False,
    first_wall=100.25,
)

cramped_failed = cramped_checklist.get("failed_items", [])
cramped_cautions = cramped_checklist.get("caution_items", [])
cramped_priority = cramped_checklist.get("decision_blockers_priority") or []
cramped_effective_priority = cramped_checklist.get("effective_decision_blockers_priority") or []

print("cramped failed_items:", cramped_failed)
print("cramped caution_items:", cramped_cautions)
print("cramped decision_blockers_priority:", cramped_priority)
print("cramped effective_decision_blockers_priority:", cramped_effective_priority)

if "clear_room" not in cramped_failed:
    failures.append("cramped_room_should_hard_fail_clear_room")

if "room_caution" in cramped_cautions:
    failures.append("cramped_room_should_not_be_only_caution")

if not cramped_priority or cramped_priority[0] != "clear_room":
    failures.append("cramped_room_clear_room_not_first_decision_blocker")

if not cramped_effective_priority or cramped_effective_priority[0] != "clear_room":
    failures.append("cramped_room_clear_room_not_first_effective_blocker")

if failures:
    print("ROOM CAUTION / CRAMPED ROOM CONTRACT FAILURES:", ", ".join(failures))
    raise SystemExit(2)

print("ROOM CAUTION / CRAMPED ROOM CONTRACT PASS")
