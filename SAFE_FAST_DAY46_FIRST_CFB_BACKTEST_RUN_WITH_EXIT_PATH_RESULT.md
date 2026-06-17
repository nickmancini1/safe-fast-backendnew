# SAFE-FAST Day 46 First CFB Backtest Run With Exit Path Result

## Result

The first CFB local runner result with the new selected-contract exit-path data is:

- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`: `completed_review_only`, `completed_profit_target`.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`: `no_trade_quote_after_signal`.
- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`: `no_trade_quote_age_above_5_minutes`.

## SPY CFB 002 Output

```text
result_status: completed_review_only
result_name: completed_profit_target
entry_time: 2026-04-13T16:30:00+00:00
entry_quote_time: 2026-04-13T16:29:04.514819+00:00
entry_ask: 6.35
entry_fill_basis: ask_plus_slippage
cost_adjusted_entry_basis: 6.37
profit_target_adjusted_exit_threshold: 7.9625
option_stop_adjusted_exit_threshold: 5.4145
exit_time: 2026-04-13T19:37:14.335714+00:00
exit_reason: profit_target
exit_bid: 8.00
exit_fill_basis: bid_minus_slippage
cost_adjusted_exit_basis: 7.98
gross_result: +1.65
cost_slippage_adjusted_result: +1.61
missing_fields: []
```

## Controls

```text
SPY CFB 003: no_trade, quote_after_signal
QQQ CFB 001: no_trade, quote_age_above_5_minutes
```

## Non-Goals Preserved

- No data was downloaded.
- No raw Databento file was changed.
- No proof was accepted.
- No profitability was claimed.
- No promotion decision was made.
- No candidate was marked ready.
- No intake-ready count changed.
- No live trading, broker/order/account, Railway, `main.py`, `.env`, or secrets files were changed.
