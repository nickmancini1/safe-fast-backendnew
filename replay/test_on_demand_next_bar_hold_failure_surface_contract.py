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


for root_name in {
    "_derive_trade_day_acceptability_condition",
    "_humanize_trigger_reason_key",
    "_humanize_reason_text",
}:
    collect_function_dependencies(root_name)

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

_derive_trade_day_acceptability_condition = ns["_derive_trade_day_acceptability_condition"]
_humanize_trigger_reason_key = ns["_humanize_trigger_reason_key"]
_humanize_reason_text = ns["_humanize_reason_text"]


def assert_next_bar_hold_surface(raw_reason, setup_state):
    next_step = _derive_trade_day_acceptability_condition(
        {
            "setup_state": setup_state,
            "why": raw_reason,
        },
        {
            "trigger_level": 100.55,
            "why": raw_reason,
        },
    )
    human_trigger = _humanize_trigger_reason_key(raw_reason)
    human_reason = _humanize_reason_text(raw_reason)

    print(f"{raw_reason} next_step:", next_step)
    print(f"{raw_reason} human_trigger:", human_trigger)
    print(f"{raw_reason} human_reason:", human_reason)

    failures = []
    next_step_text = str(next_step or "")
    next_step_lower = next_step_text.lower()
    human_text = f"{human_trigger or ''} {human_reason or ''}"

    says_failed_or_rebuild = (
        "breakout hold failed" in next_step_lower
        or "rebuild" in next_step_lower
        or (
            "breakout hold" in next_step_lower
            and ("next 1h bar" in next_step_lower or "confirm" in next_step_lower)
        )
    )
    if not says_failed_or_rebuild:
        failures.append(f"{raw_reason}_next_step_should_explain_failed_or_rebuild_hold")

    if next_step_text == "Get a live SAFE-FAST trigger with structure still clean.":
        failures.append(f"{raw_reason}_next_step_should_not_be_generic_live_trigger")
    if "structure not ready" in next_step_lower:
        failures.append(f"{raw_reason}_next_step_should_not_be_generic_structure_not_ready")
    if raw_reason in next_step_text or raw_reason in human_text:
        failures.append(f"{raw_reason}_surface_should_not_expose_raw_underscore_reason")

    return failures


failures = []
for setup_state in ["PENDING", "NO TRADE"]:
    for raw_reason in ["next_bar_hold_failed", "next_bar_hold_not_confirmed"]:
        failures.extend(assert_next_bar_hold_surface(raw_reason, setup_state))

if failures:
    print("NEXT-BAR HOLD FAILURE SURFACE CONTRACT FAILURES:", ", ".join(failures))
    raise SystemExit(2)

print("NEXT-BAR HOLD FAILURE SURFACE CONTRACT PASS")
