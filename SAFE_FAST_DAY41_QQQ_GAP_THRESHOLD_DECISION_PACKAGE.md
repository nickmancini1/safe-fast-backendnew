# SAFE-FAST Day 41 QQQ Gap Threshold Decision Package

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Target setup: QQQ Clean Fast Break.

Target setup/signal time: `2026-04-13T12:30:00-04:00`.

This package gathers repo examples that can inform a future QQQ Clean Fast Break gap-context threshold decision. It does not choose thresholds, write calculator code, write tests, fill evidence, mark QQQ ready, claim proof, or claim profitability.

## Decision Result

Repo evidence does not support numeric QQQ Clean Fast Break clean/caution/fail gap thresholds yet.

Reason: the repo has raw gap measurements and chart-outcome gap context examples, but it does not contain an accepted QQQ Clean Fast Break threshold rule, enough labeled QQQ Clean Fast Break examples, failed/adverse examples, no-trade examples, or boundary fixtures mapping measured gap percent/direction to `clean`, `caution`, or `fail`.

Until that decision exists, the target measured gap must remain threshold-status `unknown`.

## Direct Target Measurement

The target QQQ Clean Fast Break gap can be measured from source-backed underlying candles:

| Field | Value |
| --- | --- |
| Source file | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` |
| Signal/setup time | `2026-04-13T12:30:00-04:00` |
| Previous regular-session close | `611.02` at `2026-04-10T15:30:00-04:00` |
| Signal-day open | `609.455` at `2026-04-13T09:30:00-04:00` |
| Gap points | `-1.5650` |
| Gap percent | `-0.2561%` |
| Direction | `down` |

Calculation:

```text
gap_points = 609.455 - 611.02 = -1.565
gap_percent = -1.565 / 611.02 * 100 = -0.2561% approximately
```

This is a raw chart measurement only. It is not an accepted SAFE-FAST `gap_context_status`.

## Examples Found

### Usable For Raw Measurement

These examples have source-backed previous regular-session close and signal-day open inputs available in local source CSVs. They can help test measurement mechanics and fixture shape.

| Example | Setup | Signal time | Previous RTH close | Signal-day open | Gap points | Gap percent | Directly usable for QQQ CFB thresholds? |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| QQQ CFB target | QQQ Clean Fast Break | `2026-04-13T12:30:00-04:00` | `611.02` | `609.455` | `-1.5650` | `-0.2561%` | Yes for measurement; no for thresholds by itself |
| SPY CFB 002 | SPY Clean Fast Break | `2026-04-13T12:30:00-04:00` | `679.31` | `677.41` | `-1.9000` | `-0.2797%` | Context only; different symbol |
| SPY CFB 003 | SPY Clean Fast Break | `2026-04-15T14:30:00-04:00` | `694.40` | `695.26` | `0.8600` | `0.1238%` | Context only; different symbol |
| QQQ Ideal | QQQ Ideal | `2026-05-13T12:30:00-04:00` | `707.22` | `709.965` | `2.7450` | `0.3881%` | Context only; different setup |
| QQQ Continuation | QQQ Continuation | `2026-04-30T15:30:00-04:00` | `661.61` | `665.39` | `3.7800` | `0.5713%` | Context only; different setup |
| SPY Ideal | SPY Ideal | `2026-05-13T11:30:00-04:00` | `738.20` | `738.45` | `0.2500` | `0.0339%` | Context only; different symbol/setup |
| SPY Continuation | SPY Continuation | `2026-04-30T12:30:00-04:00` | `711.58` | `714.63` | `3.0500` | `0.4286%` | Context only; different symbol/setup |

### Chart Outcome Gap Context Examples

The chart outcome fixtures and reports contain gap measurements under `headline_gap_risk_context`:

| Artifact family | Gap points | Gap percent | Usefulness |
| --- | ---: | ---: | --- |
| `qqq_clean_fast_break_chart_outcome_*` | `-1.565` | `-0.2561%` | Same raw target gap; does not classify clean/caution/fail |
| `third_spy_clean_fast_break_chart_outcome_*` | `0.86` | `0.1238%` | SPY CFB context only |
| `qqq_ideal_chart_outcome_*` | `0.14` | `0.0196%` | QQQ but Ideal, and chart-outcome gap is not a QQQ CFB threshold label |
| `qqq_continuation_chart_outcome_*` | `1.54` | `0.2307%` | QQQ but Continuation, and chart-outcome gap is entry-window context |
| `second_spy_ideal_chart_outcome_*` | `0.25` | `0.0339%` | Different symbol/setup |
| `first_spy_continuation_chart_outcome_*` | `3.05` | `0.429%` | Different symbol/setup |

These are useful as examples that raw gaps were recorded in chart-only artifacts. They are not accepted threshold decisions. They do not define whether any measured gap is `clean`, `caution`, or `fail`.

## Unusable Or Insufficient Examples

- `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl` identifies QQQ Clean Fast Break lifecycle rows, trigger, invalidation, state, and blocker/caution shape, but it does not include `gap_context_status`, accepted gap thresholds, or threshold labels.
- `historical_signal_replay/source_data/richer_export_package_work/qqq_cfb_gap_context_completeness_fields_rule.jsonl` remains partial and explicitly records `TASTYTRADE_DATA_NOT_AVAILABLE` for `gap_context_status`, `gap_context_as_of`, and `gap_context_reviewed_before_signal`.
- The wider work-package files list QQQ/SPY evidence requests, but they do not contain accepted QQQ CFB gap thresholds.
- SPY Clean Fast Break examples may help compare measurement mechanics, but they cannot be copied into QQQ thresholds without symbol-specific proof.
- QQQ Ideal and QQQ Continuation examples may help with QQQ raw gap boundary testing, but they cannot define QQQ Clean Fast Break thresholds because setup behavior can differ.
- Chart-outcome terminal results cannot be used to backfit thresholds because that would mix setup-time context with after-setup outcome.

## Threshold Options

No threshold options are accepted by repo evidence.

The missing decision is still whether thresholds should use:

- signed percent gap,
- absolute percent gap,
- point gap,
- direction-specific thresholds,
- symmetric favorable/adverse thresholds,
- separate clean/caution and caution/fail boundaries,
- or a combination of those fields.

No numeric option should be treated as accepted until it is backed by enough QQQ Clean Fast Break examples and regression fixtures.

## Missing Sample/Data

The smallest missing sample/data set is:

- Multiple QQQ Clean Fast Break examples with source-backed previous regular-session close, signal-day open, signal/setup time, trigger, invalidation, and no-hindsight boundary.
- At least one QQQ Clean Fast Break clean candidate with accepted setup-time outcome classification.
- At least one QQQ Clean Fast Break caution candidate where the gap is material but not disqualifying.
- At least one QQQ Clean Fast Break fail candidate where the gap is disqualifying.
- Negative/no-trade QQQ Clean Fast Break examples, including tempting but blocked setups.
- Direction coverage: down-gap, up-gap, and flat/near-flat examples.
- Boundary coverage around every proposed clean/caution and caution/fail threshold.
- Proof that threshold labels are based only on setup-time raw inputs and not on later chart outcome.

## Exact Regression Fixtures Needed Next

1. Target raw measurement: QQQ previous close `611.02`, signal-day open `609.455`, signal time `2026-04-13T12:30:00-04:00`, expected gap `-1.5650`, expected percent `-0.2561%`, direction `down`, status `unknown` until thresholds are accepted.
2. Missing threshold decision: same target inputs must not emit `clean`, `caution`, or `fail`.
3. Missing previous close: no previous regular-session final candle must emit `unknown` and cannot pass evidence validation.
4. Missing signal-day open: no first regular-session candle on signal date must emit `unknown` and cannot pass evidence validation.
5. Future-bar exclusion: changing any candle after `2026-04-13T12:30:00-04:00` must not change raw gap fields or status.
6. Replay future exclusion: replay log line 4 and later rows must not affect setup-time gap context.
7. Non-RTH contamination: premarket and after-hours rows must not be selected as previous close or signal-day open.
8. Wrong-symbol contamination: SPY, IWM, and GLD rows must not be selected for QQQ.
9. Setup contamination: QQQ Ideal and QQQ Continuation gap examples must not be treated as QQQ Clean Fast Break threshold labels.
10. Boundary fixtures after threshold decision: exact clean/caution and caution/fail boundary cases for adverse, favorable, and flat/near-flat gaps.
11. Label independence: chart outcome follow-through, time stop, MFE, MAE, option data, broker/account/order data, and profitability fields must not change setup-time gap status.

## Current Status

QQQ CFB numeric threshold support: NO.

QQQ CFB threshold options accepted: NO.

QQQ CFB calculator authorized: NO.

QQQ CFB gap-context evidence filled: NO.

QQQ candidate marked ready: NO.

Proof accepted: NO.

Profitability claimed: NO.
