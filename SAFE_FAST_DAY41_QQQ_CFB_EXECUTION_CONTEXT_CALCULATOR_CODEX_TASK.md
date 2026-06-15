# SAFE-FAST Day 41 QQQ CFB execution context calculator task

Baseline:
- Latest commit before this task: e3f4d44 Add QQQ CFB execution context fixtures

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Implement the QQQ CFB execution-context calculator using the accepted fixtures.
- Do not fill evidence yet.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Accepted rule:
- clean: quote at or before signal and quote age <= 60 seconds
- caution: quote at or before signal and quote age > 60 seconds and <= 5 minutes
- fail: quote age > 5 minutes
- fail: quote after signal
- fail: missing bid/ask
- fail: spread too wide
- fail: missing required size/volume
- unknown: missing source data or unresolved rule
- later long-call fill basis: ask price only
- no P&L in this task
- no future quotes
- no fallback
- no proof/readiness inference

Known QQQ expected case:
- selected contract: QQQ 260427C00615000
- signal time: 2026-04-13T12:30:00-04:00
- nearest setup-safe quote: 2026-04-13T16:06:30.640301037Z
- bid: 7.76
- ask: 7.80
- spread: 0.04
- quote age: about 23m 29s
- expected execution_context_status: fail

Read:
- SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_RULE_DECISION.md
- SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_FIXTURES_REVIEW.md
- historical_signal_replay/fixtures/qqq_cfb_execution_context_regression_fixtures.json
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Task:
1. Create:
   - historical_signal_replay/execution_context_calculator.py
2. Create:
   - tests/test_execution_context_calculator.py
3. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_CALCULATOR_REVIEW.md
4. Calculator must:
   - calculate quote age
   - classify execution_context_status
   - reject future quotes
   - reject missing bid/ask
   - reject bad spread
   - reject missing size/volume
   - return unknown for missing source data
   - refuse fallback
   - refuse P&L/proof/profitability/readiness inference
5. Tests must use:
   - historical_signal_replay/fixtures/qqq_cfb_execution_context_regression_fixtures.json
6. Tests must prove all 13 fixtures pass.
7. Run:
   - python -m unittest tests.test_execution_context_calculator
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
8. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_CALCULATOR_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_CALCULATOR_REVIEW.md
- historical_signal_replay/execution_context_calculator.py
- tests/test_execution_context_calculator.py
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
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
