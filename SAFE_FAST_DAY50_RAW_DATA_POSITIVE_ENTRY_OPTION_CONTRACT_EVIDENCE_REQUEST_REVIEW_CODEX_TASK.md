# SAFE-FAST Option Contract Evidence and Costed Backtest Batch

Read `SAFE_FAST_BUILD_STATE.md` first.

Read the accepted mapper, mapper-to-generation, and package-to-candidate results and their JSON files. Read the existing contract-selection, option-evidence, execution-cost, and exit-replay rules before changing code.

## Objective

Process the three March 16, 2026 SPY setup-qualified candidates separately:

- Ideal
- Clean Fast Break
- Continuation

Use existing local option evidence to select contracts and execute costed entry/exit replays. Do not stop after planning or merely restating the blocker.

## Required execution

For each setup:

1. Recover the frozen setup timestamp, underlying price, trigger, invalidation, freshness state, and no-hindsight boundary.
2. Inspect existing local option definitions, quotes, trades, volume, open interest, strike, and expiration evidence.
3. Apply the existing frozen contract-selection rules without weakening them.
4. Record the exact contract-selection inputs and winner-selection result.
5. Continue through:
   - trade candidate
   - selected contract
   - eligible entry
   - recorded entry
6. When exact local entry and exit evidence exists, calculate:
   - signal time
   - intended and simulated entry time
   - bid, ask, midpoint, spread, and quote age
   - fill assumption and execution delay
   - entry price
   - exit rule and exit time
   - exit price
   - gross P&L
   - commissions, fees, slippage, and spread cost
   - net P&L
   - holding duration
7. Report Ideal, Clean Fast Break, and Continuation separately.

## Missing-evidence behavior

Do not guess, fabricate, or download paid data.

When local evidence is incomplete, complete every supported step and produce one grouped exact request containing:

- setup family
- SPY setup timestamp
- intended expiration/strike/right or selection range
- exact contract identifier when derivable
- dataset and schema
- start and end timestamps
- definitions, quotes, trades, volume, or open-interest fields required
- entry/exit evidence required
- exact blocker scope
- exact estimated cost
- whether approval would enable contract selection, entry replay, exit replay, or full net-P&L calculation

Run an exact cost check only. Do not purchase or download without explicit approval.

## Regression requirements

Batch the relevant tests covering:

- all three setup families
- contract selection
- deterministic winner selection
- quote age and spread limits
- setup-time and no-hindsight boundaries
- session boundaries and carry-forward
- stale/spent and blocker rejection
- no-trade preservation
- existing mapper cases
- mapper-to-generation retry
- package-to-candidate contract
- unchanged preserved funnel controls

Also run the focused validators, Day 51 handoff consistency test, safe checks with `-ExecutionPolicy Bypass`, and `git diff --check`.

## Outputs

Create:

- `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_OPTION_CONTRACT_EVIDENCE_REQUEST_REVIEW_RESULT.md`
- a machine-readable JSON result under `historical_signal_replay/results/`
- focused implementation, validator, and regression-test files

Update the build state, dashboard, rule index, proof pipeline, data registry, and canonical handoff.

Do not touch `main.py`, production/live backend, Railway/deploy, broker/account/order behavior, credentials, `.env`, sizing, alerts, or frozen `patch8` thresholds.

Do not claim profitability, paper eligibility, or live eligibility.