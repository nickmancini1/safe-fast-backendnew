# SAFE-FAST Day 46 first CFB backtest run with exit-path data

Baseline:
- Latest committed checkpoint: 60f3ef0 Add first CFB backtest runner attempt
- Local raw Databento exit-path files exist and are ignored by git.

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.
- Then read SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_REVIEW.md.
- Then read SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_RESULT.md.
- Then read historical_signal_replay/cfb_backtest_runner.py.

Goal:
- Rerun the first CFB backtest path using the newly downloaded SPY CFB 002 exit-path option data.
- Use SPY CFB 002 as the first reference case.
- Keep SPY CFB 003 and QQQ CFB 001 as rejection controls.
- Use existing local data only.
- Do not download more data.
- Do not touch live trading, broker/order/account, Railway, main.py, or secrets.

New local files:
- historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_002_selected_contract_tcbbo_entry_to_1545_et.csv
- historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_002_selected_contract_trades_entry_to_1545_et.csv
- historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_002_selected_contract_exit_path_manifest.json

Candidate:
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002

Selected contract:
- SPY 260427C00685000
- instrument_id=1258293281

Accepted CFB rules:
- Entry: ask + 0.02
- Exit: bid - 0.02
- Profit target: +25% option premium
- Stop: -15% option premium
- Time exit: 15:45 ET
- Setup invalidation if source-backed
- Named result and named reason required

Task:
1. Confirm the new exit-path files exist.
2. Load the SPY CFB 002 option bid path from entry through 15:45 ET.
3. Run the CFB backtest runner for SPY CFB 002.
4. Keep SPY CFB 003 rejected for quote-after-signal.
5. Keep QQQ CFB 001 rejected for stale quote.
6. Produce a result for SPY CFB 002:
   - entry time
   - entry price
   - target price
   - stop price
   - exit time
   - exit reason
   - exit price
   - gross result
   - cost/slippage-adjusted result
   - named failure/success reason
7. If required data is still missing, stop and name the exact missing field.
8. Create or update:
   - SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_WITH_EXIT_PATH_REVIEW.md
   - SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_WITH_EXIT_PATH_RESULT.md
9. Add or update tests if needed:
   - tests/test_cfb_backtest_runner.py
10. Update:
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_BUILD_STATE.md
   - historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_002.md
   - historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_003.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Run:
- python -m unittest tests.test_cfb_trade_rule_checker
- python -m unittest tests.test_cfb_backtest_runner
- powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
- content validator if safe/local
- bridge if safe/local

Allowed writes:
- SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_WITH_EXIT_PATH_CODEX_TASK.md
- SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_WITH_EXIT_PATH_REVIEW.md
- SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_WITH_EXIT_PATH_RESULT.md
- historical_signal_replay/cfb_backtest_runner.py
- tests/test_cfb_backtest_runner.py
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_BUILD_STATE.md
- historical_signal_replay/candidate_packets/

Excluded writes:
- raw Databento files
- live trading files
- broker/order/account files
- Railway/deploy files
- main.py
- .env or secrets

Final response:
Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:
