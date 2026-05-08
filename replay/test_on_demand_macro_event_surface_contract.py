import ast
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

source = Path("main.py").read_text(encoding="utf-8")
tree = ast.parse(source)

needed = {
    "_build_macro_brief",
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

macro_brief = ns["_build_macro_brief"]
build_surface = ns["_build_decisive_response_surface"]

failures = []

cases = [
    ("major_event_today", {"ok": True, "has_major_event_today": True}, "major event today"),
    ("major_event_tomorrow", {"ok": True, "has_major_event_tomorrow": True}, "major event tomorrow"),
    ("normal_risk", {"ok": True, "risk_level": "normal"}, "clear today"),
    ("high_risk", {"ok": True, "risk_level": "high"}, "event risk high"),
    ("unconfirmed", {"ok": False}, "unconfirmed"),
]

for name, ctx, expected in cases:
    actual = macro_brief(ctx)
    ok = actual == expected
    print(f"{name}: {'PASS' if ok else 'FAIL'} | got={actual}")
    if not ok:
        failures.append(f"{name}:expected_{expected}_got_{actual}")

surface = build_surface(
    ticker="SPY",
    action="watch only",
    good_idea_now="NO",
    reason="Setup is forming, but macro event risk is active.",
    next_step="Wait for event risk to clear or for a clean confirmed trigger.",
    invalidation="1H close beyond invalidation level.",
    market_closed_context_only=False,
    caution_line="Major event today caution.",
    also_failing=None,
    trap_line=None,
)

response_text = surface.get("response_text", "")
watchouts = surface.get("watchouts", "")

print("response_text:", response_text)
print("watchouts:", watchouts)

if "Major event today caution" not in response_text:
    failures.append("macro_caution_missing_from_response_text")

if "Major event today caution" not in str(watchouts):
    failures.append("macro_caution_missing_from_watchouts")

if failures:
    print("MACRO EVENT SURFACE CONTRACT FAILURES:", ", ".join(failures))
    raise SystemExit(2)

print("MACRO EVENT SURFACE CONTRACT PASS")
