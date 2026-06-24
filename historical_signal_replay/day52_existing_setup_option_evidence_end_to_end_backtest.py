import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from historical_signal_replay import cfb_contract_selector
from historical_signal_replay import cfb_trade_rule_checker


REPO_ROOT = Path(__file__).resolve().parents[1]
DAY52_RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day52_family_numeric_binding_and_promotion.json"
)
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day52_existing_setup_option_evidence_end_to_end_backtest.json"
)
RESULT_DOC_PATH = (
    REPO_ROOT
    / "SAFE_FAST_EXISTING_SETUP_OPTION_EVIDENCE_END_TO_END_BACKTEST_RESULT.md"
)
OPTION_DATA_DIR = (
    REPO_ROOT / "historical_signal_replay" / "source_data" / "external_option_data_drop"
)
OPERATOR_SCRIPT_PATH = (
    REPO_ROOT / "scripts" / "safe_fast_day52_existing_setup_databento_cost_request.py"
)

RESULT_VERSION = "day52_existing_setup_option_evidence_end_to_end_backtest_v1"
TASK_FILENAME = "SAFE_FAST_EXISTING_SETUP_OPTION_EVIDENCE_END_TO_END_BACKTEST_CODEX_TASK.md"
SELECTED_WINNER_ID = "DAY52-SPY-2026-03-16-CLEAN-FAST-BREAK-20260316T133000Z-P39"
SELECTED_FAMILY = "Clean Fast Break"
SYMBOL = "SPY"
SETUP_TIMESTAMP_UTC = "2026-03-16T13:30:00Z"
TRIGGER_TIMESTAMP_UTC = "2026-03-16T13:31:00Z"
SETUP_TIMESTAMP_ET = "2026-03-16T09:30:00-04:00"
TRIGGER_TIMESTAMP_ET = "2026-03-16T09:31:00-04:00"
TRIGGER_NUMERIC = "668.360000000"
INVALIDATION_NUMERIC = "667.870000000"
EXPIRATION = "2026-03-30"
STRIKE = "669"
CALL_OR_PUT = "C"
VENDOR_SYMBOL = "SPY   260330C00669000"
ENTRY_WINDOW_START_UTC = "2026-03-16T13:31:00Z"
ENTRY_WINDOW_END_UTC = "2026-03-16T13:36:00Z"
EXIT_WINDOW_END_UTC = "2026-03-16T19:45:00Z"


def build_document(*, source_commit=None, run_timestamp=None):
    run_timestamp = run_timestamp or _utc_now()
    local_evidence = _local_evidence_inventory()
    selected_winner = _selected_winner()
    contract_selection = _contract_selection_result(local_evidence)
    timing_rule = _timing_rule()
    entry_window = _entry_window_result(local_evidence, timing_rule)
    tastytrade = _tastytrade_result()
    databento = _databento_result()
    replay = _replay_result(contract_selection, entry_window)
    exact_request = _exact_evidence_request(contract_selection, timing_rule, databento)

    return {
        "result_version": RESULT_VERSION,
        "task": TASK_FILENAME,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp,
        "scope": {
            "symbol": SYMBOL,
            "session_date": "2026-03-16",
            "selected_duplicate_group_only": True,
            "broad_candidate_hunting": False,
            "provisional_recognition_layer_created": False,
            "main_py_changed": False,
            "railway_or_deploy_changed": False,
            "broker_account_order_alert_touched": False,
            "credentials_or_env_changed": False,
            "sizing_changed": False,
            "paid_data_downloaded": False,
            "schwab_wait_or_oauth": False,
            "profitability_proof": "NO",
            "paper_live_eligibility": "NO",
        },
        "first_required_decision": {
            "selected_winner_id": SELECTED_WINNER_ID,
            "setup_family_used_for_economic_winner": SELECTED_FAMILY,
            "direction": "bullish_long_call",
            "setup_timestamp_utc": SETUP_TIMESTAMP_UTC,
            "trigger_timestamp_utc": TRIGGER_TIMESTAMP_UTC,
            "trigger_numeric": TRIGGER_NUMERIC,
            "invalidation_numeric": INVALIDATION_NUMERIC,
            "selected_contract_rule": _selected_contract_rule(),
            "option_entry_timing_rule": timing_rule,
        },
        "selected_winner": selected_winner,
        "local_evidence": local_evidence,
        "contract_selection_result": contract_selection,
        "complete_entry_window_result": entry_window,
        "tastytrade_result": tastytrade,
        "databento_result": databento,
        "entry_exit_pnl_result": replay,
        "exact_evidence_request": exact_request,
        "stage_reached": replay["stage_reached"],
        "after_funnel_totals": {
            "selected_duplicate_groups_processed": 1,
            "setup_qualified_layer1_records": 3,
            "selected_winner_records": 1,
            "suppressed_duplicate_records": 2,
            "trade_candidates": 0,
            "selected_contracts": 0,
            "eligible_entries": 0,
            "recorded_entries": 0,
            "costed_exits": 0,
            "net_pnl_results": 0,
            "exact_priced_requests": 1,
            "valid_trades_captured": 0,
            "true_no_trades": 0,
            "missing_data_cases": 1,
            "missed_valid_trades": 0,
            "invalid_trades_allowed": 0,
            "unresolved_cases": 0,
        },
        "guardrails": {
            "no_future_price_performance_used_for_contract": True,
            "pre_trigger_price_rejected": True,
            "late_price_rejected": True,
            "stale_quote_rejected": True,
            "spread_liquidity_rejected_when_over_limits": True,
            "duplicate_suppression_preserved": True,
            "strict_no_trade_until_valid_entry": True,
            "network_failure_not_reported_as_market_data_unavailable": True,
            "profitability_claimed": False,
            "paper_eligible": False,
            "live_eligible": False,
        },
    }


def write_outputs(*, source_commit=None, run_timestamp=None):
    document = build_document(source_commit=source_commit, run_timestamp=run_timestamp)
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    RESULT_DOC_PATH.write_text(_markdown(document), encoding="utf-8")
    return document


def _selected_winner():
    source = json.loads(DAY52_RESULT_PATH.read_text(encoding="utf-8"))
    return {
        "source_result": "historical_signal_replay/results/day52_family_numeric_binding_and_promotion.json",
        "winner_selection": source["accepted_mode_full_session_counts"]["winner_selection"],
        "selected_winner_id": SELECTED_WINNER_ID,
        "setup_family": SELECTED_FAMILY,
        "suppressed_family_labels": ["Ideal", "Continuation"],
        "duplicate_group_trade_count": 1,
    }


def _selected_contract_rule():
    return {
        "rule_source": "historical_signal_replay/cfb_contract_selector.py and SAFE_FAST_PROJECT_PROOF_PIPELINE.md Clean Fast Break execution realism rules",
        "side": "long calls only",
        "expiration_rule": "nearest listed expiration with DTE >= 14",
        "strike_rule": "lowest reviewed-universe call strike greater than or equal to trigger",
        "moneyness_rule": "nearest OTM-by-trigger moneyness",
        "quote_rule": "nearest setup-safe quote at or before contract-selection timestamp by ts_event; no future quotes",
        "spread_cap": str(cfb_contract_selector.SPREAD_CAP),
        "spread_percent_cap": str(cfb_contract_selector.SPREAD_PCT_CAP),
        "minimum_bid_size": str(cfb_contract_selector.MIN_BID_SIZE),
        "minimum_ask_size": str(cfb_contract_selector.MIN_ASK_SIZE),
        "minimum_trade_volume": str(cfb_contract_selector.MIN_TRADE_VOLUME),
        "minimum_open_interest": str(cfb_contract_selector.MIN_OPEN_INTEREST),
        "tie_break": "latest ts_event at or before cutoff, earliest ts_recv for same event timestamp",
        "fallback_rule": "no fallback scan after top-ranked contract fails a gate",
    }


def _contract_selection_result(local_evidence):
    attempted = {
        "expiration": EXPIRATION,
        "strike": STRIKE,
        "call_or_put": CALL_OR_PUT,
        "vendor_symbol": VENDOR_SYMBOL,
        "instrument_id": None,
        "selection_inputs_available_by_cutoff": {
            "underlying_symbol": SYMBOL,
            "setup_family": SELECTED_FAMILY,
            "direction": "bullish_long_call",
            "trigger_numeric": TRIGGER_NUMERIC,
            "setup_timestamp_utc": SETUP_TIMESTAMP_UTC,
            "expiration_rule": "nearest DTE >= 14 gives 2026-03-30",
            "strike_rule": "first standard call strike >= 668.360000000 gives 669",
            "definition_evidence": False,
            "setup_safe_quote_evidence": False,
            "trade_volume_evidence": False,
            "open_interest_statistics_evidence": False,
        },
    }
    return {
        "status": "BLOCKED_DEFINITION_EVIDENCE_MISSING",
        "selected_contract": None,
        "deterministic_candidate_if_listed": attempted,
        "rule_used": _selected_contract_rule(),
        "liquidity_checks": {
            "spread": "not_evaluated_definition_and_quote_missing",
            "spread_percent": "not_evaluated_definition_and_quote_missing",
            "bid_size": "not_evaluated_definition_and_quote_missing",
            "ask_size": "not_evaluated_definition_and_quote_missing",
            "trade_volume": "not_evaluated_trades_missing",
            "open_interest": "not_evaluated_statistics_missing",
        },
        "deterministic_tie_break": _selected_contract_rule()["tie_break"],
        "rejection_reason": (
            "local March 16 SPY OPRA definition evidence is absent, so the "
            "candidate raw symbol cannot be confirmed as a listed contract with "
            "instrument_id and setup-safe liquidity"
        ),
        "local_march16_spy_opra_evidence_present": local_evidence[
            "has_march16_spy_opra_evidence"
        ],
    }


def _timing_rule():
    return {
        "rule_source": "historical_signal_replay/cfb_trade_rule_checker.py and historical_signal_replay/cfb_backtest_runner.py",
        "earliest_allowed_option_price": ENTRY_WINDOW_START_UTC,
        "latest_allowed_option_price": ENTRY_WINDOW_END_UTC,
        "trigger_timestamp_utc": TRIGGER_TIMESTAMP_UTC,
        "price_basis": "ask_plus_0.02_entry_slippage",
        "field_used_for_entry": "ask",
        "quote_timestamp_field": "ts_event",
        "receive_timestamp_field": "ts_recv_when_available_for_tie_break_only",
        "maximum_quote_age_seconds_for_clean_entry": 60,
        "maximum_quote_age_seconds_absolute_no_trade": int(
            cfb_trade_rule_checker.STALE_QUOTE_AGE_SECONDS_MAX
        ),
        "spread_requirement": {
            "maximum_spread": str(cfb_contract_selector.SPREAD_CAP),
            "maximum_spread_percent": str(cfb_contract_selector.SPREAD_PCT_CAP),
        },
        "liquidity_requirement": {
            "minimum_bid_size": str(cfb_contract_selector.MIN_BID_SIZE),
            "minimum_ask_size": str(cfb_contract_selector.MIN_ASK_SIZE),
            "minimum_trade_volume": str(cfb_contract_selector.MIN_TRADE_VOLUME),
            "minimum_open_interest": str(cfb_contract_selector.MIN_OPEN_INTEREST),
        },
        "valid_price_rule": (
            "first quote in the complete post-trigger entry window with ts_event "
            "at or after trigger, not older than 60 seconds for clean execution, "
            "ask present and positive, and contract-selection liquidity gates passed"
        ),
        "pre_trigger_price_rejection_reason": "pre_trigger_quote_not_permitted_for_entry",
        "late_price_rejection_reason": "entry_quote_after_latest_allowed_window",
        "stale_quote_rejection_reason": "quote_age_above_clean_entry_limit_or_above_5_minutes",
        "spread_liquidity_rejection_reason": "spread_or_liquidity_gate_failed",
    }


def _entry_window_result(local_evidence, timing_rule):
    return {
        "status": "BLOCKED_COMPLETE_OPTION_PRICE_WINDOW_MISSING",
        "contract": None,
        "window_start_utc": timing_rule["earliest_allowed_option_price"],
        "window_end_utc": timing_rule["latest_allowed_option_price"],
        "updates_inspected": [],
        "first_valid_price": None,
        "invalid_price_rejections": [],
        "rejection_reason": (
            "no local March 16 SPY OPRA quote stream exists for the deterministic "
            "candidate contract; the complete accepted entry window cannot be evaluated"
        ),
        "local_files_considered": local_evidence["candidate_local_files_considered"],
    }


def _tastytrade_result():
    return {
        "status": "FIELD_LIMITATION_BLOCKED",
        "path_checked": "historical_signal_replay/export_dxlink_source_csv.py",
        "result": (
            "existing local tastytrade/dxLink helper is an underlying OHLCV CSV "
            "export path; no repo path proves historical OPRA bid/ask, trades, "
            "statistics, or open-interest payloads for this March 16 option contract"
        ),
        "historical_bid_ask_supplied": False,
        "may_satisfy_entry_rule": False,
    }


def _databento_result():
    return {
        "status": "NETWORK_EXECUTION_BLOCKED",
        "dataset": "OPRA.PILLAR",
        "schemas": ["definition", "cmbp-1", "tcbbo", "trades", "statistics"],
        "cost_check_run_in_sandbox": False,
        "download_run_in_sandbox": False,
        "reason": (
            "network access is restricted for this Codex sandbox and approval policy "
            "does not permit escalating network execution; prior repo evidence also "
            "shows Databento HTTPS proxy refusal in this environment"
        ),
        "operator_script": _relative(OPERATOR_SCRIPT_PATH),
        "operator_command": (
            "python scripts/safe_fast_day52_existing_setup_databento_cost_request.py"
        ),
        "expected_output_file": (
            "historical_signal_replay/results/"
            "day52_existing_setup_databento_cost_request_operator_output.json"
        ),
    }


def _replay_result(contract_selection, entry_window):
    return {
        "stage_reached": "EXACT_EVIDENCE_REQUEST",
        "setup_family": SELECTED_FAMILY,
        "signal_time": SETUP_TIMESTAMP_UTC,
        "trigger_time": TRIGGER_TIMESTAMP_UTC,
        "contract": contract_selection["selected_contract"],
        "accepted_entry_window": {
            "start_utc": ENTRY_WINDOW_START_UTC,
            "end_utc": ENTRY_WINDOW_END_UTC,
        },
        "entry_timestamp": None,
        "entry_price": None,
        "price_basis": "ask_plus_0.02_entry_slippage",
        "quote_age": None,
        "spread": None,
        "invalidation": INVALIDATION_NUMERIC,
        "exit_timestamp": None,
        "exit_price": None,
        "exit_reason": None,
        "holding_duration": None,
        "gross_pnl": None,
        "spread_cost": None,
        "slippage": None,
        "commissions": None,
        "fees": None,
        "net_pnl": None,
        "blocking_stage": (
            contract_selection["status"]
            if contract_selection["selected_contract"] is None
            else entry_window["status"]
        ),
        "smallest_missing_evidence": [
            "Databento OPRA.PILLAR definition evidence confirming SPY 2026-03-30 669C listing and instrument_id",
            "complete selected-contract quote-freshness stream for 2026-03-16T13:31:00Z through 2026-03-16T13:36:00Z",
            "selected-contract trades and statistics/open-interest evidence through setup/entry cutoff",
            "selected-contract bid path and underlying invalidation path through 2026-03-16T19:45:00Z",
            "operator-run Databento cost estimate for the grouped request",
        ],
    }


def _exact_evidence_request(contract_selection, timing_rule, databento):
    return {
        "request_status": "EXACT_PRICED_REQUEST_PENDING_OPERATOR_COST_OUTPUT",
        "selected_contract": contract_selection["deterministic_candidate_if_listed"],
        "dataset": "OPRA.PILLAR",
        "schemas": [
            {
                "schema": "definition",
                "symbols": "SPY",
                "stype_in": "raw_symbol",
                "start": SETUP_TIMESTAMP_UTC,
                "end": "2026-03-16T13:32:00Z",
                "purpose": "confirm listed contract identity, raw symbol, instrument_id, expiration, strike, and right",
            },
            {
                "schema": "cmbp-1",
                "symbols": VENDOR_SYMBOL,
                "stype_in": "raw_symbol",
                "start": ENTRY_WINDOW_START_UTC,
                "end": ENTRY_WINDOW_END_UTC,
                "purpose": "primary quote freshness and complete entry-window bid/ask stream",
            },
            {
                "schema": "tcbbo",
                "symbols": VENDOR_SYMBOL,
                "stype_in": "raw_symbol",
                "start": ENTRY_WINDOW_START_UTC,
                "end": EXIT_WINDOW_END_UTC,
                "purpose": "trade-linked quote context and selected-contract bid path through exit boundary",
            },
            {
                "schema": "trades",
                "symbols": VENDOR_SYMBOL,
                "stype_in": "raw_symbol",
                "start": SETUP_TIMESTAMP_UTC,
                "end": EXIT_WINDOW_END_UTC,
                "purpose": "trade volume and trade context required by the selector",
            },
            {
                "schema": "statistics",
                "symbols": VENDOR_SYMBOL,
                "stype_in": "raw_symbol",
                "start": SETUP_TIMESTAMP_UTC,
                "end": ENTRY_WINDOW_END_UTC,
                "purpose": "open interest/statistics liquidity evidence",
            },
        ],
        "entry_window": {
            "start_utc": timing_rule["earliest_allowed_option_price"],
            "end_utc": timing_rule["latest_allowed_option_price"],
            "must_record_every_update": True,
        },
        "exit_window": {
            "start_utc": ENTRY_WINDOW_START_UTC,
            "end_utc": EXIT_WINDOW_END_UTC,
            "rules": {
                "profit_target": "+25% from cost-adjusted entry basis",
                "option_stop": "-15% from cost-adjusted entry basis",
                "setup_invalidation": INVALIDATION_NUMERIC,
                "time_exit": "15:45 ET",
                "exit_basis": "bid_minus_0.02_exit_slippage",
            },
        },
        "numerical_cost": "PENDING_OPERATOR_COST_OUTPUT",
        "cost_status": databento["status"],
        "exact_stages_unlocked": [
            "contract_definition_confirmation",
            "deterministic_contract_selection",
            "complete_entry_window_validation",
            "eligible_entry_or_exact_no_trade",
            "exit_replay",
            "gross_and_net_pnl_if_entry_exists",
        ],
    }


def _local_evidence_inventory():
    files = []
    if OPTION_DATA_DIR.exists():
        files = [
            _relative(path)
            for path in OPTION_DATA_DIR.rglob("*")
            if path.is_file()
        ]
    march16 = [
        path for path in files
        if "2026-03-16" in path or "20260316" in path or "260316" in path
    ]
    candidate_tokens = ("260330", "00669000", "C00669000")
    candidate_files = [
        path for path in files
        if all(token in path for token in ("SPY",))
        and any(token in path for token in candidate_tokens)
    ]
    return {
        "directory": _relative(OPTION_DATA_DIR),
        "exists": OPTION_DATA_DIR.exists(),
        "file_count": len(files),
        "march16_matching_files": march16,
        "candidate_local_files_considered": candidate_files,
        "has_march16_spy_opra_evidence": bool(march16),
        "has_selected_candidate_contract_evidence": bool(candidate_files),
    }


def _markdown(document):
    contract = document["contract_selection_result"]
    entry = document["complete_entry_window_result"]
    request = document["exact_evidence_request"]
    return f"""# SAFE-FAST Existing-Setup Option Evidence and End-to-End Backtest Result

## Decision

- Selected winner: `{SELECTED_WINNER_ID}`.
- Economic family: `{SELECTED_FAMILY}`.
- Direction: bullish long call.
- Trigger timestamp: `{TRIGGER_TIMESTAMP_UTC}`.
- Accepted trigger: `{TRIGGER_NUMERIC}`.
- Accepted invalidation: `{INVALIDATION_NUMERIC}`.
- Duplicate handling: one economic winner only; Ideal and Continuation remain suppressed.

## Contract Selection

- Status: `{contract['status']}`.
- Deterministic candidate if OPRA definition confirms listing: `{VENDOR_SYMBOL}`; expiration `{EXPIRATION}`; strike `{STRIKE}`; side `{CALL_OR_PUT}`.
- Selected contract: `None`.
- Rejection reason: {contract['rejection_reason']}.

## Entry Window

- Status: `{entry['status']}`.
- Accepted window: `{ENTRY_WINDOW_START_UTC}` through `{ENTRY_WINDOW_END_UTC}`.
- Price basis: ask plus `0.02` entry slippage.
- First valid price: `None`.
- Rejection reason: {entry['rejection_reason']}.

## Vendor Results

- Tastytrade: `{document['tastytrade_result']['status']}`; historical option bid/ask evidence was not proven by the local helper.
- Databento: `{document['databento_result']['status']}`; use operator script `{document['databento_result']['operator_script']}`.
- Expected operator output: `{document['databento_result']['expected_output_file']}`.

## P&L

No entry, exit, or net P&L was recorded. Stage reached: `{document['stage_reached']}`.

## Exact Request

Dataset: `{request['dataset']}`. Schemas: `definition`, `cmbp-1`, `tcbbo`, `trades`, and `statistics`. Numerical cost is `{request['numerical_cost']}` until the operator-run script succeeds.

## Guardrails

No `main.py`, Railway/deploy, production/live backend, broker/account/order/alert code, credentials, `.env`, sizing, paid download, proof, profitability claim, paper eligibility, or live eligibility was changed or created.
"""


def _relative(path):
    return str(Path(path).relative_to(REPO_ROOT)).replace("\\", "/")


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
        "wrote day52 existing setup option evidence result: "
        f"{doc['stage_reached']}, Databento {doc['databento_result']['status']}"
    )
