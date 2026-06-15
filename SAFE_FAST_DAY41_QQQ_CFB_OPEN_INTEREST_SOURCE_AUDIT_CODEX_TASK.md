# SAFE-FAST Day 41 QQQ CFB open-interest source audit task

Baseline:
- Latest commit before this task: 4666e96 Accept QQQ CFB open interest gate decision

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Find whether timestamp-safe same-contract open interest for QQQ 260427C00615000 exists anywhere in local source files.
- If not, define the exact next source request or decision needed.
- Do not change the open-interest gate.
- Do not fill evidence.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Known blocker:
- Top contract: QQQ 260427C00615000
- instrument_id: 1023411456
- signal time: 2026-04-13T12:30:00-04:00
- quotes exist before signal
- trades exist before signal, volume 65
- statistics request returned 0 rows
- option_context_status remains unknown because same-contract open interest is missing

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_DAY41_QQQ_CFB_OPEN_INTEREST_GATE_DECISION.md
- SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_TRADES_STATS_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_DOWNLOAD_VALIDATION.md
- historical_signal_replay/databento_opra_normalizer.py
- historical_signal_replay/cfb_contract_selector.py
- historical_signal_replay/source_data/external_option_data_drop/
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Task:
1. Inspect all local QQQ_OPRA definition, statistics, trades, quote, and manifest files.
2. Search for open-interest-like columns or statistic types.
3. Check whether instrument_id 1023411456 appears in any file with open-interest data.
4. Check whether the full-day QQQ statistics file has same-contract rows.
5. Check whether definitions contain any open-interest field.
6. If open interest exists locally, document exact file, column, timestamp, value, and whether it is setup-time-safe.
7. If open interest does not exist locally, document the exact next data-source request needed.
8. If Databento cannot provide it from the current schemas/files, state that clearly and keep the blocker.
9. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_OPEN_INTEREST_SOURCE_AUDIT.md
10. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md
11. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_OPEN_INTEREST_SOURCE_AUDIT_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_OPEN_INTEREST_SOURCE_AUDIT.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- raw Databento files
- evidence fills
- selector code
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
