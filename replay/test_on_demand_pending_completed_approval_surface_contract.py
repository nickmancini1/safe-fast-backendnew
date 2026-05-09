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


collect_function_dependencies("_derive_trade_day_acceptability_condition")

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

next_step = _derive_trade_day_acceptability_condition(
    {
        "setup_state": "PENDING",
        "why": "Intrabar shelf break is visible. SAFE-FAST is pending the completed 1H close for approval.",
    },
    {
        "trigger_level": 100.55,
        "why": "pending_completed_candle_approval",
    },
)

print("pending_completed_approval_next_step:", next_step)

failures = []
next_step_text = str(next_step or "")
next_step_lower = next_step_text.lower()

if "completed 1h close" not in next_step_lower:
    failures.append("pending_completed_approval_next_step_should_mention_completed_1h_close")
if "approval" not in next_step_lower:
    failures.append("pending_completed_approval_next_step_should_mention_approval")
if "100.55" not in next_step_text:
    failures.append("pending_completed_approval_next_step_should_include_trigger_level")
if next_step_text == "Get a live SAFE-FAST trigger with structure still clean.":
    failures.append("pending_completed_approval_next_step_should_not_be_generic_live_trigger")

if failures:
    print("PENDING COMPLETED APPROVAL SURFACE CONTRACT FAILURES:", ", ".join(failures))
    raise SystemExit(2)

print("PENDING COMPLETED APPROVAL SURFACE CONTRACT PASS")
