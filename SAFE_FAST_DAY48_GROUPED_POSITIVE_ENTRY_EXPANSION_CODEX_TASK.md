# SAFE-FAST Day 48 Grouped Positive-Entry Expansion Codex Task

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY48_POSITIVE_TRADE_CAPTURE_AND_MISS_ANALYSIS_RESULT.md`
2. `historical_signal_replay/results/day48_positive_trade_capture_funnel.json`
3. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
4. `SAFE_FAST_PROJECT_DASHBOARD.md`
5. `SAFE_FAST_PROJECT_RULE_INDEX.md`
6. Existing Clean Fast Break selected-contract replay code, fixtures, and tests
7. Existing Ideal, Clean Fast Break, and Continuation grouped lifecycle fixtures and tests

Expected branch: `main`.

This is grouped SAFE-FAST build testing and measurement.

It is not live trade evaluation.

Do not modify `main.py`, live/engine trading logic, Railway/deploy files, broker/order/account files, `.env`, secrets, or raw vendor data.

Do not download data during this task.

## Active objective

Expand positive-entry development coverage in grouped batches while preserving safety controls.

The current funnel has:

- valid trades captured: `1`;
- true no-trades: `2`;
- missing-data cases: `8`;
- missed valid trades: `0`;
- invalid trades allowed: `0`;
- unresolved cases: `4`;
- winners: `1`;
- losers: `0`.

Correct no-trade behavior is required, but it is not enough. SAFE-FAST also needs valid captured entries, including losing valid trades.

## Required scope

Use existing local data, fixtures, and ignored local raw-data directories first.

Do not cherry-pick profitable examples.

Do not remove stale-quote, future-quote, wide-spread, missing-data, unresolved, or losing controls after outcome inspection.

Do not weaken frozen safety gates to create more trades.

## Required work

1. Inventory locally available positive-entry candidates and controls across Ideal, Clean Fast Break, and Continuation.
2. Keep `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` as the current review-only captured valid-entry reference.
3. Rerun and preserve the CFB stale-quote true no-trade controls:
   - `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`;
   - `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.
4. Identify whether any existing local evidence can add a grouped positive-entry case without new data.
5. Require every candidate to remain classified as exactly one of:
   - `VALID_TRADE_CAPTURED`;
   - `TRUE_NO_TRADE`;
   - `MISSING_DATA`;
   - `MISSED_VALID_TRADE`;
   - `INVALID_TRADE_ALLOWED`;
   - `UNRESOLVED`.
6. Produce before-and-after family and combined funnel scorecards.
7. Run the grouped batch twice and require deterministic equality.
8. If no local positive-entry expansion is possible, create the smallest exact grouped missing-data request package for setup-time fields only. Do not cost-check or download in this task unless a later task explicitly authorizes that.

## Required output

Create a result document:

`SAFE_FAST_DAY48_GROUPED_POSITIVE_ENTRY_EXPANSION_RESULT.md`

Update the machine-readable funnel artifact only if the grouped expansion adds or reclassifies cases:

`historical_signal_replay/results/day48_positive_trade_capture_funnel.json`

If a request package is needed, keep setup-time evidence separate from conditional exit-path evidence. Do not request exit evidence until a valid entry exists.

## Required tests

Run:

1. direct `scripts/safe_fast_run_safe_checks.ps1`;
2. the execution-policy bypass when direct execution is blocked;
3. positive-trade funnel tests;
4. positive-trade funnel validator;
5. CFB backtest runner tests;
6. all Ideal replay tests;
7. all Clean Fast Break replay tests;
8. all Continuation replay tests;
9. Day 48 grouped three-family replay tests;
10. developing-stage transition tests;
11. session-boundary tests;
12. contract-selection tests;
13. execution-realism tests;
14. context and caution tests;
15. stable winner-selection tests;
16. evidence content validator;
17. package-to-intake bridge;
18. handoff/control-file consistency tests if updated;
19. `git diff --check`.

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
- Before funnel totals
- After funnel totals
- Valid trades captured
- True no-trades
- Missing-data cases
- Missed valid trades
- Invalid trades allowed
- Unresolved cases
- Winners
- Losers
- First blockers by stage
- Five owner questions and answers
- Exact next grouped task filename
