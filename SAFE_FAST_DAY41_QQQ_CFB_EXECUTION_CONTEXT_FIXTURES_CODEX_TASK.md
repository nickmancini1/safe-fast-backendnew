# SAFE-FAST Day 41 QQQ CFB execution context fixtures task

Baseline:
- Latest commit before this task: 4d6d363 Accept QQQ CFB execution context rule

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Add regression fixtures for the accepted QQQ CFB execution-context rule.
- Do not create calculator code yet.
- Do not fill evidence.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Accepted execution-context rule:
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
- instrument_id: 1023411456
- signal time: 2026-04-13T12:30:00-04:00
- nearest setup-safe quote: 2026-04-13T16:06:30.640301037Z
- bid: 7.76
- ask: 7.80
- spread: 0.04
- quote age: about 23m 29s
- expected execution_context_status: fail

Read:
- SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_RULE_DECISION.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Task:
1. Create:
   - historical_signal_replay/fixtures/qqq_cfb_execution_context_regression_fixtures.json
2. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_FIXTURES_REVIEW.md
3. Fixtures must cover:
   - clean quote age
   - caution quote age
   - fail quote too old
   - QQQ known stale quote fail
   - quote after signal rejected
   - missing bid rejected
   - missing ask rejected
   - bad spread rejected
   - missing size rejected
   - missing volume rejected
   - missing source data unknown
   - no fallback
   - forbidden P&L/proof/readiness fields rejected
4. Each fixture must include:
   - fixture_id
   - signal_time
   - quote_time
   - bid
   - ask
   - spread
   - bid_size
   - ask_size
   - setup_time_trade_volume
   - expected_quote_age_seconds
   - expected_execution_context_status
   - expected_rejection_reason if applicable
   - reason
5. Validate JSON parses and required fields exist.
6. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
7. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_FIXTURES_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_FIXTURES_REVIEW.md
- historical_signal_replay/fixtures/qqq_cfb_execution_context_regression_fixtures.json
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- calculator code
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
