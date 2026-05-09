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
    "_screened_sort_key",
    "_select_screened_best_candidate",
}:
    collect_function_dependencies(root_name)

ns = {
    "Any": Any,
    "Dict": Dict,
    "List": List,
    "Optional": Optional,
    "SYMBOL_ORDER": ["SPY", "QQQ", "IWM", "GLD"],
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

_screened_sort_key = ns["_screened_sort_key"]
_select_screened_best_candidate = ns["_select_screened_best_candidate"]


def candidate(
    symbol,
    final_verdict,
    setup_type,
    primary_blocker=None,
    trigger_present=False,
    risk_mid=10.0,
):
    failed_items = []
    decision_blockers = []
    if primary_blocker:
        failed_items = [primary_blocker]
        decision_blockers = [primary_blocker]

    return {
        "symbol": symbol,
        "engine_verdict": final_verdict,
        "final_verdict": final_verdict,
        "reason": primary_blocker or "ok",
        "primary_candidate": {
            "distance_from_target_risk_mid": risk_mid,
        },
        "structure_context": {
            "setup_type": setup_type,
            "allowed_setup": True,
            "room_quality": "pass",
            "room_pass": True,
            "wall_pass": True,
            "extension_state": "acceptable",
            "extension_blocks_now": False,
            "trend_label": "Trend-aligned",
            "room_ratio": 3.0,
            "continuation_context": {},
        },
        "trigger_state": {
            "trigger_present": trigger_present,
        },
        "checklist": {
            "failed_items": failed_items,
            "decision_blockers_priority": decision_blockers,
        },
    }


raw_no_trade_clean_fast_break = candidate(
    symbol="QQQ",
    final_verdict="NO_TRADE",
    setup_type="Clean Fast Break",
    primary_blocker="one_hour_clean_around_ema",
    trigger_present=True,
    risk_mid=1.0,
)

trade_ready_ideal = candidate(
    symbol="SPY",
    final_verdict="TRADE",
    setup_type="Ideal",
    trigger_present=True,
    risk_mid=20.0,
)

ranked = sorted(
    [raw_no_trade_clean_fast_break, trade_ready_ideal],
    key=_screened_sort_key,
)
selected = _select_screened_best_candidate(
    ranked,
    raw_engine_best_ticker="QQQ",
    freeze_to_raw_engine=False,
)

actual = selected.get("symbol") if selected else None
print(
    "raw_no_trade_override_vs_trade_ready_candidate: "
    f"selected={actual}, expected=SPY, ranked={[item.get('symbol') for item in ranked]}"
)

if actual != "SPY":
    print("RAW NO-TRADE WINNER OVERRIDE CONTRACT FAILURE: expected_SPY_got_" + str(actual))
    raise SystemExit(2)

print("RAW NO-TRADE WINNER OVERRIDE CONTRACT PASS")
