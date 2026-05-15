# SAFE-FAST Broader Chart Outcome Backtesting Coverage Plan

## Planning Status

- **Planning status:** PASS - docs-only coverage plan
- **Baseline:** patch8
- **Latest local commit before planning:** `5fd128f Add deferred Continuous Watcher MVP plan`
- **Scope:** plan broader chart-based trade outcome backtesting coverage before Continuous Watcher implementation.

This task does not implement new calculations, pull new market data, change `main.py`, change schemas, change fixtures, change runner code, change chart outcome code, model option P&L, add account sizing, start watcher implementation, auto-trade, use live reads, or make live trade decisions.

## Reason Broader Coverage Comes Before Watcher Implementation

Continuous Watcher work remains deferred because the current chart outcome evidence is limited to three SPY setup-family samples. A watcher that tracks lifecycle states and emits alerts across SPY, QQQ, IWM, and GLD should not be implemented around only one symbol and one sample per setup family.

Broader chart-based outcome coverage should come first so watcher planning can be grounded in cross-symbol evidence for the same setup families the watcher is expected to monitor: Ideal, Clean Fast Break, and Continuation.

## Current SPY Three-Setup Evidence Summary

- **Validated chart outcome samples:** 3
- **Symbol covered:** SPY
- **Setup families covered:** Continuation, Ideal, Clean Fast Break
- **Terminal outcomes:** 2 follow-through, 0 invalidated/failure, 1 time stop
- **Aggregate MFE:** average 1.5817 points / 0.2177% / 0.1922R; max 2.29 points / 0.3199% / 0.3074R
- **Aggregate MAE:** average 0.3617 points / 0.0507% / 0.0547R; max 0.735 points / 0.105% / 0.1286R
- **Same-day/fast-swing classification:** 2 same-day, 1 time-stop same-day
- **Headline/gap-risk context:** chart gaps detected in all 3 samples; gap cause known in 0 samples; macro, IV, and event context unconfirmed; headline context unavailable
- **Boundary:** chart-only proof, not profitability proof, not option P&L, not account sizing, not watcher readiness

## Minimum Next-Symbol Coverage Target

The minimum next-symbol target is QQQ.

QQQ should receive the next full coverage pass before IWM or GLD because no inspected evidence contradicts the requested order, and QQQ is part of the allowed SAFE-FAST universe with equity-index behavior closest to the existing SPY proof surface.

## Recommended Symbol Order

Recommended order:

1. QQQ
2. IWM
3. GLD

This order should stand unless later source-data validation or window selection evidence shows that a symbol lacks enough valid no-hindsight setup windows for the next coverage step. If that happens, document the evidence and move to the next symbol without inventing coverage.

## Setup-Family Coverage Target

Each new symbol should target the same three setup families:

- Ideal
- Clean Fast Break
- Continuation

Each setup-family sample must start from real historical replay evidence before chart outcome calculation.

## Minimum Sample Target Per Setup Family

Minimum target: 3 validated chart outcome samples per setup family per symbol.

For each new symbol, the minimum full target is:

- Ideal: 3 samples
- Clean Fast Break: 3 samples
- Continuation: 3 samples
- Symbol total: 9 validated chart outcome samples

For QQQ, IWM, and GLD combined, the minimum broader-coverage target is 27 validated chart outcome samples. The current SPY evidence remains useful context, but it should not be counted as broader next-symbol coverage.

## Source-Data Requirements

Each symbol coverage pass requires validated historical source data before any replay or outcome work:

- approved source such as `dxlink_candles.get_1h_ema50_snapshot` or another explicitly reviewed source
- symbol matches the target symbol
- timeframe is 1H RTH unless a separate reviewed task approves otherwise
- timestamps are ordered and session-valid
- OHLCV values are present and internally valid
- EMA/context fields are either supplied by the source or explicitly marked unavailable/unconfirmed
- no future rows, outcome labels, P&L labels, option data, account sizing, broker/order data, or after-the-fact trade conclusions
- source file metadata includes source, as-of time, vendor when known, symbol, timeframe, and row count

## Real Historical Replay Requirement Before Chart Outcome Calculation

For each symbol and setup family, real historical replay must be completed and reviewed before chart outcome calculation.

The replay step must document:

- source-data validation status
- selected no-hindsight source window
- fixture row count
- generated signal log row count
- setup-family count
- stage/lifecycle sequence
- runner output validation result
- explicit boundary that replay is signal/stage/lifecycle only

No chart outcome calculation should start from an unreviewed or after-the-fact selected setup candidate.

## Chart Outcome Calculation Requirement

After replay review passes, chart outcome calculation may be planned for approved candidates only.

Each chart outcome output should preserve the existing chart-only boundary:

- entry reference from the eligible next candle/open rule used by v1
- invalidation reference copied from reviewed replay evidence
- terminal outcome type
- MFE and MAE in points, percent, and chart R
- same-day or fast-swing classification
- chart gap context when visible from candles
- no option P&L
- no account sizing
- no broker/order/fill/slippage modeling
- no watcher output

## Aggregate Summary Requirement

Each completed symbol pass should include an aggregate summary that reads existing validated result files only.

The summary must include:

- sample count
- setup families included
- follow-through, invalidated/failure, and time-stop counts
- aggregate MFE and MAE
- by-family MFE and MAE
- same-day/fast-swing classification counts
- headline/gap-risk context summary
- chart-only boundary fields

The aggregate summary must not calculate new outcomes from OHLCV rows.

## No-Hindsight Rules

- Source rows must be available at or before the replay row timestamp.
- Window selection must not depend on later outcome success.
- Replay fixtures must not include future-row labels, P&L, option results, account sizing, or broker/order outcomes.
- Invalidation and trigger references must come from replay-visible chart evidence.
- Chart outcome calculations may look forward only after a replay-derived candidate is frozen for outcome measurement.
- Gap cause, macro, IV, event, headline, option, account, and broker fields must remain unavailable or unconfirmed unless an approved source supplies them.

## Headline and Gap-Risk Context Handling

Chart gaps should be recorded when visible from candles, including direction, points, and percent when available.

Gap causes must not be inferred from price action alone. Macro, IV, event, and headline context should be marked `unconfirmed` or `unavailable` unless a reviewed data source supplies that context. Headline and gap-risk fields are context only and must not become live trade permission.

## Likely Risk vs Full-Risk Note

The existing chart outcome work reports likely chart risk as underlying-chart distance from entry reference to invalidation reference. This is chart-only context.

Likely chart risk is not full financial risk. It does not model option debit exposure, spread width, contract Greeks, bid/ask behavior, fill quality, slippage, gap-through-invalidation losses, account sizing, or broker execution.

## Decision Gate For Watcher Planning To Resume

Continuous Watcher implementation must remain deferred until broader chart outcome coverage is completed and reviewed.

Minimum gate to resume watcher planning beyond the deferred reference:

- QQQ, IWM, and GLD each have validated real historical replay coverage for Ideal, Clean Fast Break, and Continuation
- each setup family has at least 3 validated chart outcome samples per symbol, or a written reviewed exception explains why the minimum could not be met without hindsight
- each symbol has a validated aggregate summary
- all validation and replay/regression commands pass locally
- build state is updated with the broader coverage result and remaining limits

This gate resumes watcher planning only. It does not authorize watcher implementation, live reads, alert delivery, option P&L, account sizing, auto-trading, or production deployment.

## Known Limits

- This is a docs-only plan.
- No new data was pulled.
- No new calculations were implemented.
- No new fixtures, schemas, runners, reports, or chart outcome code were changed.
- The only current chart outcome evidence remains the three validated SPY setup-family samples.
- QQQ, IWM, and GLD do not yet have equivalent chart outcome evidence in the inspected artifacts.
- The sample target is a minimum coverage threshold, not a profitability threshold.
- Chart outcome coverage does not prove option performance, account safety, live trading readiness, watcher readiness, or production readiness.

## Recommended Next Task

Begin QQQ broader chart outcome coverage as a bounded source-data validation and real historical replay planning task for Ideal, Clean Fast Break, and Continuation, without pulling data or changing fixtures unless that task explicitly authorizes those steps.
