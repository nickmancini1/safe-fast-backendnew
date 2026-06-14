# SAFE-FAST Day 41 QQQ CFB top-contract quote coverage audit task

Baseline:
- Latest commit before this task: 7d1c45d Test QQQ CFB option context selector evidence

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Figure out why the top-ranked QQQ contract had no valid TCBBO quote before signal time.
- Determine whether this is a Databento data-window problem, a symbol/instrument mapping problem, or a real no-quote blocker.
- Do not download more data.
- Do not change the selector rule.
- Do not fill evidence.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Known result:
- Top-ranked contract: QQQ 260427C00615000
- Expiration: 2026-04-27
- Strike: 615 call
- DTE: 14
- Signal time: 2026-04-13T12:30:00-04:00
- Blocker: no TCBBO quote at or before signal time in the local downloaded data
- option_context_status remains unknown

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_SELECTOR_EVIDENCE_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTOR_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_DOWNLOAD_VALIDATION.md
- historical_signal_replay/databento_opra_normalizer.py
- historical_signal_replay/cfb_contract_selector.py
- historical_signal_replay/source_data/external_option_data_drop/
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Task:
1. Inspect local Databento definition, TCBBO, trade, and statistics CSV files.
2. Identify the exact instrument id / symbol mapping for QQQ 260427C00615000.
3. Count whether any TCBBO rows exist for that exact contract in the local files.
4. If TCBBO rows exist, list the nearest row before signal and nearest row after signal.
5. If no TCBBO rows exist, check whether:
   - the contract appears in definitions,
   - the contract appears in trades,
   - the contract appears in statistics,
   - nearby contracts have TCBBO rows.
6. Determine whether the blocker is likely:
   - downloaded time window too narrow,
   - symbol/instrument mapping problem,
   - top contract genuinely had no quote in the local window,
   - or selector rule needs a future human decision.
7. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_TOP_CONTRACT_QUOTE_COVERAGE_AUDIT.md
8. Include the exact next Databento request needed if a wider quote pull is justified:
   - dataset
   - schema
   - symbol or instrument id
   - start/end window
   - cost-check first
   - no full download without cost check
9. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md
10. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_TOP_CONTRACT_QUOTE_COVERAGE_AUDIT_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_TOP_CONTRACT_QUOTE_COVERAGE_AUDIT.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- raw Databento files
- evidence fills
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
