# SAFE-FAST Day 45 Trade Rule Gap Package

## Bottom Line

The project is not blocked by a lack of candidate names. It is blocked by missing trade-plan rules.

The next useful grouped build should define the first conservative trade-rule package before any backtest-prep harness or full-window data pull.

## Required Rule Gaps

| Rule | Current state | Needed decision before counting a trade-plan result |
| --- | --- | --- |
| Entry rule | Missing. | Exact entry timing after setup, allowed quote source, no-hindsight boundary, and whether entry can occur on the setup candle, next quote, next bar, or another fixed trigger. |
| Selected contract rule | Partially accepted for QQQ CFB and starter SPY CFB; not project-wide. | Decide whether the first trade-rule package uses SPY CFB starter-selected contract logic only, reuses QQQ CFB shape with SPY-specific fixtures, or requires a full-window reviewed universe. |
| Fill price rule | Missing for countable results. | Decide long-call fill basis: ask, midpoint, bid/ask condition, delayed quote, or explicit no-fill. The QQQ execution doc notes ask-only for later long-call testing, but this is not yet a complete fill rule. |
| Exit rule | Missing. | Define profit-taking, invalidation response, target/stop priority, quote source, and whether exits use bid, mid, or another fixed assumption. |
| Stop/invalidation rule | Missing. | Translate underlying invalidation into option exit behavior: immediate option exit, candle-close confirmation, intrabar rule, or no-trade failure. |
| Time exit rule | Missing. | Define end-of-day, max-hold, expiration-proximity, and stale-signal handling. |
| Spread/cost/slippage rule | Missing for countable results. | Define commission, fees, spread crossing, slippage, max spread, max spread percent, and whether starter context is enough or full-window data is required. |
| Failure diagnosis rule | Missing. | Label no-trade and failed cases separately: stale quote, missing quote, missing OI, post-signal quote, headline unknown, rule missing, cost too high, invalidation before entry, and data insufficient. |
| Sample-size rule | Missing. | Define minimum counts by family, symbol, pass/fail/no-trade category, and how much repair evidence is enough before promotion. |
| Promotion rule | Missing. | Define movement from reconsideration-eligible to backtest-prep, intake-ready, shadow planning, and later money stages. |

## First Conservative Package Scope

Recommended first scope: SPY Clean Fast Break starter trade-rule package using `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` as the reference case and `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` as the paired failure/no-trade diagnostic case.

This avoids starting with the QQQ CFB stale-quote failure and avoids applying Ideal or Continuation rules before their setup-family packages exist.

## Required Regression Cases Before Backtest-Prep

- valid SPY CFB 002 entry using only setup-time-safe source fields
- SPY CFB 003 no-trade because top-ranked quote is after signal
- QQQ CFB no-trade or failure because selected quote age is above five minutes
- missing headline source keeps headline status unknown unless a headline/no-headline policy is accepted
- missing entry rule blocks trade counting
- missing exit rule blocks trade counting
- missing cost/slippage rule blocks trade counting
- future option quote, outcome, P&L, proof, or readiness fields cannot change setup-time eligibility

## Data Rule

Use cheap starter data for rule shape and no-trade/failure diagnosis first. Full-window Databento data remains blocked until an exact cost check and user approval exist.

## Gate Result

- Backtest-prep harness should wait until the first trade-rule package exists.
- Full-window data approval should wait until the trade-rule package states exactly what data fields and windows it needs.
- No candidate is intake-ready.

