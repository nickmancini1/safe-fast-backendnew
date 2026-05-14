# SAFE-FAST Chart-Based Trade Outcome Backtesting v1 Plan

## Planning Status

- **Planning status:** PASS
- **Baseline:** patch8
- **Latest local commit reviewed:** `5e1cdbe Add next bounded phase decision review`
- **Scope:** docs-only planning review for chart-based trade outcome backtesting v1.
- **Implementation status:** not started.

This plan defines the intended chart-outcome methodology only. It does not implement a backtester, change runner behavior, change schemas, change fixtures, change reports, model option P&L, add account sizing, start watcher behavior, auto-trade, or make live trade decisions.

## Purpose

Chart-based trade outcome backtesting v1 should test whether qualifying SAFE-FAST historical signals led to useful underlying-chart outcomes after entry, using only candles and setup state that would have been available at the time.

The purpose is to measure whether the chart thesis worked, failed, or required a time stop before any later phase attempts option-spread pricing, execution realism, account sizing, or proof-mode trading readiness.

## What SPY Real Historical Replay Already Proves

The SPY real historical replay v1 closeout proves:

- A validated real SPY 1h RTH source CSV exists with 293 rows from 2026-03-16T09:30:00-04:00 through 2026-05-13T14:30:00-04:00.
- Continuation, Ideal, and Clean Fast Break each have selected real SPY source windows.
- Each setup family has a six-row no-hindsight fixture built from real SPY source candles.
- The runner emits signal log, summary, and regression candidate reports for all three SPY setup-family fixtures.
- The replay artifacts remain signal/stage/lifecycle only.

It does not prove profitability, expected option behavior, fill quality, trade management, account safety, or production readiness.

## What v1 Must Prove

Chart-based trade outcome backtesting v1 must prove:

- Qualifying signal rows can be converted into deterministic chart-only trade outcome candidates.
- Entry, invalidation, follow-through, failure, and time-stop rules are defined before looking at future candles.
- Max favorable move and max adverse move can be measured from the underlying chart without option pricing.
- Same-day versus fast-swing outcomes can be classified from candle behavior and time-in-trade.
- Results can be reported by symbol, setup family, direction, entry type, outcome type, and hold classification without hindsight.

## Allowed Universe

v1 universe is limited to:

- SPY
- QQQ
- IWM
- GLD

SPY may be used first because SPY already has real three-setup replay coverage. QQQ, IWM, and GLD remain allowed by methodology but need their own source-data and replay evidence before broad performance claims.

## Setup Families

Allowed setup families:

- Ideal
- Clean Fast Break
- Continuation

No other setup families should be introduced in v1.

## Chart-Only Boundary

v1 is chart outcome only:

- No option P&L.
- No spread pricing.
- No Greeks.
- No bid/ask or slippage modeling.
- No fills or missed-fill logic.
- No account sizing.
- No broker/order/execution modeling.
- No live trade decisions.

The unit of measurement is the underlying chart move after a qualifying entry condition, not the dollar result of an option contract or spread.

## Entry-Condition Definition

An entry candidate exists only when a replay row reaches an approved signal stage for an allowed setup family and the candle information available at that row supports a defined manual-style trigger.

The entry condition must be recorded with:

- symbol
- setup family
- direction
- signal timestamp
- entry trigger type
- trigger price or trigger reference level
- invalidation reference known at entry
- available blockers and cautions
- source row or replay row that created the signal

The planned v1 default is to use the next eligible candle after the signal row for outcome measurement unless the future schema explicitly defines same-candle completed-trigger handling. This rule must be finalized in the schema design before implementation.

## Invalidation Definition

Invalidation is the underlying chart level or condition that says the setup thesis failed. It must be defined at entry and cannot be moved using future information.

Expected invalidation references may include:

- 1H 50 EMA loss or reclaim failure, when that is the setup's primary invalidation reference.
- Setup-specific shelf, base, retest, or breakout-hold failure.
- Break back through the trigger level when the setup requires immediate hold.
- A prior structure level identified by the replay row.

The backtest must distinguish likely invalidation risk from full-risk exposure. Likely risk is the chart distance from entry to invalidation. Full-risk exposure remains a later option/account concept and is not modeled in v1.

## Follow-Through Definition

Follow-through means the underlying chart confirms the signal after entry.

v1 should record follow-through when price moves favorably from entry and either:

- reaches a predefined chart target or measured favorable threshold,
- closes in the expected direction after entry,
- holds the breakout/retest/shelf and continues without violating invalidation,
- or reaches a setup-specific first trouble area or continuation objective.

The exact threshold must be fixed in the schema design before implementation. The threshold must not be chosen after seeing the outcome.

## Failure Definition

Failure means the underlying chart invalidates the setup or does not confirm the thesis before risk control requires exit.

Failure cases include:

- invalidation level touched or closed through, according to the schema-defined rule,
- trigger fails to hold when hold is required,
- setup reverses back through the thesis level,
- no meaningful favorable movement before a time stop,
- or a hard blocker appears in the available chart state before follow-through.

The implementation must report failure type separately from raw price movement.

## Time-Stop Definition

A time stop is a planned exit classification when the chart does not produce enough follow-through within the allowed holding window and does not clearly invalidate first.

v1 should support:

- same-day time stop for signals that must work during the current session,
- fast-swing time stop for signals that remain structurally valid but fail to follow through within the allowed 1-3 day window.

The exact candle count, session boundary, and overnight handling must be finalized in the schema design before implementation.

## Max Favorable Move

Max favorable move is the best underlying-chart move in the trade direction after entry and before the first terminal condition.

It must be recorded in chart terms, such as:

- points,
- percent from entry,
- R multiple versus planned chart invalidation distance,
- timestamp of max favorable move,
- candle count to max favorable move.

No option delta, spread value, or contract P&L should be inferred from this field.

## Max Adverse Move

Max adverse move is the worst underlying-chart move against the trade direction after entry and before the first terminal condition.

It must be recorded in chart terms, such as:

- points,
- percent from entry,
- R multiple versus planned chart invalidation distance,
- timestamp of max adverse move,
- candle count to max adverse move.

Max adverse move should help evaluate whether the chart risk was realistic before option or account modeling exists.

## Same-Day vs Fast-Swing Classification

Each outcome should be classified as:

- `same_day`: entry and terminal condition occur in the same regular trading session.
- `fast_swing`: setup remains valid beyond the entry session and terminal condition occurs within the allowed short holding window.
- `time_stop_same_day`: same-day thesis did not follow through before the planned same-day stop.
- `time_stop_fast_swing`: fast-swing thesis did not follow through before the planned fast-swing stop.
- `invalidated_same_day`: invalidation occurred during the entry session.
- `invalidated_fast_swing`: invalidation occurred after the entry session but within the allowed fast-swing window.

Overnight carry is a chart classification only in v1. It is not approval for real overnight trading and does not model option gap risk.

## Headline and Gap-Risk Note

v1 must surface headline and gap risk as a known limitation because the current real replay source does not include reliable news, macro, IV, earnings, or event feeds.

Chart gaps can be measured if they appear in candles, but the cause of a gap must not be invented. Missing headline/event context should be marked unavailable or unconfirmed, not inferred.

## Likely Risk vs Full-Risk Distinction

v1 should report likely chart risk as the measured distance from entry to planned invalidation.

It must not treat that as full financial risk. Full risk belongs to later option/account phases and may include:

- full debit exposure,
- widened spreads,
- gap through invalidation,
- failed exit liquidity,
- slippage,
- assignment or exercise edge cases if options are later modeled.

v1 may document the distinction, but it must not calculate option loss or account drawdown.

## Output and Report Requirements

Future v1 reports should include:

- source artifact references,
- symbol,
- setup family,
- direction,
- signal timestamp,
- entry timestamp,
- entry reference price,
- invalidation reference,
- terminal outcome type,
- terminal timestamp,
- max favorable move,
- max adverse move,
- chart R multiple based on planned invalidation distance,
- same-day or fast-swing classification,
- blockers and cautions available at entry,
- no-hindsight audit fields,
- known unavailable context fields.

Reports must separate:

- qualifying signals,
- skipped or disqualified signals,
- invalidated outcomes,
- follow-through outcomes,
- time-stop outcomes,
- unresolved outcomes if source data ends before a terminal condition.

No report should claim profitability, account suitability, or option-spread performance.

## No-Hindsight Rules

v1 must enforce:

- Entry eligibility uses only replay state and candle data available at or before the signal timestamp.
- Invalidation and follow-through thresholds are defined before scanning future candles.
- Future candles are used only to measure what happened after entry.
- Outcome classification stops at the first terminal condition.
- Source-data end must produce unresolved or insufficient-lookahead status, not a fabricated outcome.
- Manual overrides, if ever allowed, must be recorded with reason and timestamp.

## Known Limits

- SPY has three-setup real replay coverage; QQQ, IWM, and GLD do not yet have equivalent local real replay closeout evidence.
- 24H/daily, macro, IV, and event context remain unavailable or unconfirmed in the current SPY source.
- Chart outcomes do not equal option-spread outcomes.
- Chart invalidation risk does not equal full debit risk.
- Same-day and fast-swing classifications are methodology labels, not live trade permission.
- v1 does not prove production readiness, watcher readiness, proof-mode manual trading readiness, or account safety.

## Non-Changes

- **`main.py` changed:** no
- **Runner code changed:** no
- **Schemas changed:** no
- **Fixtures changed:** no
- **Reports changed:** no
- **Backtesting implementation started:** no
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Watcher implementation started:** no

## Recommended Next Task

Design the chart-based trade outcome backtesting v1 schema, including entry, invalidation, follow-through, failure, time-stop, max favorable move, max adverse move, same-day/fast-swing classification, no-hindsight audit fields, and chart-only report fields.
