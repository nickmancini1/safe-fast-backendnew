# SAFE-FAST Day 45 CFB exact trade-rule values task

Baseline:
- Latest commit before this task: 7728d1e Add CFB exit stop cost rule package

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.
- Then read SAFE_FAST_DAY45_CFB_EXIT_STOP_COST_RULE_PACKAGE.md.
- Then read SAFE_FAST_DAY45_CFB_BACKTEST_GATE_DECISION.md.
- Then read SAFE_FAST_DAY45_CFB_GROUPED_TRADE_RULE_PACKAGE.md.

Goal:
- Set the first exact Clean Fast Break trade-rule values for regression/backtest prep.
- Keep this grouped.
- Do not download data.
- Do not run backtest.
- Do not calculate P&L.
- Do not mark any candidate ready.

Reference candidates:
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003
- QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001

Proposed first-pass conservative values to assess:
- Entry:
  - Long call only.
  - Entry is allowed only when setup, option context, and execution context pass.
  - Entry fill for later backtest uses ask price from the accepted setup-safe quote.
- Exit:
  - First-pass testing uses earliest of profit target, stop, invalidation, or time exit.
  - Profit target: +25% option premium from entry.
- Stop:
  - Hard option premium stop: -15% from entry.
  - Setup invalidation stop also applies if underlying invalidates the setup.
- Time exit:
  - Exit no later than 15:45 ET on the signal day.
- Cost/slippage:
  - Entry uses ask.
  - Exit uses bid.
  - Add .02 per contract slippage buffer on entry and exit for first-pass testing.
  - No zero-cost fills.
- Failure diagnosis:
  - Every no-trade or failed trade must name one primary reason.
- Sample size:
  - First backtest-prep batch can run on the current candidates.
  - No promotion can occur from fewer than 20 valid completed CFB examples.
- Promotion:
  - Promotion requires accepted rules, passing replay/regression, enough valid examples, and a positive expectancy review after costs.
  - One candidate can be a reference case, not a promotion basis.

Task:
1. Create:
   - SAFE_FAST_DAY45_CFB_EXACT_TRADE_RULE_VALUES.md

2. For each proposed value, decide:
   - accepted for first regression pass
   - changed with reason
   - still blocked with exact missing decision

3. Create or update:
   - historical_signal_replay/fixtures/cfb_exit_stop_cost_regression_fixtures.json

4. Fixtures must cover:
   - accepted SPY CFB 002 entry-rule-ready but awaiting later backtest harness
   - SPY CFB 003 no-trade because quote after signal
   - QQQ CFB 001 no-trade because stale quote
   - profit target exit
   - option premium stop
   - setup invalidation stop
   - time exit
   - entry ask rule
   - exit bid rule
   - slippage buffer rule
   - failure reason required
   - sample-size gate
   - promotion gate

5. Create:
   - SAFE_FAST_DAY45_CFB_EXACT_TRADE_RULE_VALUES_REVIEW.md

6. Create:
   - SAFE_FAST_DAY45_CFB_BACKTEST_PREP_IMPLEMENTATION_TASK.md

7. The implementation task should be grouped and should prepare:
   - trade-rule checker updates
   - tests
   - first backtest-prep harness if all required values are accepted
   - no P&L until the harness is explicitly authorized by a later task

8. Update:
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_BUILD_STATE.md
   - relevant CFB candidate packets

9. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
   - python -m unittest tests.test_cfb_trade_rule_checker
   - content validator if safe/local
   - bridge if safe/local

Allowed writes:
- SAFE_FAST_DAY45_CFB_EXACT_TRADE_RULE_VALUES_CODEX_TASK.md
- SAFE_FAST_DAY45_CFB_EXACT_TRADE_RULE_VALUES.md
- SAFE_FAST_DAY45_CFB_EXACT_TRADE_RULE_VALUES_REVIEW.md
- SAFE_FAST_DAY45_CFB_BACKTEST_PREP_IMPLEMENTATION_TASK.md
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
