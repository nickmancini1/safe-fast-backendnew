# SAFE_FAST_DAY55_QUOTE_TRADE_STATISTICS_COST_CHECK_TASK

Read .\SAFE_FAST_BUILD_STATE.md first.

Objective:
Create the Day 55 quote/trade/statistics vendor cost-only checker for:
historical_signal_replay/results/day55_quote_trade_statistics_cost_request_for_selected_contracts.json

Use existing repo patterns from:
scripts/safe_fast_day55_definition_cost_check.py
scripts/safe_fast_day52_existing_setup_databento_cost_request.py

Requirements:
- metadata.get_cost only
- no download
- no definition schema
- preserve profitability proof NO and paper/live eligibility NO
- output machine JSON under historical_signal_replay/results/
- output short markdown review
- add validator/test coverage
- do not commit

Run:
- focused new test
- validator
- existing quote/trade/statistics request validator
- git diff --check
