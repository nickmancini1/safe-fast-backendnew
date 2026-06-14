# SAFE-FAST Day 41 QQQ CFB context/caution evidence fill task

Baseline:
- Latest commit before this task: a61e734 Add QQQ CFB context caution calculator

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Fill only the QQQ CFB context/caution evidence fields that are honestly supported by the accepted blocker-preserving calculator.
- Do not backtest.
- Do not choose a trade.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Candidate:
- QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001

Fields to update only if calculator-backed:
- option_context_status
- headline_context_status
- execution_context_status
- complete_caution_review_status

Accepted conservative defaults:
- no selected contract/universe -> option_context_status = unknown
- no source-confirmed headline/no-headline source -> headline_context_status = unknown
- no accepted entry/fill rule -> execution_context_status = unknown
- any required unknown blocks complete_caution_review_status from passing
- complete-caution precedence: fail, unknown, caution, clean

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_CALCULATOR_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_MISSING_DECISIONS.md
- historical_signal_replay/context_caution_calculator.py
- historical_signal_replay/fixtures/qqq_cfb_context_caution_regression_fixtures.json
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- historical_signal_replay/source_data/richer_export_package_work/

Task:
1. Find the exact QQQ CFB context/caution evidence request rows/files.
2. Use the calculator and accepted blocker defaults to determine source-backed statuses.
3. Fill only the context/caution fields that are supported.
4. If a field cannot honestly be filled, leave it blocked and explain why.
5. Do not alter unrelated evidence fields.
6. Add source notes showing calculator, framework decision, missing-decision defaults, and no-hindsight timing.
7. Run:
   - python -m unittest tests.test_context_caution_calculator
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
   - relevant content validator and bridge if safe/local
8. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_EVIDENCE_FILL_REVIEW.md
9. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_EVIDENCE_FILL_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_EVIDENCE_FILL_REVIEW.md
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
