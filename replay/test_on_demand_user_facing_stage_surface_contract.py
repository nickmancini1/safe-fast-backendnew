import ast
import re
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
    "_humanize_trigger_reason_key",
    "_humanize_reason_text",
    "_derive_trade_day_acceptability_condition",
    "_build_decisive_response_surface",
}:
    collect_function_dependencies(root_name)

ns = {
    "re": re,
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

_humanize_trigger_reason_key = ns["_humanize_trigger_reason_key"]
_humanize_reason_text = ns["_humanize_reason_text"]
_derive_trade_day_acceptability_condition = ns["_derive_trade_day_acceptability_condition"]
_build_decisive_response_surface = ns["_build_decisive_response_surface"]

failures = []

prior_spent_human = _humanize_trigger_reason_key("prior_completed_shelf_break_spent")
print("prior_spent_human:", prior_spent_human)
if "already happened" not in str(prior_spent_human) or "no fresh trigger" not in str(prior_spent_human):
    failures.append("prior_spent_trigger_reason_not_humanized")
if "_" in str(prior_spent_human):
    failures.append("prior_spent_trigger_reason_still_raw_key")

pending_completed_human = _humanize_reason_text("pending_completed_candle_approval")
print("pending_completed_human:", pending_completed_human)
if pending_completed_human != "pending completed-candle approval":
    failures.append("pending_completed_candle_reason_not_humanized")

market_closed_next = _derive_trade_day_acceptability_condition(
    {
        "setup_state": "PENDING",
        "why": "Market is closed. Context only.",
    },
    {
        "trigger_level": 100.55,
        "live_entry_waiting_on": "market_open",
    },
)
print("market_closed_next:", market_closed_next)
if "Next regular session opens" not in str(market_closed_next) or "100.55" not in str(market_closed_next):
    failures.append("market_closed_next_step_not_clear")

pending_shelf_next = _derive_trade_day_acceptability_condition(
    {
        "setup_state": "PENDING",
        "why": "Hold proven. Waiting for completed shelf break.",
    },
    {
        "trigger_level": 100.55,
        "why": "waiting_for_completed_shelf_break_close",
    },
)
print("pending_shelf_next:", pending_shelf_next)
if "completed 1H" not in str(pending_shelf_next) or "100.55" not in str(pending_shelf_next):
    failures.append("pending_shelf_next_step_not_clear")

surface = _build_decisive_response_surface(
    ticker="SPY",
    action="wait for live trigger",
    good_idea_now="NO",
    reason="Setup is forming but not ready.",
    next_step="1H close beyond EMA50.",
    invalidation="1H close beyond EMA50.",
    market_closed_context_only=False,
    caution_line="24H countertrend caution.",
    also_failing="room caution.",
    trap_line="hidden left structure.",
)
print("surface:", surface)
response_text = surface.get("response_text", "")
watchouts = surface.get("watchouts", "")
if "Watchouts:" not in response_text:
    failures.append("watchouts_missing_from_response_text")
for expected in ["24H countertrend caution", "room caution", "hidden left structure"]:
    if expected not in str(watchouts):
        failures.append(f"watchout_missing_{expected}")
if surface.get("next_step") is not None:
    failures.append("duplicate_next_step_not_suppressed_when_same_as_invalidation")
if "None" in response_text:
    failures.append("response_text_contains_none")

if failures:
    print("USER-FACING STAGE SURFACE CONTRACT FAILURES:", ", ".join(failures))
    raise SystemExit(2)

print("USER-FACING STAGE SURFACE CONTRACT PASS")
