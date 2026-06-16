# SAFE-FAST Day 41 SPY Ideal starter batch implement and fill task

Baseline:
- Latest commit before this task: db44a14 Process SPY CFB starter option execution context batch

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.
- Then read SAFE_FAST_DAY41_STARTER_BATCH_OPTION_INSPECTION.md.
- Then read SAFE_FAST_DAY41_STARTER_BATCH_RULE_AND_DATA_MATRIX.md.

Goal:
- Handle the remaining SPY Ideal failed requests in one grouped task.
- Use cheap starter Databento data only.
- Do not download more data.
- Do not use full-window data.
- Do not split into one-field tasks.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark any candidate ready.

Candidate:
- SPY-REAL-HISTORICAL-IDEAL-001

Known current state:
- Content validator after SPY CFB batch: 7 passed, 2 failed.
- Remaining failed work-package area: SPY Ideal.
- Starter files exist for SPY Ideal:
  - definitions_full_day
  - statistics_full_day
  - tcbbo_signal_10min
  - trades_signal_10min

Task:
1. Create:
   - SAFE_FAST_DAY41_SPY_IDEAL_STARTER_BATCH_IMPLEMENT_AND_FILL_REVIEW.md

2. Find the exact two remaining SPY Ideal failed evidence requests.

3. For SPY Ideal, inspect:
   - signal time
   - trigger/level if present
   - setup-window quotes
   - setup-window trades
   - setup-time-safe statistics/open-interest
   - existing evidence rows
   - candidate packet state

4. Do not blindly apply Clean Fast Break rules to Ideal.
   - If an Ideal-specific rule already exists, reuse it.
   - If no Ideal rule exists, define a conservative Ideal-specific rule only if repo evidence supports it.
   - If a human decision is still needed, say exactly what is missing and stop that field.

5. In this same grouped task, attempt as much as safely possible:
   - Ideal lifecycle/expiry rule, fixtures, calculator/test support, and evidence fill if source-backed.
   - Ideal option context rule, fixtures, selector/test support, and evidence fill if source-backed.
   - Ideal execution context rule, fixtures, calculator/test support, and evidence fill if source-backed.
   - Ideal complete caution/status update if directly supported by accepted precedence rules.

6. Do not fill unsupported fields.
7. Do not alter unrelated evidence rows.
8. Do not request full-window data in this task.
9. If starter data is not enough, name the exact blocker and whether full-window data would actually answer it.

10. Update:
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_BUILD_STATE.md
   - historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_IDEAL_001.md

11. Run:
   - python -m unittest tests.test_cfb_contract_selector if present
   - python -m unittest tests.test_execution_context_calculator if present
   - python -m unittest tests.test_context_caution_calculator if present
   - python -m unittest tests.test_cfb_lifecycle_calculator if present
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
   - relevant content validator and bridge if safe/local

Allowed writes:
- SAFE_FAST_DAY41_SPY_IDEAL_STARTER_BATCH_IMPLEMENT_AND_FILL_CODEX_TASK.md
- SAFE_FAST_DAY41_SPY_IDEAL_STARTER_BATCH_IMPLEMENT_AND_FILL_REVIEW.md
- SAFE_FAST_DAY41_SPY_IDEAL_*RULE*.md
- historical_signal_replay/fixtures/
- historical_signal_replay/*calculator.py
- historical_signal_replay/*selector.py
- tests/
- historical_signal_replay/source_data/richer_export_package_work/
- historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_IDEAL_001.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- raw Databento files
- full-window data
- unrelated evidence fields
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
