# SAFE-FAST Day 41 Databento QQQ evidence field mapping task

Baseline:
- Latest commit before this task: 6f1eac1 Add project control consolidation audit

First action:
- Read SAFE_FAST_BUILD_STATE.md first.

Goal:
- Map the validated Databento QQQ option files to SAFE-FAST evidence-field requirements.
- Do not fill evidence yet.
- Do not choose a trade.
- Do not calculate P&L.
- Do not mark QQQ ready.

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_DOWNLOAD_VALIDATION.md
- SAFE_FAST_DAY41_QQQ_EXTERNAL_OPTION_DATA_REQUEST_PACKAGE.md
- SAFE_FAST_PROJECT_PROOF_PIPELINE.md
- SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- historical_signal_replay/source_data/richer_export_package_work/
- historical_signal_replay/source_data/external_option_data_drop/README.md
- local QQQ_OPRA CSV files only if present

Task:
1. Identify every SAFE-FAST evidence field needed for QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001.
2. For each field, say whether Databento can support it from the validated files.
3. Map Databento columns to SAFE-FAST fields.
4. Identify fields still not supported.
5. Identify fields that require SAFE-FAST rules before they can be filled.
6. Identify fields that are raw-data supported but not yet label-supported.
7. Identify the minimum next code/tests needed.
8. Create:
   - SAFE_FAST_DAY41_DATABENTO_QQQ_EVIDENCE_FIELD_MAPPING.md
9. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_DATABENTO_QQQ_EVIDENCE_FIELD_MAPPING_CODEX_TASK.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_EVIDENCE_FIELD_MAPPING.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- evidence fills
- calculator code
- tests
- raw data files
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
