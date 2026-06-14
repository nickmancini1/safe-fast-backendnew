# SAFE-FAST Day 41 QQQ Gap-Context Regression Fixtures Review

## Scope

Baseline: `fcb8d0e Accept QQQ gap threshold fixtures`.

Candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00`.

This review records the data-only regression fixtures added for the accepted QQQ Clean Fast Break gap-context threshold fixture set. It does not create calculator logic, fill evidence, backtest, choose a trade, calculate P&L, mark a candidate ready, accept proof, or claim profitability.

## Fixture File

Created:

- `historical_signal_replay/fixtures/qqq_gap_context_regression_fixtures.json`

The fixture file records the accepted first threshold set:

- `clean`: absolute gap percent `<= 0.30%`.
- `caution`: absolute gap percent `> 0.30%` and `<= 0.75%`.
- `fail`: absolute gap percent `> 0.75%`.
- `unknown`: required inputs, source/session identity, symbol match, timestamp parsing, no-hindsight clipping, or threshold fixture metadata missing/ambiguous/unproven.

The fixture file uses the accepted formula:

```text
gap_percent = (signal_day_open - previous_close) / previous_close * 100
```

## Fixtures Added

| Fixture | Expected status | Purpose |
| --- | --- | --- |
| `qqq_gap_clean_exact_030_up` | `clean` | Clean example at exactly `+0.30%`, proving the clean boundary is inclusive. |
| `qqq_gap_caution_lower_boundary_just_over_030_up` | `caution` | Caution lower-boundary example just above `+0.30%`. |
| `qqq_gap_caution_upper_boundary_exact_075_up` | `caution` | Caution upper-boundary example at exactly `+0.75%`, proving the caution boundary is inclusive. |
| `qqq_gap_fail_just_over_075_up` | `fail` | Fail example just above `+0.75%`. |
| `qqq_gap_unknown_missing_previous_close` | `unknown` | Missing prior regular-session close blocks completed gap-context evidence. |
| `qqq_gap_unknown_missing_signal_day_open` | `unknown` | Missing signal-day open blocks completed gap-context evidence. |
| `qqq_gap_future_data_rejection_2026_04_13` | `clean` | Future-data rejection fixture: `2026-04-13T13:30:00-04:00` must not change setup-time gap context. |
| `qqq_gap_known_target_2026_04_13_clean` | `clean` | Known target fixture using previous close `611.02`, signal-day open `609.455`, gap `-1.565`, and gap percent about `-0.2561%`. |

## Known QQQ Target Values

The known target fixture preserves:

- Previous regular-session close: `611.02` at `2026-04-10T15:30:00-04:00`.
- Signal-day open: `609.455` at `2026-04-13T09:30:00-04:00`.
- Signal/setup time: `2026-04-13T12:30:00-04:00`.
- Gap amount: `-1.565`.
- Gap percent: `-0.2561290956106183%`, about `-0.2561%`.
- Expected status under the first fixture threshold set: `clean`.
- Expected latest allowed source time: `2026-04-13T12:30:00-04:00`.
- Expected reviewed-before-signal: `true`, only after the no-hindsight regression path proves future data cannot affect the result.

## Guardrails Preserved

- Calculator logic created: NO.
- Evidence filled: NO.
- Backtest authorized: NO.
- Trade chosen: NO.
- P&L calculated: NO.
- QQQ candidate marked ready: NO.
- Intake-ready count changed: NO.
- Proof accepted: NO.
- Profitability claimed: NO.
- `main.py`, live/engine/broker/order/account/Railway files, raw data files, `.env`, secrets, generated reports/logs, trade-selection code, backtest code, and P&L files changed: NO.

## Remaining Work

The next valid step is calculator work only if it consumes these fixtures with tests that prove no-hindsight clipping, missing-input behavior, and future-data rejection. Evidence fill, backtest, trade selection, P&L, proof, profitability, and readiness remain blocked.
