import ast
from pathlib import Path
from typing import Any, Dict, List, Optional

source = Path("main.py").read_text(encoding="utf-8")
tree = ast.parse(source)

needed = {"_to_float", "_round_or_none", "_continuation_one_more_hold_needed", "_continuation_hold_progress_message"}
ns = {
    "Any": Any,
    "Dict": Dict,
    "List": List,
    "Optional": Optional,
}

for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in needed:
        mod = ast.Module(body=[node], type_ignores=[])
        ast.fix_missing_locations(mod)
        exec(compile(mod, filename="main.py", mode="exec"), ns)

msg = ns["_continuation_hold_progress_message"]

tests = [
    (
        "early_waiting_for_first_break",
        {
            "exact_reason": "early",
            "main_blocker": "no_valid_trigger",
            "reclaim_hold_proven": True,
            "trigger_level": 103.5,
            "hold_closes_above_reclaim_count": 2,
        },
        "waiting for the first completed",
        True,
    ),
    (
        "spent_prior_break_should_not_say_waiting_first_break",
        {
            "exact_reason": "spent",
            "main_blocker": "no_valid_trigger",
            "reclaim_hold_proven": True,
            "prior_completed_shelf_break_seen": True,
            "trigger_level": 103.5,
            "hold_closes_above_reclaim_count": 2,
            "status_message": "The first completed 1H shelf break already happened. SAFE-FAST is not waiting for a first break anymore.",
        },
        "waiting for the first completed",
        False,
    ),
    (
        "late_should_not_say_waiting_first_break",
        {
            "exact_reason": "late",
            "main_blocker": "move_too_extended",
            "reclaim_hold_proven": True,
            "trigger_level": 103.5,
            "hold_closes_above_reclaim_count": 2,
            "status_message": "Too late: the break already expanded too far from the hold.",
        },
        "waiting for the first completed",
        False,
    ),
]

failures = []

for name, ctx, text, should_contain in tests:
    result = msg(ctx)
    contains = text.lower() in str(result or "").lower()
    ok = contains == should_contain
    print(f"{name}: {'PASS' if ok else 'FAIL'} | message={result}")
    if not ok:
        failures.append(name)

if failures:
    print("STAGE MESSAGE CONTRACT FAILURES:", ", ".join(failures))
    raise SystemExit(2)

print("STAGE MESSAGE CONTRACT PASS")
