# SAFE-FAST Day 41 SPY Batch Databento Cost-Check Plan

## Baseline

- This is a cost-check plan only.
- Dataset target: Databento `OPRA.PILLAR`.
- Raw data download authorized: NO.
- Vendor API call authorized in this task: NO.
- Evidence fill authorized: NO.
- Backtest/P&L/proof/readiness: NO.

## Candidates Covered

| Candidate | Setup time ET | Setup time UTC | Trigger | Invalidation | Included in cost-check |
| --- | --- | --- | --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | `2026-04-13T12:30:00-04:00` | `2026-04-13T16:30:00Z` | `682.03` | `678.45` | Yes |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | `2026-04-15T14:30:00-04:00` | `2026-04-15T18:30:00Z` | `698.65` | `694.2801` | Yes |
| `SPY-REAL-HISTORICAL-IDEAL-001` | `2026-05-13T11:30:00-04:00` | `2026-05-13T15:30:00Z` | `740.75` | `731.83` | Optional same SPY pass |

## Databento Request Shape For Cost Check

Cost-check first. Do not download in this task.

| Schema | Purpose | Symbol/parent/instrument approach | Start/end window | Expected file role |
| --- | --- | --- | --- | --- |
| `definition` | Find SPY option listing, expiration, strike, side, raw symbol, and instrument id; support prior-day listing/open-interest reasoning | Parent/root `SPY` first; narrow by date, expiration range, and strike band after the reviewed-universe rule is accepted | Signal date definitions for `2026-04-13`, `2026-04-15`, and optional `2026-05-13`; prior trading days `2026-04-10`, `2026-04-14`, and optional `2026-05-12` | `SPY_OPRA_definitions_<date>.csv` or DBN equivalent |
| `tcbbo` | Selected-contract bid/ask, quote timestamp, spread, spread percent, bid size, ask size, and quote freshness | Cost-check parent/root `SPY` with strike/expiration narrowing when possible; after contract identity exists, prefer selected instrument id for wider quote windows | Regular-session open through setup for each signal: `2026-04-13T13:30:00Z` to `2026-04-13T16:30:00Z`; `2026-04-15T13:30:00Z` to `2026-04-15T18:30:00Z`; optional `2026-05-13T13:30:00Z` to `2026-05-13T15:30:00Z` | `SPY_OPRA_tcbbo_<candidate>_rth_to_setup.csv` |
| `trades` | Setup-time-safe same-contract trade volume | Same parent/root or selected instrument id after selected contract is known | Same regular-session-open-through-setup windows as `tcbbo` | `SPY_OPRA_trades_<candidate>_rth_to_setup.csv` |
| `statistics` | Setup-time-safe same-contract open interest or explicit missing-OI diagnosis | Same parent/root or selected instrument id after selected contract is known; prior-day and signal-day statistics may both matter | Prior trading day through signal setup where Databento availability supports it; at minimum cost-check prior day and signal-day availability for each setup | `SPY_OPRA_statistics_<candidate>_prior_and_signal.csv` |

## Reviewed Universe Placeholder

No SPY contract-selection rule is accepted in this task. For cost estimation only, use broad but bounded ranges around known trigger levels, then narrow after a reviewed-universe rule exists.

| Candidate | Cost-check expiration range | Cost-check strike band | Notes |
| --- | --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | `2026-04-27` through `2026-05-13`, or all SPY expirations if vendor filtering is not available | `660` through `705`, or full chain if vendor filtering is not available | Centered around trigger `682.03`; rule acceptance still needed before selection |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | `2026-04-29` through `2026-05-15`, or all SPY expirations if vendor filtering is not available | `675` through `720`, or full chain if vendor filtering is not available | Centered around trigger `698.65`; rule acceptance still needed before selection |
| `SPY-REAL-HISTORICAL-IDEAL-001` | `2026-05-27` through `2026-06-12`, or all SPY expirations if vendor filtering is not available | `715` through `765`, or full chain if vendor filtering is not available | Optional cost-check only; Ideal contract-selection rule is not accepted |

These ranges are cost-check bounds, not trade rules.

## Expected Checks After A Later Authorized Pull

If a later task authorizes data download, inspect only for source availability before evidence fill:

- Definition rows exist for candidate dates and prior trading days.
- Candidate-specific symbol/instrument-id mappings are consistent.
- TCBBO has at least one quote at or before setup for the selected/top-ranked contract.
- Nearest selected quote age is measured before any broader rule work proceeds.
- Bid/ask, spread, spread percent, bid size, ask size, and no-future-data gates can be evaluated.
- Trades contain setup-time-safe same-contract volume.
- Statistics contain setup-time-safe same-contract open interest, or the absence is diagnosed without inventing an exception.

## Non-Authorized Work

- No Databento download.
- No raw Databento file write.
- No evidence row update.
- No contract selected as a real trade.
- No fill, slippage, cost, P&L, proof, profitability, or readiness inference.

## Cost-Check Result Needed Next

The next grouped task should run a Databento cost-check only for all three SPY windows, record estimated cost and available filtering, then stop. If the cost-check is acceptable and a later task explicitly authorizes download, the first post-download inspection should check selected-contract quote freshness before spending effort on full evidence fills.
