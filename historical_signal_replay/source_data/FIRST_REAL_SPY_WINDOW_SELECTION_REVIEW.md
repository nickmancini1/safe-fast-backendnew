# First Real SPY Window Selection Review

## Scope

- **Baseline:** patch8
- **Source CSV file:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- **Purpose:** select one bounded SPY source-data window for first real historical replay v1 signal/stage/lifecycle fixture design.

This review selects source rows only. It does not create a replay fixture, change OHLCV data, fabricate data, start backtesting, model trade outcomes, model option P&L, add account sizing, modify trading logic, or change replay runner/test/schema behavior.

## Selection Result

- **Selection status:** PASS
- **Source CSV file:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- **Symbol:** SPY
- **Timeframe:** 1h_rth
- **Total source row count:** 293
- **Selected window start timestamp:** 2026-04-24T09:30:00-04:00
- **Selected window end timestamp:** 2026-04-30T15:30:00-04:00
- **Selected window row count:** 35
- **Likely setup family candidate:** Continuation
- **Expected lifecycle/stage design target:** developing continuation context into a bounded shelf/pullback, then a later completed break/follow-through candidate, with later fixture design expected to separate watching, pending/completed-candle approval, triggered signal stage, and spent/no-fresh-trigger states if supported by the no-hindsight row-by-row review.

## Why This Window Is Suitable

- **Bounded contiguous source rows:** the window uses complete 1h RTH source rows from 2026-04-24 through 2026-04-30, with seven rows per full session and no invented timestamps.
- **Enough pre-break context:** 2026-04-24 and 2026-04-27 show upside progression from the low 710s into the 715 area before the later pullback.
- **Constructive pullback/shelf behavior:** 2026-04-28 and 2026-04-29 compress mostly in the 708.37-712.20 area after the prior push, giving future fixture design a source-only candidate for developing Continuation lifecycle review.
- **Later break/follow-through candidate:** 2026-04-30 opens back above the prior two-session shelf area and later extends through 715 and 718, giving future fixture design candidate rows for completed-break and follow-through stage review.
- **No-hindsight friendly:** every selected row is source OHLCV/context metadata only; future fixture design can evaluate each row using only rows at or before that timestamp.

## No-Hindsight Result

- **No-hindsight result:** PASS
- **Reason:** the selected window is copied conceptually from validated source OHLCV rows only. It contains no setup labels, trigger labels, blocker labels, lifecycle labels, trade outcomes, profit/loss, account sizing, option contract data, broker/order/execution fields, or backtest labels.

## Known Limits

- The setup family is only a candidate. It is not a final fixture label and must be confirmed during fixture design from no-hindsight row-by-row evidence.
- 24H/daily context, macro context, IV context, and event context are unavailable/unconfirmed in the source CSV, so fixture design must keep those fields unconfirmed unless later source data is added.
- The selected window does not prove profitability, trade outcome, option P&L, position sizing, production readiness, alert quality, or live trade decision behavior.
- The selected window was chosen for signal/stage/lifecycle fixture design only; no backtest or execution interpretation is included.

## Boundary Result

- **Boundary result:** PASS
- **Replay fixture created:** no
- **Backtesting started:** no
- **OHLCV data changed:** no
- **`main.py` changed:** no
- **`dxlink_candles.py` changed:** no
- **Replay tests changed:** no
- **Schemas changed:** no
- **Generated reports changed:** no
- **Runner code changed:** no

## Recommended Next Task

Design the first real historical replay v1 fixture from the selected SPY window, staying signal/stage/lifecycle only and preserving no-hindsight row boundaries.
