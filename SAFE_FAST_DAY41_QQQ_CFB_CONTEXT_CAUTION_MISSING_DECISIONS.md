# SAFE-FAST Day 41 QQQ CFB Context/Caution Missing Decisions

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00`.

Baseline from task file: `3ce6409 Add QQQ CFB context caution regression fixtures`.

This document resolves the still-missing QQQ Clean Fast Break context/caution decisions conservatively enough for calculator work to proceed. It does not fill evidence, backtest, choose a trade, calculate P&L, claim proof or profitability, mark QQQ ready, or change intake-ready status.

## Decision Result

First conservative missing-decision rule accepted: YES, for context/caution calculator and regression work only.

Evidence fill authorized: NO.

Backtest authorized: NO.

Trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Proof accepted: NO.

Profitability claimed: NO.

The accepted rule is intentionally blocker-preserving:

- no selected option contract or reviewed-contract-universe policy means `option_context_status=unknown`;
- no source-confirmed historical headline/no-headline source means `headline_context_status=unknown`;
- no accepted execution entry/fill rule means `execution_context_status=unknown`;
- `complete_caution_review_status` cannot pass as `clean` or `caution` if any required component is `unknown`.

## Shared Statuses

Allowed statuses for option, headline, execution, and complete caution review remain:

| Status | Meaning |
| --- | --- |
| `clean` | Required source-backed setup-time inputs are present and pass the accepted component rule. |
| `caution` | Required source-backed setup-time inputs are present, no fail condition is triggered, but one or more accepted caution conditions are present. |
| `fail` | Required source-backed setup-time inputs are present and an accepted hard-block/no-trade condition is triggered. |
| `unknown` | Required input, accepted policy, threshold, source confirmation, timestamp proof, or no-hindsight proof is missing or ambiguous. |

## Option Context Decision

### Accepted Rule

`option_context_status` must be `unknown` unless a prior accepted rule provides either:

- one selected option contract for the target setup, or
- a reviewed-contract-universe policy that defines which contracts are eligible and how their component statuses aggregate.

Raw Databento OPRA definitions, TCBBO quotes, trades, and statistics may be used only as source-backed inspection inputs. They do not choose a contract and do not create a label by themselves.

### Required Raw Inputs

For any future clean, caution, or fail option label, the calculator must require candidate identity, accepted contract policy, option contract metadata, bid/ask, sizes, quote timestamps, quote age, midpoint, spread, spread percent, required volume/open-interest inputs, and Databento source references.

### Threshold Decision

No numeric option clean/caution/fail thresholds are accepted in this task.

Reason: the repo has raw quote, spread, volume, and open-interest inputs, but it still has no accepted selected-contract or reviewed-universe policy. Applying quote-age, spread, spread-percent, size, volume, open-interest, or minimum-price thresholds without first defining the contract set would create a fake option label.

Current threshold behavior:

- missing selected-contract/reviewed-universe policy: `unknown`;
- missing quote-age threshold: `unknown`;
- missing spread or spread-percent threshold: `unknown`;
- missing bid/ask size threshold: `unknown`;
- missing volume or cleared-volume threshold: `unknown`;
- missing open-interest threshold: `unknown`;
- missing minimum-price threshold: `unknown`.

### Timestamps

- Quote selection for setup-time option context must use Databento `ts_event` nearest-at-or-before `2026-04-13T12:30:00-04:00`.
- `ts_recv` may be preserved as receive-time metadata but cannot make a post-signal `ts_event` valid.
- Definition rows must describe contracts available for the signal date.
- Statistics rows may not be used for a setup-time label unless their accepted reference timestamp rule proves no future-data use.

### Future-Data Rejection

The option context calculator must reject post-signal option quotes, trades, or statistics unless a later pre-accepted rule explicitly allows them, plus future candles, future replay rows, outcome movement, fills, broker/order/account data, P&L, profitability, readiness, and promotion labels.

### Missing-Data Behavior

Any missing required raw input, selected-contract policy, reviewed-universe policy, timestamp proof, threshold, or source reference returns `unknown`, not `clean`, `caution`, or `fail`.

### Regression Fixture Cases Needed Next

1. Missing selected-contract policy returns option `unknown`.
2. Missing reviewed-universe policy returns option `unknown`.
3. Source-backed raw quote fields are preserved for inspection but still return `unknown` when threshold policy is absent.
4. Future option quote/trade/statistic rejection.
5. Wrong symbol and wrong setup rejection.
6. Missing quote, missing bid/ask, missing timestamp, missing statistics, and missing threshold metadata return `unknown`.
7. Quote-age, spread, spread-percent, size, volume, open-interest, and minimum-price boundaries remain blocked until a selected-contract or universe policy is accepted.

## Headline Context Decision

### Accepted Rule

`headline_context_status` must be `unknown` unless the repo contains a source-confirmed historical headline/news/event/macro payload or an explicit source-confirmed no-material-headline payload for the setup-time review.

Absence of a headline source is not clean. Runtime defaults, assumptions, or silence in unrelated files are not a historical no-headline check.

### Required Raw Inputs

For any future clean, caution, or fail headline label, the calculator must require source name, source reference, source timestamp, target symbol or market-wide scope, payload text or structured event/no-event value, accepted category mapping, and no-hindsight proof.

### Threshold/Category Decision

No headline clean/caution/fail category mapping is accepted in this task.

Reason: the repo still has no source-confirmed historical headline/news/event feed or explicit no-headline source for the target row. Category thresholds without a source would create a fake headline check.

### Timestamps

- The latest usable headline/event source timestamp must be at or before `2026-04-13T12:30:00-04:00`.
- Post-signal headline updates, later macro interpretations, and outcome-based labels are forbidden.

### Future-Data Rejection

The headline context calculator must reject post-signal headlines, event updates, or later interpretations, plus future candles, future replay rows, outcomes, fills, P&L, profitability, readiness, and promotion labels.

### Missing-Data Behavior

No source-confirmed historical headline/news/event/no-headline payload returns `unknown`.

### Regression Fixture Cases Needed Next

1. Missing headline source returns headline `unknown`.
2. Source-unconfirmed text returns headline `unknown`.
3. Future headline/event rejection.
4. Wrong symbol, wrong date, and unrelated market scope rejection.
5. Explicit no-material-headline clean, caution headline, and hard-block headline fixtures remain blocked until a source and category mapping are accepted.

## Execution Context Decision

### Accepted Rule

`execution_context_status` must be `unknown` unless a prior accepted rule defines the entry timing, selected quote rule, fill assumption, quote-age threshold, spread/liquidity thresholds, slippage/cost interaction, and no-fill behavior.

Databento quotes and trades may support inspection, but quotes are not fills and do not prove execution by themselves.

### Required Raw Inputs

For any future clean, caution, or fail execution label, the calculator must require accepted entry timing, selected contract or universe policy, selected quote, bid/ask/midpoint if used, spread, spread percent, quote age, bid/ask size, accepted fill assumption, accepted slippage/cost rule, and accepted no-fill behavior.

### Threshold Decision

No numeric execution clean/caution/fail thresholds are accepted in this task.

Reason: the repo has no accepted entry or fill rule. Spread, liquidity, quote age, no-fill, slippage, and cost thresholds cannot honestly classify execution context until the trade-plan execution path exists.

Current threshold behavior:

- missing entry timing rule: `unknown`;
- missing selected quote rule: `unknown`;
- missing fill assumption: `unknown`;
- missing quote-age threshold: `unknown`;
- missing spread/liquidity threshold: `unknown`;
- missing slippage/cost/no-fill rule: `unknown`.

### Timestamps

- Setup-time execution context must use a selected quote nearest-at-or-before `2026-04-13T12:30:00-04:00` unless a later entry timestamp is accepted before evidence fill.
- Post-signal option quotes cannot prove setup-time execution context under the current rule.

### Future-Data Rejection

The execution context calculator must reject post-signal quotes unless a later entry rule is accepted first, actual broker/order/account/fill data, future candles, future replay rows, outcomes, P&L, profitability, readiness, and promotion labels.

### Missing-Data Behavior

Any missing entry, contract-selection, quote-selection, fill, quote-age, spread/liquidity, slippage/cost, no-fill, timestamp, or source rule returns `unknown`.

### Regression Fixture Cases Needed Next

1. Missing entry rule returns execution `unknown`.
2. Missing fill assumption returns execution `unknown`.
3. Raw quote inspection fields are preserved but still return `unknown` when execution thresholds are absent.
4. Future quote rejection.
5. Broker/order/account/fill, outcome, P&L, profitability, and readiness rejection.
6. Clean, caution, fail, no-fill, quote-age, spread/liquidity, slippage, and cost boundary fixtures remain blocked until an entry/fill trade-plan rule is accepted.

## Complete Caution Review Decision

### Accepted Rule

`complete_caution_review_status` cannot pass if any required component is `unknown`.

Current required components for QQQ CFB complete caution review are accepted `gap_context_status`, accepted QQQ CFB lifecycle status, `option_context_status`, `headline_context_status`, and `execution_context_status`.

Additional 24H room, wall-thesis, macro, IV, event, or blocker fields are not accepted as pass-through substitutes in this task. If a later rule keeps any of those fields as required components, missing or unknown values must block complete review until explicitly changed.

### Aggregation Precedence

Accepted precedence:

1. `fail`
2. `unknown`
3. `caution`
4. `clean`

If any required component is `fail`, complete status is `fail`. If no required component is `fail` and any required component is `unknown`, complete status is `unknown`. If all required components are known and at least one is `caution`, complete status is `caution`. Only all required components known and `clean` can produce complete `clean`.

### Timestamps

Each component must use its own accepted setup-time timestamp rule. The complete review must not use post-signal evidence to improve or downgrade the status.

### Future-Data Rejection

The complete review calculator must reject future candles, future replay rows, post-signal option/headline data unless explicitly allowed by a pre-accepted component rule, actual fills, P&L, outcomes, profitability, readiness, and promotion labels.

### Missing-Data Behavior

Any missing component, source-unconfirmed component, missing no-hindsight proof, or `unknown` required component returns complete `unknown` unless a source-backed fail is accepted and present.

### Regression Fixture Cases Needed Next

1. Current target-style case with option/headline/execution `unknown` produces complete `unknown`.
2. All components clean produces complete `clean`.
3. One caution and no fail/unknown produces complete `caution`.
4. One fail produces complete `fail`.
5. One unknown and no fail produces complete `unknown`.
6. Missing required component produces complete `unknown`.
7. Wrong symbol, wrong setup, future option/headline/candle/replay row, fill, P&L, outcome, profitability, and readiness rejection.

## Current QQQ Target Implication

For `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`, calculator work may now honestly produce:

- `option_context_status=unknown` because no selected-contract or reviewed-universe policy and no numeric option thresholds are accepted;
- `headline_context_status=unknown` because no source-confirmed historical headline/news/event/no-headline source exists;
- `execution_context_status=unknown` because no entry/fill/quote-age/spread/liquidity/slippage/no-fill rule is accepted;
- `complete_caution_review_status=unknown` because required components are unknown and unknown cannot pass.

This is a blocker-preserving calculation result, not an evidence pass.

## Remaining Blocked Decisions

Still blocked before clean/caution/fail labels can be filled:

- exact selected-contract or reviewed-contract-universe policy;
- numeric option quote-age, spread, spread-percent, size, volume, open-interest, and minimum-price thresholds;
- exact entry timing, quote selection, fill assumption, no-fill behavior, slippage, cost, spread, and liquidity execution rules;
- historical headline/news/event/no-headline source and category mapping;
- exit, stop/invalidation translation, time exit, sample-size, promotion, and profitability gates.

## Result

Missing-decision defaults accepted: YES.

Context/caution calculator work can proceed: YES, only to calculate source-backed blocker-preserving statuses under these rules.

Evidence filled: NO.

Backtest authorized: NO.

Trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Proof accepted: NO.

Profitability claimed: NO.
