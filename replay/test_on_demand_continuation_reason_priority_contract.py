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
    "_is_allowed_setup_type_name",
    "_continuation_family_detected",
}

ns = {
    "Any": Any,
    "Dict": Dict,
    "List": List,
    "Optional": Optional,
    "OnDemandRequest": object,
    "ALLOWED_SETUP_TYPES": {"Ideal", "Clean Fast Break", "Continuation"},
}

for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in needed:
        mod = ast.Module(body=[node], type_ignores=[])
        ast.fix_missing_locations(mod)
        exec(compile(mod, filename="main.py", mode="exec"), ns)


class Req:
    open_positions = 0


def build_case(
    *,
    main_blocker: str,
    exact_reason: str,
    shelf_proven: bool,
    reclaim_hold_proven: bool,
    extension_blocks_now: bool = False,
):
    continuation_context = {
        "shelf_exists": True,
        "shelf_proven": shelf_proven,
        "reclaim_hold_proven": reclaim_hold_proven,
        "tradeable_now": False,
        "exact_reason": exact_reason,
        "main_blocker": main_blocker,
        "trigger_level": 103.5,
        "shelf_candle_count": 2,
        "status_message": f"Continuation developing: {main_blocker}.",
    }

    structure_context = {
        "setup_type": "Continuation",
        "setup_type_allowed": True,
        "allowed_setup": True,
        "twentyfour_hour_supportive": True,
        "chop_risk": False,
        "noisy_chop_explicit": False,
        "room_hard_fail": False,
        "room_pass": True,
        "room_quality": "pass",
        "first_wall": 105.0,
        "price_vs_ema50_1h": "inside",
        "extension_blocks_now": extension_blocks_now,
        "extension_soft_flag": False,
        "extension_material": extension_blocks_now,
        "ath_open_air_blocks_now": False,
        "continuation_context": continuation_context,
    }

    chart_check = {"ema50_1h": 100.0, "price_vs_ema50_1h": "inside"}

    trigger_state = {
        "trigger_present": False,
        "structure_ready": False,
        "why": "no_valid_continuation_trigger",
    }

    checklist = ns["_build_checklist_block"](
        request=Req(),
        market_context={"is_open": True},
        time_day_gate={"fresh_entry_allowed": True},
        structure_context=structure_context,
        chart_check=chart_check,
        primary_candidate={"fits_risk_budget": True},
        liquidity_context={"liquidity_pass": True},
        trigger_state=trigger_state,
        wall_thesis_fit_context={"wall_thesis_fit_status": "pass"},
    )

    approval_requirements = ns["_build_approval_requirements_context_block"](
        checklist_block=checklist,
        structure_context=structure_context,
        trigger_state=trigger_state,
        market_context={"is_open": True},
        time_day_gate={"fresh_entry_allowed": True},
        macro_context={
            "has_major_event_today": False,
            "has_major_event_tomorrow": False,
        },
        liquidity_context={"liquidity_pass": True},
        approval_context={
            "approval_ready_now": False,
            "approval_ready_on_completed_candle": False,
            "approval_status": "NO_SIGNAL_YET",
            "intrabar_raw_signal_detected": False,
            "completed_raw_signal_detected": False,
        },
    )

    return checklist, approval_requirements


tests = [
    (
        "no_proven_hold_beats_generic_blockers",
        {
            "main_blocker": "no_proven_hold",
            "exact_reason": "early",
            "shelf_proven": False,
            "reclaim_hold_proven": False,
        },
        "no_proven_hold",
    ),
    (
        "no_valid_trigger_beats_clear_trigger",
        {
            "main_blocker": "no_valid_trigger",
            "exact_reason": "early",
            "shelf_proven": True,
            "reclaim_hold_proven": True,
        },
        "no_valid_trigger",
    ),
    (
        "move_too_extended_beats_early_enough",
        {
            "main_blocker": "move_too_extended",
            "exact_reason": "late",
            "shelf_proven": True,
            "reclaim_hold_proven": True,
            "extension_blocks_now": True,
        },
        "move_too_extended",
    ),
]

failures = []

generic_blockers = {
    "allowed_setup_type",
    "twentyfour_hour_supportive",
    "one_hour_clean_around_ema",
    "clear_room",
    "early_enough",
    "clear_trigger",
    "structure_ready",
    "trigger_present",
}

for name, kwargs, expected in tests:
    checklist, approval_requirements = build_case(**kwargs)

    decision_priority = checklist.get("decision_blockers_priority") or []
    effective_priority = checklist.get("effective_decision_blockers_priority") or []
    override = checklist.get("continuation_blocker_override")
    approval_next_flip = approval_requirements.get("next_flip_needed")

    actual_first = decision_priority[0] if decision_priority else None
    actual_effective_first = effective_priority[0] if effective_priority else None

    print(
        f"{name}: override={override}, first={actual_first}, "
        f"effective_first={actual_effective_first}, "
        f"approval_next_flip={approval_next_flip}"
    )
    print("  failed_items:", checklist.get("failed_items"))
    print("  decision_blockers_priority:", decision_priority)

    ok = all(
        value == expected
        for value in [
            override,
            actual_first,
            actual_effective_first,
            approval_next_flip,
        ]
    )

    if not ok:
        failures.append(name)
        continue

    if actual_first in generic_blockers and actual_first != expected:
        failures.append(name)

if failures:
    print("CONTINUATION REASON PRIORITY CONTRACT FAILURES:", ", ".join(failures))
    raise SystemExit(2)

print("CONTINUATION REASON PRIORITY CONTRACT PASS")
