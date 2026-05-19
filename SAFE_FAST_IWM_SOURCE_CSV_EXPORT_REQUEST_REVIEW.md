# SAFE-FAST IWM Source CSV Export Request / Instruction Review

## Review Status

- Review status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Work mode: build work only, no live trade decisions

## Baseline Checked

- Current HEAD: `a8e597d Add IWM sample source extraction review`
- IWM active target: yes; IWM remains the active broader coverage target.
- Trigger-card contracts complete for this phase: yes.
- IWM source extraction result: PASS; IWM source CSV was not found, and the smallest missing input is IWM dxLink 1H RTH source CSV in the SPY/QQQ template, an existing export location, or exporter output access/path.
- SPY/QQQ closeout remains accepted: yes.
- GLD deferred: yes.
- Continuous Watcher deferred: yes.

## Repo State Checked

- Git status result: `## main...origin/main`
- Latest commits:
  - `a8e597d Add IWM sample source extraction review`
  - `7d67095 Add IWM sample sourcing method review`
  - `be35e52 Add IWM sample evidence intake review`
  - `d202a33 Add missing-data trigger card surface contract`
  - `1318fa4 Add near-trigger early warning trigger card surface contract`
  - `1f6b5f1 Add blocked identifiable trigger card surface contract`
  - `7b46718 Add put-side trigger card surface contract`
  - `79fbe77 Add Clean Fast Break trigger card surface contract`
  - `8a1c4c4 Add Ideal trigger card surface contract`
  - `4954a91 Add Day 60 product business handoff addendum`
  - `6f322c1 Add Continuation trigger card surface contract`
  - `de65702 Add trigger card surface contract gap review`
- Conflicts found: none. Working tree was clean before this task, and expected HEAD `a8e597d` was present.

## SPY/QQQ CSV Template Findings

SPY/QQQ used the header-only template at:

```text
historical_signal_replay/source_data/templates/first_real_historical_replay_v1_source_template.csv
```

Exact source CSV header:

```text
symbol,timestamp,timezone,session_date,session_type,regular_session,timeframe,open,high,low,close,volume,source,source_as_of,data_vendor,context_24h_status,context_24h_as_of,macro_context_status,macro_context_as_of,iv_context_status,iv_context_as_of,event_context_status,event_context_as_of,notes
```

Required timeframe/session from repo evidence:

- Timeframe: `1h_rth`
- Session: regular U.S. equity ETF RTH rows
- Timezone/session interpretation: `America/New_York`
- Regular-session flag: `regular_session=true`
- Source/vendor convention: `source=dxlink_candles.get_1h_ema50_snapshot`, `data_vendor=dxFeed via tastytrade dxLink`

SPY source CSV path:

```text
historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv
```

QQQ source CSV path:

```text
historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv
```

Repo validation reviews accepted SPY and QQQ only after file existence, exact header/template match, single-symbol rows, timezone-aware timestamps, strict RTH/session metadata, numeric valid OHLCV, non-negative volume, populated source/vendor/as-of metadata, explicit unconfirmed context fields where unavailable, no forbidden outcome/P&L/account/option/broker/execution fields, no after-the-fact labels, and no-hindsight source-data boundary.

## Exporter / Source Access Findings

- Exporter/source process found: yes

Exporter script:

```text
historical_signal_replay/export_dxlink_source_csv.py
```

Exporter evidence:

- `ALLOWED_SYMBOLS = {"SPY", "QQQ", "IWM", "GLD"}`
- reads the same template header
- writes `timeframe=1h_rth`
- filters RTH bars from 9:30 AM through before 4:00 PM America/New_York
- uses `dxlink_candles.get_1h_ema50_snapshot`
- requires tastytrade/dxLink environment credentials for non-dry-run export
- does not import `main.py` or execute trade/order paths

Exact IWM export instruction, using the same SPY/QQQ method:

```text
python -B historical_signal_replay/export_dxlink_source_csv.py --symbol IWM --output historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv
```

Optional setup check without network request or file write:

```text
python -B historical_signal_replay/export_dxlink_source_csv.py --symbol IWM --output historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv --dry-run
```

Placeholder only where unavoidable: exporter execution requires the repo's tastytrade/dxLink credential environment variables and network/source access outside this docs-only review.

## Requested IWM Source CSV

- Symbol: IWM
- Source: dxLink
- Timeframe/session: `1h_rth`, regular RTH
- Template: same as SPY/QQQ, `historical_signal_replay/source_data/templates/first_real_historical_replay_v1_source_template.csv`
- Expected filename/path:

```text
historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv
```

- Required columns/header:

```text
symbol,timestamp,timezone,session_date,session_type,regular_session,timeframe,open,high,low,close,volume,source,source_as_of,data_vendor,context_24h_status,context_24h_as_of,macro_context_status,macro_context_as_of,iv_context_status,iv_context_as_of,event_context_status,event_context_as_of,notes
```

- No invented chart windows, setup labels, trigger labels, outcomes, levels, option fields, account sizing, broker/order/execution fields, or live trade decisions.

## Immediate Validation After CSV Is Supplied

Next validation task: create IWM source CSV validation review.

The IWM source CSV validation review should check:

- file exists at the expected IWM source CSV path or at the supplied exporter output path
- header/template exactly matches SPY/QQQ
- symbol is `IWM` only
- rows are valid real source rows
- timestamps are ISO 8601 and timezone-aware
- timezone/session metadata align with `America/New_York` `1h_rth` RTH expectations
- rows are regular-session rows and ordered chronologically
- OHLCV values are numeric, internally valid, and volume is non-negative
- source, `source_as_of`, and `data_vendor` are populated
- unavailable 24H/daily, macro, IV, and event context fields are explicitly unconfirmed
- no generated replay/chart outcome assumptions yet
- no after-the-fact setup, trigger, blocker, lifecycle, outcome, option P&L, account sizing, broker/order/execution, production, or live-trading fields

## Exact Next Task

Run/export IWM dxLink 1H RTH source CSV using documented command, then create IWM source CSV validation review.

If exporter credentials/network/source access are unavailable in the working environment, provide IWM dxLink 1H RTH source CSV or exporter output path/access, then create IWM source CSV validation review.

## Boundary Check

- main.py changed: no
- engine logic changed: no
- replay runner changed: no
- schemas changed: no
- fixtures changed: no
- reports changed: no
- Railway touched: no
- production touched: no
- Continuous Watcher implementation started: no
- option P&L modeled: no
- account sizing added: no
- auto-trading added: no
- live trade decisions added: no

## What Remains Unproven

- IWM source CSV availability
- IWM source CSV validation
- IWM sample population
- IWM replay/fixture creation
- IWM chart-only outcomes
- IWM aggregate closeout
- GLD broader coverage
- Continuous Watcher behavior
- alert suppression
- shadow/live validation
- option P&L
- account sizing
- production readiness
