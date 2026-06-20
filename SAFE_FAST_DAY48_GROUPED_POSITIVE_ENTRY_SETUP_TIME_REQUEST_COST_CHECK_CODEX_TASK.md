# SAFE-FAST Day 48 Grouped Positive-Entry Setup-Time Request Cost Check Codex Task

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY48_GROUPED_POSITIVE_ENTRY_EXPANSION_RESULT.md`
2. `historical_signal_replay/source_data/richer_export_package_work/day48_grouped_positive_entry_setup_time_request_manifest.json`
3. `SAFE_FAST_DAY48_POSITIVE_TRADE_CAPTURE_AND_MISS_ANALYSIS_RESULT.md`
4. `historical_signal_replay/results/day48_positive_trade_capture_funnel.json`
5. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
6. `SAFE_FAST_PROJECT_DASHBOARD.md`
7. `SAFE_FAST_PROJECT_RULE_INDEX.md`

Expected branch: `main`.

This is a cost-check-only task for exact setup-time request shapes.

Do not modify `main.py`, live/engine trading logic, Railway/deploy files, broker/order/account files, `.env`, secrets, or raw vendor data.

Do not download data during this task.

## Active objective

Cost-check only the grouped setup-time-only request package created by the Day 48 grouped positive-entry expansion task.

The exact manifest is:

`historical_signal_replay/source_data/richer_export_package_work/day48_grouped_positive_entry_setup_time_request_manifest.json`

## Required scope

Only the manifest requests are in scope:

- SPY Ideal 001 setup-window `tcbbo` raw symbol `SPY   260527C00745000`
- SPY Ideal 001 setup-window `trades` raw symbol `SPY   260527C00745000`
- SPY Continuation 001 setup-window `tcbbo` raw symbol `SPY   260514C00720000`
- SPY Continuation 001 setup-window `trades` raw symbol `SPY   260514C00720000`

Do not add QQQ, GLD, IWM, alternate contracts, alternate expirations, broader windows, statistics, definitions, or conditional exit-path requests.

Do not infer purchase approval from a successful cost check.

## Required work

1. Validate the manifest is setup-time-only and has no conditional exit-path requests.
2. Check whether local credentials and a safe cost-check path are available.
3. If a safe cost-check path is available, obtain a cost estimate for each manifest request and the grouped total.
4. If credentials or safe cost tooling are unavailable, record `NOT_AVAILABLE` without attempting a vendor request.
5. Do not download data.
6. Do not change the positive-trade funnel artifact.

## Required output

Create:

`SAFE_FAST_DAY48_GROUPED_POSITIVE_ENTRY_SETUP_TIME_REQUEST_COST_CHECK_RESULT.md`

The result must state:

- whether credentials were present;
- whether a vendor request was made;
- cost by request;
- grouped total;
- download authorized: `NO`;
- purchase approval inferred: `NO`;
- raw vendor data changed: `NO`;
- proof/profitability/readiness/promotion/intake-ready status: unchanged.

## Required tests

Run:

1. direct `scripts/safe_fast_run_safe_checks.ps1`;
2. the execution-policy bypass when direct execution is blocked;
3. positive-trade funnel tests;
4. positive-trade funnel validator;
5. evidence content validator;
6. package-to-intake bridge;
7. `git diff --check`.

Remove generated `__pycache__` directories before final status.

Do not commit or push.

## Final summary

Return only:

- Baseline
- Fixed
- Blocked
- Next
- Tests
- Files changed
