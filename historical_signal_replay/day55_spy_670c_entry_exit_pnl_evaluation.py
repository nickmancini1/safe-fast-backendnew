import csv
import hashlib
import json
from datetime import datetime, time, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from zoneinfo import ZoneInfo

from historical_signal_replay import cfb_contract_selector
from historical_signal_replay import cfb_trade_rule_checker


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = (
    REPO_ROOT
    / "historical_signal_replay"
    / "source_data"
    / "external_option_data_drop"
    / "day55_quote_trade_statistics_selected_contracts"
)
MANIFEST_PATH = SOURCE_ROOT / "day55_quote_trade_statistics_download_manifest.json"
CONTRACT_SELECTION_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day55_definition_contract_selection_for_replay_ready_candidates.json"
)
COST_OUTPUT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day55_quote_trade_statistics_cost_check_for_selected_contracts.json"
)
PREVIOUS_RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day55_spy_670c_entry_exit_pnl_evaluation.json"
)
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day55_spy_670c_entry_exit_pnl_evaluation.json"
)
RESULT_DOC_PATH = REPO_ROOT / "SAFE_FAST_DAY55_SPY_670C_ENTRY_EXIT_PNL_EVALUATION_RESULT.md"

RESULT_VERSION = "day55_spy_670c_entry_exit_pnl_evaluation_v1"
TASK_FILENAME = "SAFE_FAST_DAY55_SPY_670C_ENTRY_EXIT_PNL_EVALUATION_CODEX_TASK.md"
REPLAY_TASK_FILENAME = "SAFE_FAST_DAY55_OPTION_EVIDENCE_ENTRY_EXIT_PNL_REPLAY_TASK.md"
SELECTED_WINNER_ID = "DAY52-SPY-2026-03-16-CLEAN-FAST-BREAK-20260316T133000Z-P39"
SETUP_FAMILY = "Clean Fast Break"
RAW_SYMBOL = "SPY   260330C00670000"
INSTRUMENT_ID = 1241515301
PUBLISHER_ID = 30
SETUP_TIMESTAMP_UTC = "2026-03-16T13:30:00Z"
TRIGGER_TIMESTAMP_UTC = "2026-03-16T13:31:00Z"
ENTRY_WINDOW_START_UTC = "2026-03-16T13:31:00Z"
ENTRY_WINDOW_END_UTC = "2026-03-16T13:36:00Z"
EXIT_WINDOW_END_UTC = "2026-03-16T19:45:00Z"
TRIGGER = "668.360000000"
INVALIDATION = "667.870000000"
TIME_EXIT_ET = time(15, 45)
EASTERN = ZoneInfo("America/New_York")

VALID_ENTRY_FOUND = "VALID_ENTRY_FOUND"
NO_ENTRY_EXACT_REJECTION = "NO_ENTRY_EXACT_REJECTION"
EXIT_EVALUATED = "EXIT_EVALUATED"
EXIT_BLOCKED = "EXIT_BLOCKED"
NET_PNL_EVALUATED = "NET_PNL_EVALUATED"
ECONOMIC_REPLAY_BLOCKED = "ECONOMIC_REPLAY_BLOCKED"

REQUIRED_SCHEMAS = ("cmbp-1", "tcbbo", "trades", "statistics")
CSV_BY_SCHEMA = {}


class Day55EvaluationError(ValueError):
    pass


def build_document(
    *,
    manifest_path=MANIFEST_PATH,
    contract_selection_path=CONTRACT_SELECTION_PATH,
    cost_output_path=COST_OUTPUT_PATH,
    previous_result_path=PREVIOUS_RESULT_PATH,
    source_root=SOURCE_ROOT,
    run_timestamp=None,
    source_commit=None,
):
    run_timestamp = run_timestamp or _utc_now()
    manifest = _load_json(manifest_path, "missing_manifest")
    contract_selection = _load_json(contract_selection_path, "missing_contract_selection")
    cost_output = _load_json(cost_output_path, "missing_cost_output")
    previous_result = _load_json(previous_result_path, "missing_previous_result")

    input_status = _validate_inputs(
        manifest=manifest,
        contract_selection=contract_selection,
        cost_output=cost_output,
        previous_result=previous_result,
        source_root=Path(source_root),
    )
    if input_status["status"] != "INPUTS_VALIDATED":
        evaluation = _blocked_evaluation(input_status["first_blocker"], input_status)
    elif not input_status["target_contract_in_manifest"]:
        evaluation = _target_contract_not_in_download_result(input_status)
    else:
        rows_by_schema = {
            schema: _read_csv_rows(
                _repo_path(input_status["target_schema_file_status"][schema]["csv_path"], source_root)
            )
            for schema in REQUIRED_SCHEMAS
        }
        evaluation = _evaluate_rows(rows_by_schema, input_status)

    proof_status = {
        "complete_end_to_end_backtest": (
            "YES"
            if evaluation["entry_status"] == VALID_ENTRY_FOUND
            and evaluation["exit_status"] == EXIT_EVALUATED
            and evaluation["net_pnl_status"] == NET_PNL_EVALUATED
            else "NO"
        ),
        "profitability_proof": "NO",
        "paper_live_eligibility": "NO",
    }

    return {
        "result_version": RESULT_VERSION,
        "task": REPLAY_TASK_FILENAME,
        "supersedes_task": TASK_FILENAME,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp,
        "scope": {
            "local_raw_databento_files_only": True,
            "databento_called": False,
            "tastytrade_called": False,
            "schwab_called": False,
            "more_data_requested": False,
            "definition_requested_or_needed": False,
            "main_py_changed": False,
            "railway_or_deploy_changed": False,
            "broker_account_order_alert_touched": False,
            "credentials_or_env_changed": False,
            "sizing_changed": False,
            "raw_vendor_files_mutated": False,
        },
        "accepted_setup": {
            "underlying": "SPY",
            "setup_family": SETUP_FAMILY,
            "selected_winner": SELECTED_WINNER_ID,
            "setup_timestamp": SETUP_TIMESTAMP_UTC,
            "trigger_timestamp": TRIGGER_TIMESTAMP_UTC,
            "trigger": TRIGGER,
            "invalidation": INVALIDATION,
            "entry_window": {
                "start": ENTRY_WINDOW_START_UTC,
                "end": ENTRY_WINDOW_END_UTC,
                "end_inclusive": False,
            },
        },
        "selected_contract": {
            "raw_symbol": RAW_SYMBOL,
            "expiration": "2026-03-30",
            "strike": "670",
            "side": "call",
            "instrument_id": INSTRUMENT_ID,
            "publisher_id": PUBLISHER_ID,
        },
        "input_validation": input_status,
        "evaluation": evaluation,
        "proof_status": proof_status,
        "profitability_status": "NO",
        "paper_live_eligibility": "NO",
        "remaining_blocker": evaluation["first_blocker"],
    }


def write_outputs(*, run_timestamp=None, source_commit=None):
    document = build_document(run_timestamp=run_timestamp, source_commit=source_commit)
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    RESULT_DOC_PATH.write_text(_markdown(document), encoding="utf-8")
    return document


def _validate_inputs(*, manifest, contract_selection, cost_output, previous_result, source_root):
    problems = []

    if manifest.get("status") != "SUCCESS":
        problems.append("manifest_status_not_success")
    if manifest.get("download_performed") is not True:
        problems.append("download_not_performed")
    if manifest.get("request_count") != 32:
        problems.append("request_count_not_32")
    if set(manifest.get("required_schemas", [])) != set(REQUIRED_SCHEMAS):
        problems.append("required_schema_set_mismatch")
    if "definition" not in set(manifest.get("forbidden_schemas", [])):
        problems.append("definition_not_forbidden")
    if any(request.get("schema") == "definition" for request in manifest.get("exact_requests", [])):
        problems.append("definition_schema_unexpected")

    if contract_selection.get("decision") != "DEFINITION_CONTRACT_SELECTION_COMPLETE":
        problems.append("contract_selection_not_complete")
    if cost_output.get("status") != "SUCCESS":
        problems.append("cost_check_not_success")
    if cost_output.get("download_performed") is not False:
        problems.append("cost_check_download_performed_changed")
    if cost_output.get("grouped_cost") != manifest.get("checked_grouped_cost_usd"):
        problems.append("cost_check_amount_mismatch")
    if [vendor_request(request) for request in manifest.get("exact_requests", [])] != [
        vendor_request(request) for request in cost_output.get("requests", [])
    ]:
        problems.append("manifest_cost_requests_mismatch")

    selected_contracts = []
    for candidate in contract_selection.get("candidates", []):
        for leg in ("long_contract", "short_contract"):
            contract = candidate.get(leg) or {}
            if contract:
                selected_contracts.append(
                    {
                        "candidate_id": candidate.get("candidate_id"),
                        "leg": leg.replace("_contract", ""),
                        "raw_symbol": contract.get("raw_symbol"),
                        "instrument_id": _int_or_none(contract.get("instrument_id")),
                    }
                )

    file_status = {}
    output_files = manifest.get("output_files", [])
    for output in output_files:
        request_id = output.get("request_id") or f"{output.get('schema')}_{output.get('symbols')}"
        csv_path = _repo_path(output.get("csv_path"), source_root)
        dbn_path = _repo_path(output.get("dbn_path"), source_root)
        expected_records = int(output.get("parsed_record_count") or 0)
        csv_exists = csv_path.exists()
        dbn_exists = dbn_path.exists()
        actual_records = _csv_record_count(csv_path) if csv_exists else None
        file_status[request_id] = {
            "schema": output.get("schema"),
            "symbols": output.get("symbols"),
            "csv_path": _relative(csv_path),
            "dbn_path": _relative(dbn_path),
            "csv_exists": csv_exists,
            "dbn_exists": dbn_exists,
            "manifest_record_count": expected_records,
            "actual_csv_record_count": actual_records,
            "manifest_empty": output.get("empty"),
            "csv_sha256_match": _sha256_matches(csv_path, output.get("csv_sha256")) if csv_exists else False,
            "dbn_sha256_match": _sha256_matches(dbn_path, output.get("dbn_sha256")) if dbn_exists else False,
        }
        if output.get("schema") not in REQUIRED_SCHEMAS:
            problems.append(f"{request_id}_unexpected_schema")
        if output.get("contract_identity_validated") is not True:
            problems.append(f"{request_id}_contract_identity_not_validated")
        if not csv_exists:
            problems.append(f"{request_id}_csv_missing")
        if not dbn_exists:
            problems.append(f"{request_id}_dbn_missing")
        if csv_exists and actual_records != expected_records:
            problems.append(f"{request_id}_csv_record_count_mismatch")
        if csv_exists and not file_status[request_id]["csv_sha256_match"]:
            problems.append(f"{request_id}_csv_sha256_mismatch")
        if dbn_exists and not file_status[request_id]["dbn_sha256_match"]:
            problems.append(f"{request_id}_dbn_sha256_mismatch")

    target_outputs = [
        output for output in output_files
        if str(output.get("symbols", "")).strip() == RAW_SYMBOL.strip()
    ]
    target_schema_file_status = {}
    for output in target_outputs:
        schema = output.get("schema")
        if schema in REQUIRED_SCHEMAS:
            target_schema_file_status[schema] = {
                "csv_path": _relative(_repo_path(output.get("csv_path"), source_root)),
                "exists": _repo_path(output.get("csv_path"), source_root).exists(),
                "manifest_record_count": output.get("parsed_record_count"),
                "manifest_empty": output.get("empty"),
            }

    target_contract_in_manifest = bool(target_outputs)
    if target_contract_in_manifest and set(target_schema_file_status) != set(REQUIRED_SCHEMAS):
        problems.append("target_contract_schema_set_incomplete")

    previous_evaluation = previous_result.get("evaluation", {})
    previous_input_validation = previous_result.get("input_validation", {})
    previous_blocker = (
        previous_input_validation.get("previous_blocker")
        or previous_result.get("remaining_blocker")
        or previous_evaluation.get("first_blocker")
    )
    old_blocker_closed = False
    if previous_blocker == "open_interest_statistics_zero_rows" and target_contract_in_manifest:
        stats_path = target_schema_file_status.get("statistics", {}).get("csv_path")
        if stats_path:
            old_blocker_closed = (
                _statistics_status(_read_csv_rows(_repo_path(stats_path, source_root)))["status"]
                == "OPEN_INTEREST_VALID"
            )

    first_blocker = problems[0] if problems else None
    return {
        "status": "INPUTS_VALIDATED" if not problems else ECONOMIC_REPLAY_BLOCKED,
        "first_blocker": first_blocker,
        "problems": problems,
        "manifest_status": manifest.get("status"),
        "download_performed": manifest.get("download_performed"),
        "request_count": manifest.get("request_count"),
        "completed_or_reused_request_count": len(manifest.get("completed_or_reused_request_ids", [])),
        "remaining_request_count": len(manifest.get("remaining_request_ids", [])),
        "completed_or_reused_schemas": sorted(set(item.get("schema") for item in output_files)),
        "schema_file_status": file_status,
        "target_contract_in_manifest": target_contract_in_manifest,
        "target_schema_file_status": target_schema_file_status,
        "selected_contracts": selected_contracts,
        "previous_blocker": previous_blocker,
        "old_blocker_closed_by_raw_statistics": old_blocker_closed,
        "definition_requested_or_needed": False,
        "contract_identity_verified": all(
            output.get("contract_identity_validated") is True for output in output_files
        ),
    }


def _evaluate_rows(rows_by_schema, input_status):
    entry_window_start = _parse_time(ENTRY_WINDOW_START_UTC)
    entry_window_end = _parse_time(ENTRY_WINDOW_END_UTC)
    trigger_at = _parse_time(TRIGGER_TIMESTAMP_UTC)
    time_exit_at = _time_exit_datetime(trigger_at)

    statistics_status = _statistics_status(rows_by_schema["statistics"])
    quote_candidates = _entry_quote_candidates(
        rows_by_schema["cmbp-1"],
        start=entry_window_start,
        end=entry_window_end,
    )
    trade_context = _trade_volume_context(rows_by_schema["trades"], cutoff=entry_window_end)

    entry_attempt = {
        "accepted_window_start": ENTRY_WINDOW_START_UTC,
        "accepted_window_end": ENTRY_WINDOW_END_UTC,
        "window_end_inclusive": False,
        "quotes_considered": len(quote_candidates),
        "first_quote_timestamp": _iso(quote_candidates[0]["time"]) if quote_candidates else None,
        "first_quote_bid": _decimal_string(quote_candidates[0]["bid"]) if quote_candidates else None,
        "first_quote_ask": _decimal_string(quote_candidates[0]["ask"]) if quote_candidates else None,
        "first_quote_bid_size": _decimal_string(quote_candidates[0]["bid_size"]) if quote_candidates else None,
        "first_quote_ask_size": _decimal_string(quote_candidates[0]["ask_size"]) if quote_candidates else None,
        "quote_age_seconds": None,
        "spread": None,
        "spread_percent": None,
        "entry_bid_ask_basis": "ask_plus_0.02_entry_slippage",
        "entry_ask": None,
        "entry_price": None,
    }

    if not quote_candidates:
        return _no_entry_result(
            "complete_entry_window_quote_missing",
            input_status,
            entry_attempt,
            trade_context,
            statistics_status,
        )

    for quote in quote_candidates:
        quote_eval = _evaluate_quote(quote, trigger_at)
        entry_attempt.update(quote_eval["context"])
        if quote_eval["blocker"]:
            return _no_entry_result(
                quote_eval["blocker"],
                input_status,
                entry_attempt,
                trade_context,
                statistics_status,
            )
        if trade_context["trade_volume_through_entry_window"] < cfb_contract_selector.MIN_TRADE_VOLUME:
            return _no_entry_result(
                "trade_volume_below_1",
                input_status,
                entry_attempt,
                trade_context,
                statistics_status,
            )
        if statistics_status["status"] != "OPEN_INTEREST_VALID":
            return _no_entry_result(
                statistics_status["first_blocker"],
                input_status,
                entry_attempt,
                trade_context,
                statistics_status,
            )
        entry_price = quote["ask"] + cfb_trade_rule_checker.ENTRY_SLIPPAGE_BUFFER
        entry_attempt["entry_ask"] = _decimal_string(quote["ask"])
        entry_attempt["entry_price"] = _decimal_string(entry_price)
        return _entry_and_exit_result(
            entry_quote=quote,
            entry_price=entry_price,
            rows_by_schema=rows_by_schema,
            input_status=input_status,
            entry_attempt=entry_attempt,
            trade_context=trade_context,
            statistics_status=statistics_status,
            time_exit_at=time_exit_at,
        )

    return _no_entry_result(
        "no_valid_entry_quote",
        input_status,
        entry_attempt,
        trade_context,
        statistics_status,
    )


def _target_contract_not_in_download_result(input_status):
    entry_attempt = {
        "accepted_window_start": ENTRY_WINDOW_START_UTC,
        "accepted_window_end": ENTRY_WINDOW_END_UTC,
        "window_end_inclusive": False,
        "target_raw_symbol": RAW_SYMBOL,
        "downloaded_symbols": sorted(
            {
                contract["raw_symbol"]
                for contract in input_status.get("selected_contracts", [])
                if contract.get("raw_symbol")
            }
        ),
        "previous_blocker": input_status.get("previous_blocker"),
        "old_blocker_closed_by_raw_statistics": input_status.get(
            "old_blocker_closed_by_raw_statistics"
        ),
    }
    return _base_evaluation(
        entry_status=NO_ENTRY_EXACT_REJECTION,
        exit_status=EXIT_BLOCKED,
        net_pnl_status=ECONOMIC_REPLAY_BLOCKED,
        first_blocker="target_contract_not_in_day55_download_manifest",
        input_status=input_status,
        entry_attempt=entry_attempt,
        trade_context={
            "status": "NOT_EVALUATED",
            "reason": "target_contract_not_in_day55_download_manifest",
        },
        statistics_status={
            "status": "NOT_EVALUATED_TARGET_CONTRACT_NOT_IN_MANIFEST",
            "rows": None,
            "open_interest": None,
            "first_blocker": "target_contract_not_in_day55_download_manifest",
            "previous_blocker": input_status.get("previous_blocker"),
            "old_blocker_closed_by_raw_statistics": input_status.get(
                "old_blocker_closed_by_raw_statistics"
            ),
        },
        exit_result={"status": EXIT_BLOCKED, "exit_timestamp": None},
    )


def _statistics_status(rows):
    matching = [_normalized_row(row) for row in rows if _identity_matches(row)]
    oi_rows = []
    for row in matching:
        stat_type = str(row.get("stat_type", "")).strip()
        quantity = _decimal_or_none(row.get("quantity"))
        price = _decimal_or_none(row.get("price"))
        value = quantity if quantity is not None else price
        if stat_type in ("9", "open_interest", "OI") or value is not None:
            oi_rows.append((row, value))
    if not matching:
        return {
            "status": "STATISTICS_ZERO_ROWS",
            "rows": 0,
            "open_interest": None,
            "first_blocker": "open_interest_statistics_zero_rows",
        }
    for row, value in oi_rows:
        if value is not None and value >= cfb_contract_selector.MIN_OPEN_INTEREST:
            return {
                "status": "OPEN_INTEREST_VALID",
                "rows": len(matching),
                "open_interest": _decimal_string(value),
                "statistics_timestamp": _iso(_parse_time(row["ts_event"])),
                "first_blocker": None,
            }
    return {
        "status": "OPEN_INTEREST_INVALID",
        "rows": len(matching),
        "open_interest": None,
        "first_blocker": "open_interest_below_1",
    }


def _entry_quote_candidates(rows, *, start, end):
    candidates = []
    for raw_row in rows:
        if not _identity_matches(raw_row):
            continue
        row = _normalized_row(raw_row)
        event_time = _parse_time(row["ts_event"])
        if event_time < start or event_time >= end:
            continue
        bid = _decimal_or_none(row.get("bid_px_00"))
        ask = _decimal_or_none(row.get("ask_px_00"))
        bid_size = _decimal_or_none(row.get("bid_sz_00"))
        ask_size = _decimal_or_none(row.get("ask_sz_00"))
        recv_time = _parse_time(row["ts_recv"]) if row.get("ts_recv") else event_time
        candidates.append(
            {
                "time": event_time,
                "recv_time": recv_time,
                "bid": bid,
                "ask": ask,
                "bid_size": bid_size,
                "ask_size": ask_size,
                "row": row,
            }
        )
    return sorted(candidates, key=lambda item: (item["time"], item["recv_time"]))


def _evaluate_quote(quote, trigger_at):
    bid = quote["bid"]
    ask = quote["ask"]
    bid_size = quote["bid_size"]
    ask_size = quote["ask_size"]
    quote_age_seconds = Decimal(str((quote["time"] - trigger_at).total_seconds()))
    context = {
        "quote_timestamp": _iso(quote["time"]),
        "quote_age_seconds": _decimal_string(quote_age_seconds),
        "first_quote_bid": _decimal_string(bid),
        "first_quote_ask": _decimal_string(ask),
        "first_quote_bid_size": _decimal_string(bid_size),
        "first_quote_ask_size": _decimal_string(ask_size),
        "spread": None,
        "spread_percent": None,
    }
    if quote["time"] < trigger_at:
        return {"blocker": "pre_trigger_quote_not_permitted_for_entry", "context": context}
    if quote_age_seconds > Decimal("60"):
        return {"blocker": "quote_age_above_clean_entry_limit_or_above_5_minutes", "context": context}
    if bid is None or ask is None or ask <= 0 or bid <= 0:
        return {"blocker": "missing_or_non_positive_bid_ask", "context": context}
    if ask <= bid:
        return {"blocker": "ask_not_greater_than_bid", "context": context}
    spread = ask - bid
    midpoint = (ask + bid) / Decimal("2")
    spread_percent = spread / midpoint
    context["spread"] = _decimal_string(spread)
    context["spread_percent"] = _decimal_string(spread_percent)
    if spread > cfb_contract_selector.SPREAD_CAP:
        return {"blocker": "spread_above_0_15", "context": context}
    if spread_percent > cfb_contract_selector.SPREAD_PCT_CAP:
        return {"blocker": "spread_percent_above_2_percent", "context": context}
    if bid_size is None or bid_size < cfb_contract_selector.MIN_BID_SIZE:
        return {"blocker": "bid_size_below_1", "context": context}
    if ask_size is None or ask_size < cfb_contract_selector.MIN_ASK_SIZE:
        return {"blocker": "ask_size_below_1", "context": context}
    return {"blocker": None, "context": context}


def _trade_volume_context(rows, *, cutoff):
    selected = []
    for raw_row in rows:
        if not _identity_matches(raw_row):
            continue
        row = _normalized_row(raw_row)
        event_time = _parse_time(row["ts_event"])
        if event_time <= cutoff:
            selected.append((event_time, _decimal_or_none(row.get("size")) or Decimal("0")))
    total = sum((size for _, size in selected), Decimal("0"))
    return {
        "status": "TRADE_VOLUME_VALID" if total >= cfb_contract_selector.MIN_TRADE_VOLUME else "TRADE_VOLUME_INVALID",
        "trade_count_through_entry_window": len(selected),
        "trade_volume_through_entry_window": total,
        "first_trade_timestamp": _iso(selected[0][0]) if selected else None,
        "minimum_trade_volume": str(cfb_contract_selector.MIN_TRADE_VOLUME),
    }


def _entry_and_exit_result(
    *,
    entry_quote,
    entry_price,
    rows_by_schema,
    input_status,
    entry_attempt,
    trade_context,
    statistics_status,
    time_exit_at,
):
    target = entry_price * (Decimal("1") + cfb_trade_rule_checker.PROFIT_TARGET_PERCENT)
    stop = entry_price * (Decimal("1") + cfb_trade_rule_checker.OPTION_STOP_PERCENT)
    exit_event = _first_exit_event(
        rows_by_schema["tcbbo"],
        start=entry_quote["time"],
        end=time_exit_at,
        target=target,
        stop=stop,
    )
    if exit_event is None:
        return _base_evaluation(
            entry_status=VALID_ENTRY_FOUND,
            exit_status=EXIT_BLOCKED,
            net_pnl_status=ECONOMIC_REPLAY_BLOCKED,
            first_blocker="selected_contract_tcbbo_bid_path_through_1545_et",
            input_status=input_status,
            entry_attempt=entry_attempt,
            trade_context=trade_context,
            statistics_status=statistics_status,
            exit_result={"status": EXIT_BLOCKED, "exit_timestamp": None},
        )

    gross_pnl = exit_event["bid"] - entry_quote["ask"]
    exit_price = exit_event["bid"] - cfb_trade_rule_checker.EXIT_SLIPPAGE_BUFFER
    net_pnl = exit_price - entry_price
    return _base_evaluation(
        entry_status=VALID_ENTRY_FOUND,
        exit_status=EXIT_EVALUATED,
        net_pnl_status=NET_PNL_EVALUATED,
        first_blocker=None,
        input_status=input_status,
        entry_attempt=entry_attempt,
        trade_context=trade_context,
        statistics_status=statistics_status,
        exit_result={
            "status": EXIT_EVALUATED,
            "exit_timestamp": _iso(exit_event["time"]),
            "exit_reason": exit_event["reason"],
            "exit_bid": _decimal_string(exit_event["bid"]),
            "exit_bid_minus_slippage": _decimal_string(exit_price),
            "target_threshold": _decimal_string(target),
            "stop_threshold": _decimal_string(stop),
        },
        pnl_result={
            "gross_pnl": _decimal_string(gross_pnl),
            "entry_slippage": str(cfb_trade_rule_checker.ENTRY_SLIPPAGE_BUFFER),
            "exit_slippage": str(cfb_trade_rule_checker.EXIT_SLIPPAGE_BUFFER),
            "commissions": "0",
            "fees": "0",
            "net_pnl": _decimal_string(net_pnl),
            "basis": "one_contract_per_share_option_premium_points",
        },
    )


def _first_exit_event(rows, *, start, end, target, stop):
    events = []
    for raw_row in rows:
        if not _identity_matches(raw_row):
            continue
        row = _normalized_row(raw_row)
        event_time = _parse_time(row["ts_event"])
        if event_time < start or event_time > end:
            continue
        bid = _decimal_or_none(row.get("bid_px_00"))
        bid_size = _decimal_or_none(row.get("bid_sz_00"))
        if bid is None or bid_size is None or bid_size < cfb_contract_selector.MIN_BID_SIZE:
            continue
        adjusted_exit = bid - cfb_trade_rule_checker.EXIT_SLIPPAGE_BUFFER
        if adjusted_exit >= target:
            events.append({"time": event_time, "bid": bid, "reason": "profit_target"})
        elif adjusted_exit <= stop:
            events.append({"time": event_time, "bid": bid, "reason": "option_premium_stop"})
    time_exit = _latest_quote_at_or_before(rows, end)
    if time_exit is not None:
        events.append({**time_exit, "reason": "time_exit_1545_et"})
    return min(events, key=lambda item: item["time"]) if events else None


def _latest_quote_at_or_before(rows, cutoff):
    latest = None
    for raw_row in rows:
        if not _identity_matches(raw_row):
            continue
        row = _normalized_row(raw_row)
        event_time = _parse_time(row["ts_event"])
        if event_time > cutoff:
            continue
        bid = _decimal_or_none(row.get("bid_px_00"))
        bid_size = _decimal_or_none(row.get("bid_sz_00"))
        if bid is None or bid_size is None or bid_size < cfb_contract_selector.MIN_BID_SIZE:
            continue
        latest = {"time": event_time, "bid": bid}
    return latest


def _no_entry_result(first_blocker, input_status, entry_attempt, trade_context, statistics_status):
    return _base_evaluation(
        entry_status=NO_ENTRY_EXACT_REJECTION,
        exit_status=EXIT_BLOCKED,
        net_pnl_status=ECONOMIC_REPLAY_BLOCKED,
        first_blocker=first_blocker,
        input_status=input_status,
        entry_attempt=entry_attempt,
        trade_context=trade_context,
        statistics_status=statistics_status,
        exit_result={"status": EXIT_BLOCKED, "exit_timestamp": None},
    )


def _blocked_evaluation(first_blocker, input_status):
    return _base_evaluation(
        entry_status=ECONOMIC_REPLAY_BLOCKED,
        exit_status=EXIT_BLOCKED,
        net_pnl_status=ECONOMIC_REPLAY_BLOCKED,
        first_blocker=first_blocker,
        input_status=input_status,
        entry_attempt={},
        trade_context={},
        statistics_status={},
        exit_result={"status": EXIT_BLOCKED, "exit_timestamp": None},
    )


def _base_evaluation(
    *,
    entry_status,
    exit_status,
    net_pnl_status,
    first_blocker,
    input_status,
    entry_attempt,
    trade_context,
    statistics_status,
    exit_result,
    pnl_result=None,
):
    return {
        "entry_status": entry_status,
        "entry_timestamp": entry_attempt.get("quote_timestamp") if entry_status == VALID_ENTRY_FOUND else None,
        "entry_bid_ask_basis": entry_attempt.get("entry_bid_ask_basis"),
        "entry_price": entry_attempt.get("entry_price"),
        "quote_age": entry_attempt.get("quote_age_seconds"),
        "spread": entry_attempt.get("spread"),
        "spread_percent": entry_attempt.get("spread_percent"),
        "entry_context": entry_attempt,
        "trade_volume_context": _stringify_decimals(trade_context),
        "statistics_open_interest_status": statistics_status,
        "exit_status": exit_status,
        "exit_result": exit_result,
        "gross_pnl": (pnl_result or {}).get("gross_pnl"),
        "net_pnl_status": net_pnl_status,
        "net_pnl": (pnl_result or {}).get("net_pnl"),
        "pnl_result": pnl_result,
        "first_blocker": first_blocker,
        "input_status": input_status["status"],
        "profitability_status": "NO",
        "paper_live_eligibility": "NO",
    }


def _read_csv_rows(path):
    if not Path(path).exists():
        raise Day55EvaluationError(f"missing schema csv: {path}")
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle) if any((value or "").strip() for value in row.values())]


def _csv_record_count(path):
    return len(_read_csv_rows(path))


def _sha256_matches(path, expected):
    if not expected:
        return False
    return hashlib.sha256(Path(path).read_bytes()).hexdigest() == expected


def _repo_path(value, fallback_root):
    if not value:
        return Path(fallback_root)
    path = Path(value)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def _int_or_none(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def vendor_request(request):
    return {
        "dataset": request.get("dataset"),
        "schema": request.get("schema"),
        "start": request.get("start"),
        "end": request.get("end"),
        "stype_in": request.get("stype_in"),
        "symbols": request.get("symbols"),
    }


def _identity_matches(row):
    try:
        instrument_id = int(row.get("instrument_id"))
    except (TypeError, ValueError):
        return False
    return str(row.get("symbol", "")).strip() == RAW_SYMBOL.strip() and instrument_id == INSTRUMENT_ID


def _normalized_row(row):
    return {key: (value.strip() if isinstance(value, str) else value) for key, value in row.items()}


def _load_json(path, missing_blocker):
    path = Path(path)
    if not path.exists():
        raise Day55EvaluationError(missing_blocker)
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_time(value):
    text = str(value).strip()
    if " " in text and "T" not in text:
        text = text.replace(" ", "T", 1)
    return datetime.fromisoformat(_trim_nanoseconds(text).replace("Z", "+00:00"))


def _trim_nanoseconds(text):
    timezone_suffix = ""
    timestamp = text
    if text.endswith("Z"):
        timestamp = text[:-1]
        timezone_suffix = "Z"
    else:
        for index in range(len(text) - 1, 9, -1):
            if text[index] in "+-":
                timestamp = text[:index]
                timezone_suffix = text[index:]
                break
    if "." not in timestamp:
        return text
    prefix, fraction = timestamp.split(".", 1)
    return f"{prefix}.{fraction[:6]}{timezone_suffix}"


def _time_exit_datetime(trigger_at):
    trigger_et = trigger_at.astimezone(EASTERN)
    return trigger_et.replace(
        hour=TIME_EXIT_ET.hour,
        minute=TIME_EXIT_ET.minute,
        second=0,
        microsecond=0,
    )


def _decimal_or_none(value):
    if value in (None, ""):
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def _decimal_string(value):
    if value is None:
        return None
    return format(value, "f")


def _stringify_decimals(value):
    if isinstance(value, Decimal):
        return _decimal_string(value)
    if isinstance(value, dict):
        return {key: _stringify_decimals(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_stringify_decimals(item) for item in value]
    return value


def _iso(value):
    return value.isoformat().replace("+00:00", "Z")


def _relative(path):
    try:
        return str(Path(path).resolve().relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _git_short_head():
    head = REPO_ROOT / ".git" / "HEAD"
    if not head.exists():
        return "UNKNOWN"
    text = head.read_text(encoding="utf-8").strip()
    if text.startswith("ref: "):
        ref = REPO_ROOT / ".git" / text[5:]
        if ref.exists():
            return ref.read_text(encoding="utf-8").strip()[:7]
    return text[:7]


def _utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _markdown(document):
    evaluation = document["evaluation"]
    proof = document["proof_status"]
    return f"""# SAFE-FAST Day 55 SPY 670C Entry / Exit / Net P&L Evaluation Result

## Decision

- Status: `{evaluation['entry_status']}`.
- Selected winner: `{SELECTED_WINNER_ID}`.
- Contract: `{RAW_SYMBOL}`, instrument `{INSTRUMENT_ID}`, publisher `{PUBLISHER_ID}`.
- Entry window: `{ENTRY_WINDOW_START_UTC}` through `{ENTRY_WINDOW_END_UTC}`.
- First blocker: `{evaluation['first_blocker']}`.

## Entry / Exit / P&L

- Entry timestamp: `{evaluation['entry_timestamp']}`.
- Entry price: `{evaluation['entry_price']}`.
- Quote age: `{evaluation['quote_age']}`.
- Spread: `{evaluation['spread']}`.
- Trade-volume status: `{evaluation['trade_volume_context'].get('status')}`.
- Statistics/OI status: `{evaluation['statistics_open_interest_status'].get('status')}`.
- Exit status: `{evaluation['exit_status']}`.
- Gross P&L: `{evaluation['gross_pnl']}`.
- Net P&L: `{evaluation['net_pnl']}`.

## Proof

- Complete end-to-end backtest: `{proof['complete_end_to_end_backtest']}`.
- Profitability proof: `{proof['profitability_proof']}`.
- Paper/live eligibility: `{proof['paper_live_eligibility']}`.

## Guardrails

Local Databento files only. No Databento, tastytrade, Schwab, definition request, credential, `.env`, `main.py`, Railway/deploy, production/live backend, broker/account/order/fill/alert, sizing, stage, commit, push, profitability claim, or paper/live eligibility change was made.
"""


if __name__ == "__main__":
    doc = write_outputs()
    print(
        "wrote day55 SPY 670C evaluation: "
        f"{doc['evaluation']['entry_status']} first_blocker={doc['evaluation']['first_blocker']}"
    )
