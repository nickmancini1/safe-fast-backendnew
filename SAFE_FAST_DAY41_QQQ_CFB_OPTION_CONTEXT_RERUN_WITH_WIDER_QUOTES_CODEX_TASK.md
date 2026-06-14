# SAFE-FAST Day 41 QQQ CFB option-context rerun with wider quotes task

Baseline:
- Latest committed checkpoint: 3c754f1 Audit QQQ CFB top contract quote coverage
- Repo status should be clean.
- Raw Databento files are local-only and ignored.

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Rerun the QQQ CFB option-context selector using the newly downloaded wider top-contract quote file.
- Determine whether option_context_status can move from unknown to a source-backed value.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Known new local file:
- historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_top_contract_1023411456_tcbbo_0930_1230_et.csv

Known top contract:
- QQQ 260427C00615000
- instrument_id: 1023411456
- expiration: 2026-04-27
- strike: 615 call
- DTE: 14
- signal time: 2026-04-13T12:30:00-04:00

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_DAY41_QQQ_CFB_TOP_CONTRACT_QUOTE_COVERAGE_AUDIT.md
- SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_SELECTOR_EVIDENCE_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTOR_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION.md
- historical_signal_replay/databento_opra_normalizer.py
- historical_signal_replay/cfb_contract_selector.py
- historical_signal_replay/source_data/external_option_data_drop/
- historical_signal_replay/source_data/richer_export_package_work/
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Task:
1. Confirm the wider quote CSV exists.
2. Confirm it contains TCBBO rows for instrument_id 1023411456.
3. Find the nearest quote at or before signal time.
4. Rerun the existing selector using the wider quote file.
5. If the contract passes all accepted rules, fill only option_context_status and source notes.
6. If it still fails, leave option_context_status unknown and state the exact reason.
7. Do not update headline_context_status, execution_context_status, or complete_caution_review_status unless directly supported by already accepted rules.
8. Run:
   - python -m unittest tests.test_cfb_contract_selector
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
   - relevant content validator and bridge if safe/local
9. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_WIDER_QUOTES_REVIEW.md
10. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_WIDER_QUOTES_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_WIDER_QUOTES_REVIEW.md
- historical_signal_replay/source_data/richer_export_package_work/
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- raw Databento files
- unrelated evidence fields
- backtest code
- P&L
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
