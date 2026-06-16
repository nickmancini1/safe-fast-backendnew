# SAFE-FAST Day 41 Cheap Starter Batch Next Steps

## Scope

This is a next-step plan after validating the cheap starter Databento files. It does not authorize downloads, evidence fills, backtests, P&L, proof, profitability, or readiness.

## Current Starter Status

- Cheap starter manifest exists.
- All six requested candidates have nonempty starter files for definitions, statistics, 10-minute TCBBO quotes, and 10-minute trades.
- Starter data can support first-pass raw option inspection for option universe, setup-time quote freshness, setup-time trade volume, and setup-time statistics/open-interest availability.
- Starter data does not prove a trade plan.

## Ordered Next Steps

1. Keep all raw Databento files local-only and unchanged.
2. Decide which setup family gets the next rule/regression authorization:
   - SPY Clean Fast Break for `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` and `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`;
   - Ideal for `SPY-REAL-HISTORICAL-IDEAL-001` and `QQQ-REAL-HISTORICAL-IDEAL-001`;
   - Continuation for `QQQ-REAL-HISTORICAL-CONTINUATION-001` and `SPY-REAL-HISTORICAL-CONTINUATION-001`.
3. Before evidence fill, create or accept the setup-specific lifecycle and contract-selection regression cases.
4. Use the starter data only for read-only option-universe and setup-window inspection after the relevant rules are accepted.
5. Record any starter-only blocker as missing evidence or missing rule authorization, not as low confidence.
6. Do not request full-window data until a later task explicitly authorizes the reason and scope.

## Candidate Routing

| Candidate | Starter-only route | Still blocked by |
| --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | First SPY CFB starter inspection batch with CFB 003. | SPY initial-break lifecycle/regression, SPY CFB contract-selection authorization, headline/execution/context rules, trade-plan rules. |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | First SPY CFB starter inspection batch with CFB 002. | SPY higher-base fresh-break lifecycle/regression, SPY CFB contract-selection authorization, headline/execution/context rules, trade-plan rules. |
| `SPY-REAL-HISTORICAL-IDEAL-001` | Ideal starter inspection only after Ideal rule package authorization. | Ideal lifecycle/gap/context/contract-selection rules and trade-plan rules. |
| `QQQ-REAL-HISTORICAL-CONTINUATION-001` | Continuation starter inspection only after Continuation rule package authorization. | Continuation lifecycle/context/contract-selection rules and trade-plan rules. |
| `QQQ-REAL-HISTORICAL-IDEAL-001` | Ideal starter inspection only after Ideal rule package authorization. | Ideal lifecycle/gap/context/contract-selection rules and trade-plan rules. |
| `SPY-REAL-HISTORICAL-CONTINUATION-001` | Continuation starter inspection only after Continuation rule package authorization. | Continuation lifecycle/context/contract-selection rules and trade-plan rules. |

## Full-Window Deferral

Full-window data should remain deferred until a later explicit task, because starter validation alone does not define:

- selected-contract entry and fill basis;
- exit, stop, invalidation, or time-exit rules;
- full quote path needs;
- cost and slippage assumptions;
- sample-size and promotion gates.

## Stop Condition

Stop after documenting starter coverage and updating project state. Do not fill evidence or run a backtest from this validation result.
