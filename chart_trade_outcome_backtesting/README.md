# SAFE-FAST Chart Trade Outcome Backtesting

## Status

This directory contains schema and documentation files for chart-based trade outcome backtesting v1 only.

Backtesting implementation has not started. There is no runner, fixture, report generation, watcher behavior, auto-trading, live read, live trade decision, option P&L model, account sizing model, or broker/order execution model in this directory.

## Boundary

Chart outcome backtesting v1 is limited to underlying-chart behavior after a qualifying historical signal replay row.

It may describe:

- chart entry conditions
- chart invalidation conditions
- chart follow-through conditions
- chart failure conditions
- chart time-stop conditions
- max favorable move on the underlying chart
- max adverse move on the underlying chart
- same-day versus fast-swing chart classification
- headline and gap-risk context availability
- no-hindsight audit fields

It must not model:

- option P&L
- option-spread pricing
- Greeks
- bid/ask behavior
- fills or missed fills
- slippage
- broker/order execution
- account sizing
- account drawdown
- watcher state mutation
- auto-trading
- live trade decisions

## Allowed v1 Universe

- SPY
- QQQ
- IWM
- GLD

## Allowed v1 Setup Families

- Ideal
- Clean Fast Break
- Continuation

## Schema Files

- `schemas/chart_outcome_backtest_input_v1.schema.json`
- `schemas/chart_outcome_backtest_output_v1.schema.json`

The input schema describes one chart-outcome candidate derived from a qualifying historical signal/stage/lifecycle replay row plus source candles for measuring future chart behavior.

The output schema describes the measured chart-only outcome for one input candidate after applying predeclared entry, invalidation, follow-through, failure, and time-stop rules.

## Next Task

Create the first chart-based trade outcome backtesting v1 sample input/output fixture.
