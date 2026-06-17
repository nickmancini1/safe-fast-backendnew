# SAFE-FAST Day 46 first CFB backtest run task

Baseline:
- Latest commit before this task: a8acf13 Add CFB backtest prep harness

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.
- Then read SAFE_FAST_DAY45_CFB_EXACT_TRADE_RULE_VALUES.md.
- Then read SAFE_FAST_DAY45_CFB_BACKTEST_PREP_READINESS_REVIEW.md.
- Then read historical_signal_replay/cfb_trade_rule_checker.py.
- Then read historical_signal_replay/cfb_backtest_prep_harness.py.

Goal:
- Run the first actual Clean Fast Break backtest path.
- Use SPY CFB 002 as the first reference case.
- Use SPY CFB 003 and QQQ CFB 001 as rejection controls.
- Keep this grouped.
- Use existing local data only.
- Do not download more Databento data.
- Do not touch live trading, broker/order/account, Railway, main.py, or secrets.

Candidates:
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002 = first reference case
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003 = quote-after-signal rejection control
- QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001 = stale-quote rejection control

Accepted CFB trade rules:
- Long call only.
- Entry uses ask + 0.02.
- Exit uses bid - 0.02.
- Profit target: +25% option premium from entry.
- Stop: -15% option premium from entry.
- Setup invalidation stop applies when source-backed.
- Time exit: 15:45 ET on signal day.
- Named failure reason required.
- Sample-size gate: no promotion from fewer than 20 valid completed CFB examples.
- Promotion requires positive expectancy review after costs.

Task:
1. Create:
   - SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_REVIEW.md

2. Implement or extend a local CFB backtest runner if needed:
   - historical_signal_replay/cfb_backtest_runner.py

3. Add tests:
   - tests/test_cfb_backtest_runner.py

4. The runner must:
   - load one prepared candidate row
   - apply the accepted CFB trade rules
   - reject SPY CFB 003 because quote is after signal
   - reject QQQ CFB 001 because quote is too old
   - process SPY CFB 002 as the first reference case if required data exists
   - apply entry, target, stop, invalidation, and time exit rules
   - include costs/slippage exactly as accepted
   - produce a named result and named failure reason
   - produce a local review output, not a promotion decision

5. If SPY CFB 002 lacks required exit-path data, do not guess.
   - Record exact missing field.
   - Say whether starter data is enough or whether full-window data is required.
   - Include exact cost-check request needed before any full-window download.

6. Create or update local result artifact:
   - SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_RESULT.md

7. Update:
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_BUILD_STATE.md
   - the three CFB candidate packets

8. Run:
   - python -m unittest tests.test_cfb_trade_rule_checker
   - python -m unittest tests.test_cfb_backtest_runner
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
   - content validator if safe/local
   - bridge if safe/local

Allowed writes:
- SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_CODEX_TASK.md
- SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_REVIEW.md
- SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_RESULT.md
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
