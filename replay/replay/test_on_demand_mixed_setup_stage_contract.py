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
    setup_allowed=True,
    primary_blocker=None,
    continuation_context=None,
    trigger_present=False,
    room_pass=True,
    extension_blocks_now=False,
    room_quality="pass",
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
            "allowed_setup": setup_allowed,
            "room_quality": room_quality,
            "room_pass": room_pass,
            "wall_pass": True,
            "extension_state": "extended" if extension_blocks_now else "acceptable",
            "extension_blocks_now": extension_blocks_now,
            "trend_label": "Trend-aligned",
            "room_ratio": 3.0,
            "continuation_context": continuation_context or {},
        },
        "trigger_state": {
            "trigger_present": trigger_present,
        },
        "checklist": {
            "failed_items": failed_items,
            "decision_blockers_priority": decision_blockers,
        },
    }


spent_continuation = candidate(
    symbol="QQQ",
    final_verdict="NO_TRADE",
    setup_type="Continuation",
    primary_blocker="no_valid_trigger",
    continuation_context={
        "exact_reason": "spent",
        "main_blocker": "no_valid_trigger",
        "prior_completed_shelf_break_seen": True,
        "tradeable_now": False,
        "status_message": "A prior completed 1H shelf break already happened. No fresh trigger now.",
    },
    risk_mid=1.0,
)

fresh_ideal_pending = candidate(
    symbol="SPY",
    final_verdict="PENDING",
    setup_type="Ideal",
    primary_blocker="clear_trigger",
    trigger_present=False,
    risk_mid=20.0,
)

fresh_clean_fast_break_trade = candidate(
    symbol="IWM",
    final_verdict="TRADE",
    setup_type="Clean Fast Break",
    trigger_present=True,
    risk_mid=30.0,
)

fresh_continuation_pending = candidate(
    symbol="GLD",
    final_verdict="PENDING",
    setup_type="Continuation",
    primary_blocker="no_valid_trigger",
    continuation_context={
        "exact_reason": "early",
        "main_blocker": "no_valid_trigger",
        "reclaim_hold_proven": True,
        "tradeable_now": False,
        "status_message": "Hold proven. Waiting for first completed shelf break.",
    },
    risk_mid=40.0,
)

failures = []


def assert_selected(name, pool, expected_symbol, raw_engine_best_ticker=None):
    ranked = sorted(pool, key=_screened_sort_key)
    selected = _select_screened_best_candidate(
        ranked,
        raw_engine_best_ticker=raw_engine_best_ticker,
        freeze_to_raw_engine=False,
    )
    actual = selected.get("symbol") if selected else None
    print(f"{name}: selected={actual}, expected={expected_symbol}, ranked={[item.get('symbol') for item in ranked]}")
    if actual != expected_symbol:
        failures.append(f"{name}:expected_{expected_symbol}_got_{actual}")


assert_selected(
    "spent_continuation_does_not_beat_pending_ideal",
    [spent_continuation, fresh_ideal_pending],
    "SPY",
    raw_engine_best_ticker="QQQ",
)

assert_selected(
    "spent_continuation_does_not_beat_trade_ready_clean_fast_break",
    [spent_continuation, fresh_clean_fast_break_trade],
    "IWM",
    raw_engine_best_ticker="QQQ",
)

assert_selected(
    "trade_ready_clean_fast_break_beats_pending_fresh_continuation",
    [fresh_continuation_pending, fresh_clean_fast_break_trade],
    "IWM",
    raw_engine_best_ticker="GLD",
)

assert_selected(
    "pending_ideal_beats_spent_continuation_even_when_spent_has_better_risk_rank",
    [fresh_ideal_pending, spent_continuation],
    "SPY",
    raw_engine_best_ticker="QQQ",
)

if failures:
    print("MIXED SETUP STAGE CONTRACT FAILURES:", ", ".join(failures))
    raise SystemExit(2)

print("MIXED SETUP STAGE CONTRACT PASS")
