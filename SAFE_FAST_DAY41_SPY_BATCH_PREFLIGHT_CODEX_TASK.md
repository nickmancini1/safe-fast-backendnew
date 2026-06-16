# SAFE-FAST Day 41 SPY batch preflight task

Baseline:
- Latest commit before this task: 7d483ab Add batch restart plan after QQQ diagnosis

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.
- Then read SAFE_FAST_DAY41_BATCH_RESTART_QQQ_DIAGNOSIS_AND_CANDIDATE_PLAN.md.
- Then read SAFE_FAST_DAY41_BATCH_NEXT_ACTIONS.md.

Goal:
- Batch process the next SPY candidates together.
- Do not grind one tiny field at a time.
- Do not fill evidence yet.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark any candidate ready.

Batch candidates:
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003
- SPY-REAL-HISTORICAL-IDEAL-001

Use lessons from QQQ:
- QQQ failed because execution quote was too old.
- Do not try to force failed examples through.
- Check quote freshness early.
- Check selected-contract data early.
- Check missing data before writing lots of rule work.
- Use existing calculators/tools where possible.

Task:
1. Create:
   - SAFE_FAST_DAY41_SPY_BATCH_PREFLIGHT.md

2. For all three SPY candidates, find:
   - candidate id
   - setup type
   - signal date/time
   - symbol
   - known trigger/level if present
   - existing source files
   - existing evidence rows
   - current passed/failed evidence state
   - current blocker list

3. Create/update candidate packets for all three:
   - historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_002.md
   - historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_003.md
   - historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_IDEAL_001.md

4. Reuse existing tools conceptually:
   - gap calculator
   - lifecycle calculator if applicable
   - context/caution calculator if applicable
   - Databento OPRA normalizer
   - contract selector only if the rule applies safely

5. Do not assume QQQ CFB rules automatically apply to Ideal unless the repo already supports that.

6. Build a batch data-needs table:
   - underlying candles needed
   - option definitions needed
   - option quotes needed
   - option trades needed
   - option statistics/open-interest needed
   - headline/context source needed
   - execution quote freshness needed

7. Build a Databento cost-check plan only:
   - dataset
   - schema
   - symbol/parent/instrument approach
   - start/end window
   - expected files
   - cost-check first
   - no download in this task unless explicitly already local

8. Identify which checks can be attempted immediately from local data and which need Databento pulls.

9. Create:
   - SAFE_FAST_DAY41_SPY_BATCH_DATABENTO_COST_CHECK_PLAN.md

10. Create:
   - SAFE_FAST_DAY41_SPY_BATCH_NEXT_TASK.md
   This must be one grouped next task, not three separate tiny tasks.

11. Update:
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_BUILD_STATE.md

12. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1

Allowed writes:
- SAFE_FAST_DAY41_SPY_BATCH_PREFLIGHT_CODEX_TASK.md
- SAFE_FAST_DAY41_SPY_BATCH_PREFLIGHT.md
- SAFE_FAST_DAY41_SPY_BATCH_DATABENTO_COST_CHECK_PLAN.md
- SAFE_FAST_DAY41_SPY_BATCH_NEXT_TASK.md
- historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_002.md
- historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_003.md
- historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_IDEAL_001.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- evidence fills
- backtest code
- P&L
- raw Databento files
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
