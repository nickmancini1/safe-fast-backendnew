# QQQ Continuation Window Selection Review

## Selection Status

- **Selection status:** PASS
- **Baseline:** patch8
- **Latest local commit before selection:** `4d2dc08 Add QQQ Clean Fast Break replay evidence review`
- **Scope:** bounded QQQ Continuation source-data window selection for future real historical replay v1 fixture design only.

This review does not create a fixture, change OHLCV data, fabricate labels, start chart outcome calculations, change `main.py`, change schemas, change runner code, change chart outcome code, model option P&L, add account sizing, or start watcher implementation.

## Source Data

- **Source CSV file:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- **Symbol:** QQQ
- **Timeframe:** `1h_rth`
- **Total source row count:** 301 data rows
- **Source timestamp range:** `2026-03-16T15:30:00-04:00` through `2026-05-15T14:30:00-04:00`
- **Context fields:** 24H, macro, IV, and event context remain unconfirmed in the accepted source rows.

## Already Covered QQQ Windows

- **Ideal:** `2026-05-05T09:30:00-04:00` through `2026-05-14T15:30:00-04:00`
- **Clean Fast Break:** `2026-04-08T09:30:00-04:00` through `2026-04-17T15:30:00-04:00`

The selected Continuation window does not overlap either already covered QQQ window.

## Selected Window

- **Selected window start timestamp:** `2026-04-20T09:30:00-04:00`
- **Selected window end timestamp:** `2026-05-01T15:30:00-04:00`
- **Selected window row count:** 70
- **Likely setup family candidate:** Continuation

## Why This Window Is Suitable

The selected source window is suitable as a QQQ Continuation candidate because it begins after the already reviewed upside impulse window and contains source-visible continuation structure without needing outcome labels:

- `2026-04-20` and `2026-04-21` show a pullback and shelf/base attempt after the prior accepted upside run, with repeated candles holding roughly the mid-640s instead of immediately invalidating the prior advance.
- `2026-04-22` shows recovery above the short shelf area, with the session pressing from the high 640s into the mid-650s.
- `2026-04-23` shows a test and shake inside the developing continuation area rather than a clean new fast-break-only profile.
- `2026-04-24` and `2026-04-27` show higher-price consolidation around the low/mid-660s.
- `2026-04-28` through `2026-05-01` provide additional bounded lifecycle context, including a dip, rebuild, and push toward the mid-670s, for later fixture design to decide whether to represent a fresh trigger, spent trigger, blocked continuation, or higher-base continuation state.

This is a source-data selection only. The window is selected for visible formation, shelf/rebuild behavior, and enough bounded pre-trigger and post-state rows for later signal/stage/lifecycle fixture design, not because of any measured chart outcome.

## No-Hindsight Result

- **No-hindsight result:** PASS
- **Reason:** selection used only accepted QQQ 1H RTH OHLCV/source rows and prior reviewed evidence boundaries. No setup labels, trigger labels, lifecycle labels, future-row result labels, profitability labels, MFE/MAE, chart outcome measurements, option data, account sizing, broker/order/execution data, or backtest conclusions were added.

## Known Limits

- This review selects a candidate window only; it does not prove the final fixture stage sequence.
- The selected window follows the prior Clean Fast Break source window, so later fixture design must preserve the distinction between prior impulse context and a new Continuation candidate.
- 24H, macro, IV, event, headline, option, account, and broker context remain unavailable or unconfirmed.
- This does not prove profitability, option performance, account safety, watcher readiness, production readiness, or live-trading readiness.

## Watcher Deferral

- **Watcher remains deferred:** yes
- **Watcher implementation started:** no

## Boundary Result

- **Boundary result:** PASS; source-window selection only, no fixture creation, no OHLCV edits, no fabricated labels, no chart outcome calculation, no option P&L, no account sizing, no watcher implementation, no `main.py` changes, no schema changes, no runner-code changes, and no chart-outcome-code changes.

## Recommended Next Task

Design the QQQ Continuation real historical replay v1 fixture from the selected source-data window, preserving the source-data/no-hindsight boundary and staying signal/stage/lifecycle only.
