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

checklist = ns["_build_checklist_block"](
    request=Req(),
    market_context={"is_open": True},
    time_day_gate={"fresh_entry_allowed": True},
    structure_context={
        "setup_type": "Ideal",
        "setup_type_allowed": True,
        "twentyfour_hour_supportive": True,
        "chop_risk": False,
        "noisy_chop_explicit": False,

        # Room is workable/caution, not a hard fail.
        "room_quality": "caution",
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
    wall_thesis_fit_context={"wall_thesis_fit_status": "pass"},
)

failed = checklist.get("failed_items", [])
cautions = checklist.get("caution_items", [])

print("failed_items:", failed)
print("caution_items:", cautions)

if "clear_room" in failed:
    print("ROOM CAUTION CONTRACT FAIL: workable room caution is still a hard blocker")
    raise SystemExit(2)

if "room_caution" not in cautions:
    print("ROOM CAUTION CONTRACT FAIL: room caution is not surfaced")
    raise SystemExit(2)

print("ROOM CAUTION CONTRACT PASS")
