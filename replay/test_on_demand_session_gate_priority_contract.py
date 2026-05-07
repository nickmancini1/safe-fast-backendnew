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


def build_checklist(*, market_open=True, fresh_entry_allowed=True):
    return ns["_build_checklist_block"](
        request=Req(),
        market_context={"is_open": market_open},
        time_day_gate={"fresh_entry_allowed": fresh_entry_allowed},
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


def assert_global_gate(name, checklist, expected):
    failed = checklist.get("failed_items") or []
    effective_failed = checklist.get("effective_failed_items") or []
    global_failures = checklist.get("global_gate_failures") or []
    effective_priority = checklist.get("effective_decision_blockers_priority") or []
    live_entry = checklist.get("live_entry_now_available")

    print(f"{name} failed_items:", failed)
    print(f"{name} global_gate_failures:", global_failures)
    print(f"{name} effective_failed_items:", effective_failed)
    print(f"{name} effective_decision_blockers_priority:", effective_priority)
    print(f"{name} live_entry_now_available:", live_entry)

    failures = []

    if expected in failed:
        failures.append(f"{name}:{expected}_should_not_be_base_failed_item")

    if expected not in global_failures:
        failures.append(f"{name}:{expected}_missing_from_global_gate_failures")

    if expected not in effective_failed:
        failures.append(f"{name}:{expected}_missing_from_effective_failed_items")

    if not effective_priority or effective_priority[0] != expected:
        failures.append(f"{name}:{expected}_not_first_effective_blocker")

    if live_entry is not False:
        failures.append(f"{name}:live_entry_should_be_false")

    return failures


failures = []

clean = build_checklist()
print("clean failed_items:", clean.get("failed_items"))
print("clean global_gate_failures:", clean.get("global_gate_failures"))
print("clean effective_failed_items:", clean.get("effective_failed_items"))
print("clean live_entry_now_available:", clean.get("live_entry_now_available"))

if clean.get("global_gate_failures"):
    failures.append("clean_case_should_have_no_global_gate_failures")

if clean.get("effective_failed_items"):
    failures.append("clean_case_should_have_no_effective_failed_items")

if clean.get("live_entry_now_available") is not True:
    failures.append("clean_case_should_allow_live_entry")

failures.extend(
    assert_global_gate(
        "market_closed",
        build_checklist(market_open=False, fresh_entry_allowed=True),
        "market_open",
    )
)

failures.extend(
    assert_global_gate(
        "time_gate_blocked",
        build_checklist(market_open=True, fresh_entry_allowed=False),
        "fresh_entry_allowed",
    )
)

if failures:
    print("SESSION GATE PRIORITY CONTRACT FAILURES:", ", ".join(failures))
    raise SystemExit(2)

print("SESSION GATE PRIORITY CONTRACT PASS")
