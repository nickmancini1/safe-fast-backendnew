# SAFE-FAST Day 41 QQQ gap-context regression fixtures task

Baseline:
- Latest commit before this task: fcb8d0e Accept QQQ gap threshold fixtures

First action:
- Read SAFE_FAST_BUILD_STATE.md first.

Goal:
- Add regression fixtures for the accepted QQQ CFB gap thresholds.
- Do not create calculator logic yet.
- Do not fill evidence.
- Do not backtest.
- Do not choose a trade.
- Do not calculate P&L.

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_DAY41_QQQ_GAP_THRESHOLD_FIXTURE_DECISION.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_RULE_DEFINITION.md
- SAFE_FAST_DAY41_QQQ_CFB_RULE_DECISION_PACKAGE.md
- SAFE_FAST_PROJECT_RULE_INDEX.md

Accepted QQQ CFB gap thresholds:
- clean: absolute gap percent <= 0.30%
- caution: absolute gap percent > 0.30% and <= 0.75%
- fail: absolute gap percent > 0.75%
- unknown: missing or unproven inputs

Known QQQ raw fixture:
- Candidate: QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001
- Signal time: 2026-04-13T12:30:00-04:00
- Previous close: 611.02
- Signal-day open: 609.455
- Gap amount: -1.565
- Gap percent: about -0.2561%
- Expected status: clean, after no-hindsight regression passes

Task:
1. Create:
   - historical_signal_replay/fixtures/qqq_gap_context_regression_fixtures.json
2. Create:
   - SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_REGRESSION_FIXTURES_REVIEW.md
3. Fixtures must include:
   - clean example
   - caution lower-boundary example
   - caution upper-boundary example
   - fail example
   - unknown missing previous close
   - unknown missing signal-day open
   - future-data rejection example
   - known QQQ 2026-04-13 example
4. Each fixture must include:
   - fixture_id
   - previous_close
   - signal_day_open
   - signal_time
   - latest_allowed_source_time
   - forbidden_future_source_time if applicable
   - expected_gap_amount
   - expected_gap_percent
   - expected_status
   - expected_reviewed_before_signal
   - reason
5. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_REGRESSION_FIXTURES_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_REGRESSION_FIXTURES_REVIEW.md
- historical_signal_replay/fixtures/qqq_gap_context_regression_fixtures.json
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- calculator code
- evidence fills
- backtest code
- trade-selection code
- P&L
- raw data files
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
