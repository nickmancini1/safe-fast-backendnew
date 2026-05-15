# SAFE-FAST QQQ Broader Chart Outcome Coverage Start Review

## Review Status

- **Review status:** PASS
- **Baseline:** patch8
- **Latest local commit before review:** `ef92993 Add broader chart outcome coverage plan`
- **Scope:** docs-only QQQ broader chart outcome coverage start review.

This review starts QQQ coverage only as source-data validation and real historical replay planning. It does not pull new market data, create fixtures, implement calculations, change `main.py`, change schemas, change runner code, change chart outcome code, model option P&L, add account sizing, or start watcher implementation.

## Reason QQQ Is Next

QQQ is next because the broader coverage plan sets the order as QQQ, then IWM, then GLD, and QQQ is an allowed SAFE-FAST universe symbol with equity-index behavior closest to the already validated SPY proof surface.

Watcher implementation remains deferred because the current chart outcome evidence is limited to three SPY samples, one per setup family.

## Current SPY Evidence Summary

- **Validated SPY chart outcome samples:** 3
- **Setup families covered:** Continuation, Ideal, Clean Fast Break
- **Terminal outcomes:** 2 follow-through, 0 invalidated/failure, 1 time stop
- **Aggregate MFE:** average 1.5817 points / 0.2177% / 0.1922R; max 2.29 points / 0.3199% / 0.3074R
- **Aggregate MAE:** average 0.3617 points / 0.0507% / 0.0547R; max 0.735 points / 0.105% / 0.1286R
- **Same-day/fast-swing classification:** 2 same-day, 1 time-stop same-day
- **Boundary:** chart-only evidence, not profitability proof, not option P&L, not account sizing, not watcher readiness

## QQQ Source Data Status

- **QQQ source data already exists:** NO
- **Inspected source-data folder:** `historical_signal_replay/source_data/`
- **Existing incoming source CSVs:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- **Required next QQQ source-data target file path:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`

No new QQQ data pull was started by this review.

## Existing dxLink Exporter Support

- **Existing exporter supports QQQ:** YES
- **Exporter file:** `historical_signal_replay/export_dxlink_source_csv.py`
- **Evidence:** `ALLOWED_SYMBOLS = {"SPY", "QQQ", "IWM", "GLD"}` and the CLI accepts `--symbol` plus `--output`.
- **Required use for QQQ:** run only in a later explicitly authorized data-pull task with `--symbol QQQ` and the QQQ target output path.

## Required QQQ Timeframe And Session

- **Symbol:** QQQ only
- **Timeframe:** 1H RTH
- **Session:** regular session only
- **Timezone:** America/New_York
- **Required source metadata:** source, source as-of time, data vendor, symbol, timeframe, and row count
- **Required row properties:** ordered timestamps, session-valid rows, present and internally valid OHLCV values
- **Unavailable context:** 24H/daily, macro, IV, event, headline, option, account, and broker fields must remain unavailable or unconfirmed unless a reviewed source supplies them

## Setup-Family Coverage Target

QQQ coverage should target the same setup families as the SPY proof surface:

- Ideal
- Clean Fast Break
- Continuation

Each QQQ setup-family candidate must start from validated real source rows and no-hindsight historical replay evidence before any chart outcome calculation.

## No-Hindsight Rules

- Source rows must be available at or before the replay row timestamp.
- QQQ window selection must not depend on later outcome success.
- Replay fixtures must not include future-row labels, P&L, option results, account sizing, broker/order outcomes, or chart outcome conclusions.
- Trigger and invalidation references must come from replay-visible chart evidence.
- Chart outcome calculation may look forward only after a replay-derived QQQ candidate is frozen for outcome measurement.
- Gap cause, macro, IV, event, headline, option, account, and broker fields must remain unavailable or unconfirmed unless an approved source supplies them.

## Watcher Deferral

- **Watcher remains deferred:** YES
- **Reason:** QQQ/IWM/GLD broader replay plus chart outcome coverage and aggregate summaries are not completed.
- **Watcher implementation started:** NO

## Boundary Result

- **Boundary result:** PASS
- **New data pull started:** NO
- **Fixture created:** NO
- **Chart outcome calculation started:** NO
- **Option P&L modeled:** NO
- **Account sizing added:** NO
- **`main.py` changed:** NO
- **Schemas changed:** NO
- **Runner code changed:** NO
- **Chart outcome code changed:** NO

## Recommended Next Task

Pull the first real QQQ 1H RTH dxLink source CSV into `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` and perform a bounded source-data validation review only. Do not create fixtures or calculate chart outcomes in that task unless explicitly authorized after source validation passes.
