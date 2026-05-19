# SAFE-FAST IWM Sample Source Extraction Review

## Review Status

- Review status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Work mode: build work only, no live trade decisions

## Baseline Checked

- Current HEAD: `7d67095 Add IWM sample sourcing method review`
- IWM active target: yes; IWM remains the active broader coverage target.
- Trigger-card contracts complete for this phase: yes.
- IWM sourcing method review result: PASS; SPY/QQQ used read-only dxLink 1H RTH source CSV export, source validation, bounded source-window selection, replay validation, and chart-only outcome validation, and the same method can be reused for IWM.
- SPY/QQQ closeout remains accepted: yes.
- GLD deferred: yes.
- Continuous Watcher deferred: yes.

## Repo State Checked

- Git status result before edits: `## main...origin/main`
- Latest commits:
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
  - `5dc2481 Add on-demand trigger card requirement review`
- Conflicts found: none. Working tree was clean before this task, and expected HEAD `7d67095` was present.

## SPY/QQQ Source CSV Method

SPY and QQQ used a repo-backed source-data method, not manual chart hunting.

- Source CSV type: read-only dxLink OHLCV source CSV exported by `historical_signal_replay/export_dxlink_source_csv.py`.
- Timeframe/session: `1h_rth`, regular-session rows, `America/New_York`, `regular_session=true`.
- Template: `historical_signal_replay/source_data/templates/first_real_historical_replay_v1_source_template.csv`.
- SPY source CSV: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`.
- QQQ source CSV: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`.
- Source metadata: `source=dxlink_candles.get_1h_ema50_snapshot`, `data_vendor=dxFeed via tastytrade dxLink`, populated `source_as_of`.
- Context metadata: 24H/daily, macro, IV, and event context fields remain explicitly unconfirmed when unavailable.

Exact source CSV columns:

```text
symbol,timestamp,timezone,session_date,session_type,regular_session,timeframe,open,high,low,close,volume,source,source_as_of,data_vendor,context_24h_status,context_24h_as_of,macro_context_status,macro_context_as_of,iv_context_status,iv_context_as_of,event_context_status,event_context_as_of,notes
```

The validation step used by SPY/QQQ checked:

- file exists
- header matches the required template
- one allowed symbol only
- `1h_rth` timeframe/session fields
- timezone-aware ISO 8601 timestamps
- `America/New_York` RTH session interpretation
- regular-session rows and strict timestamp ordering
- numeric OHLCV
- non-negative volume
- high/low internally contain open/close
- populated source, `source_as_of`, and vendor fields
- unavailable context fields explicitly unconfirmed
- no outcome/profit/P&L/account-sizing/option/broker/order/execution fields
- no after-the-fact setup, trigger, blocker, lifecycle, or outcome labels
- no-hindsight source-data boundary

The bounded window-selection process used by SPY/QQQ was:

1. Start only from an accepted source CSV.
2. Select contiguous bounded `1h_rth` source rows for one candidate setup family.
3. Keep the selected setup family as a candidate until fixture design confirms row-by-row evidence.
4. Avoid overlapping already-selected windows when adding additional setup-family samples.
5. Document selected start/end timestamps, selected row count, candidate family, source-only rationale, no-hindsight result, known limits, and boundary result.
6. Do not create fixtures, edit OHLCV, add labels, calculate chart outcomes, model option P&L, add account sizing, change `main.py`, change schemas, change runners, or start watcher work in the window-selection review.

SPY selected:

- Continuation: `historical_signal_replay/source_data/FIRST_REAL_SPY_WINDOW_SELECTION_REVIEW.md`
- Ideal: `historical_signal_replay/source_data/SECOND_REAL_SPY_WINDOW_SELECTION_REVIEW.md`
- Clean Fast Break: `historical_signal_replay/source_data/THIRD_REAL_SPY_WINDOW_SELECTION_REVIEW.md`

QQQ selected:

- Ideal: `historical_signal_replay/source_data/QQQ_FIRST_WINDOW_SELECTION_REVIEW.md`
- Clean Fast Break: `historical_signal_replay/source_data/QQQ_CLEAN_FAST_BREAK_WINDOW_SELECTION_REVIEW.md`
- Continuation: `historical_signal_replay/source_data/QQQ_CONTINUATION_WINDOW_SELECTION_REVIEW.md`

The replay/chart-outcome chain after source windows were selected was:

1. Fixture design review from the selected source window.
2. Fixture creation review copying accepted source OHLCV rows without invented data.
3. Historical signal replay runner output validation.
4. Per-setup replay evidence and next-step review.
5. Three-setup real historical replay closeout.
6. Chart-only outcome calculation for accepted replay-derived candidates.
7. Chart outcome output validation.
8. Aggregate chart outcome summary and output validation.
9. Chart outcome closeout.

This chain remains signal/stage/lifecycle first, then chart-only outcome. It does not prove option P&L, account sizing, watcher readiness, production readiness, or live trade readiness.

## IWM Source CSV Availability

- IWM source CSV found: no

No repo file matching an accepted IWM dxLink source CSV was found. Specifically, this expected SPY/QQQ-shaped path is not present:

```text
historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv
```

Expected IWM CSV template/columns are the same as the SPY/QQQ template:

```text
historical_signal_replay/source_data/templates/first_real_historical_replay_v1_source_template.csv
```

Expected IWM filename/path, based on the existing SPY/QQQ incoming-file convention:

```text
historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv
```

Expected exporter command shape, based on `historical_signal_replay/export_dxlink_source_csv.py`:

```text
python -B historical_signal_replay/export_dxlink_source_csv.py --symbol IWM --output historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv
```

Smallest missing input: the IWM read-only dxLink `1h_rth` source CSV in the same SPY/QQQ template, or access/path to the exporter output if it already exists outside the repo.

Codex can proceed without user chart hunting if the dxLink CSV/export method is available. It cannot proceed to IWM source validation, window selection, fixtures, replay, or chart outcomes without the IWM source CSV or exporter access/output.

## Extraction / Validation Plan For IWM

1. Obtain or generate IWM read-only dxLink 1H RTH source CSV using the same template as SPY/QQQ.
2. Validate the IWM source CSV shape.
3. Create IWM bounded source-window selection review.
4. Select candidate windows for Ideal / Clean Fast Break / Continuation.
5. Populate IWM historical sample collection worksheet.
6. Create IWM real historical replay review assets.
7. Create IWM chart-only outcome reviews.
8. Create IWM aggregate closeout review.

Validation should use the SPY/QQQ checks: template header, single allowed symbol `IWM`, `1h_rth`, regular RTH rows, timezone-aware timestamps, ordered source rows, numeric internally valid OHLCV, source/vendor/as-of metadata, explicit unconfirmed context fields where unavailable, no forbidden P&L/account/option/broker/outcome fields, and no after-the-fact labels.

## User Input Required

- User input required: yes

Smallest possible input:

- provide the IWM dxLink 1H RTH source CSV in the same template as SPY/QQQ, or
- provide the location of an existing IWM source CSV/export, or
- provide access/path to the exporter output folder.

Manual chart hunting is not required by repo evidence. The missing input is the repo-backed IWM source export, not manually identified chart dates or setup facts.

## Exact Next Task

Create IWM source CSV export request/instruction review using the SPY/QQQ dxLink 1H RTH template.

This is the correct next task because the IWM CSV does not exist in the repo, while the exporter/template/source method is known.

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

- IWM source CSV availability/validation
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
