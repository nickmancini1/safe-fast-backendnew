# SAFE-FAST Day 41 QQQ CFB new-contract OI exception fixtures task

Baseline:
- Latest commit before this task: 63a4748 Accept QQQ CFB new contract OI exception rule

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Add regression fixtures for the accepted new-contract open-interest exception.
- Do not change selector code yet.
- Do not fill evidence.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Accepted rule:
- If selected contract was not listed on prior trading day, prior-day open interest is not required.
- Contract must be listed before signal.
- Quote must be setup-time-safe.
- Spread must pass accepted caps.
- Bid/ask size must pass.
- Setup-time trade volume must pass.
- No future data.
- No fallback.
- Result is caution, not clean, because open interest is unavailable.

Known QQQ facts:
- Contract: QQQ 260427C00615000
- instrument_id: 1023411456
- Listed before setup: 2026-04-13T12:00:00.445628903Z
- Signal: 2026-04-13T12:30:00-04:00
- Apr 10 parent definitions had 0 target matches.
- Setup-time quote exists.
- Setup-time trade volume exists: 65.
- Setup-time same-contract open interest does not exist.

Read:
- SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_RULE.md
- SAFE_FAST_DAY41_QQQ_CFB_TARGET_CONTRACT_LISTING_OI_AUDIT.md
- SAFE_FAST_DAY41_QQQ_CFB_OPEN_INTEREST_GATE_DECISION.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Task:
1. Create:
   - historical_signal_replay/fixtures/qqq_cfb_new_contract_oi_exception_regression_fixtures.json
2. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_FIXTURES_REVIEW.md
3. Fixtures must cover:
   - valid new-contract OI exception returns caution
   - contract listed after signal rejected
   - contract existed prior day but OI missing rejected/unknown
   - missing listing timestamp rejected/unknown
   - missing quote rejected/unknown
   - quote after signal rejected
   - spread above cap rejected
   - spread percent above cap rejected
   - bid size below minimum rejected
   - ask size below minimum rejected
   - volume below minimum rejected
   - fallback rejected
   - future data rejected
4. Each fixture must include:
   - fixture_id
   - signal_time
   - contract
   - instrument_id
   - listed_before_signal
   - existed_prior_trading_day
   - has_setup_safe_quote
   - spread
   - spread_percent
   - bid_size
   - ask_size
   - setup_time_trade_volume
   - has_setup_safe_open_interest
   - expected_option_context_status
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
- SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_FIXTURES_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_FIXTURES_REVIEW.md
- historical_signal_replay/fixtures/qqq_cfb_new_contract_oi_exception_regression_fixtures.json
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- selector code
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
