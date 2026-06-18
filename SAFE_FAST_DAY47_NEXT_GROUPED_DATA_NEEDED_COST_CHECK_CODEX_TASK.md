# SAFE-FAST Day 47 Next Grouped Data-Needed Cost-Check Codex Task

You are working in the SAFE-FAST local repo.

Repo source of truth:
`C:\Users\nickm\Desktop\New folder\safe-fast-backendnew`

Branch:
`main`

Baseline:
`SAFE_FAST_DAY47_GROUPED_CFB_EXPANSION_DATA_NEEDED_PLAN.md`

## Hard Rules

- Read `SAFE_FAST_BUILD_STATE.md` first.
- Read `SAFE_FAST_DAY47_GROUPED_CFB_EXPANSION_DATA_NEEDED_PLAN.md` second.
- Do not touch `main.py`.
- Do not touch Railway, production, broker, order, account, credentials, `.env`, or secrets.
- Do not patch live trading logic.
- Do not change frozen baseline logic.
- Keep this as a grouped data-needed cost-check task unless explicit approval language below authorizes more.
- Do not download Databento data unless this task has explicit approval language and the user approval requirement is satisfied.
- Keep raw Databento files local and ignored.
- Do not run a new backtest.
- Do not calculate new P&L.
- Do not claim proof, profitability, readiness, promotion, or intake-ready status.

## Read First

Read these files in order:

1. `SAFE_FAST_BUILD_STATE.md`
2. `SAFE_FAST_DAY47_GROUPED_CFB_EXPANSION_DATA_NEEDED_PLAN.md`
3. `SAFE_FAST_PROJECT_DASHBOARD.md`
4. `SAFE_FAST_PROJECT_RULE_INDEX.md`
5. `SAFE_FAST_DAY46_NEXT_GROUPED_BACKTEST_BATCH_DECISION.md`
6. The relevant candidate packets:
   - `historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_002.md`
   - `historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_003.md`
   - `historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md`
   - `historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_IDEAL_001.md`
   - `historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_IDEAL_001.md`
   - `historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CONTINUATION_001.md`
   - `historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CONTINUATION_001.md`

## Objective

Identify exact Databento symbols, schemas, and windows needed for the next grouped batch, then cost-check the grouped batch before any download.

The grouped batch must preserve:

- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` as the positive CFB review-only reference.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` as the `quote_after_signal` no-entry control.
- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` as the `quote_age_above_5_minutes` no-entry control.
- Ideal and Continuation candidates as comparison/parking references unless their setup-family rule state explicitly supports inclusion.

## Cost-Check Requirements

Before any data download:

- Identify exact Databento dataset, schema, symbols or instrument IDs, and UTC windows.
- Separate setup-window requests from full exit-path requests.
- Separate parent-symbol discovery needs from selected-contract needs.
- Prefer already-local data and selected-contract windows where possible.
- Print the exact checked price.
- If cost cannot be checked because of environment/network/proxy/API issues, report that directly and stop without downloading.
- Require user approval before any full-window download unless the checked cost is clearly tiny and this task explicitly says the tiny-cost exception applies.
- This task does not include approval to download data.

## Expected Output

Create or update only planning/cost-check documentation unless a stronger repo instruction requires another exact file.

The output should include:

- grouped candidates covered;
- exact Databento dataset and schemas checked;
- exact symbols or instrument IDs checked;
- exact UTC windows checked;
- checked price;
- whether user approval is required before download;
- whether download was performed, which must be `NO` for this task;
- data still missing after cost check;
- next recommended action.

## Required Checks

Run:

1. `.\scripts\safe_fast_run_safe_checks.ps1`
2. `python -m watcher_foundation.source_evidence_work_package_content_validator`
3. `python -m watcher_foundation.source_evidence_package_to_intake_bridge`

If a check is impossible because the environment is missing something, report it directly and do not fake a pass.

## Final Response Format

Respond in plain English using exactly:

Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:

Do not push.
Do not create a commit.
