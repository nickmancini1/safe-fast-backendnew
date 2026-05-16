# QQQ Real Historical Replay v1 Planning Review

## Planning Status

- **Planning status:** PASS
- **Baseline:** patch8
- **Latest local commit before planning:** `9afbb80 Add QQQ source data validation`
- **Scope:** docs-only QQQ real historical signal replay planning review from the accepted QQQ source CSV.

This planning review does not create fixtures, select final windows, calculate chart outcomes, pull new market data, change `main.py`, change schemas, change runner code, change chart outcome code, model option P&L, add account sizing, or start watcher implementation.

## Accepted QQQ Source Data Summary

- **Source CSV:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- **Source validation review:** `historical_signal_replay/source_data/QQQ_FIRST_REAL_SOURCE_HISTORICAL_DATA_VALIDATION_REVIEW.md`
- **Source validation status:** PASS
- **Source CSV accepted:** yes
- **Symbol:** QQQ
- **Timeframe:** `1h_rth`
- **Source CSV row count:** 301 data rows
- **Timestamp range:** `2026-03-16T15:30:00-04:00` through `2026-05-15T14:30:00-04:00`
- **Session window:** 2026-03-16 15:30 ET through 2026-05-15 14:30 ET; 44 session dates; partial boundary sessions are present because the exported window starts and ends intraday
- **Source:** `dxlink_candles.get_1h_ema50_snapshot`
- **Source as-of:** `2026-05-15T18:48:44Z`
- **Data vendor:** dxFeed via tastytrade dxLink
- **Context fields:** 24H, macro, IV, and event context fields remain explicitly unconfirmed

The accepted source CSV passed header, symbol, timestamp/session, OHLCV, source/as-of, unavailable-context, no-outcome, and no-after-the-fact-label checks. It is source data only, not a replay fixture, chart outcome file, option model, account-sizing model, watcher input, or live-trading artifact.

## Setup-Family Target

QQQ real historical signal replay planning targets the same setup families used by the SPY proof surface and broader coverage plan:

- Ideal
- Clean Fast Break
- Continuation

Each setup family must be reviewed from source-visible candle structure before any fixture design. A later task may select a bounded candidate source-data window, but this planning review does not select one.

## No-Hindsight Rules

- Candidate identification must use only rows available at or before the candidate row timestamp.
- Window selection must not depend on later outcome success, future candles, chart outcome labels, or hindsight profitability.
- Replay fixture design must not include future-row labels, P&L, option results, account sizing, broker/order outcomes, or chart outcome conclusions.
- Trigger, invalidation, blocker, caution, and lifecycle references must come from replay-visible chart evidence.
- Chart outcome calculation may look forward only after a replay-derived QQQ candidate is frozen in a later reviewed task.
- Gap cause, macro, IV, event, headline, option, account, and broker fields must remain unavailable or unconfirmed unless an approved reviewed source supplies them.

## Candidate Window Selection Rules

Candidate windows must be selected in a later bounded task using only accepted QQQ source rows and source-visible structure.

Selection rules:

- Select one bounded source-data window at a time unless a later task explicitly authorizes broader selection.
- Frame all windows as candidate-only until fixture design is separately reviewed.
- Prefer windows with enough pre-context and post-signal lifecycle rows to demonstrate formation, trigger-adjacent state, and post-trigger or spent/invalidated state without using outcome success as the reason for selection.
- Require a clear setup-family target before window extraction: Ideal, Clean Fast Break, or Continuation.
- Preserve the 1H RTH, America/New_York, ordered-row source boundary.
- Do not select a window because it produced a favorable chart outcome.
- Do not calculate MFE, MAE, terminal outcome, same-day outcome, option P&L, or account impact during window selection.
- Document source row count, timestamp range, setup-family rationale, and known unavailable context for any later selected candidate window.

## Lifecycle And Stage Requirements

Any later QQQ replay fixture design should preserve signal, stage, and lifecycle review only.

Requirements:

- Show setup-family formation or context before trigger-adjacent rows.
- Preserve setup identity through blockers, cautions, market-closed state, unavailable context, and session-boundary behavior when the source-visible evidence supports that identity.
- Include stage transitions that are meaningful for the selected family, such as developing context, pullback/retest/base, pending confirmation, trigger candidate, spent/follow-through context, invalidated, or blocked state as applicable.
- Keep output review limited to setup-family counts, stage counts, lifecycle sequence, signal log rows, summary rows, and boundary checks.
- Do not interpret replay output as profitability, trade outcome, option performance, watcher readiness, or live-trading readiness.

## Duplicate And State-Change Requirements

Later replay planning and fixture design should support future watcher proof requirements without starting watcher implementation.

Requirements:

- Distinguish a meaningful lifecycle or stage change from a repeated same-state row.
- Preserve enough source-row identity to support later state-change fingerprints: symbol, setup family, direction when known, timestamp, lifecycle/stage, trigger freshness, first blocker, first caution, and session date.
- Repeated same-state rows should be counted or reviewed as repeats, not treated as new alerts or new setup candidates.
- A fresh rebuild after spent, invalidated, or expired context must be represented as a new candidate only when source-visible evidence supports it.
- Do not implement alert suppression, watcher storage, schedulers, live polling, or alert delivery in this planning step.

## Chart Outcome Dependency

Chart outcome work remains downstream of replay review.

- **Chart outcome dependency:** a QQQ candidate must first pass source-data validation, bounded no-hindsight window selection, fixture design, and historical signal replay output validation.
- **Chart outcome calculation started:** no
- **Allowed later chart outcome scope:** chart-only MFE, MAE, terminal outcome, same-day or fast-swing classification, and chart-visible gap context after a replay-derived candidate is frozen.
- **Disallowed in this planning review:** chart outcome calculations, option P&L, account sizing, broker/order/fill/slippage modeling, watcher output, live reads, and live trade decisions.

## Watcher Deferral

- **Watcher remains deferred:** yes
- **Watcher implementation started:** no
- **Reason:** QQQ real historical signal replay has not yet selected a bounded source-data window, created a fixture, validated runner output, calculated chart outcomes, or contributed to broader QQQ/IWM/GLD aggregate coverage.

Watcher planning may use this review only as a future evidence boundary. It does not authorize watcher design, watcher storage, duplicate suppression implementation, alert delivery, schedulers, live reads, or production work.

## Boundary Result

- **Boundary result:** PASS
- **Fixture created:** no
- **Window selected:** no
- **Chart outcome calculation started:** no
- **Watcher implementation started:** no
- **Option P&L modeled:** no
- **Account sizing added:** no
- **New market data pulled:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Runner code changed:** no
- **Chart outcome code changed:** no

## Known Limits

- This is a planning review only.
- No QQQ replay fixture exists from this task.
- No final QQQ candidate window is selected.
- No QQQ historical replay output is generated from the accepted source CSV by this task.
- No QQQ chart outcome calculation or aggregate summary is started.
- The QQQ source CSV begins and ends intraday, so boundary sessions are partial.
- 24H, macro, IV, event, headline, option, account, and broker context remain unavailable or unconfirmed.
- This does not prove profitability, option performance, account safety, watcher readiness, production readiness, or live-trading readiness.

## Recommended Next Task

Select the first bounded QQQ source-data window for real historical replay fixture design, preserving no-hindsight candidate-only planning and targeting one of Ideal, Clean Fast Break, or Continuation without calculating chart outcomes.
