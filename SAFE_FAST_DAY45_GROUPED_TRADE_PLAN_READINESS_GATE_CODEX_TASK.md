# SAFE-FAST Day 45 grouped trade-plan readiness gate task

Baseline:
- Latest commit before this task: 55bb4c5 Add Day 45 bounded final sprint control update

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.
- Then read SAFE_FAST_DAY45_BOUNDED_FINAL_SPRINT_UPDATE.md.
- Then read SAFE_FAST_DAY45_200_TO_20_TIER_TRANSITION_PLAN.md.
- Then read SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md.

Goal:
- Run one grouped readiness gate across the current candidate set.
- Plain English output.
- Batch mode only.
- Find exactly what trade-plan rules are still missing before backtest work.
- Prepare the final high-intensity sprint decision path.

Candidates to check:
- QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003
- SPY-REAL-HISTORICAL-IDEAL-001
- QQQ-REAL-HISTORICAL-CONTINUATION-001
- QQQ-REAL-HISTORICAL-IDEAL-001
- SPY-REAL-HISTORICAL-CONTINUATION-001

Task:
1. Create:
   - SAFE_FAST_DAY45_GROUPED_TRADE_PLAN_READINESS_GATE.md

2. Re-run or inspect the content validator and bridge.

3. For each candidate, write a plain-English status:
   - usable data state
   - evidence state
   - setup state
   - option/quote state
   - execution state
   - current blocker
   - whether it belongs in the first backtest batch, repair batch, or parking list

4. Create:
   - SAFE_FAST_DAY45_CANDIDATE_COMPARISON_TABLE.md

5. Compare candidates by setup family:
   - Clean Fast Break
   - Ideal
   - Continuation

6. Create:
   - SAFE_FAST_DAY45_TRADE_RULE_GAP_PACKAGE.md

7. The trade-rule gap package must cover:
   - entry rule
   - selected contract rule
   - fill price rule
   - exit rule
   - stop/invalidation rule
   - time exit rule
   - spread/cost/slippage rule
   - failure diagnosis rule
   - sample-size rule
   - promotion rule

8. Create:
   - SAFE_FAST_DAY45_NEXT_GROUPED_BUILD_TASK.md

9. The next grouped task must choose the best batch path:
   - trade-rule package
   - backtest-prep harness
   - candidate comparison expansion
   - full-window data approval package
   - or setup-family repair package

10. Update:
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_BUILD_STATE.md
   - relevant candidate packets

11. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
   - content validator if safe/local
   - bridge if safe/local

Allowed writes:
- SAFE_FAST_DAY45_GROUPED_TRADE_PLAN_READINESS_GATE_CODEX_TASK.md
- SAFE_FAST_DAY45_GROUPED_TRADE_PLAN_READINESS_GATE.md
- SAFE_FAST_DAY45_CANDIDATE_COMPARISON_TABLE.md
- SAFE_FAST_DAY45_TRADE_RULE_GAP_PACKAGE.md
- SAFE_FAST_DAY45_NEXT_GROUPED_BUILD_TASK.md
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
