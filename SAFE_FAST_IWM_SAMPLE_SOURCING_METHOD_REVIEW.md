# SAFE-FAST IWM Sample Sourcing Method Review

## Review Status

- Review status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Work mode: build work only, no live trade decisions

## Baseline Checked

- Current HEAD: `be35e52 Add IWM sample evidence intake review`
- IWM active target: yes; IWM remains the active broader coverage target after SPY + QQQ closeout.
- Trigger-card coverage complete for this phase: yes; trigger-card surface contracts for this phase are complete.
- IWM intake review found no concrete IWM samples: yes; `SAFE_FAST_IWM_SAMPLE_EVIDENCE_INTAKE_REVIEW.md` found no concrete IWM sample windows/evidence in repo.
- SPY/QQQ closeout remains accepted: yes; no reviewed evidence changes SPY or QQQ closeout.
- GLD deferred: yes.
- Continuous Watcher deferred: yes.

## Repo State Checked

- Git status result: `## main...origin/main`
- Latest commits:
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
  - `5d114c8 Add IWM historical sample collection worksheet`
- Conflicts found: none. Working tree was clean before this task, and expected HEAD `be35e52` was present.

## SPY Sample Source Findings

SPY samples were sourced from an accepted read-only dxLink source-data export, not from manually supplied chart screenshots.

Repo-backed sequence:

1. `historical_signal_replay/export_dxlink_source_csv.py` defines a read-only source CSV exporter using `dxlink_candles.get_1h_ema50_snapshot`, with allowed symbols including `SPY`, `QQQ`, `IWM`, and `GLD`.
2. `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` was created from dxFeed via tastytrade dxLink.
3. `historical_signal_replay/source_data/FIRST_REAL_SOURCE_HISTORICAL_DATA_VALIDATION_REVIEW.md` accepted that SPY CSV: 293 `1h_rth` rows from `2026-03-16T09:30:00-04:00` through `2026-05-13T14:30:00-04:00`, sourced from `dxlink_candles.get_1h_ema50_snapshot`.
4. SPY window-selection reviews selected bounded candidate windows from that accepted source CSV:
   - Continuation: `historical_signal_replay/source_data/FIRST_REAL_SPY_WINDOW_SELECTION_REVIEW.md`
   - Ideal: `historical_signal_replay/source_data/SECOND_REAL_SPY_WINDOW_SELECTION_REVIEW.md`
   - Clean Fast Break: `historical_signal_replay/source_data/THIRD_REAL_SPY_WINDOW_SELECTION_REVIEW.md`
5. SPY fixture design, fixture creation, runner output validation, and closeout artifacts were then created from those selected source windows.
6. SPY chart outcome samples were downstream of the accepted replay-derived candidates and real SPY source rows, then summarized in chart-only aggregate reports.

SPY therefore used existing repo source CSVs, window-selection reviews, replay fixtures/reports, and chart outcome fixtures/reports. The repo evidence does not show SPY samples being sourced from user-manual screenshot collection.

## QQQ Sample Source Findings

QQQ used the same repo-backed source-data pattern as SPY.

Repo-backed sequence:

1. `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` was created from dxFeed via tastytrade dxLink.
2. `historical_signal_replay/source_data/QQQ_FIRST_REAL_SOURCE_HISTORICAL_DATA_VALIDATION_REVIEW.md` accepted that QQQ CSV: 301 `1h_rth` data rows from `2026-03-16T15:30:00-04:00` through `2026-05-15T14:30:00-04:00`, sourced from `dxlink_candles.get_1h_ema50_snapshot`.
3. QQQ window-selection reviews selected bounded candidate windows from that accepted source CSV:
   - Ideal: `historical_signal_replay/source_data/QQQ_FIRST_WINDOW_SELECTION_REVIEW.md`
   - Clean Fast Break: `historical_signal_replay/source_data/QQQ_CLEAN_FAST_BREAK_WINDOW_SELECTION_REVIEW.md`
   - Continuation: `historical_signal_replay/source_data/QQQ_CONTINUATION_WINDOW_SELECTION_REVIEW.md`
4. QQQ fixture design/creation, runner output validation, evidence reviews, and closeout artifacts were created from those selected source windows.
5. QQQ chart outcome samples were downstream of accepted QQQ replay evidence and source rows, then validated and summarized in `chart_trade_outcome_backtesting/reports/qqq_three_setup_chart_outcome_summary_v1.json`.

QQQ samples were therefore created from the same documented source-data extraction and repo review chain, not from manual user chart hunting.

## IWM Evidence Gap

IWM currently has planning, candidate inventory, worksheet slots, intake review, and trigger-card field requirements. It does not have the concrete source-data layer that SPY and QQQ had.

IWM has:

- IWM-first broader coverage decision and planning reviews.
- Required candidate slots for Ideal, Clean Fast Break, Continuation, stage correctness, session-boundary, winner-selection, no-trade discipline, chart-only outcome, and aggregate closeout.
- A worksheet defining the concrete fields needed before replay/fixture creation.
- Intake review confirmation that existing IWM-like shape fixtures are not real IWM evidence.
- Trigger-card field requirements for future IWM samples.

IWM does not have:

- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`
- IWM source-data validation review.
- IWM bounded source-window selection reviews.
- IWM real historical replay fixture design/creation reviews.
- IWM fixture JSON.
- IWM replay signal logs, summaries, or regression candidate reports.
- IWM chart outcome fixtures/reports.
- IWM aggregate chart outcome summary or closeout.

The concrete missing input is not broad manual chart hunting. The missing repo-backed input is accepted IWM 1H RTH source data, then bounded IWM source-window selection from that data.

## Can SPY/QQQ Method Be Reused For IWM?

YES

The same method can be reused because the source-data intake spec allows `IWM`, and `historical_signal_replay/export_dxlink_source_csv.py` explicitly includes `IWM` in `ALLOWED_SYMBOLS`. The documented SPY/QQQ process is repeatable for IWM:

1. Export read-only IWM 1H RTH OHLCV source rows using the existing dxLink source CSV exporter.
2. Validate the IWM source CSV against the existing source-data intake spec and template.
3. Select bounded IWM candidate source windows for Ideal, Clean Fast Break, and Continuation.
4. Only after source validation and window selection, design/create IWM replay fixtures and output validations.
5. Only after accepted replay-derived candidates, create IWM chart-only outcome samples and aggregate closeout.

Codex/repo work can produce the missing IWM samples without asking the user to hunt charts, provided the read-only dxLink export can be run in an environment with the required market-data credentials and network access. If that environment is unavailable, the smallest user input would be one accepted IWM source CSV exported in the existing template format, not a broad request to manually find all samples.

This does not change SPY/QQQ closeout. SPY and QQQ remain accepted because this review only identifies the sourcing method and IWM gap.

This does block IWM fixture/replay/chart-outcome creation until IWM source-data export and IWM source-window selection are completed. It does not block the next docs/replay-prep task to create the IWM sample source extraction review.

## Exact Next Task

Create IWM sample source extraction review using the same SPY/QQQ sourcing method.

The review should stay docs/replay-prep unless explicitly authorized to run the read-only exporter. It should define the exact IWM export target, validation checklist, expected source CSV path, and follow-on IWM window-selection sequence without creating fixtures, changing replay runner logic, changing schemas, changing generated reports, touching `main.py`, touching Railway/production, or making live trade decisions.

User input required: no chart hunting required. If the read-only export environment is unavailable, the smallest possible user input is one IWM source CSV in the existing historical signal replay source-data template format, with real IWM 1H RTH OHLCV rows and source metadata.

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

- IWM concrete sample sourcing
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
