import ast
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

source = Path("main.py").read_text(encoding="utf-8")
tree = ast.parse(source)

needed = {
    "_surface_text",
    "_strip_after_hours_prefix",
    "_surface_item_list",
    "_build_decisive_response_surface",
}

ns = {
    "re": re,
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

build_surface = ns["_build_decisive_response_surface"]

surface = build_surface(
    ticker="QQQ",
    action="watch only",
    good_idea_now="NO",
    reason="Setup is forming, but IV/event-day risk requires caution.",
    next_step="Wait for cleaner pricing or a stronger confirmed trigger.",
    invalidation="1H close beyond invalidation level.",
    market_closed_context_only=False,
    caution_line="High IV / event-day caution.",
    also_failing=None,
    trap_line=None,
)

response_text = surface.get("response_text", "")
watchouts = surface.get("watchouts", "")

print("response_text:", response_text)
print("watchouts:", watchouts)

failures = []

if "High IV / event-day caution" not in response_text:
    failures.append("iv_event_caution_missing_from_response_text")

if "High IV / event-day caution" not in str(watchouts):
    failures.append("iv_event_caution_missing_from_watchouts")

if failures:
    print("IV EVENT SURFACE CONTRACT FAILURES:", ", ".join(failures))
    raise SystemExit(2)

print("IV EVENT SURFACE CONTRACT PASS")
