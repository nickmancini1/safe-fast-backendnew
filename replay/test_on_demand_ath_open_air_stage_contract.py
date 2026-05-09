import ast
from pathlib import Path
from typing import Any, Dict, List, Optional

source = Path("main.py").read_text(encoding="utf-8")
tree = ast.parse(source)

needed = {
    "_to_float",
    "_build_checklist_block",
    "_build_approval_requirements_context_block",
    "_derive_global_gate_primary_blocker",
    "_failed_reason_messages",
    "_continuation_hold_progress_message",
    "_continuation_one_more_hold_needed",
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


structure_context = {
    "setup_type": "Ideal",
    "setup_type_allowed": True,
    "allowed_setup": True,
    "twentyfour_hour_supportive": True,
    "chop_risk": False,
    "noisy_chop_explicit": False,
    "valid_post_impulse_shelf_not_chop": False,
    "room_quality": "fail",
    "room_hard_fail": True,
    "room_pass": False,
    "first_wall": None,
    "price_vs_ema50_1h": "above",
    "wall_pass": True,
    "extension_blocks_now": True,
    "extension_state": "extended",
    "extension_soft_flag": False,
    "extension_material": True,
    "ath_open_air_blocks_now": True,
    "continuation_context": {},
}

market_context = {"is_open": True}
time_day_gate = {"fresh_entry_allowed": True}
liquidity_context = {"liquidity_pass": True}
trigger_state = {"trigger_present": True, "structure_ready": False, "why": "structure_not_ready"}
wall_thesis_fit_context = {"wall_thesis_fit_status": "pass"}

checklist = ns["_build_checklist_block"](
    request=Req(),
    market_context=market_context,
    time_day_gate=time_day_gate,
    structure_context=structure_context,
    chart_check={"ema50_1h": 100.0, "price_vs_ema50_1h": "above"},
    primary_candidate={"fits_risk_budget": True},
    liquidity_context=liquidity_context,
    trigger_state=trigger_state,
    wall_thesis_fit_context=wall_thesis_fit_context,
)

approval_requirements = ns["_build_approval_requirements_context_block"](
    checklist_block=checklist,
    structure_context=structure_context,
    trigger_state=trigger_state,
    market_context=market_context,
    time_day_gate=time_day_gate,
    macro_context={
        "has_major_event_today": False,
        "has_major_event_tomorrow": False,
    },
    liquidity_context=liquidity_context,
    approval_context={
        "approval_ready_now": False,
        "approval_ready_on_completed_candle": False,
        "approval_status": "NO_SIGNAL_YET",
        "intrabar_raw_signal_detected": False,
        "completed_raw_signal_detected": False,
    },
)

failed_messages = ns["_failed_reason_messages"](
    checklist=checklist,
    time_day_gate=time_day_gate,
    market_context=market_context,
    structure_context=structure_context,
    liquidity_context=liquidity_context,
    trigger_state=trigger_state,
    wall_thesis_fit_context=wall_thesis_fit_context,
)

decision_priority = checklist.get("decision_blockers_priority") or []
effective_priority = checklist.get("effective_decision_blockers_priority") or []
next_flip_needed = approval_requirements.get("next_flip_needed")

print("failed_items:", checklist.get("failed_items"))
print("decision_blockers_priority:", decision_priority)
print("effective_decision_blockers_priority:", effective_priority)
print("approval next_flip_needed:", next_flip_needed)
print("failed reason messages:", failed_messages)

failures = []

if not decision_priority or decision_priority[0] != "ath_open_air":
    failures.append("ath_open_air_not_first_decision_blocker")

if not effective_priority or effective_priority[0] != "ath_open_air":
    failures.append("ath_open_air_not_first_effective_blocker")

if next_flip_needed != "ath_open_air":
    failures.append("ath_open_air_not_next_flip_needed")

if not failed_messages or "rebuilt 1H structure near all-time highs" not in failed_messages[0]:
    failures.append("ath_open_air_stage_message_not_first")

if failed_messages and failed_messages[0] in {
    "room to the first wall fails",
    "entry is too late or overextended for SAFE-FAST",
}:
    failures.append("generic_room_or_extension_message_beat_ath_open_air")

if failures:
    print("ATH OPEN-AIR STAGE CONTRACT FAILURES:", ", ".join(failures))
    raise SystemExit(2)

print("ATH OPEN-AIR STAGE CONTRACT PASS")
