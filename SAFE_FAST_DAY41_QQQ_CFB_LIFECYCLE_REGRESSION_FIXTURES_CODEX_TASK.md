# SAFE-FAST Day 41 QQQ CFB lifecycle regression fixtures task

Baseline:
- Latest commit before this task: cec29a7 Accept QQQ CFB stale spent expiry rule

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Add data-only regression fixtures for the accepted QQQ CFB stale/spent/expiry lifecycle rule.
- Do not create calculator logic yet.
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
- SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_RULE.md
- SAFE_FAST_DAY41_QQQ_CFB_RULE_DECISION_PACKAGE.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Task:
1. Create:
   - historical_signal_replay/fixtures/qqq_cfb_lifecycle_regression_fixtures.json
2. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_LIFECYCLE_REGRESSION_FIXTURES_REVIEW.md
3. Fixtures must test the accepted rule for:
   - fresh
   - stale
   - spent
   - expired
   - unknown
   - missing required data
   - future-data rejection
   - higher-base refresh allowed
   - higher-base refresh rejected
   - state precedence
4. Each fixture must include:
   - fixture_id
   - setup_type
   - signal_time
   - source_time
   - candle_start
   - candle_end
   - candidate_state_inputs
   - expected_lifecycle_status
   - expected_as_of
   - expected_reviewed_before_signal
   - expected_rejection_reason if applicable
   - reason
5. If the accepted decision doc is not specific enough to create honest fixtures, do not invent behavior. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_LIFECYCLE_FIXTURES_BLOCKED.md
   and name the exact missing decision.
6. Validate the JSON can be parsed and all required fields exist.
7. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
8. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_LIFECYCLE_REGRESSION_FIXTURES_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_LIFECYCLE_REGRESSION_FIXTURES_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_LIFECYCLE_FIXTURES_BLOCKED.md
- historical_signal_replay/fixtures/qqq_cfb_lifecycle_regression_fixtures.json
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- lifecycle calculator code
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
