# SAFE-FAST Historical Signal Replay v1 Plan

## Purpose

Historical Signal Replay v1 proves SAFE-FAST signal and stage behavior over historical bars.

It is not a profitability test. It does not measure trade outcome, option P&L, account sizing, or execution quality. The goal is to verify that the engine can walk forward through historical market structure and produce disciplined signal states, blockers, cautions, stage transitions, and human next steps without hindsight.

## Scope

Replay v1 scope is limited to:

- `SPY`
- `QQQ`
- `IWM`
- `GLD`

The first implementation should remain local and non-production.

## No-Hindsight Rules

Replay must process bars strictly bar by bar.

- No future candles may be read while evaluating the current bar.
- No future option prices may be read while evaluating the current bar.
- No retroactive labels may be applied to prior bars after later bars become known.
- Setup state, trigger state, blockers, cautions, and final verdict must be based only on data available at the evaluated timestamp.
- Any unavailable macro, IV, event, headline, or live-context field must be marked unconfirmed instead of inferred.

## Required Input Schema

Each replay input row or object must provide:

- `symbol`
- `timestamp`
- `candles_1h_rth`
- `context_24h_daily_placeholder`
- `market_calendar_session_info`
- `macro_placeholder`
- `iv_placeholder`
- `event_placeholder`

Placeholder fields must explicitly distinguish confirmed values from missing values. When macro, IV, or event data is unavailable, the value must be marked unconfirmed.

Example placeholder state names:

- `MACRO_UNCONFIRMED`
- `IV_UNCONFIRMED`
- `EVENT_UNCONFIRMED`
- `CONTEXT_24H_DAILY_UNCONFIRMED`

## Required Output Schema

Each replay signal log row or object must emit:

- `timestamp`
- `symbol`
- `setup_type`
- `setup_state`
- `stage`
- `trigger_state`
- `trigger_level`
- `invalidation`
- `room_status`
- `extension_status`
- `context_24h`
- `wall_thesis_fit`
- `final_verdict`
- `primary_blocker`
- `cautions_watchouts`
- `winner_selection_result`
- `human_next_step`

`final_verdict` must be limited to signal-state verdicts such as `TRADE`, `PENDING`, or `NO_TRADE`. It must not include realized trade outcome, profit, loss, or option performance.

## Lifecycle Fields for Continuous Watcher Foundation

Replay v1 should include lifecycle fields needed by a future watch-only Continuous Watcher:

- `first_seen`
- `last_seen`
- `state_changed`
- `prior_state`
- `current_state`
- `trigger_changed`
- `blocker_changed`
- `duplicate_alert_suppression_key`

These fields are for future lifecycle tracking and duplicate alert suppression only. They must not introduce live trade decisions, production alerts, or auto-trading.

## Replay Run Outputs

Each replay run should produce:

- CSV or JSONL signal log
- Summary report
- Regression candidate list

The regression candidate list should identify historically interesting bars or state transitions that deserve fixture coverage before engine behavior changes.

## Metrics

Replay v1 summary reporting should include:

- Signal count by ticker
- Signal count by setup type
- `TRADE`, `PENDING`, and `NO_TRADE` counts
- Blocker frequency
- Caution frequency
- Stage transition counts
- Stale, spent, late, and pending counts

These metrics describe signal behavior and stage quality. They do not prove profitability.

## Explicit Boundary

Historical Signal Replay v1 must not include:

- Trade outcome backtesting
- Option P&L
- Account-mode sizing
- Production deployment
- Auto-trading
- Live trade decisions

Replay v1 is a signal and stage replay layer only.

## Handoff to Trade Outcome Backtest v1

Trade Outcome Backtest v1 may start only after replay planning/schema approval, fixture definition, and clean local regression evidence.

Replay v1 should hand off:

- Timestamped signal logs
- Signal verdicts and blockers
- Trigger and invalidation levels known at the evaluated timestamp
- Regression candidates that prove no-hindsight signal behavior

Trade Outcome Backtest v1 is the later phase that may evaluate trade outcomes, option paths, planned invalidation risk, and realized P&L. Those concerns stay out of Replay v1.

## Handoff to Continuous Watcher Foundation

Continuous Watcher foundation can reuse replay lifecycle fields to design watch-only state tracking:

- When a setup first appears
- Whether a setup state changed
- Whether trigger or blocker state changed
- Whether duplicate alerts should be suppressed
- What human next step should be surfaced

This handoff is planning-only until replay fixture/schema scaffolding and regression gates are complete.

## Required Next Implementation Gate

Before implementation begins:

- Planning/schema approved
- No-hindsight sample fixture defined
- Local regression still clean
- Build state updated

The next task after this plan is to create the signal replay fixture/schema scaffold only, not full replay implementation and not trade outcome backtesting.
