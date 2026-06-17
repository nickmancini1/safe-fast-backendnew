# SAFE-FAST Day 45 CFB Exact Trade-Rule Values

## Direct Answer

The proposed first-pass conservative Clean Fast Break trade-rule values are accepted for regression and backtest-prep implementation.

This is not a backtest authorization. It does not calculate P&L, prove profitability, choose a real trade, mark a candidate ready, or change intake-ready status.

## Rule Decisions

| Proposed value | Decision | Reason |
| --- | --- | --- |
| Long call only | accepted for first regression pass | Matches the current selected-contract policy and keeps the first pass narrow. |
| Entry allowed only when setup, option context, and execution context pass | accepted for first regression pass | Prevents entry from stale quotes, quote-after-signal rows, missing selected contracts, failed execution context, or failed option context. |
| Entry fill for later backtest uses accepted setup-safe quote ask | accepted for first regression pass | Conservative long-call entry basis already used by prior checker work. |
| Exit uses earliest of profit target, stop, invalidation, or time exit | accepted for first regression pass | Gives one deterministic exit order for the later harness. |
| Profit target +25% option premium from entry | accepted for first regression pass | Conservative first exact target; must be sample-tested before promotion. |
| Hard option premium stop -15% from entry | accepted for first regression pass | Explicit loss-control value for first regression pass. |
| Setup invalidation stop also applies if underlying invalidates setup | accepted for first regression pass | Preserves the setup invalidation level as an active trade-plan exit. |
| Time exit no later than 15:45 ET on signal day | accepted for first regression pass | Avoids overnight and end-of-session ambiguity in the first pass. |
| Entry uses ask | accepted for first regression pass | Conservative long-call entry basis. |
| Exit uses bid | accepted for first regression pass | Conservative long-call exit basis. |
| Add 0.02 per contract slippage buffer on entry and exit | accepted for first regression pass | Numeric first-pass cost buffer; later cost review may change it. |
| No zero-cost fills | accepted for first regression pass | Prevents synthetic free option fills. |
| Every no-trade or failed trade must name one primary reason | accepted for first regression pass | Required for repair and comparison. |
| First backtest-prep batch can run on current candidates | accepted for implementation planning only | The current candidates can test the harness gates, but this task does not run the harness. |
| No promotion from fewer than 20 valid completed CFB examples | accepted for first regression pass | One reference case is not enough for promotion. |
| Promotion requires accepted rules, passing replay/regression, enough examples, and positive expectancy review after costs | accepted for first regression pass | Keeps readiness blocked until post-cost evidence exists. |

## Exact First-Pass Values

| Rule area | Exact first-pass value |
| --- | --- |
| Side | Long calls only. |
| Entry prerequisite | Setup passes, selected option context passes, and execution context passes. |
| Entry basis | Accepted setup-safe ask plus `0.02` slippage buffer. |
| Profit target | Exit when selected option bid minus `0.02` is at least `+25%` above ask plus `0.02`. |
| Hard option stop | Exit when selected option bid minus `0.02` is at or below `-15%` from ask plus `0.02`. |
| Setup invalidation stop | Exit selected option if the underlying trades through the accepted setup invalidation; exit basis is bid minus `0.02`. |
| Time exit | Exit any still-open same-day CFB test position no later than `15:45 ET` on signal day; exit basis is bid minus `0.02`. |
| Zero-cost fills | Forbidden. |
| Sample-size gate | Promotion requires at least `20` valid completed CFB examples. |
| Promotion gate | Accepted rules, passing replay/regression, at least `20` valid completed CFB examples, and positive expectancy review after costs. |

## Candidate Application

| Candidate | First-pass result |
| --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | Entry-rule-ready for later grouped backtest-prep harness implementation. Selected contract `SPY   260427C00685000`, quote `2026-04-13T16:29:04.514819033Z`, bid `6.33`, ask `6.35`, option context `clean`, execution context `clean`, invalidation `678.45`. No P&L is counted here. |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | No-trade/repair reference because top-ranked quote is after signal; reason `quote_after_signal`. |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | No-trade/repair reference because selected quote is older than five minutes; reason `quote_age_above_5_minutes`. |

## Fixture Package

Updated fixture file: `historical_signal_replay/fixtures/cfb_exit_stop_cost_regression_fixtures.json`.

Coverage now includes the entry-ready SPY CFB 002 reference, SPY CFB 003 quote-after-signal no-trade, QQQ CFB 001 stale-quote no-trade, profit target, option premium stop, setup invalidation stop, 15:45 ET time exit, entry ask rule, exit bid rule, 0.02 slippage buffer, zero-cost fill rejection, required failure reason, 20-example sample-size gate, and promotion gate.

## Guardrails

- Evidence filled: NO.
- Raw Databento files changed: NO.
- Databento downloaded: NO.
- Full-window data used or requested: NO.
- Backtest authorized: NO.
- Backtest run: NO.
- Real trade chosen: NO.
- P&L calculated: NO.
- Candidate marked ready: NO.
- Intake-ready count changed: NO.
- Proof accepted: NO.
- Profitability claim made: NO.
