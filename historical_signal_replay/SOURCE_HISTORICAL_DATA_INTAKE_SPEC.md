# SAFE-FAST Source Historical Data Intake Spec

## Purpose

This spec defines the strict source historical data intake requirements for the first real historical replay v1 source file.

The source file is used only to support future signal/stage/lifecycle replay fixture creation. It is not a real historical replay implementation, trade outcome backtest, option P&L model, account sizing model, production workflow, live trading workflow, or Continuous Watcher implementation.

## Allowed Symbols

Only these symbols are allowed:

- `SPY`
- `QQQ`
- `IWM`
- `GLD`

Rows for any other symbol are out of scope for the first real historical replay v1 source file.

## Allowed Source-Data Purpose

The source data may be used only for historical signal/stage/lifecycle replay validation.

It may support later review of setup state, stage, lifecycle transition, blocker, caution, session context, no-hindsight behavior, and duplicate/state-change behavior. It must not include or imply trade profitability, option economics, account sizing, broker execution, live trade decisions, or production readiness.

## Required Columns

The first source CSV must include exactly these columns:

```text
symbol,timestamp,timezone,session_date,session_type,regular_session,timeframe,open,high,low,close,volume,source,source_as_of,data_vendor,context_24h_status,context_24h_as_of,macro_context_status,macro_context_as_of,iv_context_status,iv_context_as_of,event_context_status,event_context_as_of,notes
```

Required column meanings:

- `symbol`: one allowed symbol only.
- `timestamp`: timezone-aware bar timestamp.
- `timezone`: timezone used to interpret the row, expected `America/New_York` for RTH session interpretation.
- `session_date`: trading session date in `YYYY-MM-DD`.
- `session_type`: one of `regular`, `short`, `closed`, or `unknown`.
- `regular_session`: boolean-style value, expected `true` or `false`.
- `timeframe`: source bar interval, for example `1h_rth` when the file contains RTH hourly bars.
- `open`, `high`, `low`, `close`: real sourced OHLC values.
- `volume`: real sourced volume, numeric and non-negative.
- `source`: source location or source document/feed identifier for the row.
- `source_as_of`: timestamp when the source data was obtained or exported.
- `data_vendor`: vendor, platform, feed, or provider name.
- `context_24h_status`: real context status or explicit unconfirmed status.
- `context_24h_as_of`: as-of timestamp for 24H/daily context, or blank when unconfirmed.
- `macro_context_status`: real context status or explicit unconfirmed status.
- `macro_context_as_of`: as-of timestamp for macro context, or blank when unconfirmed.
- `iv_context_status`: real context status or explicit unconfirmed status.
- `iv_context_as_of`: as-of timestamp for IV context, or blank when unconfirmed.
- `event_context_status`: real context status or explicit unconfirmed status.
- `event_context_as_of`: as-of timestamp for event/headline/gap-risk context, or blank when unconfirmed.
- `notes`: optional source notes. Notes must not add invented market facts or after-the-fact trade outcomes.

## Accepted Timestamp Format

Use ISO 8601 timezone-aware timestamps.

Accepted examples:

- `2026-04-23T09:30:00-04:00`
- `2026-04-23T13:30:00Z`

Do not use naive timestamps without an offset or timezone marker.

## Timezone Requirement

Use `America/New_York` for RTH session interpretation. If the raw source exports UTC timestamps, preserve the source timestamp and identify the interpretation timezone in `timezone`.

Do not infer session context from a later timestamp. Session metadata must match what is knowable at the row timestamp.

## RTH And Regular-Session Requirement

The first source file should contain regular trading hours bars only.

For standard U.S. equity ETF sessions, RTH means 9:30 AM to 4:00 PM America/New_York, except short or closed sessions. If the source contains premarket, postmarket, overnight, or mixed extended-hours data, do not use it for the first source file unless those rows are removed or clearly excluded before fixture conversion.

## Session Date And Type Requirement

Each row must include:

- `session_date` as `YYYY-MM-DD`
- `session_type` as `regular`, `short`, `closed`, or `unknown`
- `regular_session` as `true` or `false`
- `timezone` as the session interpretation timezone

Prior-session, weekend, or holiday context must not be used to create a fresh current-session trigger.

## OHLCV Requirements

Each row must contain real sourced values for:

- `open`
- `high`
- `low`
- `close`
- `volume`

OHLC values must be numeric. `volume` must be numeric and non-negative.

Do not round, smooth, backfill, interpolate, or reconstruct missing values unless the source file explicitly documents that vendor-provided adjusted values are being used. Do not mix adjusted and unadjusted bars in one file without explicit source documentation.

## Source, Vendor, And As-Of Requirements

Each row must identify:

- `source`
- `source_as_of`
- `data_vendor`

`source_as_of` must be an ISO 8601 timestamp or date-time value describing when the source data was obtained, exported, or snapshotted. The vendor/source fields must be specific enough to trace the data back to the original provider or export.

## Context Fields Rule

Context fields must contain either real sourced context or an explicit unconfirmed status.

Allowed context status values:

- `CONFIRMED`
- `CONTEXT_24H_DAILY_UNCONFIRMED`
- `MACRO_UNCONFIRMED`
- `IV_UNCONFIRMED`
- `EVENT_UNCONFIRMED`
- `UNCONFIRMED`

If context is confirmed, include the matching `*_as_of` timestamp. If context is unavailable, use the specific unconfirmed status where applicable and leave the matching as-of field blank.

Do not infer macro, IV, event, headline, gap-risk, or 24H/daily context from later price action.

## No-Hindsight Rules

- Each row may use only market bars and context available at or before that row timestamp.
- Future candles must not be used to decide setup identity, trigger state, blocker priority, lifecycle state, or duplicate/state-change status.
- Session context must be assigned from the row timestamp, not from later session knowledge.
- Context fields must include real `as_of` timing when confirmed.
- Unavailable context must be marked unconfirmed instead of inferred.
- Row-level expected outputs in later fixtures must not rely on future trade outcome.
- A historical sequence may be selected after review, but the selected rows must remain no-hindsight at the row level.

## No Fabricated Data Rule

Do not invent or fabricate:

- timestamps
- OHLC values
- volume
- levels
- setup labels
- blocker labels
- lifecycle labels
- macro context
- IV context
- event or headline context
- source/vendor metadata

If valid source data is missing, stop and request the missing source data instead of creating placeholder market rows.

## Forbidden Data

The source file must not include:

- invented values
- after-the-fact setup labels
- after-the-fact trigger labels
- after-the-fact blocker labels
- after-the-fact outcome labels
- win/loss fields
- target-hit fields
- stop-hit fields
- expectancy fields
- option contract fields
- option price fields
- spread price fields
- option P&L fields
- slippage fields
- commission fields
- buying-power fields
- risk-per-trade fields
- position size fields
- account sizing fields
- broker/order/execution fields

## Minimum Row Requirement For First Source File

The first source file must include enough consecutive rows for one allowed symbol to support a multi-row signal/stage/lifecycle review without hindsight.

Minimum acceptable first file:

- one allowed symbol only
- one session or a clearly bounded session window
- at least 4 consecutive RTH bars
- complete OHLCV for every row
- complete session metadata for every row
- source/vendor/as-of metadata for every row
- context fields either confirmed with as-of timestamps or explicitly unconfirmed

Preferred first file:

- one allowed symbol only
- one regular RTH session
- 1H RTH bars aligned to regular-session cadence
- enough rows to review developing, pending/blocked/triggered, and spent/no-fresh-trigger or duplicate/state-change behavior if the historical structure supports it

## Recommended First Source File Naming Convention

Use:

```text
<symbol>_<YYYY-MM-DD>_<timeframe>_source.csv
```

Example naming shape only:

```text
SPY_YYYY-MM-DD_1h_rth_source.csv
```

Do not create an example filled file with fake data.

## Recommended First Source File Path

Place the first real source file at:

```text
historical_signal_replay/source_data/<symbol>_<YYYY-MM-DD>_<timeframe>_source.csv
```

The template file lives at:

```text
historical_signal_replay/source_data/templates/first_real_historical_replay_v1_source_template.csv
```

## Validation Checklist Before Fixture Conversion

Before converting source data into a replay fixture:

- Confirm the file contains one allowed symbol: `SPY`, `QQQ`, `IWM`, or `GLD`.
- Confirm all required columns are present.
- Confirm the file contains no fake/example market rows.
- Confirm timestamps are ISO 8601 and timezone-aware.
- Confirm session metadata is complete.
- Confirm bars are RTH-only for the intended first source file.
- Confirm OHLCV values are numeric and sourced.
- Confirm volume is non-negative.
- Confirm source, `source_as_of`, and `data_vendor` are filled.
- Confirm context fields are real sourced context or explicitly unconfirmed.
- Confirm no future bars are used for any row-level interpretation.
- Confirm no outcome, P&L, account sizing, option, broker, execution, or production fields are present.
- Confirm the source file has enough consecutive rows to support a multi-row signal/stage/lifecycle replay review.
- Confirm fixture conversion remains signal/stage/lifecycle only.

## Next Task

Add the first real source historical data file for one allowed symbol.
