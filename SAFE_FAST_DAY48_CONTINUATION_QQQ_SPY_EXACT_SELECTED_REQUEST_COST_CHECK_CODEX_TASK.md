# SAFE-FAST Day 48 Continuation QQQ/SPY Exact Selected-Request Cost Check - Codex Task

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY48_CONTINUATION_QQQ_SPY_OPTION_CONTEXT_EVIDENCE_PACKAGE_RESULT.md`
2. `historical_signal_replay/source_data/richer_export_package_work/day48_continuation_qqq_spy_option_context_request_manifest.json`
3. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
4. `SAFE_FAST_PROJECT_DASHBOARD.md`
5. `SAFE_FAST_PROJECT_RULE_INDEX.md`

Expected branch: `main`.
Expected status: clean except this task file if it is untracked.

If local git and the canonical files disagree, stop and report the conflict.

## Active objective

Run a cost-only check for the exact SPY selected raw-symbol setup-window requests recorded in the Day 48 Continuation QQQ/SPY option-context request manifest.

Do not download data.

Do not request GLD or IWM data.

Do not broaden symbols, contracts, schemas, or windows.

## Exact request scope

Use only:

- Candidate: `SPY-REAL-HISTORICAL-CONTINUATION-001`
- Raw symbol: `SPY   260514C00720000`
- Dataset: `OPRA.PILLAR`
- Schemas: `tcbbo` and `trades`
- Setup window: `2026-04-30T09:30:00-04:00` through `2026-04-30T12:30:00-04:00`
- UTC setup window: `2026-04-30T13:30:00Z` through `2026-04-30T16:30:00Z`

No conditional exit-path request is allowed because no valid entry exists.

## Required output

Create a result document that records:

- whether HTTPS and credentials were available;
- exact checked total or `NOT_AVAILABLE` with exact reason;
- subtotal by schema;
- request shape used;
- any rejected request and corrected shape;
- no-download status;
- no purchase approval inferred.

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`

## Next-task decision

If the cost check succeeds, create an exact selected-request download task requiring explicit user approval before download.

If the cost check cannot run, create one package/cost-check repair task only if the failure is due to request-shape or local tooling problems.

If no repair is needed but credentials are unavailable, stop after documenting `NOT_AVAILABLE`.

## Restrictions

Do not modify:

- `main.py`;
- trading behavior;
- Railway or deployment files;
- broker, account, or order code;
- credentials or `.env`;
- raw vendor data;
- P&L files.

Do not download data.

Do not run a profitability backtest.

Do not claim proof, profitability, readiness, promotion, paper eligibility, or live eligibility.

## Required tests

Run:

1. direct safe-check script;
2. execution-policy bypass if direct PowerShell is blocked;
3. Day 48 Continuation option-context request validator;
4. evidence content validator;
5. package-to-intake bridge;
6. `git diff --check`.

Remove generated `__pycache__` directories.

Do not commit or push.
