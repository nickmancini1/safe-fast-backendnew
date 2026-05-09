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
    market_context={"is_open": False},
    time_day_gate={"fresh_entry_allowed": False},
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
    wall_thesis_fit_context={"wall_thesis_fit_status": "pass"},
)

global_failures = checklist.get("global_gate_failures") or []
effective_failed = checklist.get("effective_failed_items") or []
effective_priority = checklist.get("effective_decision_blockers_priority") or []
live_entry = checklist.get("live_entry_now_available")

print("global_gate_failures:", global_failures)
print("effective_failed_items:", effective_failed)
print("effective_decision_blockers_priority:", effective_priority)
print("live_entry_now_available:", live_entry)

failures = []

if global_failures[:2] != ["market_open", "fresh_entry_allowed"]:
    failures.append("market_closed_and_time_gate_should_keep_gate_failure_order")

if "market_open" not in effective_failed:
    failures.append("market_open_missing_from_effective_failed_items")

if "fresh_entry_allowed" not in effective_failed:
    failures.append("fresh_entry_allowed_missing_from_effective_failed_items")

if not effective_priority or effective_priority[0] != "market_open":
    failures.append("market_closed_should_be_first_effective_blocker_when_both_session_gates_fail")

if len(effective_priority) < 2 or effective_priority[1] != "fresh_entry_allowed":
    failures.append("fresh_entry_allowed_should_follow_market_open_when_both_session_gates_fail")

if live_entry is not False:
    failures.append("live_entry_should_be_false")

if failures:
    print("MARKET-CLOSED GATE PRIORITY CONTRACT FAILURES:", ", ".join(failures))
    raise SystemExit(2)

print("MARKET-CLOSED GATE PRIORITY CONTRACT PASS")
