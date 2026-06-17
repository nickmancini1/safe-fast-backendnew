# SAFE-FAST Day 45 Clean Fast Break grouped trade-rule package task

Baseline:
- Latest commit before this task: eaebc3d Add Day 45 grouped trade plan readiness gate

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.
- Then read SAFE_FAST_DAY45_GROUPED_TRADE_PLAN_READINESS_GATE.md.
- Then read SAFE_FAST_DAY45_CANDIDATE_COMPARISON_TABLE.md.
- Then read SAFE_FAST_DAY45_TRADE_RULE_GAP_PACKAGE.md.
- Then read SAFE_FAST_DAY45_BOUNDED_FINAL_SPRINT_UPDATE.md.

Goal:
- Build one grouped Clean Fast Break trade-rule package.
- Use SPY CFB 002 as the main reference.
- Use SPY CFB 003 as the quote-after-signal repair/no-trade reference.
- Use QQQ CFB 001 as the stale-quote fail reference.
- Keep batching.
- Do not split into one-field tasks.
- Do not download more data.
- Do not run backtest yet.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark any candidate ready.

Reference candidates:
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003
- QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001

Known current routing:
- SPY CFB 002: best first backtest-prep reference after trade rules are accepted.
- SPY CFB 003: repair/no-trade reference because top contract quote was post-signal in starter data.
- QQQ CFB 001: failed-execution reference because selected option quote was too old.

Task:
1. Create:
   - SAFE_FAST_DAY45_CFB_GROUPED_TRADE_RULE_PACKAGE.md

2. Define the first Clean Fast Break trade-plan rule package:
   - entry rule
   - selected-contract use rule
   - fill price rule
   - exit rule
   - stop/invalidation rule
   - time exit rule
   - cost/slippage rule
   - failure diagnosis rule
   - sample-size rule
   - promotion rule

3. For each rule, classify:
   - accepted for first regression pass
   - decision still needed
   - blocked by data
   - blocked by tests

4. Use conservative defaults when supportable:
   - entry can only use setup-time-safe data
   - long call fill basis uses ask price for entry
   - quotes after signal are rejected
   - stale quotes are rejected
   - no fallback contract if top-ranked selected contract fails
   - costs/slippage must be explicit
   - failure reasons must be named, not hidden

5. Create:
   - historical_signal_replay/fixtures/cfb_trade_rule_regression_fixtures.json

6. Fixtures must cover:
   - SPY CFB 002 as first usable reference if accepted rules support it
   - SPY CFB 003 as quote-after-signal rejection
   - QQQ CFB 001 as stale-quote rejection
   - missing selected contract
   - missing entry quote
   - missing exit rule
   - stop/invalidation missing
   - cost/slippage missing
   - failure diagnosis required
   - sample-size gate required
   - promotion gate required

7. Create:
   - SAFE_FAST_DAY45_CFB_BACKTEST_PREP_READINESS_REVIEW.md

8. The review must answer in plain English:
   - which CFB candidate is the first backtest-prep reference
   - which CFB candidates are repair references
   - which trade rules are accepted
   - which trade rules still need decisions
   - what blocks the first CFB backtest batch
   - whether more data is needed now or deferred

9. Create:
   - SAFE_FAST_DAY45_CFB_NEXT_GROUPED_IMPLEMENTATION_TASK.md

10. The next grouped task should be one of:
   - implement CFB trade-rule checker plus tests
   - define missing exit/stop rules
   - prepare first CFB backtest harness
   - build candidate comparison expansion

11. Update:
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_BUILD_STATE.md
   - relevant candidate packets

12. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
   - content validator if safe/local
   - bridge if safe/local

Allowed writes:
- SAFE_FAST_DAY45_CFB_GROUPED_TRADE_RULE_PACKAGE_CODEX_TASK.md
- SAFE_FAST_DAY45_CFB_GROUPED_TRADE_RULE_PACKAGE.md
- SAFE_FAST_DAY45_CFB_BACKTEST_PREP_READINESS_REVIEW.md
- SAFE_FAST_DAY45_CFB_NEXT_GROUPED_IMPLEMENTATION_TASK.md
- historical_signal_replay/fixtures/cfb_trade_rule_regression_fixtures.json
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
