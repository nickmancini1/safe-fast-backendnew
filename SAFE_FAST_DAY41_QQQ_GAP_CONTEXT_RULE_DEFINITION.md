# SAFE-FAST Day 41 QQQ Gap-Context Rule Definition

## Scope

Candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00`.

This document defines the no-hindsight rule shape for QQQ Clean Fast Break gap context. It does not fill evidence, create trade proof, mark QQQ ready, or authorize live/engine/broker/order/account/Railway work.

## Required Output Fields

The QQQ Clean Fast Break gap-context review produces these fields:

- `gap_context_status`
- `gap_context_as_of`
- `gap_context_reviewed_before_signal`

Allowed `gap_context_status` values:

- `clean`
- `caution`
- `fail`
- `unknown`

The current repo evidence is not enough to honestly define numeric clean/caution/fail thresholds. Until those thresholds are accepted, any calculator must either emit `unknown` for threshold-dependent classifications or remain unbuilt.

## Allowed Raw Inputs

Allowed data is limited to source-backed QQQ regular-session candle rows available at or before the setup candle.

For `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`, the known raw inputs from the prior reviews are:

- Previous regular-session final exported close: `611.02` at `2026-04-10T15:30:00-04:00`.
- Signal-day open: `609.455` at `2026-04-13T09:30:00-04:00`.
- Through-signal candles: QQQ regular-session candles through `2026-04-13T12:30:00-04:00` only.
- Signal/setup time: `2026-04-13T12:30:00-04:00`.

Allowed source paths for this candidate:

- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl`

The replay log may identify the candidate, setup time, trigger, invalidation, and no-hindsight boundary. It must not supply future outcome evidence for setup-time gap context.

## Forbidden Data

The rule must not use:

- Any candle after `2026-04-13T12:30:00-04:00`.
- The first post-signal candle at `2026-04-13T13:30:00-04:00`.
- Same-session follow-through/spent context from replay log line 4 to backfill setup-time gap context.
- Later session candles.
- Outcome, MFE, MAE, terminal result, profitability, option, broker, order, account, or live-data information.
- Inferred headline, macro, IV, event, or gap-cause explanations from price action.

## Previous Close Selection

Previous close is the close of the latest source-backed QQQ regular-session candle before the signal-day regular session starts.

For the target candidate, that is the final exported QQQ RTH candle from the prior regular session:

- Timestamp: `2026-04-10T15:30:00-04:00`
- Close: `611.02`

If the previous regular-session final candle is missing, ambiguous, not QQQ, not regular-session, after the signal-day open, or not source-backed, `gap_context_status` must be `unknown`.

## Signal-Day Open Selection

Signal-day open is the open of the first source-backed QQQ regular-session candle on the signal date.

For the target candidate, that is:

- Timestamp: `2026-04-13T09:30:00-04:00`
- Open: `609.455`

If the signal-day opening candle is missing, ambiguous, not QQQ, not regular-session, after the signal time, or not source-backed, `gap_context_status` must be `unknown`.

## Gap Calculation

Gap points:

```text
gap_points = signal_day_open - previous_regular_session_close
```

Gap percent:

```text
gap_percent = gap_points / previous_regular_session_close * 100
```

Gap direction:

- `up` when `gap_points > 0`
- `down` when `gap_points < 0`
- `flat` when `gap_points == 0`
- `unknown` when either input is missing or invalid

For the target candidate:

```text
gap_points = 609.455 - 611.02 = -1.565
gap_percent = -1.565 / 611.02 * 100 = -0.2561% approximately
gap_direction = down
```

The numerical gap can be recorded from chart data. Gap cause must remain unknown unless a separate reviewed source artifact explicitly supplies it.

## Status Classification

`unknown` means the required raw inputs, no-hindsight boundary, or accepted numeric threshold rule are missing or unresolved.

`clean` means all required raw inputs are source-backed and through-signal only, and the accepted threshold rule classifies the measured gap as acceptable for QQQ Clean Fast Break setup-time review.

`caution` means all required raw inputs are source-backed and through-signal only, and the accepted threshold rule classifies the measured gap as material enough to require caution but not disqualifying.

`fail` means all required raw inputs are source-backed and through-signal only, and the accepted threshold rule classifies the measured gap as disqualifying for QQQ Clean Fast Break setup-time review.

Current threshold decision:

- The repo permits measuring gap direction, points, and percent from candles.
- The repo does not define numeric QQQ Clean Fast Break thresholds for clean/caution/fail.
- Therefore the target candidate's measured `-0.2561%` down gap must not be labeled clean, caution, or fail yet.
- A threshold gap is documented in `SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_THRESHOLD_GAP.md`.

## `gap_context_as_of`

`gap_context_as_of` is the latest candle timestamp used by the gap-context rule, not the later export `source_as_of` timestamp.

For this candidate, if the future calculator uses only the previous close, signal-day open, and through-signal audit boundary, the review as-of timestamp is:

```text
2026-04-13T12:30:00-04:00
```

Reason: the review is a setup-time reconstruction clipped to the setup candle. The local export `source_as_of` of `2026-05-15T18:48:44Z` can be retained as source provenance, but it is not the setup-time review as-of field.

If the latest allowed candle used by a future implementation is earlier than the signal candle because the through-signal candle is unavailable, the result must be `unknown` unless the accepted regression suite explicitly allows an earlier as-of model.

## `gap_context_reviewed_before_signal`

`gap_context_reviewed_before_signal` is `true` only when the calculated `gap_context_as_of` is less than or equal to the setup/signal time and the implementation proves no candle after the signal time affected the result.

For the target candidate, the value may be true only if all of the following are regression-proven:

- Previous close comes from `2026-04-10T15:30:00-04:00`.
- Signal-day open comes from `2026-04-13T09:30:00-04:00`.
- The calculation clips all candidate-context inputs at `2026-04-13T12:30:00-04:00`.
- The `2026-04-13T13:30:00-04:00` candle and all later candles cannot change any output.
- The output does not use replay log line 4 or any later outcome row.

If those conditions are not proven, `gap_context_reviewed_before_signal` must be `false` or unresolved by the validator, and the candidate must remain blocked.

## Missing Data Handling

Missing required data is a blocker, not low confidence.

If previous close is missing, signal-day open is missing, source identity is missing, regular-session identity is missing, timestamps are unparsable, candles are out of order, symbol does not match QQQ, or the no-hindsight clip cannot be enforced:

- `gap_context_status` must be `unknown`.
- `gap_context_as_of` must be blank or unresolved unless the latest allowed input timestamp is known.
- `gap_context_reviewed_before_signal` must be `false` or unresolved.
- No evidence package row may pass content validation on this rule.

## Required Regression Cases Before Calculator Work

Calculator work requires regression cases before implementation.

Required cases:

1. Happy path: previous RTH close `611.02`, signal-day open `609.455`, signal time `2026-04-13T12:30:00-04:00`, expected raw gap `-1.565`, expected percent about `-0.2561%`, direction `down`, as-of `2026-04-13T12:30:00-04:00`.
2. Future-bar exclusion: adding or changing the `2026-04-13T13:30:00-04:00` candle must not change previous close, signal-day open, gap points, gap percent, direction, status, as-of, or reviewed-before-signal.
3. Replay future exclusion: replay log line 4 and any later lifecycle row must not change setup-time gap context.
4. Missing previous close: no previous regular-session final candle produces `unknown` and cannot pass validation.
5. Missing signal-day open: no `2026-04-13T09:30:00-04:00` regular-session open produces `unknown` and cannot pass validation.
6. Non-regular-session contamination: premarket, after-hours, or non-RTH rows must not be selected as previous close or signal-day open.
7. Wrong symbol contamination: SPY/IWM/GLD rows must not be selected for QQQ.
8. Source timestamp distinction: later `source_as_of` remains provenance and must not make `gap_context_reviewed_before_signal` false when the candle timestamps prove a clipped setup-time reconstruction.
9. No threshold invention: without an accepted threshold fixture, the classifier must not label the target measured gap as `clean`, `caution`, or `fail`.
10. Threshold fixtures, once accepted: exact boundary cases around every clean/caution/fail threshold must be added before any non-`unknown` status is emitted.

## Current Candidate Decision

QQQ CFB gap-context evidence filled: NO.

QQQ candidate ready: NO.

Proof accepted: NO.

Profitability claimed: NO.

Next required action: define and accept numeric QQQ Clean Fast Break gap-context thresholds, then create regression cases before any calculator or evidence-package fill.
