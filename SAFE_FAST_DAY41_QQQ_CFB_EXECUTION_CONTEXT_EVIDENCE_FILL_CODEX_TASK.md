# SAFE-FAST Day 41 QQQ CFB execution-context evidence fill task

Baseline:
- Latest commit before this task: ed008eb Add QQQ CFB execution context calculator

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Fill only QQQ CFB execution-context evidence that is calculator-backed.
- If directly supported by accepted rules, update complete_caution_review_status too.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Known current QQQ state:
- gap_context_status = clean
- lifecycle/stale-spent status filled
- option_context_status = caution
- headline_context_status = unknown
- execution_context_status currently needs update
- complete_caution_review_status currently needs review

Known expected execution result:
- selected contract: QQQ 260427C00615000
- signal time: 2026-04-13T12:30:00-04:00
- nearest setup-safe quote: 2026-04-13T16:06:30.640301037Z
- bid: 7.76
- ask: 7.80
- spread: 0.04
- quote age: about 23m 29s
- expected execution_context_status: fail
- reason: quote_age_above_5_minutes

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_CALCULATOR_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_RULE_DECISION.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_CALCULATOR_REVIEW.md
- historical_signal_replay/execution_context_calculator.py
- historical_signal_replay/context_caution_calculator.py
- historical_signal_replay/fixtures/qqq_cfb_execution_context_regression_fixtures.json
- historical_signal_replay/source_data/richer_export_package_work/
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Task:
1. Use the execution-context calculator to verify the known QQQ execution result.
2. Find the QQQ CFB context/caution evidence row.
3. Fill only:
   - execution_context_status
   if calculator-backed.
4. If the accepted complete-caution precedence directly supports it, also update:
   - complete_caution_review_status
   Expected logic: fail beats unknown/caution/clean.
5. Do not update headline_context_status unless a source-backed headline rule already supports it.
6. Add source notes explaining quote time, signal time, quote age, bid, ask, spread, and rejection reason.
7. Run:
   - python -m unittest tests.test_execution_context_calculator
   - python -m unittest tests.test_context_caution_calculator
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
   - relevant content validator and bridge if safe/local
8. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_EVIDENCE_FILL_REVIEW.md
9. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_EVIDENCE_FILL_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_EVIDENCE_FILL_REVIEW.md
- historical_signal_replay/source_data/richer_export_package_work/
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- unrelated evidence fields
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
