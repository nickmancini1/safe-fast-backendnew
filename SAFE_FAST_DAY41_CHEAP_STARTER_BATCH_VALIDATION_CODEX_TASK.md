# SAFE-FAST Day 41 cheap starter Databento batch validation task

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Validate the cheap starter Databento files for the remaining candidates.
- Do not download more data.
- Do not use full-window data.
- Do not fill evidence yet.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark any candidate ready.

Mode:
- Batch validation only.
- Cheap starter data only.

Candidates:
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003
- SPY-REAL-HISTORICAL-IDEAL-001
- QQQ-REAL-HISTORICAL-CONTINUATION-001
- QQQ-REAL-HISTORICAL-IDEAL-001
- SPY-REAL-HISTORICAL-CONTINUATION-001

Use local files in:
- historical_signal_replay/source_data/external_option_data_drop/

Expected starter file types:
- definitions_full_day
- statistics_full_day
- tcbbo_signal_10min
- trades_signal_10min

Task:
1. Confirm the cheap starter manifest exists.
2. Confirm expected files exist for each candidate.
3. For each candidate, count rows for:
   - definitions
   - statistics
   - 10-minute quotes
   - 10-minute trades
4. For each candidate, check whether the starter data is enough to attempt:
   - option universe review
   - setup-time quote freshness
   - setup-time trade volume
   - setup-time open-interest/statistics check
5. Identify which candidates can move forward using starter data only.
6. Identify which candidates likely need full-window data later.
7. Do not request or download full-window data.
8. Do not fill evidence.
9. Create:
   - SAFE_FAST_DAY41_CHEAP_STARTER_BATCH_VALIDATION.md
10. Create:
   - SAFE_FAST_DAY41_CHEAP_STARTER_BATCH_NEXT_STEPS.md
11. Update:
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_BUILD_STATE.md
   - relevant candidate packets in historical_signal_replay/candidate_packets/
12. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1

Allowed writes:
- SAFE_FAST_DAY41_CHEAP_STARTER_BATCH_VALIDATION_CODEX_TASK.md
- SAFE_FAST_DAY41_CHEAP_STARTER_BATCH_VALIDATION.md
- SAFE_FAST_DAY41_CHEAP_STARTER_BATCH_NEXT_STEPS.md
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
