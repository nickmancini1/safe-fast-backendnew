# SAFE-FAST Day 41 QQQ CFB contract-selection regression fixtures task

Baseline:
- Latest commit before this task: 362972a Accept QQQ CFB contract selection rule

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Add regression fixtures for the accepted QQQ CFB contract-selection rule.
- Do not create selector code yet.
- Do not fill evidence.
- Do not backtest.
- Do not choose a real trade.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Accepted rule to fixture:
- side: long calls
- expiration: nearest reviewed expiration with DTE >= 14
- strike: lowest call strike >= 613.67
- moneyness: OTM-by-trigger
- spread cap: 0.15
- spread percent cap: 2.00%
- minimum bid size: 1
- minimum ask size: 1
- minimum trade volume: 1
- minimum open interest: 1
- quote timestamp: nearest at or before signal time
- statistics timestamp: strict no-hindsight
- missing data: abstain
- fallback: none

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION.md
- SAFE_FAST_DAY41_QQQ_CFB_SELECTED_CONTRACT_POLICY.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_DOWNLOAD_VALIDATION.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_EVIDENCE_FIELD_MAPPING.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_OPRA_NORMALIZER_REVIEW.md
- historical_signal_replay/databento_opra_normalizer.py
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Task:
1. Create:
   - historical_signal_replay/fixtures/qqq_cfb_contract_selection_regression_fixtures.json
2. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_FIXTURES_REVIEW.md
3. Fixtures must cover:
   - valid selected contract
   - wrong side rejected
   - DTE below 14 rejected
   - nearest valid expiration selected
   - strike below 613.67 rejected
   - lowest strike >= 613.67 selected
   - spread above 0.15 rejected
   - spread percent above 2.00% rejected
   - missing bid rejected
   - missing ask rejected
   - bid size below 1 rejected
   - ask size below 1 rejected
   - volume below 1 rejected
   - open interest below 1 rejected
   - quote after signal rejected
   - statistics after signal rejected
   - no fallback if selected contract fails
   - abstain when no contract passes
4. Each fixture must include:
   - fixture_id
   - signal_time
   - trigger_price
   - candidate_contracts
   - expected_selected_contract
   - expected_status
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
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_FIXTURES_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_FIXTURES_REVIEW.md
- historical_signal_replay/fixtures/qqq_cfb_contract_selection_regression_fixtures.json
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- selector code
- evidence fills
- backtest code
- trade-selection execution code
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
