# SAFE-FAST Day 41 QQQ CFB option-context rerun with trades/statistics task

Baseline:
- Latest committed checkpoint: 2842cbd Rerun QQQ option context with wider quotes
- Repo status should be clean.
- Raw Databento files are local-only and ignored.

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Rerun QQQ CFB option-context review using the newly downloaded top-contract trades/statistics files.
- Determine whether option_context_status can move from unknown.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Known top contract:
- QQQ 260427C00615000
- instrument_id: 1023411456
- expiration: 2026-04-27
- strike: 615 call
- DTE: 14
- signal time: 2026-04-13T12:30:00-04:00

Known new local files:
- historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_top_contract_1023411456_trades_0930_1230_et.csv
- historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_top_contract_1023411456_statistics_0930_1230_et.csv
- historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_top_contract_1023411456_trades_statistics_0930_1230_et_manifest.json

Known latest result:
- Wider quotes fixed the quote blocker.
- option_context_status stayed unknown because trade volume was 0 and no setup-time-safe open-interest/statistics row was found.
- New trades file downloaded successfully.
- New statistics request returned no data.

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_WIDER_QUOTES_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_TOP_CONTRACT_QUOTE_COVERAGE_AUDIT.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTOR_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION.md
- historical_signal_replay/databento_opra_normalizer.py
- historical_signal_replay/cfb_contract_selector.py
- historical_signal_replay/source_data/external_option_data_drop/
- historical_signal_replay/source_data/richer_export_package_work/
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Task:
1. Confirm the new trades/statistics CSV files exist.
2. Count rows for instrument_id 1023411456.
3. Calculate setup-time-safe trade volume at or before signal time.
4. Confirm whether any setup-time-safe open-interest/statistics row exists.
5. Rerun the existing selector using:
   - wider TCBBO file
   - new trades file
   - new statistics file
   - existing definitions
6. If all accepted gates pass, fill only option_context_status and source notes.
7. If it still fails, leave option_context_status unknown and state the exact blocker.
8. Do not update headline_context_status, execution_context_status, or complete_caution_review_status unless directly supported by already accepted rules.
9. Run:
   - python -m unittest tests.test_cfb_contract_selector
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
   - relevant content validator and bridge if safe/local
10. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_TRADES_STATS_REVIEW.md
11. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_TRADES_STATS_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_TRADES_STATS_REVIEW.md
- historical_signal_replay/source_data/richer_export_package_work/
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- raw Databento files
- unrelated evidence fields
- selector rule changes
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
