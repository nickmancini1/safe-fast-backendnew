# SAFE-FAST Day 46 first backtest review and expansion plan task

Baseline:
- Latest commit before this task: 59b2a03 Run first CFB backtest reference case

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.
- Then read SAFE_FAST_DAY45_BOUNDED_FINAL_SPRINT_UPDATE.md.
- Then read SAFE_FAST_DAY45_200_TO_20_TIER_TRANSITION_PLAN.md.
- Then read SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_WITH_EXIT_PATH_REVIEW.md.
- Then read SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_WITH_EXIT_PATH_RESULT.md.

Goal:
- Review the first actual CFB backtest result in plain English.
- Do not overreact to one good example.
- Build the next grouped expansion plan.
- Keep batching.
- Do not download more data.
- Do not calculate new P&L beyond summarizing the already completed result.
- Do not claim proof or profitability.
- Do not mark any candidate ready.

Known first backtest result:
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002 completed profit target.
- Entry: 6.37.
- Adjusted exit: 7.98.
- Adjusted result: +1.61.
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003 remained no-trade because quote was after signal.
- QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001 remained no-trade because quote was too old.

Task:
1. Create:
   - SAFE_FAST_DAY46_FIRST_BACKTEST_REVIEW_AND_EXPANSION_PLAN.md

2. In plain English, state:
   - what this result means
   - what it does not prove
   - what worked
   - what still needs comparison
   - what the next grouped batch should test

3. Create:
   - SAFE_FAST_DAY46_CANDIDATE_EXPANSION_PRIORITY_TABLE.md

4. The table must rank the next grouped work:
   - more Clean Fast Break examples
   - Ideal examples
   - Continuation examples
   - repair/no-trade examples
   - data-needed examples

5. Create:
   - SAFE_FAST_DAY46_NEXT_GROUPED_BACKTEST_BATCH_TASK.md

6. The next task must be grouped and must avoid one-example grinding.
   It should define the next batch using:
   - SPY CFB 002 as positive reference
   - SPY CFB 003 as no-trade control
   - QQQ CFB 001 as stale-quote control
   - SPY Ideal 001 as next setup-family comparison candidate if ready enough
   - Continuation candidates only if their rule/data state supports it

7. Update:
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_BUILD_STATE.md
   - relevant candidate packets

8. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
   - content validator if safe/local
   - bridge if safe/local

Allowed writes:
- SAFE_FAST_DAY46_FIRST_BACKTEST_REVIEW_AND_EXPANSION_PLAN_CODEX_TASK.md
- SAFE_FAST_DAY46_FIRST_BACKTEST_REVIEW_AND_EXPANSION_PLAN.md
- SAFE_FAST_DAY46_CANDIDATE_EXPANSION_PRIORITY_TABLE.md
- SAFE_FAST_DAY46_NEXT_GROUPED_BACKTEST_BATCH_TASK.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_BUILD_STATE.md
- historical_signal_replay/candidate_packets/

Excluded writes:
- raw Databento files
- backtest code
- P&L beyond summarizing existing result
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
