# SAFE-FAST Day 47 Grouped CFB Expansion / Data-Needed Plan

## Baseline

- Branch/checkpoint baseline: `main`, `021bead Add Day 46 grouped backtest batch decision`.
- Today: June 18, 2026, Project Day 47.
- Latest grouped decision: `SAFE_FAST_DAY46_NEXT_GROUPED_BACKTEST_BATCH_DECISION.md`.
- Current work type: planning, comparison, and data-needed package only.
- Databento downloaded: NO.
- Raw Databento files changed: NO.
- New backtest run: NO.
- New P&L calculated: NO.
- Proof/profitability/readiness/intake-ready change: NO.

## Fixed

- Clean Fast Break now has one completed positive review-only reference:
  - `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`
  - result `completed_review_only` / `completed_profit_target`
  - entry basis `6.37`
  - adjusted exit basis `7.98`
  - adjusted result `+1.61`
- Clean Fast Break no-entry discipline is preserved:
  - `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` stays `no_trade` / `quote_after_signal`.
  - `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` stays `no_trade` / `quote_age_above_5_minutes`.
- First-pass CFB rule values exist for review/prep:
  - long calls only;
  - setup, option context, and execution context required before entry;
  - entry ask plus `0.02`;
  - exit bid minus `0.02`;
  - earliest accepted exit among `+25%` target, `-15%` option stop, setup invalidation stop, or `15:45 ET` time exit;
  - named failure/no-trade reason required;
  - minimum `20` valid completed CFB examples before promotion.

## Still Unproven

- One positive CFB result does not prove a profitable trading plan.
- One positive CFB result does not prove CFB works across symbols, dates, or setup variants.
- The current CFB result does not calibrate entry, exit, stop, time-exit, cost, or slippage values for promotion.
- The current CFB result does not weaken no-trade controls.
- Ideal and Continuation families are not backtest-ready under current repo rules.
- No candidate is intake-ready, proof-accepted, promotion-ready, or a chosen real trade.

## Active Build Objective

Build the next grouped expansion and data-needed path without running another backtest. The next useful package is a grouped cost-check plan that identifies exact Databento symbols, schemas, and windows needed for the next batch before any download.

## Grouped Comparison Table

| Candidate | Setup family | Current grouped role | Current result/state | Data/rule state | Day 47 routing |
| --- | --- | --- | --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | Clean Fast Break | Positive tradable reference | `completed_review_only`; `completed_profit_target`; entry `6.37`; adjusted exit `7.98`; adjusted result `+1.61` | Selected contract and exit path exist locally for the completed review; headline/complete caution remain blocker-preserving; promotion sample blocker remains | Keep as the positive CFB anchor; do not treat as proof |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | Clean Fast Break | Quote-after-signal no-entry reference | `no_trade`; `quote_after_signal` | Starter top-ranked contract quote/trade row is after setup; no fallback allowed | Keep as no-entry control; only consider more quote coverage after grouped cost check |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | Clean Fast Break | Stale-quote no-entry reference | `no_trade`; `quote_age_above_5_minutes` | Option context `caution`; execution context `fail`; complete caution `fail`; selected quote about `23m 29s` old | Keep as stale-execution control; no fallback scan |
| `SPY-REAL-HISTORICAL-IDEAL-001` | Ideal | Deferred setup-family comparison | Both mapped work-package requests pass, but blocker-preserving unknown statuses remain | Ideal gap/context thresholds, option/execution, entry, exit, cost, slippage, sample-size, and promotion rules incomplete | Do not force into CFB path; prepare only after Ideal-specific package |
| `QQQ-REAL-HISTORICAL-IDEAL-001` | Ideal | Parked comparison candidate | Replay artifact and starter option data exist | No current richer work-package request; no accepted QQQ Ideal lifecycle, contract-selection, context, entry, exit, cost, slippage, sample-size, or promotion rules | Park until grouped Ideal rule/evidence package |
| `SPY-REAL-HISTORICAL-CONTINUATION-001` | Continuation | Parked comparison candidate | Replay artifact and starter option data exist | No accepted Continuation lifecycle, request-shaped evidence, contract-selection, context, entry, exit, cost, slippage, sample-size, or promotion rules | Park until grouped Continuation package |
| `QQQ-REAL-HISTORICAL-CONTINUATION-001` | Continuation | Parked comparison candidate | Replay artifact and starter option data exist | No accepted Continuation lifecycle, request-shaped evidence, contract-selection, context, entry, exit, cost, slippage, sample-size, or promotion rules | Park until grouped Continuation package |

## What The First Positive CFB Result Supports

- The local CFB runner can apply the accepted first-pass CFB values to one source-backed SPY CFB row.
- The selected-contract entry and exit path can produce a named completed review result.
- Ask-plus-entry and bid-minus-exit handling can be applied mechanically.
- Profit-target exit handling can trigger before the `15:45 ET` time exit.
- Existing no-entry controls remain enforced in the same grouped review.

## What It Does Not Prove

- It does not prove the CFB family has positive expectancy.
- It does not prove the rule values are promotion-grade.
- It does not prove SPY behavior transfers to QQQ.
- It does not prove CFB is stronger than Ideal or Continuation.
- It does not satisfy the minimum `20` valid completed CFB examples blocker.
- It does not authorize Databento download, live trading, broker/order work, readiness, proof, or profitability claims.

## Weak-Result / No-Entry Diagnosis

- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`: the top-ranked starter contract quote is after the setup boundary, so the correct current result is `quote_after_signal`. This protects the no-hindsight boundary.
- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`: the selected quote is older than five minutes at setup, so the correct current result is `quote_age_above_5_minutes`. This protects execution freshness.
- These no-entry rows are not failures to ignore. They are controls that prevent the first positive row from being reviewed alone.
- Weak, missing, or no-entry results should drive grouped diagnosis and data-needed planning, not a single-row grind.

## Next Grouped Candidate Batch Recommendation

The next grouped batch should be a data-needed and cost-check batch, not a backtest batch.

Recommended grouped batch:

1. Keep the three CFB anchors together:
   - `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`
   - `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`
   - `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`
2. Identify any additional CFB or CFB-like historical rows already present in local replay/source docs that can be evaluated under the existing CFB rule family without inventing new setup-family rules.
3. Keep `SPY-REAL-HISTORICAL-IDEAL-001` as a comparison reference only, not as a CFB backtest row.
4. Keep `QQQ-REAL-HISTORICAL-IDEAL-001` and both Continuation candidates parked until setup-family packages exist.
5. Produce a grouped Databento cost-check request for only the exact symbols, schemas, contracts, and windows needed by the next CFB/data-needed batch.

## Data Needed Before Backtest

Before any additional completed result can count, the next task must identify exact local availability and exact Databento cost-check needs for:

- Candidate identity and no-hindsight setup source rows:
  - source CSV row;
  - replay signal row;
  - setup timestamp;
  - trigger;
  - invalidation;
  - lifecycle state at setup.
- Option contract selection inputs:
  - signal-date OPRA definitions;
  - prior-trading-day definitions when listing or open-interest logic needs them;
  - accepted expiration, strike, side, DTE, and no-fallback rules.
- Setup-time execution inputs:
  - TCBBO quotes at or before setup;
  - quote age;
  - bid, ask, spread, bid size, ask size;
  - trades and setup-time-safe same-contract volume;
  - statistics/open interest or an explicit accepted exception.
- Exit-path inputs for rows that pass entry:
  - selected-contract TCBBO bid path from entry through `15:45 ET`;
  - selected-contract trades if needed by the exit rule;
  - source-backed underlying invalidation path from entry through `15:45 ET`;
  - time-exit coverage.
- Context/caution inputs:
  - historical headline/no-headline source policy;
  - option context;
  - execution context;
  - complete caution aggregation.

Known current CFB anchors:

- SPY CFB 002 already has a local selected-contract exit-path review result. It still cannot promote because one completed example is not enough and context/promotion gates remain incomplete.
- SPY CFB 003 needs exact quote-coverage/cost-check diagnosis only if a later task tests whether broader setup-time option coverage changes the current `quote_after_signal` no-entry result under accepted no-fallback rules.
- QQQ CFB 001 already has local QQQ OPRA data and targeted top-contract files sufficient to preserve the current stale-quote diagnosis. It should not be fallback-scanned.

## Cost-Control Rule

- No Databento download in this package.
- No Databento request in this package.
- The next task may cost-check only.
- Full-window Databento data requires exact checked price and user approval before download unless the checked cost is clearly tiny and the next task explicitly allows that exception.
- Keep grouped cost checks narrow:
  - use parent symbol checks only where contract identity is not yet fixed;
  - use selected-contract/instrument windows where identity is fixed;
  - separate setup-window needs from full exit-path needs;
  - prefer cheap starter or already-local data before full-window requests.
- Raw Databento files stay local-only and ignored.

## Promotion Blockers

- Fewer than `20` valid completed CFB examples.
- No accepted positive-expectancy review after costs across a sufficient sample.
- No proof that no-entry controls are preserved across the expansion.
- No proof that headline/complete caution requirements are promotion-grade.
- Ideal-specific and Continuation-specific trade-plan rules remain incomplete.
- No intake-ready transition is authorized by this plan.

## Day 60 Decision-Package Relevance

This plan supports the Day 60 checkpoint by separating:

- what currently works: one SPY CFB positive reference and named no-entry controls;
- what failed or stayed out: quote-after-signal and stale-quote controls;
- what needs repair: more CFB examples, exact data windows, context/caution, and cost-controlled data;
- what is less ready: Ideal and Continuation setup families;
- what remains expensive: full-window OPRA data after cost check;
- what can continue on a lower tier: grouped planning, local replay review, rule packages, and validator checks;
- what would require serious spend: broad full-window option data across more candidates.

## Exact Next Action

Run the follow-up task `SAFE_FAST_DAY47_NEXT_GROUPED_DATA_NEEDED_COST_CHECK_CODEX_TASK.md`.

That task should identify exact Databento symbols, schemas, and windows for the next grouped batch and cost-check them before any download. It must not download data unless the task includes explicit approval language and the user approves the checked cost when required.

## Guardrails Preserved

- Databento downloaded: NO.
- Raw Databento files changed: NO.
- New backtest run: NO.
- New P&L calculated: NO.
- Proof accepted: NO.
- Profitability claimed: NO.
- Candidate marked ready: NO.
- Intake-ready count changed: NO.
- `main.py`, live/engine trading logic, broker/order/account files, Railway/deploy files, `.env`, secrets, raw vendor data, backtest code, generated reports/logs, and P&L files changed: NO.
