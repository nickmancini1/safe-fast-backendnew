# SAFE-FAST Day 41 QQQ Gap-Context Rule Gap

## Scope

Candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Target fields:

- `gap_context_status`
- `gap_context_as_of`
- `gap_context_reviewed_before_signal`

This review looked for an existing repo rule that turns raw QQQ candle data into those SAFE-FAST labels. No such clear rule was found.

## Inputs Found

The QQQ candidate signal/setup time is `2026-04-13T12:30:00-04:00`.

Repo-backed inputs exist in `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`:

- Previous regular-session final exported candle: CSV line 128, `2026-04-10T15:30:00-04:00`, close `611.02`.
- Signal-day opening exported RTH candle: CSV line 129, `2026-04-13T09:30:00-04:00`, open `609.455`.
- Through-signal candles: CSV lines 129-132, ending at `2026-04-13T12:30:00-04:00`.
- First post-signal candle exists at CSV line 133, `2026-04-13T13:30:00-04:00`, and must not be used for setup-time gap context.
- Source timestamp on these rows: `2026-05-15T18:48:44Z`.

Repo-backed replay input exists in `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl`:

- Replay log line 3 is the setup-time signal row at `2026-04-13T12:30:00-04:00`.
- Replay log line 4 is same-session follow-through/spent context and must not be used to backfill setup-time gap context.

## Existing Rule Search Result

Found:

- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_CALCULATION_RULES_PLAN.md` says chart gaps may be measured from candles when a session opens away from the prior available RTH close.
- `SAFE_FAST_QQQ_CHART_OUTCOME_CALCULATION_PHASE_PLAN.md` says QQQ chart gaps may be measured from QQQ candles when a regular-session open differs from the prior available RTH close.
- `watcher_foundation/candidate_freshness_blocker_rule_gate.py` and `SAFE_FAST_RULE_FAMILY_DECISION_TABLE.md` explicitly classify Clean Fast Break gap context as `SOURCE_DATA_INSUFFICIENT`.

Not found:

- An accepted `gap_context_status` vocabulary.
- A threshold for when a measured raw gap is complete, blocked, clean, material, insignificant, up, down, flat, or unavailable.
- A rule that maps previous close, signal-day open, and through-signal candles into `gap_context_status`.
- A rule defining whether `gap_context_as_of` should be the signal candle timestamp, the source export `source_as_of`, the latest candle timestamp used, or a separate review timestamp.
- A rule defining `gap_context_reviewed_before_signal`, especially when the local historical export `source_as_of` is after the historical signal time.

## Decision

No calculator was created.

The repo has enough raw candle data to calculate a numerical chart gap:

- raw gap points: `609.455 - 611.02 = -1.565`
- raw gap percent: approximately `-0.2561%`

But calculating those raw values is not the same as producing the required SAFE-FAST labels. Implementing `gap_context_status`, `gap_context_as_of`, or `gap_context_reviewed_before_signal` now would require inventing project behavior that the repo has not accepted.

## Exact Missing Rule

SAFE-FAST needs a no-hindsight QQQ Clean Fast Break gap-context rule that defines:

- The accepted `gap_context_status` values.
- How raw previous-session close and signal-day open map to `gap_context_status`.
- Whether through-signal intraday candles affect the status or are only audit inputs.
- The minimum raw data required for a pass versus a clear failure.
- The exact `gap_context_as_of` timestamp source.
- Whether historical `source_as_of` after the signal time makes `gap_context_reviewed_before_signal` false, or whether replay-time reconstruction has a separate accepted review-time model.
- Regression cases proving no candles after the signal time can affect the labels.

Until that rule exists, `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` remains blocked on QQQ CFB gap context.
