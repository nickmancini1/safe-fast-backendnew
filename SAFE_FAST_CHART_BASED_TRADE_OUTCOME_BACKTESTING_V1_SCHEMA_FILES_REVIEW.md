# SAFE-FAST Chart-Based Trade Outcome Backtesting v1 Schema Files Review

## Schema Files Status

- **Schema files status:** PASS
- **Baseline:** patch8
- **Latest local commit reviewed:** `a48c6a2 Add chart-based trade outcome backtesting v1 schema design`
- **Scope:** create chart-based trade outcome backtesting v1 schema files only.
- **Backtesting implementation started:** no

## Files Created

- `chart_trade_outcome_backtesting/schemas/chart_outcome_backtest_input_v1.schema.json`
- `chart_trade_outcome_backtesting/schemas/chart_outcome_backtest_output_v1.schema.json`
- `chart_trade_outcome_backtesting/README.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_SCHEMA_FILES_REVIEW.md`

## Input Schema Coverage

The input schema defines a deterministic chart-only candidate derived from a qualifying historical signal replay row.

It includes:

- allowed symbols: SPY, QQQ, IWM, GLD
- allowed setup families: Ideal, Clean Fast Break, Continuation
- setup identity fields
- stage and lifecycle fields
- entry condition fields
- invalidation fields
- follow-through fields
- failure fields
- time-stop fields
- source candle window fields
- same-day and fast-swing policy fields through time-stop and lookahead definitions
- headline and gap-risk context fields
- likely risk versus full-risk notes
- no-hindsight audit fields
- explicit exclusion flags for option P&L, option-spread pricing, account sizing, broker/order execution, and watcher implementation

## Output Schema Coverage

The output schema defines the measured chart-only result for one predeclared input candidate.

It includes:

- entry status
- terminal outcome type
- terminal timestamp and terminal candle reference
- holding-period fields
- max favorable move fields
- max adverse move fields
- chart R multiple
- likely chart risk fields
- same-day versus fast-swing classification fields
- headline and gap-risk context fields
- no-hindsight audit fields
- known unavailable context fields
- explicit `false` flags for full-risk modeling, option P&L modeling, account sizing modeling, and broker/order execution modeling

## Chart-Only Boundary

The schema files are chart-only. They measure underlying-chart behavior after a qualifying signal candidate and do not create a backtester.

Excluded from v1 schema files:

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

## No-Hindsight Boundary

The schema files preserve no-hindsight controls:

- setup identity is copied from source replay artifacts or predeclared candidate input
- entry, invalidation, follow-through, failure, and time-stop rules are recorded before future candles are scanned
- future candles are only used to measure post-entry chart behavior
- outcome classification stops at the first terminal condition
- insufficient source lookahead is represented as unresolved rather than fabricated
- manual overrides are not permitted in v1 schema records

## Non-Changes

- **`main.py` changed:** no
- **Historical replay runner changed:** no
- **Existing historical replay schemas changed:** no
- **Fixtures changed:** no
- **Reports changed:** no
- **Backtesting implementation started:** no
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Watcher implementation started:** no

## Validation

- **Input schema JSON validation result:** PASS
- **Output schema JSON validation result:** PASS
- **Historical signal replay runner result:** PASS
- **Contract tests result:** PASS
- **Stage-message result:** PASS
- **Fixture validation result:** PASS
- **Full replay result:** PASS

## Recommended Next Task

Create the first chart-based trade outcome backtesting v1 sample input/output fixture.
