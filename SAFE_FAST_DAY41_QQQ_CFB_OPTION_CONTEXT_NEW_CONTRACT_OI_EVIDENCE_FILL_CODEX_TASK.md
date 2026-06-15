# SAFE-FAST Day 41 QQQ CFB option-context evidence fill with new-contract OI exception

Baseline:
- Latest commit before this task: aec19d8 Update QQQ CFB selector for new contract OI exception

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Rerun QQQ option-context evidence using the updated selector.
- Fill only option_context_status if the tested new-contract OI exception supports it.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Known expected result to verify:
- Selected contract: QQQ 260427C00615000
- instrument_id: 1023411456
- Quote exists before signal.
- Trade volume exists before signal.
- Prior-day open interest cannot exist because the contract was not listed on Apr 10.
- Accepted new-contract OI exception should allow option_context_status = caution if all gates pass.

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_SELECTOR_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_RULE.md
- SAFE_FAST_DAY41_QQQ_CFB_TARGET_CONTRACT_LISTING_OI_AUDIT.md
- SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_TRADES_STATS_REVIEW.md
- historical_signal_replay/cfb_contract_selector.py
- historical_signal_replay/databento_opra_normalizer.py
- historical_signal_replay/source_data/external_option_data_drop/
- historical_signal_replay/source_data/richer_export_package_work/
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Task:
1. Rerun the selector using the local QQQ Databento files.
2. Verify whether the selected contract passes through the new-contract OI exception.
3. If supported, update only:
   - option_context_status
   in the QQQ context/caution evidence row.
4. Do not update headline_context_status, execution_context_status, or complete_caution_review_status unless already directly supported by accepted rules.
5. Add source notes explaining:
   - selected contract
   - quote timestamp
   - bid/ask/spread
   - trade volume
   - listing timestamp
   - Apr 10 not-listed result
   - new-contract OI exception
6. Run:
   - python -m unittest tests.test_cfb_contract_selector
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
   - relevant content validator and bridge if safe/local
7. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_NEW_CONTRACT_OI_EVIDENCE_FILL_REVIEW.md
8. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_NEW_CONTRACT_OI_EVIDENCE_FILL_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_NEW_CONTRACT_OI_EVIDENCE_FILL_REVIEW.md
- historical_signal_replay/source_data/richer_export_package_work/
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- unrelated evidence fields
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
