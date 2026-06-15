# SAFE-FAST Day 41 QQQ CFB target contract listing/open-interest audit task

Baseline:
- Latest committed checkpoint: feb2e74 Audit QQQ CFB open interest source
- Repo status should be clean.
- Raw Databento files are local-only and ignored.

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Audit whether the target contract was listed before setup time and whether missing prior-day open interest should remain a blocker.
- Do not change the open-interest rule.
- Do not fill evidence.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Known facts:
- Target contract: QQQ 260427C00615000
- instrument_id: 1023411456
- signal time: 2026-04-13T12:30:00-04:00
- Apr 13 definition exists.
- Apr 10 QQQ parent definitions had target_matches=0.
- Apr 13 full-day stats had target rows but no stat_type=9 open interest for target.
- setup-time trades exist with volume 65.
- setup-time quote exists.
- open interest remains missing.

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_DAY41_QQQ_CFB_OPEN_INTEREST_SOURCE_AUDIT.md
- SAFE_FAST_DAY41_QQQ_CFB_OPEN_INTEREST_GATE_DECISION.md
- SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_TRADES_STATS_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION.md
- historical_signal_replay/source_data/external_option_data_drop/
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Task:
1. Inspect Apr 13 definitions for instrument_id 1023411456.
2. Record the definition timestamps and whether the definition existed at or before signal time.
3. Inspect Apr 10 definitions result if local file exists.
4. Confirm whether the target contract existed on Apr 10.
5. Inspect Apr 13 target statistics rows and record stat types/timestamps.
6. Confirm whether any setup-time-safe open-interest row exists.
7. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_TARGET_CONTRACT_LISTING_OI_AUDIT.md
8. The audit must answer:
   - Was the contract listed before signal time?
   - Did it exist on the prior trading day?
   - Is prior-day open interest unavailable because the contract was not listed?
   - Does the current open-interest gate still block option context?
   - What exact next human decision is needed?
9. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md
10. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_TARGET_CONTRACT_LISTING_OI_AUDIT_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_TARGET_CONTRACT_LISTING_OI_AUDIT.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- raw Databento files
- evidence fills
- selector code
- rule changes
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
