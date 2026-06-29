# SAFE_FAST_DAY55_APPROVED_QUOTE_TRADE_STATISTICS_DOWNLOAD_TASK

Read .\SAFE_FAST_BUILD_STATE.md first.

Objective:
Create the approved Day 55 Databento quote/trade/statistics evidence download step from:
historical_signal_replay/results/day55_quote_trade_statistics_cost_check_for_selected_contracts.json

Approval:
- Operator approved grouped cost 0.054846107958 USD.
- Download is allowed only for the exact 32 cost-checked requests.
- No definition schema.
- No Schwab, Railway, broker, account, order, fill, .env, or live trading.
- Preserve profitability proof NO and paper/live eligibility NO.
- Do not claim entry, exit, gross P&L, or net P&L.

Use existing repo download patterns, especially:
scripts/safe_fast_day52_spy_670c_databento_download.py

Output:
- downloader script
- download manifest under source_data/external_option_data_drop
- validator/test coverage
- short result markdown
- do not commit

Required checks:
- focused new test
- manifest validator
- existing cost-check validator
- existing cost-request validator
- git diff --check
