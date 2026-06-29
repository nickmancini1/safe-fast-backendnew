# SAFE_FAST_DAY55_OPTION_EVIDENCE_ENTRY_EXIT_PNL_REPLAY_TASK

Read .\SAFE_FAST_BUILD_STATE.md first.

Objective:
Use the approved/downloaded Day 55 quote/trade/statistics option evidence to rerun SPY 670C entry/exit/P&L evaluation.

Source manifest:
historical_signal_replay/source_data/external_option_data_drop/day55_quote_trade_statistics_selected_contracts/day55_quote_trade_statistics_download_manifest.json

Inputs:
- historical_signal_replay/results/day55_definition_contract_selection_for_replay_ready_candidates.json
- historical_signal_replay/results/day55_quote_trade_statistics_cost_check_for_selected_contracts.json
- historical_signal_replay/results/day55_spy_670c_entry_exit_pnl_evaluation.json

Requirements:
- Validate downloaded cmbp-1, tcbbo, trades, statistics evidence before using it.
- Close the old blocker open_interest_statistics_zero_rows only if raw statistics evidence proves it closed.
- Produce either valid entry/exit/P&L or exact rejection with blocker.
- Preserve profitability proof NO and paper/live eligibility NO unless replay evidence proves otherwise.
- No Schwab, Railway, broker, account, order, fill, .env, or live trading.
- Do not commit.

Required output:
- updated machine result JSON
- updated short result markdown
- validator/test coverage
- Codex report: Baseline / Fixed / Blocked / Next / Tests / Files changed / Commit proof

Required checks:
- focused entry/exit/P&L test
- download manifest validator
- cost check validator
- affected Day 55 regressions
- replay safe checks
- git diff --check
