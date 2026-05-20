# SAFE-FAST GLD Broader Coverage Preparation / Source-Sourcing Review

## Review Status

- Review status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Work mode: build work only, no live trade decisions

## Baseline Checked

- Current HEAD: `e4608bc Add IWM chart outcome closeout review`
- SPY current-depth closeout complete: yes.
- QQQ current-depth closeout complete: yes.
- IWM current-depth closeout complete at known-limits depth: yes.
- GLD now next broader coverage target: yes.
- Continuous Watcher deferred: yes.
- Day 60 target preserved: yes; the Day 60 addendum still targets a shadow watcher covering SPY / QQQ / IWM / GLD, but this task does not start watcher implementation.

## Repo State Checked

- Git status result: `## main...origin/main`
- Latest commits:
  - `e4608bc Add IWM chart outcome closeout review`
  - `ebc3a75 Add IWM chart outcome aggregate summary review`
  - `d288fc6 Add IWM Continuation 001 chart-only outcome review`
  - `680c2d2 Add IWM Clean Fast Break 001 chart-only outcome review`
  - `bf3cc2b Add IWM Ideal 001 chart-only outcome review`
  - `490152f Add IWM chart-only outcome phase planning review`
  - `1ce64f7 Add IWM Continuation 001 replay fixture output validation`
  - `9093764 Add IWM Continuation 001 replay fixture asset`
  - `fda5d32 Add IWM Continuation 001 replay fixture specification review`
  - `2727576 Add IWM Continuation 001 real historical replay review`
  - `baa36b6 Add IWM Continuation 001 replay readiness review`
  - `be235a1 Add IWM Clean Fast Break 001 replay fixture output validation`
- Conflicts found: none. The worktree was clean before this docs-only review.
- Known non-conflict preserved: `SAFE_FAST_BUILD_STATE.md` may list `5d33edc` as the completed QQQ closeout milestone while Git HEAD is newer.

## Prior Symbol Source Method

Repo-backed SPY / QQQ / IWM broader coverage used the same source method:

- Source method: read-only dxLink 1H RTH source CSV.
- Exporter: `historical_signal_replay/export_dxlink_source_csv.py`.
- Source CSV template/header: `historical_signal_replay/source_data/templates/first_real_historical_replay_v1_source_template.csv`.
- Header:

```text
symbol,timestamp,timezone,session_date,session_type,regular_session,timeframe,open,high,low,close,volume,source,source_as_of,data_vendor,context_24h_status,context_24h_as_of,macro_context_status,macro_context_as_of,iv_context_status,iv_context_as_of,event_context_status,event_context_as_of,notes
```

- Required session/timeframe convention: `1h_rth`, `America/New_York`, regular-session rows, `regular_session=true`.
- Source/vendor convention: `source=dxlink_candles.get_1h_ema50_snapshot`, `data_vendor=dxFeed via tastytrade dxLink`, populated `source_as_of`.
- Source validation: file existence, exact header match, single-symbol rows, timezone-aware timestamps, chronological RTH rows, numeric internally valid OHLCV, non-negative volume, populated source/vendor/as-of metadata, explicitly unconfirmed unavailable context fields, and no forbidden outcome/P&L/account/option/broker/execution or after-the-fact label fields.
- Bounded source-window selection: select contiguous candidate windows only after source validation, document row counts and no-hindsight limits, and avoid fixture/report/engine/schema changes in the window-selection review.
- Fixture/replay validation: create per-setup replay readiness/review/spec/fixture/output validation chains for Ideal, Clean Fast Break, and Continuation.
- Chart-only outcome review: create per-setup chart-only outcome reviews after replay evidence, then aggregate summary and closeout.
- Aggregate closeout: SPY, QQQ, and IWM each closed at current known-limits depth before moving to the next target.

## GLD Evidence Search

- GLD source CSV found: no.
- GLD replay docs found: no GLD-specific replay readiness, replay review, fixture specification, fixture asset, or replay output validation docs were found.
- GLD chart outcome docs found: no GLD-specific chart-only outcome reviews, aggregate summary, or closeout docs were found.
- GLD fixtures found: no GLD-named fixture files were found.
- Existing GLD references: planning/source-scope references identify GLD as part of the intended SPY / QQQ / IWM / GLD coverage universe, and `historical_signal_replay/export_dxlink_source_csv.py` includes `GLD` in `ALLOWED_SYMBOLS`. These are not GLD source rows, replay evidence, chart windows, outcomes, levels, or setup facts.

## GLD Source CSV Availability

- GLD source CSV found: no.

Expected source CSV path:

```text
historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv
```

Expected source/export method:

- Use the existing read-only dxLink source CSV exporter.
- Export `GLD` 1H RTH OHLCV rows into the same SPY/QQQ/IWM source template.
- Do not invent GLD dates, candles, chart windows, outcomes, levels, setup labels, trigger labels, or replay facts.

Smallest missing input:

- The GLD dxLink `1h_rth` source CSV at the expected path, or a supplied exporter output path containing the same template/header and real GLD source rows.

## Exporter / Source Access

- Exporter found: yes.
- Exporter path: `historical_signal_replay/export_dxlink_source_csv.py`.
- Exporter evidence: `ALLOWED_SYMBOLS = {"SPY", "QQQ", "IWM", "GLD"}`; the script reads the shared source template, filters RTH bars, writes `timeframe=1h_rth`, uses `dxlink_candles.get_1h_ema50_snapshot`, and does not import `main.py` or execute order/trade paths.
- Source access status: exporter exists, but actual export execution requires tastytrade/dxLink credential environment variables and network/source access. This review did not run the export.

Exact command template supported by repo evidence:

```text
python -B historical_signal_replay/export_dxlink_source_csv.py --symbol GLD --output historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv
```

Optional local setup check without network request or file write:

```text
python -B historical_signal_replay/export_dxlink_source_csv.py --symbol GLD --output historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv --dry-run
```

## GLD Coverage Plan

1. Export or supply GLD dxLink 1H RTH source CSV.
2. Validate GLD source CSV.
3. Select bounded GLD source windows.
4. Populate GLD historical sample worksheet.
5. Create GLD Ideal replay readiness/review/spec/fixture/output validation chain.
6. Create GLD Clean Fast Break replay readiness/review/spec/fixture/output validation chain.
7. Create GLD Continuation replay readiness/review/spec/fixture/output validation chain.
8. Create GLD chart-only outcome phase planning.
9. Create GLD per-setup chart-only outcome reviews.
10. Create GLD aggregate chart outcome summary.
11. Create GLD chart outcome closeout review.
12. Only after SPY/QQQ/IWM/GLD current-depth closeout, revisit Continuous Watcher foundation.

## Exact Next Task

Export GLD dxLink 1H RTH source CSV, then create GLD source CSV validation review.

If exporter credentials/network/source access are blocked in the working environment, create a GLD source CSV export blocked review or supply exporter credentials/access/output path. Do not proceed to GLD bounded window selection, fixtures, replay, chart outcomes, or aggregate closeout until the GLD source CSV is exported or supplied and validated.

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

- GLD source CSV availability/validation
- GLD bounded source-window selection
- GLD sample population
- GLD replay/fixture execution
- GLD chart-only outcomes
- GLD aggregate closeout
- Continuous Watcher behavior
- alert suppression
- shadow/live validation
- option P&L
- account sizing
- production readiness
