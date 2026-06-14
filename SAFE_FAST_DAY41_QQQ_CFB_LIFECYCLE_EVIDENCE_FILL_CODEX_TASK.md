# SAFE-FAST Day 41 QQQ CFB lifecycle evidence fill task

Baseline:
- Latest commit before this task: 81bee9a Add QQQ CFB lifecycle calculator

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Fill only the QQQ CFB lifecycle/stale/spent/expiry evidence fields if calculator-backed data supports them.
- Do not fill unrelated evidence.
- Do not backtest.
- Do not choose a trade.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Candidate:
- QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_DAY41_QQQ_CFB_LIFECYCLE_CALCULATOR_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_DECISION.md
- historical_signal_replay/cfb_lifecycle_calculator.py
- historical_signal_replay/fixtures/qqq_cfb_lifecycle_regression_fixtures.json
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- historical_signal_replay/source_data/richer_export_package_work/

Task:
1. Find the exact QQQ CFB stale/spent/expiry evidence request rows/files.
2. Use the lifecycle calculator and accepted fixtures to verify the QQQ lifecycle result.
3. Fill only source-backed lifecycle/stale/spent/expiry fields that are directly supported.
4. Do not alter unrelated evidence fields.
5. Add source notes showing signal time, lifecycle rule, calculator, and no-hindsight timing.
6. Run:
   - python -m unittest tests.test_cfb_lifecycle_calculator
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
   - relevant content validator and bridge if safe/local
7. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_LIFECYCLE_EVIDENCE_FILL_REVIEW.md
8. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_LIFECYCLE_EVIDENCE_FILL_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_LIFECYCLE_EVIDENCE_FILL_REVIEW.md
- historical_signal_replay/source_data/richer_export_package_work/
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- unrelated evidence fields
- backtest code
- trade-selection code
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
