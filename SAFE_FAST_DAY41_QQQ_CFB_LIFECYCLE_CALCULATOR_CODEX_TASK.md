# SAFE-FAST Day 41 QQQ CFB lifecycle calculator task

Baseline:
- Latest commit before this task: 3a26ca8 Add QQQ CFB lifecycle regression fixtures

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Implement the QQQ CFB lifecycle calculator using the accepted lifecycle fixtures.
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
- SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_DECISION.md
- SAFE_FAST_DAY41_QQQ_CFB_LIFECYCLE_REGRESSION_FIXTURES_REVIEW.md
- historical_signal_replay/fixtures/qqq_cfb_lifecycle_regression_fixtures.json
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_PROJECT_PROOF_PIPELINE.md
- SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md

Task:
1. Create:
   - historical_signal_replay/cfb_lifecycle_calculator.py
2. Create:
   - tests/test_cfb_lifecycle_calculator.py
3. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_LIFECYCLE_CALCULATOR_REVIEW.md
4. The calculator must:
   - classify fresh/stale/spent/expired/unknown
   - preserve lifecycle_as_of
   - calculate reviewed_before_signal
   - reject future data after signal time
   - handle missing required data clearly
   - handle higher-base refresh allowed/rejected
   - apply state precedence exactly as the accepted decision says
   - not infer evidence fill, trade choice, P&L, proof, profitability, or readiness
5. Tests must use:
   - historical_signal_replay/fixtures/qqq_cfb_lifecycle_regression_fixtures.json
6. Tests must prove all 18 fixtures pass.
7. Run:
   - python -m unittest tests.test_cfb_lifecycle_calculator
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
8. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_LIFECYCLE_CALCULATOR_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_LIFECYCLE_CALCULATOR_REVIEW.md
- historical_signal_replay/cfb_lifecycle_calculator.py
- tests/test_cfb_lifecycle_calculator.py
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
