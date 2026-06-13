# SAFE-FAST Day 41 QQQ Gap Threshold Fixture Decision

## Scope

Candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00`.

Baseline: `2691a47 Record QQQ CFB rule decision package`.

This is a rule/fixture decision for regression testing the QQQ Clean Fast Break gap-context path. It is not trade proof, profitability proof, evidence fill, backtest authorization, trade selection, P&L calculation, candidate readiness, or live/engine authorization.

## Accepted Fixture Rule

The first accepted QQQ Clean Fast Break gap-context threshold fixture set uses signed gap percent for measurement and absolute gap-percent magnitude for status classification.

Formula:

```text
gap_points = signal_day_open - previous_regular_session_close
gap_percent = gap_points / previous_regular_session_close * 100
gap_abs_percent = abs(gap_percent)
```

The fixture intentionally does not infer gap cause, news context, option context, execution quality, trade direction, entry quality, or profitability.

## Status Definitions

| Status | Accepted fixture definition |
| --- | --- |
| `clean` | Required QQQ regular-session inputs are source-backed, no-hindsight clipping is proven, and `gap_abs_percent <= 0.30%`. |
| `caution` | Required QQQ regular-session inputs are source-backed, no-hindsight clipping is proven, and `0.30% < gap_abs_percent <= 0.75%`. |
| `fail` | Required QQQ regular-session inputs are source-backed, no-hindsight clipping is proven, and `gap_abs_percent > 0.75%`. |
| `unknown` | Required inputs, source identity, regular-session identity, parseable timestamps, symbol match, no-hindsight clipping, or the threshold fixture itself are missing, ambiguous, or unproven. |

Boundary behavior is inclusive on the lower-risk side:

- exactly `0.30%` is `clean`.
- just above `0.30%` is `caution`.
- exactly `0.75%` is `caution`.
- just above `0.75%` is `fail`.

This fixture is deliberately conservative for testing because it treats both up gaps and down gaps by size first. Direction remains recorded as `up`, `down`, `flat`, or `unknown`, but direction does not change the first fixture status.

## Exact Boundary Examples

These examples use a previous regular-session close of `100.00` only to make boundary math exact.

| Previous close | Signal-day open | Gap points | Gap percent | Direction | Expected status |
| ---: | ---: | ---: | ---: | --- | --- |
| `100.00` | `100.00` | `0.00` | `0.00%` | `flat` | `clean` |
| `100.00` | `100.30` | `0.30` | `0.30%` | `up` | `clean` |
| `100.00` | `99.70` | `-0.30` | `-0.30%` | `down` | `clean` |
| `100.00` | `100.3001` | `0.3001` | `0.3001%` | `up` | `caution` |
| `100.00` | `99.6999` | `-0.3001` | `-0.3001%` | `down` | `caution` |
| `100.00` | `100.75` | `0.75` | `0.75%` | `up` | `caution` |
| `100.00` | `99.25` | `-0.75` | `-0.75%` | `down` | `caution` |
| `100.00` | `100.7501` | `0.7501` | `0.7501%` | `up` | `fail` |
| `100.00` | `99.2499` | `-0.7501` | `-0.7501%` | `down` | `fail` |

Regression fixtures must also include the real QQQ target inputs:

| Field | Value |
| --- | --- |
| Previous regular-session close | `611.02` at `2026-04-10T15:30:00-04:00` |
| Signal-day open | `609.455` at `2026-04-13T09:30:00-04:00` |
| Signal/setup time | `2026-04-13T12:30:00-04:00` |
| Gap points | `-1.565` |
| Gap percent | about `-0.2561%` |
| Direction | `down` |
| Expected fixture status | `clean` |
| Expected `gap_context_as_of` after regression proof | `2026-04-13T12:30:00-04:00` |
| Expected `gap_context_reviewed_before_signal` after regression proof | `true` |

The target status is `clean` only under this accepted fixture rule and only after the no-hindsight regression cases prove that future data cannot affect the result.

## Missing-Data Behavior

Missing required data is a blocker, not low confidence.

The expected status is `unknown` when any of these conditions occurs:

- previous regular-session close is missing, ambiguous, not QQQ, not regular session, not source-backed, or not before the signal-day regular session.
- signal-day open is missing, ambiguous, not QQQ, not regular session, not source-backed, or after the signal/setup time.
- timestamps are missing, unparsable, out of order, or timezone-ambiguous.
- symbol is missing or not `QQQ`.
- source/session identity is missing or ambiguous.
- no-hindsight clipping cannot be proven.
- threshold fixture metadata is absent from the regression rule set.

For `unknown` rows:

- `gap_context_status` must be `unknown`.
- `gap_context_as_of` must be blank/unresolved unless the latest allowed input timestamp is known.
- `gap_context_reviewed_before_signal` must be `false` or unresolved.
- the row cannot pass content validation as a completed QQQ CFB gap-context evidence row.

## Future-Data Rejection Behavior

Setup-time gap context must not use future candles, future replay rows, outcome fields, option data, fills, P&L, broker/account/order data, or profitability.

Required rejection fixtures:

- Changing, adding, or deleting the `2026-04-13T13:30:00-04:00` QQQ candle must not change previous close, signal-day open, gap points, gap percent, direction, status, `gap_context_as_of`, or `gap_context_reviewed_before_signal`.
- Replay log line 4 and any later lifecycle/outcome row must not change setup-time gap context.
- Later chart outcome fields, MFE, MAE, terminal result, option quotes, option trades, spread, volume, open interest, fills, costs, slippage, account state, and profitability must not change setup-time gap context.
- The later export `source_as_of` may remain provenance only. It must not replace the setup-time `gap_context_as_of` when candle timestamps prove a clipped reconstruction.

## Regression Fixture Requirements Before Calculator Work

Calculator work remains blocked until regression fixtures exist for:

1. Real QQQ target measurement and expected `clean` fixture status.
2. Exact clean/caution boundaries at `+0.30%` and `-0.30%`.
3. Just-over clean/caution boundaries at `+0.3001%` and `-0.3001%`.
4. Exact caution/fail boundaries at `+0.75%` and `-0.75%`.
5. Just-over caution/fail boundaries at `+0.7501%` and `-0.7501%`.
6. Flat/no-gap behavior.
7. Missing previous close.
8. Missing signal-day open.
9. Missing or wrong symbol.
10. Non-regular-session contamination.
11. Future-bar exclusion.
12. Replay future-row exclusion.
13. Source timestamp versus candle timestamp distinction.
14. Label independence from outcome, option, fill, P&L, and profitability fields.

## Current Result

QQQ CFB gap-context threshold fixture set accepted: YES.

QQQ CFB calculator authorized now: NO. Regression fixtures must be added first.

QQQ CFB gap-context evidence filled: NO.

Backtest authorized: NO.

Trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Proof accepted: NO.

Profitability claimed: NO.
