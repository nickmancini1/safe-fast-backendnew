# SAFE-FAST Day 41 QQQ CFB context/caution calculator task

Baseline:
- Latest commit before this task: c1877a4 Accept QQQ CFB context caution blocker defaults

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Build the QQQ CFB context/caution calculator using the accepted framework fixtures.
- The calculator must preserve blockers honestly.
- Do not fill evidence.
- Do not backtest.
- Do not choose a trade.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

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
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_MISSING_DECISIONS.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_REGRESSION_FIXTURES_REVIEW.md
- historical_signal_replay/fixtures/qqq_cfb_context_caution_regression_fixtures.json
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_PROJECT_PROOF_PIPELINE.md
- SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md

Task:
1. Create:
   - historical_signal_replay/context_caution_calculator.py
2. Create:
   - tests/test_context_caution_calculator.py
3. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_CALCULATOR_REVIEW.md
4. The calculator must:
   - classify option_context_status
   - classify headline_context_status
   - classify execution_context_status
   - classify complete_caution_review_status
   - apply precedence exactly: fail, unknown, caution, clean
   - return unknown under the accepted blocker defaults
   - reject future data after signal time
   - reject wrong candidate/setup identity
   - reject forbidden fill/P&L/profitability/readiness inputs
   - return clear missing-data errors
   - not infer evidence fill, trade choice, P&L, proof, profitability, or readiness
5. Tests must use:
   - historical_signal_replay/fixtures/qqq_cfb_context_caution_regression_fixtures.json
6. Tests must prove all 22 fixtures pass.
7. Run:
   - python -m unittest tests.test_context_caution_calculator
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
8. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_CALCULATOR_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_CALCULATOR_REVIEW.md
- historical_signal_replay/context_caution_calculator.py
- tests/test_context_caution_calculator.py
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- evidence fills
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
