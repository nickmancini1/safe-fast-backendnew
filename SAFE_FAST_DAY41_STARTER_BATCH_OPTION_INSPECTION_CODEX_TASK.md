# SAFE-FAST Day 41 starter batch option inspection task

Baseline:
- Latest commit before this task: 1180d1b Validate cheap starter Databento batch

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.
- Then read SAFE_FAST_DAY41_CHEAP_STARTER_BATCH_VALIDATION.md.
- Then read SAFE_FAST_DAY41_CHEAP_STARTER_BATCH_NEXT_STEPS.md.

Goal:
- Inspect the cheap starter Databento files for all six remaining candidates in one batch.
- Do not download more data.
- Do not use full-window data.
- Do not fill evidence yet.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark any candidate ready.

Candidates:
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003
- SPY-REAL-HISTORICAL-IDEAL-001
- QQQ-REAL-HISTORICAL-CONTINUATION-001
- QQQ-REAL-HISTORICAL-IDEAL-001
- SPY-REAL-HISTORICAL-CONTINUATION-001

Use only local starter files:
- definitions_full_day
- statistics_full_day
- tcbbo_signal_10min
- trades_signal_10min

Task:
1. Create:
   - SAFE_FAST_DAY41_STARTER_BATCH_OPTION_INSPECTION.md

2. For each candidate, inspect starter data and report:
   - whether option definitions exist
   - whether setup-window quotes exist
   - whether setup-window trades exist
   - whether same-contract or usable statistics/open-interest exists
   - quote freshness around signal
   - trade activity around signal
   - whether starter data alone appears enough to continue
   - whether full-window data may be needed later

3. Do not apply QQQ-specific contract rules blindly to SPY, Ideal, or Continuation.

4. For each setup family, identify what rule work is needed:
   - Clean Fast Break
   - Ideal
   - Continuation

5. Create:
   - SAFE_FAST_DAY41_STARTER_BATCH_RULE_AND_DATA_MATRIX.md

6. Matrix must say:
   - process now with starter data
   - needs setup-specific rule first
   - needs full-window data later
   - parked for now
   - replace candidate still needs new rule path

7. Create:
   - SAFE_FAST_DAY41_STARTER_BATCH_NEXT_GROUPED_TASK.md

8. The next grouped task must avoid one-field grinding. It should group candidates by setup family and data readiness.

9. Update:
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_BUILD_STATE.md
   - relevant candidate packets in historical_signal_replay/candidate_packets/

10. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1

Allowed writes:
- SAFE_FAST_DAY41_STARTER_BATCH_OPTION_INSPECTION_CODEX_TASK.md
- SAFE_FAST_DAY41_STARTER_BATCH_OPTION_INSPECTION.md
- SAFE_FAST_DAY41_STARTER_BATCH_RULE_AND_DATA_MATRIX.md
- SAFE_FAST_DAY41_STARTER_BATCH_NEXT_GROUPED_TASK.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_BUILD_STATE.md
- historical_signal_replay/candidate_packets/

Do not write:
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
