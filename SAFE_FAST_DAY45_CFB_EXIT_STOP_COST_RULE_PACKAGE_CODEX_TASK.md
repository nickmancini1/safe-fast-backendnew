# SAFE-FAST Day 45 CFB exit stop cost rule package task

Baseline:
- Latest commit before this task: bd98b8b Add grouped CFB trade rule checker

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.
- Then read SAFE_FAST_DAY45_CFB_GROUPED_TRADE_RULE_PACKAGE.md.
- Then read SAFE_FAST_DAY45_CFB_BACKTEST_PREP_READINESS_REVIEW.md.

Goal:
- Define the remaining Clean Fast Break trade-plan rules in one grouped package.
- Keep batching.
- Do not download data.
- Do not backtest yet.
- Do not calculate P&L yet.
- Do not mark any candidate ready.

Reference candidates:
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003
- QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001

Known state:
- SPY CFB 002 has usable entry evidence but lacks exit/stop/cost/sample/promotion rules.
- SPY CFB 003 is a no-trade/repair reference because quote came after signal.
- QQQ CFB 001 is a no-trade/repair reference because quote was too old.

Task:
1. Create:
   - SAFE_FAST_DAY45_CFB_EXIT_STOP_COST_RULE_PACKAGE.md

2. Define first conservative CFB rules for:
   - exit
   - stop/invalidation
   - time exit
   - cost/slippage
   - failure diagnosis
   - sample size
   - promotion

3. For each rule, classify:
   - accepted for first regression pass
   - still needs human decision
   - blocked by data
   - blocked by tests

4. Create:
   - historical_signal_replay/fixtures/cfb_exit_stop_cost_regression_fixtures.json

5. Fixtures must cover:
   - SPY CFB 002 usable-entry case still blocked until exit/stop/cost are accepted
   - SPY CFB 003 quote-after-signal no-trade case
   - QQQ CFB 001 stale-quote no-trade case
   - missing exit rule
   - missing stop rule
   - missing cost/slippage rule
   - missing sample-size rule
   - missing promotion rule
   - named failure diagnosis required

6. Create:
   - SAFE_FAST_DAY45_CFB_BACKTEST_GATE_DECISION.md

7. The backtest gate decision must say in plain English:
   - whether SPY CFB 002 can enter backtest prep after these rules
   - what still blocks it
   - what can be tested with cheap starter data
   - whether full-window data is needed now or deferred

8. Create:
   - SAFE_FAST_DAY45_CFB_NEXT_GROUPED_BUILD_TASK.md

9. Update:
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_BUILD_STATE.md
   - the three CFB candidate packets

10. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
   - python -m unittest tests.test_cfb_trade_rule_checker
   - content validator if safe/local
   - bridge if safe/local

Allowed writes:
- SAFE_FAST_DAY45_CFB_EXIT_STOP_COST_RULE_PACKAGE_CODEX_TASK.md
- SAFE_FAST_DAY45_CFB_EXIT_STOP_COST_RULE_PACKAGE.md
- SAFE_FAST_DAY45_CFB_BACKTEST_GATE_DECISION.md
- SAFE_FAST_DAY45_CFB_NEXT_GROUPED_BUILD_TASK.md
- historical_signal_replay/fixtures/cfb_exit_stop_cost_regression_fixtures.json
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_BUILD_STATE.md
- historical_signal_replay/candidate_packets/

Excluded writes:
- raw Databento files
- evidence fills
- backtest code
- P&L
- main.py
- live/engine/broker/order/account/Railway files
- .env or secrets

Final response:
Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:
