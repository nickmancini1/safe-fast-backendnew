# SAFE-FAST Day 41 QQQ gap-context calculator task

Baseline:
- Latest commit before this task: b03976c Add SAFE-FAST project speed layer

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Implement the QQQ CFB gap-context calculator using the accepted regression fixtures.
- Add tests.
- Do not fill evidence.
- Do not backtest.
- Do not choose a trade.
- Do not calculate P&L.
- Do not mark QQQ ready.

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_PROOF_PIPELINE.md
- SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md
- SAFE_FAST_DAY41_QQQ_GAP_THRESHOLD_FIXTURE_DECISION.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_REGRESSION_FIXTURES_REVIEW.md
- historical_signal_replay/fixtures/qqq_gap_context_regression_fixtures.json
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Accepted thresholds:
- clean: absolute gap percent <= 0.30%
- caution: absolute gap percent > 0.30% and <= 0.75%
- fail: absolute gap percent > 0.75%
- unknown: missing or unproven inputs

Known QQQ example:
- Previous close: 611.02
- Signal-day open: 609.455
- Gap amount: -1.565
- Gap percent: about -0.2561%
- Expected status: clean if no-hindsight timing passes

Task:
1. Create:
   - historical_signal_replay/gap_context_calculator.py
2. Create:
   - tests/test_gap_context_calculator.py
3. Create:
   - SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_CALCULATOR_REVIEW.md
4. The calculator must:
   - calculate gap amount
   - calculate gap percent
   - classify clean/caution/fail/unknown
   - calculate gap_context_as_of
   - calculate gap_context_reviewed_before_signal
   - reject future data after signal time
   - return clear missing-data errors
   - not infer evidence fill, trade choice, P&L, proof, or readiness
5. Tests must use:
   - historical_signal_replay/fixtures/qqq_gap_context_regression_fixtures.json
6. Tests must prove:
   - clean fixture passes
   - caution boundary fixtures pass
   - fail fixture passes
   - missing previous close becomes unknown
   - missing signal-day open becomes unknown
   - future-data example is rejected
   - known QQQ example returns clean
   - no field implies trade choice, P&L, proof, or readiness
7. Run:
   - python -m unittest tests.test_gap_context_calculator
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
8. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_CALCULATOR_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_CALCULATOR_REVIEW.md
- historical_signal_replay/gap_context_calculator.py
- tests/test_gap_context_calculator.py
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
