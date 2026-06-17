# SAFE-FAST Day 45 CFB Exit Stop Cost Rule Package

## Direct Answer

This package defines the first conservative remaining Clean Fast Break trade-plan rule shape for grouped review and regression planning.

It does not make `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` countable in a backtest yet. The candidate has usable starter entry evidence, but the exit, stop translation, cost/slippage, sample-size, and promotion rules still need human acceptance and regression coverage before any counted result, P&L, proof, profitability, readiness, or intake-ready claim.

## Rule Classification

| Rule | First conservative rule shape | Classification | Blocker |
| --- | --- | --- | --- |
| Exit | A countable long-call CFB result must exit only by an accepted option-exit rule. No profit target, option bid/ask exit basis, partial exit, trailing exit, or discretionary exit is accepted by this package. | still needs human decision | Exact option exit basis and trigger order are not accepted. |
| Stop/invalidation | The underlying invalidation must exist before entry eligibility. A future accepted stop must translate the underlying invalidation into an option exit without using future candles or outcome data. | still needs human decision | Translation from underlying invalidation to option exit is not accepted. |
| Time exit | A future accepted time exit must name max hold, end-of-day handling, stale-signal handling, and expiration-proximity handling before countable testing. | still needs human decision | No exact time-exit values are accepted. |
| Cost/slippage | A countable result must declare explicit commission/fees and option slippage assumptions. Raw quotes alone cannot imply a cost model. | still needs human decision | Numeric costs and slippage assumptions are not accepted. |
| Failure diagnosis | Every blocked or no-trade row must carry the most specific known reason, including quote-after-signal, stale quote, missing selected contract, missing entry quote, missing exit rule, missing stop rule, missing cost/slippage, missing sample-size gate, and missing promotion gate. | accepted for first regression pass | Needs fixture coverage only; no P&L or backtest implication. |
| Sample size | Promotion cannot rely on one usable example. A later accepted gate must define minimum counts by setup family, symbol, pass/fail/no-trade category, and repair category. | still needs human decision | Exact counts are not accepted. |
| Promotion | Reconsideration-eligible cannot become intake-ready, shadow-planning-ready, or money-stage-ready without an accepted promotion gate. | still needs human decision | Exact criteria are not accepted. |

## Candidate Application

| Candidate | Package result | Reason |
| --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | Usable entry reference, still blocked before countable backtest. | Selected contract `SPY   260427C00685000`, setup-time-safe quote, ask `6.35`, and execution context `clean`; exit, stop translation, cost/slippage, sample-size, and promotion remain unaccepted. |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | No-trade/repair reference. | Top-ranked starter quote is after setup and no fallback is allowed; expected diagnosis is `quote_after_signal`. |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | No-trade/repair reference. | Selected quote is older than five minutes; expected diagnosis is `quote_age_above_5_minutes`. |

## Regression Fixture Package

Fixture file: `historical_signal_replay/fixtures/cfb_exit_stop_cost_regression_fixtures.json`.

The fixtures are data-only and cover:

- SPY CFB 002 as a usable-entry case still blocked until exit, stop, and cost rules are accepted.
- SPY CFB 003 as a quote-after-signal no-trade case.
- QQQ CFB 001 as a stale-quote no-trade case.
- Missing exit rule.
- Missing stop rule.
- Missing cost/slippage rule.
- Missing sample-size rule.
- Missing promotion rule.
- Required named failure diagnosis.

## Backtest Boundary

Cheap starter data can test the grouped gate behavior, named failure diagnosis, selected-contract/no-fallback behavior, ask entry basis presence, stale quote rejection, and missing-rule blockers.

Full-window option data is deferred. It should be requested only after exact exit, stop translation, time exit, and cost/slippage rules are accepted, exact fields/windows are known, a cost check is performed, and the user approves the download.

## Guardrails

- Backtest authorized: NO.
- Real trade chosen: NO.
- P&L calculated: NO.
- Proof accepted: NO.
- Profitability claimed: NO.
- Candidate marked ready: NO.
- Intake-ready count changed: NO.
- Raw Databento files changed: NO.
- Evidence filled: NO.
