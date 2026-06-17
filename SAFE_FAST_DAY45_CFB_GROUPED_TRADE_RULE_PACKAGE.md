# SAFE-FAST Day 45 CFB Grouped Trade-Rule Package

## Bottom Line

This package defines the first conservative Clean Fast Break trade-plan rule shape for regression work only.

`SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` is the main reference because it has accepted lifecycle evidence, starter selected-contract context `clean`, and starter execution context `clean`. `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` is the paired no-trade/repair reference because the top-ranked starter quote is after setup. `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` is the stale-quote failed-execution reference because the selected quote is older than five minutes.

This package does not authorize a backtest, choose a real trade, calculate P&L, prove profitability, mark readiness, or change intake-ready status.

## Rule Classifications

| Rule | First-pass rule | Classification | Notes |
| --- | --- | --- | --- |
| Entry rule | Entry eligibility can only use setup-time-safe data. A long-call candidate must have an accepted selected contract, a setup-time-safe selected quote, and execution context not failed. | accepted for first regression pass | This is an eligibility gate, not a full fill/backtest rule. Exact entry timing after setup still needs implementation tests. |
| Selected-contract use rule | Use the selected/top-ranked contract produced by the accepted CFB selector for that candidate family. If the selected/top-ranked contract fails a required gate, no fallback contract is allowed. | accepted for first regression pass | Supports SPY CFB 002 as usable starter reference, SPY CFB 003 as quote-after-signal no-trade, and QQQ CFB 001 as stale-quote failure. |
| Fill price rule | For long-call first-pass testing, entry fill basis is the selected quote ask price only. Missing ask blocks entry. | accepted for first regression pass | Exit fill basis is not accepted yet. Ask basis is a conservative entry assumption only. |
| Exit rule | No profit target, loss exit, or option-exit basis is accepted yet. Missing exit rule blocks countable backtest results. | decision still needed | Backtest-prep can build the checker gate, but cannot count results until exit behavior is defined. |
| Stop/invalidation rule | Underlying invalidation must be present. Exact translation from underlying invalidation to option exit is not accepted yet. | decision still needed | Missing invalidation blocks entry eligibility; option stop handling still needs a rule. |
| Time exit rule | No max-hold, end-of-day, expiration-proximity, or stale-signal time exit is accepted yet. | decision still needed | The checker must report `missing_time_exit_rule` instead of filling the gap implicitly. |
| Cost/slippage rule | Costs and slippage must be explicit before a countable result. Missing cost or slippage assumptions block proof and counted P&L. | decision still needed | Current first pass can require declared fields, but the numeric assumptions are not accepted. |
| Failure diagnosis rule | No-trade and blocked cases must carry named reasons. Required labels include `quote_after_signal`, `quote_age_above_5_minutes`, `missing_selected_contract`, `missing_entry_quote`, `missing_exit_rule`, `missing_invalidation`, `missing_cost_slippage`, `sample_size_gate_missing`, and `promotion_gate_missing`. | accepted for first regression pass | Failure reasons must not be hidden inside generic unknown or skipped rows when a specific gate is known. |
| Sample-size rule | A sample-size gate is required before promotion or proof. Exact minimum counts by symbol/family/pass/fail/no-trade category are not accepted yet. | decision still needed | Missing sample-size rule blocks readiness and promotion. |
| Promotion rule | A promotion gate is required before moving from reconsideration-eligible to intake-ready, shadow planning, or later money stages. Exact criteria are not accepted yet. | decision still needed | Missing promotion rule blocks readiness and proof claims. |

## Candidate Application

| Candidate | First-pass result | Reason |
| --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | First usable CFB backtest-prep reference after checker/tests exist and missing exit/stop/cost/time/sample/promotion decisions are handled. | Starter selected contract `SPY   260427C00685000`; quote at `2026-04-13T16:29:04.514819033Z`; ask `6.35`; execution context `clean`; no fallback needed. |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | Repair/no-trade reference. | Top-ranked starter contract `SPY   260429C00700000` has only a local quote/trade row after the `2026-04-15T18:30:00Z` setup boundary, so the quote is rejected and no fallback is allowed. |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | Repair/failed-execution reference. | Selected quote at `2026-04-13T16:06:30.640301037Z` is about `23m 29.359699s` old at setup, so execution fails with `quote_age_above_5_minutes`. |

## Regression Fixture Package

Fixture file: `historical_signal_replay/fixtures/cfb_trade_rule_regression_fixtures.json`.

The fixtures cover the usable SPY CFB 002 reference, SPY CFB 003 quote-after-signal rejection, QQQ stale-quote rejection, missing selected contract, missing entry quote, missing exit rule, missing stop/invalidation, missing cost/slippage, failure diagnosis required, sample-size gate required, and promotion gate required.

## Data Rule

No additional data is needed for this rule-package definition. More full-window option data is deferred until the checker and missing rule decisions state exact required fields and windows, then a cost check and user approval are required before any download.

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

