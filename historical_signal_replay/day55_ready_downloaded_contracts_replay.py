import csv
import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

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
SPY_670C_RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day55_spy_670c_entry_exit_pnl_evaluation.json"
)
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day55_ready_downloaded_contracts_replay.json"
)
RESULT_DOC_PATH = REPO_ROOT / "SAFE_FAST_DAY55_READY_DOWNLOADED_CONTRACTS_REPLAY_RESULT.md"

RESULT_VERSION = "day55_ready_downloaded_contracts_replay_v1"
TASK_FILENAME = "SAFE_FAST_DAY55_READY_DOWNLOADED_CONTRACTS_REPLAY_TASK.md"
REQUIRED_SCHEMAS = ("cmbp-1", "tcbbo", "trades", "statistics")
FORBIDDEN_TARGET = "SPY   260330C00670000"
FORBIDDEN_TARGET_BLOCKER = "target_contract_not_in_day55_download_manifest"
ALLOWED_CONTRACTS = (
    "QQQ   260416C00585000",
    "QQQ   260416C00590000",
    "QQQ   260501C00650000",
    "QQQ   260501C00655000",
    "SPY   260414C00645000",
    "SPY   260414C00650000",
    "SPY   260501C00702000",
    "SPY   260501C00707000",
)

VALID_ENTRY_FOUND = "VALID_ENTRY_FOUND"
NO_ENTRY_EXACT_REJECTION = "NO_ENTRY_EXACT_REJECTION"
EXIT_EVALUATED = "EXIT_EVALUATED"
EXIT_BLOCKED = "EXIT_BLOCKED"
NET_PNL_EVALUATED = "NET_PNL_EVALUATED"
ECONOMIC_REPLAY_BLOCKED = "ECONOMIC_REPLAY_BLOCKED"


class Day55ReadyReplayError(ValueError):
    pass


def build_document(
    *,
    manifest_path=MANIFEST_PATH,
    contract_selection_path=CONTRACT_SELECTION_PATH,
    cost_output_path=COST_OUTPUT_PATH,
    spy_670c_result_path=SPY_670C_RESULT_PATH,
    source_root=SOURCE_ROOT,
    run_timestamp=None,
    source_commit=None,
):
    run_timestamp = run_timestamp or _utc_now()
    manifest = _load_json(manifest_path, "missing_manifest")
    contract_selection = _load_json(contract_selection_path, "missing_contract_selection")
    cost_output = _load_json(cost_output_path, "missing_cost_output")
    spy_670c_result = _load_json(spy_670c_result_path, "missing_spy_670c_result")

    input_validation = _validate_inputs(
        manifest=manifest,
        contract_selection=contract_selection,
        cost_output=cost_output,
        spy_670c_result=spy_670c_result,
        source_root=Path(source_root),
    )

    if input_validation["status"] == "INPUTS_VALIDATED":
        contract_results = [
            _evaluate_contract(contract, input_validation, source_root=Path(source_root))
            for contract in input_validation["ready_contracts"]
        ]
    else:
        contract_results = [
            _blocked_contract_result(symbol, input_validation["first_blocker"])
            for symbol in ALLOWED_CONTRACTS
        ]

    valid_entries = sum(1 for item in contract_results if item["entry_status"] == VALID_ENTRY_FOUND)
    evaluated_exits = sum(1 for item in contract_results if item["exit_status"] == EXIT_EVALUATED)
    net_pnl_results = sum(1 for item in contract_results if item["net_pnl_status"] == NET_PNL_EVALUATED)
    exact_rejections = sum(
        1 for item in contract_results if item["entry_status"] == NO_ENTRY_EXACT_REJECTION
    )
    unresolved = sum(1 for item in contract_results if item["entry_status"] == ECONOMIC_REPLAY_BLOCKED)
    profitable_net_results = sum(
        1
        for item in contract_results
        if item.get("net_pnl") is not None and Decimal(item["net_pnl"]) > Decimal("0")
    )

    return {
        "result_version": RESULT_VERSION,
        "task": TASK_FILENAME,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp,
        "scope": {
            "local_raw_databento_files_only": True,
            "databento_called": False,
            "tastytrade_called": False,
            "schwab_called": False,
            "vendor_download_performed": False,
            "definition_requested": False,
            "more_data_requested": False,
            "main_py_changed": False,
            "railway_or_deploy_changed": False,
            "broker_account_order_alert_touched": False,
            "credentials_or_env_changed": False,
            "sizing_changed": False,
            "raw_vendor_files_mutated": False,
        },
        "baseline": {
            "download_manifest_status": manifest.get("status"),
            "downloaded_request_count": manifest.get("request_count"),
            "required_schemas": sorted(REQUIRED_SCHEMAS),
            "forbidden_schemas": manifest.get("forbidden_schemas", []),
            "allowed_contract_count": len(ALLOWED_CONTRACTS),
            "allowed_contracts": list(ALLOWED_CONTRACTS),
            "preserved_spy_670c_rejection": _spy_670c_rejection_status(spy_670c_result),
        },
        "input_validation": input_validation,
        "contract_results": contract_results,
        "summary": {
            "ready_contracts_evaluated": len(contract_results),
            "valid_entries": valid_entries,
            "evaluated_exits": evaluated_exits,
            "net_pnl_results": net_pnl_results,
            "exact_no_entry_rejections": exact_rejections,
            "unresolved_or_blocked": unresolved,
            "profitable_net_results": profitable_net_results,
            "profitability_proof": "NO",
            "paper_live_eligibility": "NO",
        },
        "profitability_proof": "NO",
        "paper_live_eligibility": "NO",
        "next_action": _next_action(contract_results),
    }


def write_outputs(*, run_timestamp=None, source_commit=None):
    document = build_document(run_timestamp=run_timestamp, source_commit=source_commit)
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    RESULT_DOC_PATH.write_text(_markdown(document), encoding="utf-8")
    return document


def _validate_inputs(*, manifest, contract_selection, cost_output, spy_670c_result, source_root):
    problems = []
    output_files = manifest.get("output_files", [])

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
        problems.append("definition_request_unexpected")
    if contract_selection.get("decision") != "DEFINITION_CONTRACT_SELECTION_COMPLETE":
        problems.append("contract_selection_not_complete")
    if cost_output.get("status") != "SUCCESS":
        problems.append("cost_check_not_success")
    if cost_output.get("download_performed") is not False:
        problems.append("cost_check_download_performed_changed")
    if cost_output.get("grouped_cost") != manifest.get("checked_grouped_cost_usd"):
        problems.append("cost_check_amount_mismatch")
    if [_vendor_request(item) for item in manifest.get("exact_requests", [])] != [
        _vendor_request(item) for item in cost_output.get("requests", [])
    ]:
        problems.append("manifest_cost_requests_mismatch")

    spy_rejection = _spy_670c_rejection_status(spy_670c_result)
    if spy_rejection["preserved"] is not True:
        problems.append("spy_670c_exact_rejection_not_preserved")

    schema_file_status = {}
    outputs_by_symbol = {}
    for output in output_files:
        request_id = output.get("request_id")
        csv_path = _repo_path(output.get("csv_path"), source_root)
        dbn_path = _repo_path(output.get("dbn_path"), source_root)
        expected_records = int(output.get("parsed_record_count") or 0)
        csv_exists = csv_path.exists()
        dbn_exists = dbn_path.exists()
        actual_records = _csv_record_count(csv_path) if csv_exists else None
        status = {
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
            "contract_identity_validated": output.get("contract_identity_validated"),
            "start": output.get("start"),
            "end": output.get("end"),
        }
        schema_file_status[request_id] = status
        outputs_by_symbol.setdefault(output.get("symbols"), {})[output.get("schema")] = {**output, **status}
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
        if csv_exists and not status["csv_sha256_match"]:
            problems.append(f"{request_id}_csv_sha256_mismatch")
        if dbn_exists and not status["dbn_sha256_match"]:
            problems.append(f"{request_id}_dbn_sha256_mismatch")

    selected_contracts = _selected_contracts(contract_selection)
    by_symbol = {item["raw_symbol"]: item for item in selected_contracts if item["raw_symbol"] in ALLOWED_CONTRACTS}
    ready_contracts = []
    for symbol in ALLOWED_CONTRACTS:
        schemas = outputs_by_symbol.get(symbol, {})
        if set(schemas) != set(REQUIRED_SCHEMAS):
            problems.append(f"{_slug(symbol)}_schema_set_incomplete")
            continue
        if symbol not in by_symbol:
            problems.append(f"{_slug(symbol)}_selection_missing")
            continue
        ready_contracts.append(
            {
                **by_symbol[symbol],
                "schema_files": {
                    schema: {
                        "request_id": schemas[schema].get("request_id"),
                        "csv_path": schemas[schema].get("csv_path"),
                        "start": schemas[schema].get("start"),
                        "end": schemas[schema].get("end"),
                        "manifest_record_count": schemas[schema].get("manifest_record_count"),
                        "manifest_empty": schemas[schema].get("manifest_empty"),
                    }
                    for schema in REQUIRED_SCHEMAS
                },
            }
        )

    if len(set(item.get("symbols") for item in output_files)) != len(ALLOWED_CONTRACTS):
        problems.append("downloaded_symbol_count_not_8")
    if FORBIDDEN_TARGET in outputs_by_symbol:
        problems.append("forbidden_spy_670c_target_downloaded_unexpectedly")

    return {
        "status": "INPUTS_VALIDATED" if not problems else ECONOMIC_REPLAY_BLOCKED,
        "first_blocker": problems[0] if problems else None,
        "problems": problems,
        "manifest_status": manifest.get("status"),
        "download_performed": manifest.get("download_performed"),
        "request_count": manifest.get("request_count"),
        "completed_or_reused_request_count": len(manifest.get("completed_or_reused_request_ids", [])),
        "remaining_request_count": len(manifest.get("remaining_request_ids", [])),
        "completed_or_reused_schemas": sorted(set(item.get("schema") for item in output_files)),
        "schema_file_status": schema_file_status,
        "ready_contracts": ready_contracts,
        "ready_contract_count": len(ready_contracts),
        "allowed_contracts": list(ALLOWED_CONTRACTS),
        "spy_670c_exact_rejection": spy_rejection,
        "definition_requested_or_needed": False,
        "contract_identity_verified": all(
            output.get("contract_identity_validated") is True for output in output_files
        ),
    }


def _evaluate_contract(contract, input_validation, *, source_root):
    rows_by_schema = {
        schema: _read_csv_rows(_repo_path(contract["schema_files"][schema]["csv_path"], source_root))
        for schema in REQUIRED_SCHEMAS
    }
    symbol = contract["raw_symbol"]
    instrument_id = contract["instrument_id"]
    entry_start = _parse_time(contract["schema_files"]["cmbp-1"]["start"])
    entry_end = _parse_time(contract["schema_files"]["cmbp-1"]["end"])
    trigger_at = entry_start
    exit_end = _parse_time(contract["schema_files"]["tcbbo"]["end"])
    quote_candidates = _entry_quote_candidates(
        rows_by_schema["cmbp-1"],
        symbol=symbol,
        instrument_id=instrument_id,
        start=entry_start,
        end=entry_end,
    )
    trade_context = _trade_volume_context(
        rows_by_schema["trades"],
        symbol=symbol,
        instrument_id=instrument_id,
        cutoff=entry_end,
    )
    statistics_status = _statistics_status(
        rows_by_schema["statistics"],
        symbol=symbol,
        instrument_id=instrument_id,
    )
    entry_context = {
        "accepted_window_start": _iso(entry_start),
        "accepted_window_end": _iso(entry_end),
        "window_end_inclusive": False,
        "quotes_considered": len(quote_candidates),
        "first_quote_timestamp": _iso(quote_candidates[0]["time"]) if quote_candidates else None,
        "entry_bid_ask_basis": "ask_plus_0.02_entry_slippage",
        "entry_ask": None,
        "entry_price": None,
    }

    if not quote_candidates:
        return _no_entry_contract_result(
            contract,
            "complete_entry_window_quote_missing",
            entry_context,
            trade_context,
            statistics_status,
        )

    quote_eval = _evaluate_quote(quote_candidates[0], trigger_at)
    entry_context.update(quote_eval["context"])
    if quote_eval["blocker"]:
        return _no_entry_contract_result(
            contract,
            quote_eval["blocker"],
            entry_context,
            trade_context,
            statistics_status,
        )
    if Decimal(trade_context["trade_volume_through_entry_window"]) < cfb_contract_selector.MIN_TRADE_VOLUME:
        return _no_entry_contract_result(
            contract,
            "trade_volume_below_1",
            entry_context,
            trade_context,
            statistics_status,
        )
    if statistics_status["status"] != "OPEN_INTEREST_VALID":
        return _no_entry_contract_result(
            contract,
            statistics_status["first_blocker"],
            entry_context,
            trade_context,
            statistics_status,
        )

    entry_price = quote_candidates[0]["ask"] + cfb_trade_rule_checker.ENTRY_SLIPPAGE_BUFFER
    entry_context["entry_ask"] = _decimal_string(quote_candidates[0]["ask"])
    entry_context["entry_price"] = _decimal_string(entry_price)
    return _entry_exit_contract_result(
        contract=contract,
        entry_quote=quote_candidates[0],
        entry_price=entry_price,
        tcbbo_rows=rows_by_schema["tcbbo"],
        exit_end=exit_end,
        entry_context=entry_context,
        trade_context=trade_context,
        statistics_status=statistics_status,
    )


def _entry_exit_contract_result(
    *,
    contract,
    entry_quote,
    entry_price,
    tcbbo_rows,
    exit_end,
    entry_context,
    trade_context,
    statistics_status,
):
    target = entry_price * (Decimal("1") + cfb_trade_rule_checker.PROFIT_TARGET_PERCENT)
    stop = entry_price * (Decimal("1") + cfb_trade_rule_checker.OPTION_STOP_PERCENT)
    exit_event = _first_exit_event(
        tcbbo_rows,
        symbol=contract["raw_symbol"],
        instrument_id=contract["instrument_id"],
        start=entry_quote["time"],
        end=exit_end,
        target=target,
        stop=stop,
    )
    if exit_event is None:
        return _contract_result(
            contract,
            entry_status=VALID_ENTRY_FOUND,
            exit_status=EXIT_BLOCKED,
            net_pnl_status=ECONOMIC_REPLAY_BLOCKED,
            first_blocker="selected_contract_tcbbo_bid_path_through_exit_boundary",
            entry_context=entry_context,
            trade_context=trade_context,
            statistics_status=statistics_status,
            exit_result={"status": EXIT_BLOCKED, "exit_timestamp": None},
        )

    gross_pnl = exit_event["bid"] - entry_quote["ask"]
    exit_price = exit_event["bid"] - cfb_trade_rule_checker.EXIT_SLIPPAGE_BUFFER
    net_pnl = exit_price - entry_price
    return _contract_result(
        contract,
        entry_status=VALID_ENTRY_FOUND,
        exit_status=EXIT_EVALUATED,
        net_pnl_status=NET_PNL_EVALUATED,
        first_blocker=None,
        entry_context=entry_context,
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


def _no_entry_contract_result(contract, blocker, entry_context, trade_context, statistics_status):
    return _contract_result(
        contract,
        entry_status=NO_ENTRY_EXACT_REJECTION,
        exit_status=EXIT_BLOCKED,
        net_pnl_status=ECONOMIC_REPLAY_BLOCKED,
        first_blocker=blocker,
        entry_context=entry_context,
        trade_context=trade_context,
        statistics_status=statistics_status,
        exit_result={"status": EXIT_BLOCKED, "exit_timestamp": None},
    )


def _blocked_contract_result(symbol, blocker):
    return {
        "raw_symbol": symbol,
        "entry_status": ECONOMIC_REPLAY_BLOCKED,
        "entry_timestamp": None,
        "exit_status": EXIT_BLOCKED,
        "net_pnl_status": ECONOMIC_REPLAY_BLOCKED,
        "gross_pnl": None,
        "net_pnl": None,
        "first_blocker": blocker,
        "profitability_status": "NO",
        "paper_live_eligibility": "NO",
    }


def _contract_result(
    contract,
    *,
    entry_status,
    exit_status,
    net_pnl_status,
    first_blocker,
    entry_context,
    trade_context,
    statistics_status,
    exit_result,
    pnl_result=None,
):
    return {
        "candidate_ids": contract.get("candidate_ids", []),
        "legs": contract.get("legs", []),
        "raw_symbol": contract["raw_symbol"],
        "instrument_id": contract["instrument_id"],
        "expiration": contract.get("expiration"),
        "strike": contract.get("strike"),
        "side": "call",
        "schema_files": contract["schema_files"],
        "entry_status": entry_status,
        "entry_timestamp": entry_context.get("quote_timestamp") if entry_status == VALID_ENTRY_FOUND else None,
        "entry_bid_ask_basis": entry_context.get("entry_bid_ask_basis"),
        "entry_price": entry_context.get("entry_price"),
        "quote_age": entry_context.get("quote_age_seconds"),
        "spread": entry_context.get("spread"),
        "spread_percent": entry_context.get("spread_percent"),
        "entry_context": entry_context,
        "trade_volume_context": trade_context,
        "statistics_open_interest_status": statistics_status,
        "exit_status": exit_status,
        "exit_result": exit_result,
        "gross_pnl": (pnl_result or {}).get("gross_pnl"),
        "net_pnl_status": net_pnl_status,
        "net_pnl": (pnl_result or {}).get("net_pnl"),
        "pnl_result": pnl_result,
        "first_blocker": first_blocker,
        "profitability_status": "NO",
        "paper_live_eligibility": "NO",
    }


def _statistics_status(rows, *, symbol, instrument_id):
    matching = [_normalized_row(row) for row in rows if _identity_matches(row, symbol, instrument_id)]
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


def _entry_quote_candidates(rows, *, symbol, instrument_id, start, end):
    candidates = []
    for raw_row in rows:
        if not _identity_matches(raw_row, symbol, instrument_id):
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


def _trade_volume_context(rows, *, symbol, instrument_id, cutoff):
    selected = []
    for raw_row in rows:
        if not _identity_matches(raw_row, symbol, instrument_id):
            continue
        row = _normalized_row(raw_row)
        event_time = _parse_time(row["ts_event"])
        if event_time <= cutoff:
            selected.append((event_time, _decimal_or_none(row.get("size")) or Decimal("0")))
    total = sum((size for _, size in selected), Decimal("0"))
    return {
        "status": "TRADE_VOLUME_VALID" if total >= cfb_contract_selector.MIN_TRADE_VOLUME else "TRADE_VOLUME_INVALID",
        "trade_count_through_entry_window": len(selected),
        "trade_volume_through_entry_window": _decimal_string(total),
        "first_trade_timestamp": _iso(selected[0][0]) if selected else None,
        "minimum_trade_volume": str(cfb_contract_selector.MIN_TRADE_VOLUME),
    }


def _first_exit_event(rows, *, symbol, instrument_id, start, end, target, stop):
    events = []
    for raw_row in rows:
        if not _identity_matches(raw_row, symbol, instrument_id):
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
    time_exit = _latest_quote_at_or_before(rows, symbol=symbol, instrument_id=instrument_id, cutoff=end)
    if time_exit is not None:
        events.append({**time_exit, "reason": "time_exit_boundary"})
    return min(events, key=lambda item: item["time"]) if events else None


def _latest_quote_at_or_before(rows, *, symbol, instrument_id, cutoff):
    latest = None
    for raw_row in rows:
        if not _identity_matches(raw_row, symbol, instrument_id):
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


def _selected_contracts(contract_selection):
    by_symbol = {}
    for candidate in contract_selection.get("candidates", []):
        for leg in ("long_contract", "short_contract"):
            contract = candidate.get(leg) or {}
            symbol = contract.get("raw_symbol")
            if not symbol:
                continue
            item = by_symbol.setdefault(
                symbol,
                {
                    "raw_symbol": symbol,
                    "instrument_id": _int_or_none(contract.get("instrument_id")),
                    "expiration": _date_only(contract.get("expiration")),
                    "strike": str(contract.get("strike")) if contract.get("strike") is not None else None,
                    "candidate_ids": [],
                    "legs": [],
                },
            )
            if candidate.get("candidate_id") not in item["candidate_ids"]:
                item["candidate_ids"].append(candidate.get("candidate_id"))
            leg_name = leg.replace("_contract", "")
            if leg_name not in item["legs"]:
                item["legs"].append(leg_name)
            if item["instrument_id"] is None:
                item["instrument_id"] = _int_or_none(contract.get("instrument_id"))
            if item["expiration"] is None:
                item["expiration"] = _date_only(contract.get("expiration"))
            if item["strike"] is None and contract.get("strike") is not None:
                item["strike"] = str(contract.get("strike"))
    return list(by_symbol.values())


def _spy_670c_rejection_status(result):
    evaluation = result.get("evaluation", {})
    input_validation = result.get("input_validation", {})
    preserved = (
        result.get("selected_contract", {}).get("raw_symbol") == FORBIDDEN_TARGET
        and input_validation.get("target_contract_in_manifest") is False
        and evaluation.get("entry_status") == NO_ENTRY_EXACT_REJECTION
        and evaluation.get("first_blocker") == FORBIDDEN_TARGET_BLOCKER
        and evaluation.get("gross_pnl") is None
        and evaluation.get("net_pnl") is None
    )
    return {
        "preserved": preserved,
        "raw_symbol": result.get("selected_contract", {}).get("raw_symbol"),
        "target_contract_in_manifest": input_validation.get("target_contract_in_manifest"),
        "entry_status": evaluation.get("entry_status"),
        "first_blocker": evaluation.get("first_blocker"),
        "gross_pnl": evaluation.get("gross_pnl"),
        "net_pnl": evaluation.get("net_pnl"),
    }


def _next_action(contract_results):
    if any(item["entry_status"] == VALID_ENTRY_FOUND for item in contract_results):
        return "Review valid entry/exit/P&L replay rows; do not claim paper/live eligibility."
    blockers = sorted({item.get("first_blocker") for item in contract_results if item.get("first_blocker")})
    return "No ready downloaded contract produced a valid entry; blockers: " + ", ".join(blockers)


def _markdown(document):
    summary = document["summary"]
    lines = [
        "# SAFE-FAST Day 55 Ready Downloaded Contracts Replay Result",
        "",
        "## Decision",
        "",
        f"- Ready downloaded contracts evaluated: `{summary['ready_contracts_evaluated']}`.",
        f"- Valid entries: `{summary['valid_entries']}`.",
        f"- Evaluated exits: `{summary['evaluated_exits']}`.",
        f"- Net P&L results: `{summary['net_pnl_results']}`.",
        f"- Exact no-entry rejections: `{summary['exact_no_entry_rejections']}`.",
        f"- Profitability proof: `{summary['profitability_proof']}`.",
        f"- Paper/live eligibility: `{summary['paper_live_eligibility']}`.",
        "",
        "## Preserved SPY 670C Rejection",
        "",
        f"- Contract: `{FORBIDDEN_TARGET}`.",
        f"- Preserved: `{document['baseline']['preserved_spy_670c_rejection']['preserved']}`.",
        f"- First blocker: `{document['baseline']['preserved_spy_670c_rejection']['first_blocker']}`.",
        "",
        "## Contract Results",
        "",
    ]
    for result in document["contract_results"]:
        lines.extend(
            [
                f"- `{result['raw_symbol']}`: entry `{result['entry_status']}`, "
                f"exit `{result['exit_status']}`, gross P&L `{result['gross_pnl']}`, "
                f"net P&L `{result['net_pnl']}`, first blocker `{result['first_blocker']}`.",
            ]
        )
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "Local downloaded Day 55 Databento files only. No vendor download, definition request, Schwab, Railway/deploy, live backend, credential, `.env`, `main.py`, sizing, commit, profitability claim, or paper/live eligibility change was made.",
        ]
    )
    return "\n".join(lines) + "\n"


def _read_csv_rows(path):
    if not Path(path).exists():
        raise Day55ReadyReplayError(f"missing schema csv: {path}")
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


def _vendor_request(request):
    return {
        "dataset": request.get("dataset"),
        "schema": request.get("schema"),
        "start": request.get("start"),
        "end": request.get("end"),
        "stype_in": request.get("stype_in"),
        "symbols": request.get("symbols"),
    }


def _identity_matches(row, symbol, instrument_id):
    try:
        row_instrument_id = int(row.get("instrument_id"))
    except (TypeError, ValueError):
        return False
    row_symbol = row.get("symbol") or row.get("raw_symbol")
    return str(row_symbol or "").strip() == symbol.strip() and row_instrument_id == instrument_id


def _normalized_row(row):
    return {key: (value.strip() if isinstance(value, str) else value) for key, value in row.items()}


def _load_json(path, missing_blocker):
    path = Path(path)
    if not path.exists():
        raise Day55ReadyReplayError(missing_blocker)
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


def _date_only(value):
    if value is None:
        return None
    return str(value).split("T", 1)[0]


def _int_or_none(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _iso(value):
    return value.isoformat().replace("+00:00", "Z")


def _relative(path):
    try:
        return str(Path(path).resolve().relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _slug(value):
    return "".join(ch.lower() for ch in str(value) if ch.isalnum())


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


if __name__ == "__main__":
    doc = write_outputs()
    print(
        "wrote day55 ready downloaded contracts replay: "
        f"valid_entries={doc['summary']['valid_entries']} "
        f"exact_no_entry_rejections={doc['summary']['exact_no_entry_rejections']}"
    )
