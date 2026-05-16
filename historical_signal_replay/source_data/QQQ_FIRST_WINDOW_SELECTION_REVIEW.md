# QQQ First Source Window Selection Review

## Scope

- **Baseline:** patch8
- **Latest local commit before selection:** `3255554 Add QQQ real historical replay planning review`
- **Source CSV file:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- **Purpose:** select one bounded QQQ source-data window for future real historical replay v1 fixture design.

This review selects source rows only. It does not create a replay fixture, change OHLCV data, fabricate labels, start chart outcome calculations, model option P&L, add account sizing, change `main.py`, change schemas, change runner code, change chart outcome code, or start watcher implementation.

## Selection Result

- **Selection status:** PASS
- **Source CSV file:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- **Symbol:** QQQ
- **Timeframe:** 1h_rth
- **Total source row count:** 301
- **Selected window start timestamp:** `2026-05-05T09:30:00-04:00`
- **Selected window end timestamp:** `2026-05-14T15:30:00-04:00`
- **Selected window row count:** 56
- **Likely setup family candidate:** Ideal

## Why This Window Is Suitable

- **Ideal candidate clearly present:** the selected range contains a clean advance, pullback/retest, and recovery structure that is more suitable for the first QQQ window than lower-priority Clean Fast Break or Continuation candidates.
- **Pre-context/base rows:** `2026-05-05` holds a tight higher-price base mostly around the 681-682 area before the next upside push.
- **Impulse context:** `2026-05-06` pushes from 687.75 to a 695.575 close, and `2026-05-08` extends through 711.14 after the brief `2026-05-07` pause.
- **Retest/pullback behavior:** `2026-05-12` pulls back in a multi-bar sequence from the 708 area into a 696.66 low, then recovers into the close.
- **Post-retest recovery rows:** `2026-05-13` and `2026-05-14` recover from the pullback and extend to new highs inside the selected bounded range.
- **Bounded source-data shape:** the window uses contiguous 1H RTH source rows from complete sessions only, with seven rows per session and no invented timestamps.
- **Future fixture utility:** later fixture design can review developing context, pullback/retest state, trigger-adjacent recovery, and spent/follow-through context row by row without using chart outcome results.

## No-Hindsight Result

- **No-hindsight result:** PASS
- **Reason:** the selection uses only validated QQQ source OHLCV/context metadata from rows inside the accepted source CSV. The review does not add setup labels, trigger labels, lifecycle labels, blocker labels, trade outcomes, profit/loss, account sizing, option data, broker/order/execution fields, or backtest conclusions.

Any future fixture design from this window must evaluate each row using only data available at or before that row timestamp.

## Known Limits

- The setup family is a candidate only. It is not a final replay fixture label and must be confirmed during fixture design from no-hindsight row-by-row evidence.
- The selected window does not prove profitability, trade outcome quality, option performance, account safety, watcher readiness, production readiness, or live-trading readiness.
- 24H, macro, IV, event, headline, option, account, broker, and order context remain unavailable or unconfirmed.
- The selected range is a source-data window only; no signal replay output has been generated from it.
- Chart outcome calculation remains downstream of fixture design and historical signal replay output validation.

## Watcher Deferral

- **Watcher remains deferred:** yes
- **Watcher implementation started:** no
- **Reason:** this task only selects the first bounded QQQ source-data window. QQQ fixture design, historical replay output validation, chart outcome calculation, and broader QQQ/IWM/GLD coverage remain incomplete.

## Boundary Result

- **Boundary result:** PASS
- **Replay fixture created:** no
- **OHLCV data changed:** no
- **Fabricated labels added:** no
- **Chart outcome calculation started:** no
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Watcher implementation started:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Runner code changed:** no
- **Chart outcome code changed:** no

## Recommended Next Task

Design the first QQQ real historical replay v1 fixture from the selected source-data window, preserving the source-data/no-hindsight boundary and staying signal/stage/lifecycle only.
