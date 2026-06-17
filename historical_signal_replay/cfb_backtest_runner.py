import csv
import json
from datetime import time
from decimal import Decimal, InvalidOperation
from pathlib import Path
from zoneinfo import ZoneInfo

from historical_signal_replay import cfb_trade_rule_checker as checker


REPO_ROOT = Path(__file__).resolve().parents[1]
EXACT_FIXTURE_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "fixtures"
    / "cfb_exit_stop_cost_regression_fixtures.json"
)
LOCAL_OPTION_DATA_DIR = (
    REPO_ROOT / "historical_signal_replay" / "source_data" / "external_option_data_drop"
)
SPY_CFB_002_SELECTED_CONTRACT_INSTRUMENT_ID = "1258293281"
SPY_CFB_002_EXIT_PATH_TCBBO_PATH = (
    LOCAL_OPTION_DATA_DIR / "SPY_CFB_002_selected_contract_tcbbo_entry_to_1545_et.csv"
)

FIRST_REFERENCE_CANDIDATE_ID = "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002"
SPY_CFB_003_CANDIDATE_ID = "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003"
QQQ_CFB_001_CANDIDATE_ID = "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"
TIME_EXIT_ET = time(15, 45)
EASTERN = ZoneInfo("America/New_York")


def load_prepared_candidate_row(candidate_id, fixture_path=EXACT_FIXTURE_PATH):
    fixture_data = json.loads(Path(fixture_path).read_text(encoding="utf-8"))
    for row in fixture_data["fixtures"]:
        if row.get("candidate_id") == candidate_id and row.get("setup_type") == "Clean Fast Break":
            return dict(row)
    raise ValueError(f"prepared CFB candidate row not found: {candidate_id}")


def run_first_cfb_backtest_path():
    rows = [
        load_prepared_candidate_row(FIRST_REFERENCE_CANDIDATE_ID),
        load_prepared_candidate_row(SPY_CFB_003_CANDIDATE_ID),
        load_prepared_candidate_row(QQQ_CFB_001_CANDIDATE_ID),
    ]
    results = []
    for row in rows:
        option_quote_rows = None
        if row["candidate_id"] == FIRST_REFERENCE_CANDIDATE_ID:
            option_quote_rows = load_local_option_quotes_for_spy_cfb_002()
        results.append(run_cfb_backtest_row(row, option_quote_rows=option_quote_rows))
    return {
        "review_status": "local_review_output",
        "promotion_decision": "not_requested_not_made",
        "candidate_marked_ready": False,
        "proof_accepted": False,
        "profitability_claimed": False,
        "results": results,
    }


def run_cfb_backtest_row(row, *, option_quote_rows=None, underlying_rows=None):
    gate_result = checker.check_cfb_trade_rules_from_fixture(row)
    if gate_result["trade_rule_status"] == "no_trade":
        return _result(
            row,
            result_status="no_trade",
            result_name=f"no_trade_{gate_result['rejection_reason']}",
            failure_reason=gate_result["rejection_reason"],
            gate_result=gate_result,
        )
    if gate_result["trade_rule_status"] != "entry_rule_ready_awaiting_backtest_harness":
        return _result(
            row,
            result_status="blocked",
            result_name=f"blocked_{gate_result['rejection_reason']}",
            failure_reason=gate_result["rejection_reason"],
            gate_result=gate_result,
            missing_fields=gate_result.get("blocking_reasons", []),
        )

    entry_basis = _decimal(row["ask"]) + checker.ENTRY_SLIPPAGE_BUFFER
    target_basis = entry_basis * (Decimal("1") + checker.PROFIT_TARGET_PERCENT)
    stop_basis = entry_basis * (Decimal("1") + checker.OPTION_STOP_PERCENT)
    signal_at = checker.normalize_timestamp(row["signal_time"])
    time_exit_at = _time_exit_datetime(signal_at)

    option_events = _selected_option_events(
        option_quote_rows or [],
        selected_contract=row.get("selected_contract"),
        signal_at=signal_at,
        time_exit_at=time_exit_at,
    )
    underlying_events = _underlying_events(
        underlying_rows or [],
        signal_at=signal_at,
        time_exit_at=time_exit_at,
    )

    first_exit = _first_exit_event(
        option_events=option_events,
        underlying_events=underlying_events,
        underlying_invalidation=_decimal(row["underlying_invalidation"]),
        target_basis=target_basis,
        stop_basis=stop_basis,
        time_exit_at=time_exit_at,
    )
    if first_exit is not None:
        return _result(
            row,
            result_status="completed_review_only",
            result_name=f"completed_{first_exit['exit_reason']}",
            failure_reason=None,
            gate_result=gate_result,
            entry_basis=entry_basis,
            target_basis=target_basis,
            stop_basis=stop_basis,
            exit_event=first_exit,
        )

    missing_fields = _missing_exit_path_fields(
        option_events=option_events,
        underlying_events=underlying_events,
        time_exit_at=time_exit_at,
    )
    return _result(
        row,
        result_status="blocked_missing_exit_path_data",
        result_name="blocked_missing_exit_path_data",
        failure_reason=missing_fields[0],
        gate_result=gate_result,
        entry_basis=entry_basis,
        target_basis=target_basis,
        stop_basis=stop_basis,
        missing_fields=missing_fields,
        starter_data_enough=False,
        full_window_data_required=True,
        cost_check_request=(
            "Before any full-window download, run a Databento OPRA.PILLAR cost check "
            "for the selected contract only: TCBBO quotes for SPY   260427C00685000 "
            "/ instrument_id 1258293281 from 2026-04-13T16:30:00Z through "
            "2026-04-13T19:45:00Z, plus source-backed underlying invalidation path "
            "coverage through 15:45 ET."
        ),
    )


def load_local_option_quotes_for_spy_cfb_002():
    path = SPY_CFB_002_EXIT_PATH_TCBBO_PATH
    if not path.exists():
        path = (
            LOCAL_OPTION_DATA_DIR
            / "SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_002_tcbbo_signal_10min.csv"
        )
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _selected_option_events(rows, *, selected_contract, signal_at, time_exit_at):
    events = []
    for row in rows:
        row_symbol = row.get("symbol")
        row_instrument_id = row.get("instrument_id")
        if row_symbol is not None and row_symbol != selected_contract:
            continue
        if row_symbol is None and row_instrument_id not in (
            None,
            SPY_CFB_002_SELECTED_CONTRACT_INSTRUMENT_ID,
        ):
            continue
        event_time = checker.normalize_timestamp(row["ts_event"])
        if event_time < signal_at or event_time > time_exit_at:
            continue
        bid = _decimal(row.get("bid_px_00"))
        events.append(
            {
                "time": event_time,
                "bid": bid,
                "cost_adjusted_exit_basis": bid - checker.EXIT_SLIPPAGE_BUFFER,
            }
        )
    return sorted(events, key=lambda event: event["time"])


def _underlying_events(rows, *, signal_at, time_exit_at):
    events = []
    for row in rows:
        event_time = checker.normalize_timestamp(row["timestamp"])
        if event_time < signal_at or event_time > time_exit_at:
            continue
        low_value = row.get("low", row.get("price"))
        events.append({"time": event_time, "low": _decimal(low_value)})
    return sorted(events, key=lambda event: event["time"])


def _first_exit_event(
    *,
    option_events,
    underlying_events,
    underlying_invalidation,
    target_basis,
    stop_basis,
    time_exit_at,
):
    candidates = []
    for event in option_events:
        if event["cost_adjusted_exit_basis"] >= target_basis:
            candidates.append({**event, "exit_reason": "profit_target"})
        if event["cost_adjusted_exit_basis"] <= stop_basis:
            candidates.append({**event, "exit_reason": "option_premium_stop"})

    for event in underlying_events:
        if event["low"] < underlying_invalidation:
            option_exit = _first_option_at_or_after(option_events, event["time"])
            if option_exit is not None:
                candidates.append(
                    {**option_exit, "exit_reason": "setup_invalidation_stop"}
                )

    time_exit = _latest_option_at_or_before(option_events, time_exit_at)
    if time_exit is not None:
        candidates.append({**time_exit, "exit_reason": "time_exit_1545_et"})

    if not candidates:
        return None
    return min(candidates, key=lambda event: event["time"])


def _first_option_at_or_after(option_events, event_time):
    for option_event in option_events:
        if option_event["time"] >= event_time:
            return option_event
    return None


def _latest_option_at_or_before(option_events, event_time):
    latest = None
    for option_event in option_events:
        if option_event["time"] <= event_time:
            latest = option_event
    return latest


def _missing_exit_path_fields(*, option_events, underlying_events, time_exit_at):
    missing = []
    if not option_events or option_events[-1]["time"] < time_exit_at:
        missing.append("selected_contract_tcbbo_bid_path_through_1545_et")
    return missing


def _time_exit_datetime(signal_at):
    signal_et = signal_at.astimezone(EASTERN)
    return signal_et.replace(
        hour=TIME_EXIT_ET.hour,
        minute=TIME_EXIT_ET.minute,
        second=0,
        microsecond=0,
    )


def _decimal(value):
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"invalid decimal value: {value!r}") from exc


def _float_or_none(value):
    if value is None:
        return None
    return float(value)


def _result(
    row,
    *,
    result_status,
    result_name,
    failure_reason,
    gate_result,
    entry_basis=None,
    target_basis=None,
    stop_basis=None,
    exit_event=None,
    missing_fields=None,
    starter_data_enough=None,
    full_window_data_required=None,
    cost_check_request=None,
):
    result = {
        "candidate_id": row.get("candidate_id"),
        "result_status": result_status,
        "result_name": result_name,
        "failure_reason": failure_reason,
        "trade_rule_status": gate_result["trade_rule_status"],
        "rejection_reason": gate_result["rejection_reason"],
        "entry_fill_basis": gate_result.get("entry_fill_basis"),
        "exit_fill_basis": "bid_minus_slippage" if exit_event is not None else None,
        "entry_time": checker.normalize_timestamp(row["signal_time"]).isoformat()
        if row.get("signal_time")
        else None,
        "entry_quote_time": checker.normalize_timestamp(row["quote_time"]).isoformat()
        if row.get("quote_time")
        else None,
        "entry_ask": _float_or_none(_decimal(row["ask"])) if row.get("ask") else None,
        "cost_adjusted_entry_basis": _float_or_none(entry_basis),
        "profit_target_adjusted_exit_threshold": _float_or_none(target_basis),
        "option_stop_adjusted_exit_threshold": _float_or_none(stop_basis),
        "exit_reason": None,
        "exit_time": None,
        "exit_bid": None,
        "cost_adjusted_exit_basis": None,
        "gross_result": None,
        "cost_slippage_adjusted_result": None,
        "missing_fields": missing_fields or [],
        "starter_data_enough": starter_data_enough,
        "full_window_data_required": full_window_data_required,
        "cost_check_request": cost_check_request,
        "promotion_decision": "not_requested_not_made",
        "candidate_marked_ready": False,
        "proof_accepted": False,
        "profitability_claimed": False,
    }
    if exit_event is not None:
        result["exit_reason"] = exit_event["exit_reason"]
        result["exit_time"] = exit_event["time"].isoformat()
        result["exit_bid"] = _float_or_none(exit_event["bid"])
        result["cost_adjusted_exit_basis"] = _float_or_none(
            exit_event["cost_adjusted_exit_basis"]
        )
        result["gross_result"] = _float_or_none(exit_event["bid"] - _decimal(row["ask"]))
        result["cost_slippage_adjusted_result"] = _float_or_none(
            exit_event["cost_adjusted_exit_basis"] - entry_basis
        )
    return result
