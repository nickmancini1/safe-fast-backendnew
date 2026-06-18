# SAFE-FAST Day 47 Grouped CFB Selected-Contract Replay Backtest Codex Task

## Authority and baseline

Read `SAFE_FAST_BUILD_STATE.md` before doing anything else.

Then read:

1. `SAFE_FAST_PROJECT_DASHBOARD.md`
2. `SAFE_FAST_PROJECT_RULE_INDEX.md`
3. `SAFE_FAST_DAY47_GROUPED_CFB_SELECTED_CONTRACT_DOWNLOAD_RESULT.md`
4. `SAFE_FAST_DAY47_NEXT_GROUPED_DATA_NEEDED_COST_CHECK_RESULT.md`
5. `SAFE_FAST_DAY47_GROUPED_CFB_EXPANSION_DATA_NEEDED_PLAN.md`

Expected starting baseline:

- branch: `main`
- current download-result baseline: `5a818d8`
- required raw data manifest: `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_003_selected_contract_download_manifest.json`

## Objective

Run the next grouped replay/backtest review using only the downloaded selected-contract evidence for `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`, while preserving the grouped CFB anchors:

- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` remains the positive review-only anchor.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` is the selected-contract data-needed row under review.
- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` remains the stale-quote no-entry control.

This is build/replay evidence work, not live trade evaluation.

## Hard rules

- Do not modify `main.py`.
- Do not touch Railway, production, broker, order, account, credentials, `.env`, or secrets.
- Do not patch live trading logic.
- Do not change frozen baseline logic.
- Do not broaden symbols, contracts, schemas, time windows, expirations, candidate count, or setup families.
- Do not download more Databento data.
- Do not claim proof, profitability, readiness, promotion, or intake-ready status.
- Raw Databento files must remain local and ignored.

## Required replay inputs

Use the existing ignored local raw files named in:

`historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_003_selected_contract_download_manifest.json`

Preserve these validation facts:

- request shape used `raw_symbol=SPY   260429C00700000`;
- the failed local `instrument_id=1333784938` request must not be substituted;
- downloaded row-level Databento `instrument_id` is `1258293278`;
- setup-window and conditional exit-path files are separate.

## Required output

Create one grouped replay/backtest result document following current repository naming and documentation conventions.

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- relevant CFB candidate packets only if their replay state changes

The result must state:

- whether the downloaded setup-window evidence changes the current `quote_after_signal` no-entry diagnosis;
- whether any entry is valid under accepted CFB rules;
- whether conditional exit-path data was used or remained unused;
- exact blocker if replay remains blocked/no-trade;
- exact row counts and raw files used;
- that the result is not proof, profitability, readiness, promotion, or intake-ready.

## Mandatory queued task after this path

After the current grouped data/replay path is completed, run:

`SAFE_FAST_DAY47_TO_DAY90_CONSOLIDATED_AUDIT_AND_COMPLETION_PLAN_CODEX_TASK.md`

Do not replace that queued audit with scattered planning docs.

## Tests

Run:

1. `.\scripts\safe_fast_run_safe_checks.ps1`
2. If direct PowerShell execution is blocked, rerun with `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`
3. `python -m watcher_foundation.source_evidence_work_package_content_validator`
4. `python -m watcher_foundation.source_evidence_package_to_intake_bridge`
5. focused replay/backtest tests touched by this task
6. `git diff --check`

Do not commit or push.

## Final response format

Return:

- Baseline
- Fixed
- Blocked
- Next
- Tests
- Files changed
