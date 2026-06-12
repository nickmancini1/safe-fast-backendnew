# SAFE-FAST Day 41 QQQ Gap-Context Threshold Decision Needed

## Scope

Candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00`.

This document records the threshold decision still needed before any QQQ Clean Fast Break gap-context calculator work. It does not create calculator code, tests, evidence-package rows, proof, profitability claims, live-data paths, or trading/deploy changes.

## Search Result

Accepted numeric QQQ Clean Fast Break gap-context thresholds were not found.

Files and areas reviewed:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_RULE_DEFINITION.md`
- `SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_THRESHOLD_GAP.md`
- `SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_CALCULATION_REVIEW.md`
- `SAFE_FAST_DAY41_TASTYTRADE_RAW_DATA_CAPABILITY_REVIEW.md`
- `historical_signal_replay/source_data/richer_export_package_work/`
- Existing tests and docs mentioning gap context, thresholds, clean, caution, fail, Clean Fast Break, and CFB.

The repo supports measuring the raw gap from source-backed candles, but it does not define how QQQ Clean Fast Break gap size and direction map to `clean`, `caution`, or `fail`.

## Fixture Inputs Available Now

Previous close fixture:

- Symbol: `QQQ`
- Source file: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- Candle timestamp: `2026-04-10T15:30:00-04:00`
- Session type: regular session
- Close: `611.02`

Signal-day open fixture:

- Symbol: `QQQ`
- Source file: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- Candle timestamp: `2026-04-13T09:30:00-04:00`
- Session type: regular session
- Open: `609.455`

Gap amount fixture:

```text
gap_points = 609.455 - 611.02 = -1.565
```

Gap percent fixture:

```text
gap_percent = -1.565 / 611.02 * 100 = -0.2561% approximately
```

Gap direction fixture:

```text
down
```

## Expected Output Until Thresholds Are Accepted

Status expected:

```text
unknown
```

Reason: the raw gap can be measured, but no accepted numeric QQQ Clean Fast Break threshold fixture maps `-0.2561%` down to `clean`, `caution`, or `fail`.

As-of expected:

```text
2026-04-13T12:30:00-04:00
```

Reason: this is the clipped setup/signal candle time for the no-hindsight reconstruction. The later export `source_as_of` timestamp is source provenance, not the setup-time review `gap_context_as_of`.

Reviewed-before-signal expected:

```text
true only after regression proof
```

The future calculator may emit true only if regressions prove previous close selection, signal-day open selection, setup-time clipping, future-bar rejection, and replay future-row rejection. Until that proof exists, the field remains unresolved for evidence-package validation.

## Missing Data Case

If the previous regular-session final candle, signal-day opening candle, symbol identity, regular-session identity, source identity, parseable timestamp, or no-hindsight clip is missing or ambiguous:

- `gap_context_status` must be `unknown`.
- `gap_context_as_of` must be blank or unresolved unless the latest valid allowed input timestamp is known.
- `gap_context_reviewed_before_signal` must be `false` or unresolved.
- No QQQ CFB gap-context evidence row may pass content validation.

## Future-Data Rejection Case

A future implementation must reject all data after `2026-04-13T12:30:00-04:00` for setup-time gap context.

Rejected future data includes:

- The `2026-04-13T13:30:00-04:00` QQQ candle.
- Any later same-session or later-session QQQ candle.
- Replay log line 4 same-session follow-through/spent context.
- Any after-setup outcome, MFE, MAE, terminal result, option, broker, account, order, P&L, live-data, headline, macro, IV, event, or gap-cause inference.

Changing or adding those future rows must not change previous close, signal-day open, gap points, gap percent, direction, status, as-of, or reviewed-before-signal.

## Decision Missing

SAFE-FAST must choose and document numeric QQQ Clean Fast Break gap-context thresholds before calculator work.

The missing choices are:

- Whether clean/caution/fail thresholds use absolute percent gap, signed percent gap, point gap, direction, or a combination.
- Whether favorable and adverse gaps use symmetric thresholds or direction-specific thresholds.
- What exact boundary values separate `clean` from `caution`.
- What exact boundary values separate `caution` from `fail`.
- Whether a flat or near-flat gap is always `clean`, or whether it can be `unknown` under missing context.
- Whether a small adverse gap like `-0.2561%` for the target candidate is `clean`, `caution`, or `fail`.
- Whether material favorable gaps can still be `caution` because they imply gap risk, extension, or chase risk.
- Whether gap cause remains excluded from this status unless separately source-backed.
- Whether any non-price context can override the raw gap threshold label. Current rule shape says it cannot.

Until these choices are accepted, a calculator must not emit non-`unknown` threshold-dependent status.

## Exact Regression Cases Needed Next

1. Happy path raw measurement: previous close `611.02`, signal-day open `609.455`, signal time `2026-04-13T12:30:00-04:00`, expected gap `-1.565`, expected percent about `-0.2561%`, direction `down`, as-of `2026-04-13T12:30:00-04:00`.
2. Missing threshold decision: same target raw inputs must produce `unknown` status until numeric clean/caution/fail thresholds are accepted.
3. Missing previous close: no prior regular-session final candle produces `unknown` and cannot pass evidence validation.
4. Missing signal-day open: no `2026-04-13T09:30:00-04:00` regular-session opening candle produces `unknown` and cannot pass evidence validation.
5. Future-bar exclusion: adding or changing the `2026-04-13T13:30:00-04:00` candle must not change any setup-time gap-context output.
6. Replay future exclusion: replay log line 4 and later lifecycle rows must not change setup-time gap context.
7. Non-regular-session contamination: premarket and after-hours rows must not be selected as previous close or signal-day open.
8. Wrong-symbol contamination: SPY, IWM, and GLD rows must not be selected for QQQ.
9. Source timestamp distinction: later `source_as_of` remains provenance and must not replace setup-time `gap_context_as_of`.
10. Threshold boundary fixtures after decision: exact clean/caution, caution/fail, favorable/adverse, flat/near-flat, and disqualifying boundary cases must be added before any calculator emits `clean`, `caution`, or `fail`.

## Current Candidate Decision

QQQ CFB gap-context threshold fixtures accepted: NO.

QQQ CFB gap-context calculator authorized: NO.

QQQ CFB gap-context evidence filled: NO.

QQQ candidate marked ready: NO.

Proof accepted: NO.

Profitability claimed: NO.
