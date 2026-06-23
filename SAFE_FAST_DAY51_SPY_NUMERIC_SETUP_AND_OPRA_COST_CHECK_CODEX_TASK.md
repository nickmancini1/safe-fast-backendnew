# SAFE-FAST Day 51 SPY Numeric Setup and OPRA Cost Check

Read `SAFE_FAST_BUILD_STATE.md` first.

Read:

1. `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_REVIEW_ONLY_PACKAGE_TO_CANDIDATE_CONTRACT_RESULT.md`
2. `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_OPTION_CONTRACT_EVIDENCE_REQUEST_REVIEW_RESULT.md`
3. Their machine-readable JSON results
4. Existing Databento request, cost-estimation, option-selection, execution-cost, and exit-replay code

## Objective

In one implementation batch, unblock actual backtesting for the three March 16, 2026 SPY setups:

- Ideal
- Clean Fast Break
- Continuation

Do not stop after planning, review, or another blocker summary.

## Part 1 — Numeric setup contract

Using only frozen setup-time SPY one-minute OHLCV evidence:

- establish the exact setup timestamp
- establish numeric underlying trigger
- establish numeric underlying invalidation
- establish direction
- establish freshness deadline
- establish no-hindsight boundary
- establish session-boundary behavior
- establish any numeric room/target field required by existing rules

Process each setup separately.

Do not invent thresholds. Reuse accepted frozen rules. When an accepted rule is incomplete, report the exact rule gap and implement every field that is evidence-backed.

## Part 2 — Exact option evidence specification

For each setup derive, using existing contract-selection rules:

- call or put
- contract-selection timestamp
- permitted expiration range
- permitted strike range
- exact Databento dataset and schemas
- definition window
- quote window
- trade window
- statistics/volume/open-interest window
- required symbols or parent-symbol query
- entry evidence window
- exit evidence window

Do not request broad dates or an unrestricted option universe.

## Part 3 — Cost check

Run the existing Databento metadata/cost-estimation path for the smallest exact grouped request.

This is a cost check only.

Do not purchase or download nonzero-cost data.

Report:

- cost per schema/window
- grouped total
- currency
- exact API or local command used
- whether existing credentials permitted the estimate
- whether the estimate is sufficient for explicit approval

If the exact cost is zero, or the evidence already exists locally, continue immediately.

## Part 4 — Actual replay/backtest

For every setup with sufficient evidence, continue through:

- trade candidate
- selected contract
- eligible entry
- recorded entry
- costed exit replay

Report separately:

- setup family
- signal timestamp
- selected contract
- entry timestamp and price
- exit timestamp and price
- gross P&L
- spread/slippage/fees
- net P&L
- hold duration
- exit reason

Do not average setup families together.

## Tests

Run one relevant batch covering:

- numeric setup contracts for all three families
- no-hindsight
- developing-stage transitions
- session boundaries and carry-forward
- deterministic winner selection
- stale/spent and blocker rejection
- no-trade preservation
- mapper regressions
- mapper-to-generation regressions
- package-to-candidate regressions
- option-selection and execution-cost controls
- Day 51 handoff consistency
- focused validators
- safe checks with `-ExecutionPolicy Bypass`
- `git diff --check`

Do not run unrelated broad suites.

## Outputs

Create implementation, validator, focused tests, machine-readable JSON, and:

`SAFE_FAST_DAY51_SPY_NUMERIC_SETUP_AND_OPRA_COST_CHECK_RESULT.md`

Update build state, dashboard, rule index, proof pipeline, data registry, and canonical handoff.

The final summary must state either:

- actual per-setup costed backtest results, or
- one exact `APPROVAL_REQUIRED` grouped cost and the precise data it unlocks.

Do not touch `main.py`, production/live backend, Railway, broker/account/order code, credentials, `.env`, sizing, alerts, or frozen `patch8` thresholds.