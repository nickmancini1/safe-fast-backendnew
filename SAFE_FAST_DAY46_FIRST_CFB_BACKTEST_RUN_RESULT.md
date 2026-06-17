# SAFE-FAST Day 46 First CFB Backtest Run Result

## Result

The first CFB local runner result is blocker-preserving:

- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`: `blocked_missing_exit_path_data`.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`: `no_trade_quote_after_signal`.
- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`: `no_trade_quote_age_above_5_minutes`.

## SPY CFB 002 Output

```text
result_status: blocked_missing_exit_path_data
failure_reason: selected_contract_tcbbo_bid_path_through_1545_et
entry_fill_basis: ask_plus_slippage
cost_adjusted_entry_basis: 6.37
profit_target_adjusted_exit_threshold: 7.9625
option_stop_adjusted_exit_threshold: 5.4145
missing_fields:
  - selected_contract_tcbbo_bid_path_through_1545_et
  - source_backed_underlying_invalidation_path_through_1545_et
starter_data_enough: false
full_window_data_required: true
```

## Controls

```text
SPY CFB 003: no_trade, quote_after_signal
QQQ CFB 001: no_trade, quote_age_above_5_minutes
```

## Cost Check Needed

Before any full-window download, run a cost check for selected-contract SPY OPRA TCBBO coverage:

```text
Dataset: Databento OPRA.PILLAR
Schema: TCBBO
Contract: SPY   260427C00685000
Instrument id: 1258293281
Window: 2026-04-13T16:30:00Z through 2026-04-13T19:45:00Z
Additional coverage: source-backed underlying invalidation path through 15:45 ET
```

## Tests

- `python -m unittest tests.test_cfb_trade_rule_checker`: PASS, `20` tests.
- `python -m unittest tests.test_cfb_backtest_runner`: PASS, `6` tests.
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`: PASS, `3` checks.
- `python -m watcher_foundation.source_evidence_work_package_content_validator`: PASS, `9` passed requests, `0` failed requests, intake-ready `0`.
- `python -m watcher_foundation.source_evidence_package_to_intake_bridge`: PASS, `4` reconsideration-eligible candidates, intake-ready `0`, proof allowed `NO`.

## Non-Goals Preserved

- No P&L calculated.
- No proof accepted.
- No profitability claimed.
- No promotion decision made.
- No candidate marked ready.
- No intake-ready count changed.
- No raw Databento files changed.
- No Databento data downloaded.
