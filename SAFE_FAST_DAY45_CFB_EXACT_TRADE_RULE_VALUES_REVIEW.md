# SAFE-FAST Day 45 CFB Exact Trade-Rule Values Review

## Result

The first exact Clean Fast Break trade-rule values are accepted for regression and later grouped backtest-prep harness implementation.

The work stays bounded to rule values and data-only fixtures. No data was downloaded, no backtest was run, no P&L was calculated, no proof or profitability was claimed, and no candidate was marked ready.

## Accepted Values

- Side: long calls only.
- Entry prerequisite: setup, option context, and execution context must pass.
- Entry basis: accepted setup-safe ask plus `0.02` per-contract slippage buffer.
- Exit basis: selected option bid minus `0.02` per-contract slippage buffer.
- Profit target: `+25%` option premium from slippage-adjusted entry basis.
- Hard stop: `-15%` option premium from slippage-adjusted entry basis.
- Setup invalidation stop: active after entry; exit selected option at bid minus slippage when underlying invalidates setup.
- Time exit: no later than `15:45 ET` on signal day.
- Zero-cost fills: forbidden.
- Failure diagnosis: one primary named reason required.
- Sample size: promotion blocked below `20` valid completed CFB examples.
- Promotion: accepted rules, passing replay/regression, enough valid completed examples, and positive expectancy review after costs.

## Candidate Review

| Candidate | Review result |
| --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | Entry-rule-ready for later harness work only. It has the usable selected contract, setup-safe quote, ask `6.35`, bid `6.33`, clean option context, clean execution context, and invalidation `678.45`. |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | Still no-trade because the top-ranked quote is after setup. |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | Still no-trade because the selected quote is older than five minutes at setup. |

## Fixture Review

`historical_signal_replay/fixtures/cfb_exit_stop_cost_regression_fixtures.json` is updated to version `2`.

The fixture package now covers all required value cases from the task, including profit target, option premium stop, setup invalidation stop, time exit, entry ask, exit bid, slippage buffer, failure reason, sample-size gate, and promotion gate.

## Remaining Boundary

The next grouped implementation task may update the checker/tests and prepare the first backtest-prep harness. The harness must not produce P&L or counted results until a later task explicitly authorizes that run.
