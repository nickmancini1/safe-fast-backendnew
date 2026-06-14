# SAFE-FAST Day 41 QQQ CFB option-context selector evidence task

Baseline:
- Latest commit before this task: fc1782c Add QQQ CFB contract selector

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Use the tested QQQ CFB contract selector against the local Databento QQQ files.
- Determine whether option_context_status can be filled honestly.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Candidate:
- QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTOR_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION.md
- historical_signal_replay/cfb_contract_selector.py
- historical_signal_replay/databento_opra_normalizer.py
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- historical_signal_replay/source_data/external_option_data_drop/
- historical_signal_replay/source_data/richer_export_package_work/

Task:
1. Load the local QQQ Databento files if present.
2. Use the Databento normalizer and QQQ CFB contract selector.
3. Determine whether the accepted contract-selection rule selects exactly one eligible contract.
4. If yes, document:
   - selected contract
   - expiration
   - strike
   - side
   - bid
   - ask
   - spread
   - spread percent
   - volume
   - open interest
   - quote timestamp
   - statistics timestamp
   - no-hindsight status
5. If no, document exact abstain/rejection reason.
6. Fill only option_context_status if honestly supported.
7. Do not fill headline_context_status, execution_context_status, or complete_caution_review_status unless already directly supported by accepted rules.
8. Run:
   - python -m unittest tests.test_cfb_contract_selector
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
   - relevant content validator and bridge if safe/local
9. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_SELECTOR_EVIDENCE_REVIEW.md
10. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_SELECTOR_EVIDENCE_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_SELECTOR_EVIDENCE_REVIEW.md
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
