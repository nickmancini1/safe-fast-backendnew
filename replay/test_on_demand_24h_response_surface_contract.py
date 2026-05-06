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

surface = ns["_build_decisive_response_surface"](
    ticker="QQQ",
    action="wait for trigger",
    good_idea_now="NO",
    reason="Setup forming but not ready.",
    next_step="Wait for valid trigger.",
    invalidation="1H close beyond EMA50.",
    market_closed_context_only=False,
    caution_line="24H countertrend caution.",
    also_failing=None,
    trap_line=None,
)

response_text = surface.get("response_text", "")
watchouts = surface.get("watchouts", "")

print("response_text:", response_text)
print("watchouts:", watchouts)

if "24H countertrend caution" not in response_text:
    print("24H RESPONSE SURFACE FAIL: caution missing from response_text")
    raise SystemExit(2)

if "24H countertrend caution" not in str(watchouts):
    print("24H RESPONSE SURFACE FAIL: caution missing from watchouts")
    raise SystemExit(2)

print("24H RESPONSE SURFACE CONTRACT PASS")
