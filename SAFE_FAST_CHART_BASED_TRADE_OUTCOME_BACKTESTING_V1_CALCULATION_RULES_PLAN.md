# SAFE-FAST Chart-Based Trade Outcome Backtesting v1 Calculation Rules Plan

## Planning Status

- **Planning status:** PASS
- **Baseline:** patch8
- **Latest local commit reviewed:** `8498f65 Add chart outcome next-step decision review`
- **Scope:** docs-only real chart outcome calculation rules plan for chart-based trade outcome backtesting v1.
- **Real calculation implementation started:** no

This plan defines deterministic calculation rules only. It does not implement real outcome calculation, change `main.py`, change schemas, change fixtures, change runner code, model option P&L, add account sizing, start watcher work, auto-trade, use live reads, or make live trade decisions.

## Chart-Only Boundary

v1 measures only underlying-chart behavior after an eligible historical signal row. The calculation may use source OHLCV candles, replay signal fields, predeclared entry/invalidation/follow-through/failure/time-stop rules, and unavailable-context markers.

It must not infer option-contract results, spread value, fill quality, account drawdown, order execution, live trade permission, or watcher state.

## Allowed Symbols

Allowed v1 symbols:

- `SPY`
- `QQQ`
- `IWM`
- `GLD`

The first real implementation should remain limited to the existing first SPY Continuation sample until explicitly expanded.

## Allowed Setup Families

Allowed v1 setup families:

- `Ideal`
- `Clean Fast Break`
- `Continuation`

The setup family must be copied from the replay signal row or candidate input. It must not be recomputed from future candles.

## Eligible Signal Rows

A row is eligible for chart outcome calculation only when all of these are true:

- `symbol` is one of the allowed v1 symbols.
- `setup_type` / `setup_family` is one of the allowed v1 setup families.
- `final_verdict` is `TRADE`.
- `current_state` is `signal`.
- `trigger_state` is `triggered`.
- `primary_blocker` is null.
- `trigger_level` is numeric.
- `invalidation` is numeric and known at entry.
- `winner_selection_result.selected_setup_type` matches the row setup family.
- The signal timestamp exists in the replay/source artifact trail and the next eligible 1H RTH candle exists in the candidate lookahead window.

Rows with `NO_TRADE`, `PENDING`, `watching`, `developing`, `confirmation_candidate`, `spent`, `follow_through_context`, `probe_unconfirmed`, `not_present`, `spent`, or a non-null primary blocker are not entry rows in v1. They may be preserved later as skipped/disqualified audit rows, but they must not produce chart outcomes in the first calculation pass.

Known eligible SPY rows from the inspected signal logs include the Continuation `triggered_signal_stage_candidate`, the Ideal `ideal_triggered_signal_stage_candidate`, and the Clean Fast Break signal rows with `final_verdict: TRADE`. The recommended first implementation should use only the first SPY Continuation sample.

## Entry Timestamp Rule

The default v1 entry timestamp is the timestamp of the next eligible 1H RTH candle after the eligible signal row timestamp.

The signal row candle is not reused as the entry candle unless a future explicit schema/rules update adds same-candle completed-trigger handling. If the next eligible candle is missing before source end, the output must be `unresolved_insufficient_lookahead` or `no_entry` according to the predeclared source-end policy, not a fabricated result.

## Entry Price Rule

The default v1 entry reference price is the next eligible candle open.

This is a chart reference price only. It is not a fill, limit order, market order, option price, spread value, or execution-quality claim. If a candidate declares a different schema-valid `entry_price_policy`, that policy must be documented before calculation and cannot be selected after future candles are reviewed.

## Invalidation Price Rule

The invalidation reference price is copied from the eligible signal row or candidate input before any future candle scan.

For bullish rows (`CALL`, `LONG`, `BULLISH`), invalidation is reached when a future candle low touches or crosses the invalidation level before follow-through or time stop. For bearish rows (`PUT`, `SHORT`, `BEARISH`), invalidation is reached when a future candle high touches or crosses the invalidation level before follow-through or time stop.

Invalidation must not be moved, widened, tightened, or re-derived from future candles. If invalidation is missing or non-numeric, the row is ineligible for real v1 calculation.

## Follow-Through Threshold Rule

Follow-through is reached only when the predeclared candidate `follow_through_condition` is satisfied before invalidation or time stop.

For the first implementation, the runner should apply the threshold already declared in the input candidate, such as `favorable_points` with a numeric threshold and touch/close policy. The threshold must not be hard-coded from observed future results. The existing first SPY Continuation fixture's 2.0 point threshold may be used only because it is already declared in the sample input, not because it is profitability proof or a global v1 threshold.

For bullish rows, favorable points are measured from entry reference price to future high. For bearish rows, favorable points are measured from entry reference price to future low. Close-based policies require the candle close to satisfy the threshold; touch-based policies may use high/low.

## Failure Rule

Failure is a chart thesis failure, not option P&L.

The default failure outcome is `invalidated` when the invalidation rule is reached before follow-through or time stop. Other failure conditions, such as trigger-hold failure or thesis-level reversal, may be applied only when predeclared in the candidate input. A future hard blocker must not be invented from future candles unless a later schema explicitly adds a predeclared blocker scan.

If follow-through and invalidation are both touched within the same post-entry candle and intrabar ordering cannot be known from 1H OHLCV, v1 should use conservative ordering: invalidation wins. This avoids using hindsight to assume favorable intrabar sequencing.

## Time-Stop Rule

Time stop applies when neither follow-through nor invalidation is reached before the predeclared maximum hold window.

The hold window is read from the candidate `time_stop_condition` and `lookahead_window`, including maximum candles, maximum sessions, same-day policy, fast-swing policy, and source-end policy. The terminal reference for a time stop is the close of the final allowed candle in the declared window.

If source data ends before the declared time-stop window can complete, the output must be `unresolved_insufficient_lookahead`.

## Same-Day Classification Rule

Classify an outcome as same-day when entry timestamp and terminal timestamp have the same regular-session date.

Use:

- `same_day` for same-session follow-through.
- `invalidated_same_day` for same-session invalidation.
- `time_stop_same_day` for same-session time stop.

Same-day is an analysis label only. It is not live trading permission.

## Fast-Swing Classification Rule

Classify an outcome as fast-swing when the terminal condition occurs after the entry session but within the predeclared fast-swing maximum session window.

Use:

- `fast_swing` for follow-through after the entry session.
- `invalidated_fast_swing` for invalidation after the entry session.
- `time_stop_fast_swing` for fast-swing time stop.

Overnight carry remains a chart classification only. It does not model option gap risk, overnight fills, account risk, or live trade permission.

## Max Favorable Move Rule

MFE is the largest favorable underlying-chart move from entry reference price through the first terminal candle, using no candles after the first terminal condition.

For bullish rows, MFE points equal max high minus entry reference price. For bearish rows, MFE points equal entry reference price minus min low. MFE percent is MFE points divided by entry reference price. MFE chart R is MFE points divided by likely chart risk points when risk is positive.

MFE should record points, percent, chart R, timestamp, candle index, and candles after entry. It must not imply option delta, spread value, or dollar P&L.

## Max Adverse Move Rule

MAE is the largest adverse underlying-chart move from entry reference price through the first terminal candle, using no candles after the first terminal condition.

For bullish rows, MAE points equal entry reference price minus min low. For bearish rows, MAE points equal max high minus entry reference price. MAE percent is MAE points divided by entry reference price. MAE chart R is MAE points divided by likely chart risk points when risk is positive.

MAE should record points, percent, chart R, timestamp, candle index, and candles after entry. It must not imply account drawdown, option loss, spread loss, or broker execution.

## Headline and Gap-Risk Handling

Macro, IV, event, 24H/daily, and headline context must be copied as unavailable or unconfirmed unless a source artifact explicitly confirms them.

Chart gaps may be measured from candles when a session opens away from the prior available RTH close. The gap direction, points, and percent may be recorded from chart data, but the cause of the gap must not be inferred. If no headline source exists, `gap_cause_known` remains false and `gap_cause_source` remains null.

## Likely Risk vs Full-Risk Handling

Likely chart risk is the absolute distance between entry reference price and invalidation reference price.

Chart R multiples may use likely chart risk when it is positive and known. Full financial risk is out of scope and must remain unmodeled. Full risk may later include option debit, spread width, slippage, liquidity, failed exits, assignment/exercise edge cases, account sizing, and gap-through-invalidation behavior, but none of those are v1 chart calculation fields.

## No-Hindsight Rules

v1 must enforce:

- Setup identity, trigger level, invalidation, blockers, cautions, and source timestamp are copied from source artifacts or predeclared input.
- Entry, invalidation, follow-through, failure, time-stop, MFE, MAE, and classification rules are fixed before scanning future candles.
- Future candles are used only after the entry candidate is defined.
- The scan stops at the first terminal condition.
- Same-candle follow-through/invalidation ambiguity uses conservative ordering rather than favorable assumed sequencing.
- Source end produces unresolved/insufficient-lookahead status when a terminal condition cannot be proven.
- Missing context is marked unavailable or unconfirmed.
- Manual overrides remain disallowed in v1 real calculation.

## Excluded Fields

Explicitly excluded from v1 calculation:

- option P&L
- option-spread pricing
- Greeks
- option chain lookup
- bid/ask behavior
- fills or missed fills
- slippage
- commissions
- account sizing
- account balance
- buying power
- account drawdown
- broker/order execution
- order routing
- live alert routing
- watcher state mutation

## Known Limits

- This is a rules plan only; real calculation implementation has not started.
- The existing runner is a scaffold/sample validator, not a real backtester.
- The first real implementation should cover only the first SPY Continuation sample before broader setup coverage.
- SPY has real replay signal coverage for Continuation, Ideal, and Clean Fast Break; QQQ, IWM, and GLD do not yet have equivalent local real replay closeout evidence.
- Current real source artifacts are 1H RTH candles and signal/stage/lifecycle logs, not tick data or intrabar sequences.
- Same-candle terminal ordering cannot be known from 1H OHLCV, so conservative ordering is required.
- Macro, IV, event, headline, and full 24H/daily context remain unavailable or unconfirmed.
- Chart outcomes do not prove option profitability, account safety, watcher readiness, production readiness, or live trade readiness.

## Non-Changes

- **`main.py` changed:** no
- **Schemas changed:** no
- **Fixtures changed:** no
- **Runner code changed:** no
- **Real calculation implementation started:** no
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Watcher work started:** no

## Recommended Next Task

Create minimal real chart outcome calculation implementation for the first SPY Continuation sample only, using this rules plan as the source of truth and preserving the chart-only boundary.
