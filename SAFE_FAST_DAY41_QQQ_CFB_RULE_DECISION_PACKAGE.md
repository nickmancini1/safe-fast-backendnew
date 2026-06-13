# SAFE-FAST Day 41 QQQ CFB Rule Decision Package

## Scope

Candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00`.

Baseline: `9f3364a Add Databento OPRA normalizer`.

This package lists rule decisions still needed before QQQ evidence fill or backtest. It does not choose unsupported rules, fill evidence, choose a trade, calculate P&L, mark QQQ ready, accept proof, or claim profitability.

## Current Supported Inputs

Repo-supported candidate context:

- Work-package rows identify the candidate, symbol, setup type, setup candle, trigger `613.67`, invalidation `609.58`, source CSV line 132, replay log lines 3-4, and the no-hindsight setup-time boundary. Source: `historical_signal_replay/source_data/richer_export_package_work/qqq_cfb_gap_context_completeness_fields_rule.jsonl`, `qqq_cfb_stale_spent_expiry_rule_regressions.jsonl`, and `qqq_cfb_complete_context_caution_fields.jsonl`.
- QQQ gap measurement is source-backed as previous regular-session close `611.02` at `2026-04-10T15:30:00-04:00`, signal-day open `609.455` at `2026-04-13T09:30:00-04:00`, gap `-1.5650`, about `-0.2561%`, direction `down`. Source: `SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_RULE_DEFINITION.md` and `SAFE_FAST_DAY41_QQQ_GAP_THRESHOLD_DECISION_PACKAGE.md`.
- Databento QQQ OPRA files support raw option definitions, bid/ask quotes, sizes, timestamps, trades, cleared volume, and open interest for inspection. Source: `SAFE_FAST_DAY41_DATABENTO_QQQ_EVIDENCE_FIELD_MAPPING.md` and `SAFE_FAST_DAY41_DATABENTO_QQQ_OPRA_NORMALIZER_REVIEW.md`.
- The Databento normalizer is read-only and supports parsing, joins, timestamp normalization, no-hindsight quote selection, spread inspection fields, statistics mapping, and refusal to infer fills, trade choice, P&L, proof, profitability, or readiness. Source: `SAFE_FAST_DAY41_DATABENTO_QQQ_OPRA_NORMALIZER_REVIEW.md`.

These inputs do not prove SAFE-FAST labels, trade execution, backtest validity, proof, profitability, or readiness.

## Rule Decision Inventory

| Rule area | Classification | Repo support | Exact decision still needed before evidence fill/backtest |
| --- | --- | --- | --- |
| Gap thresholds | missing decision; blocked by tests | Raw QQQ gap can be measured, but `SAFE_FAST_DAY41_QQQ_GAP_THRESHOLD_DECISION_PACKAGE.md` says numeric clean/caution/fail thresholds are unsupported. | Decide numeric QQQ Clean Fast Break clean/caution/fail threshold logic, including whether it uses signed percent gap, absolute percent gap, point gap, direction-specific thresholds, favorable/adverse treatment, and boundary behavior. Add threshold regression fixtures before calculator or fill. |
| Gap-context as-of/reviewed-before-signal rule | pending validation; blocked by tests | `SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_RULE_DEFINITION.md` defines the no-hindsight rule shape and expected as-of concept. | Implement only after threshold decision and regression cases prove future candles/replay rows cannot affect `gap_context_status`, `gap_context_as_of`, or `gap_context_reviewed_before_signal`. |
| Stale/spent rule | missing decision; blocked by tests | Work row cites replay log lines 3-6 and notes later rows as lifecycle context, but the required rule artifact is still unavailable. | Decide the QQQ Clean Fast Break lifecycle rule for when an initial break remains fresh, becomes spent, becomes stale, or remains eligible after follow-through/base behavior. Add regression rows for fresh, spent, stale, invalidated, blocked, and missing-data cases. |
| CFB expiry rule | missing decision; blocked by tests | `qqq_cfb_stale_spent_expiry_rule_regressions.jsonl` requests `clean_fast_break_stale_spent_expiry_rule` and `clean_fast_break_expiry_regression_rows`; both remain unresolved. | Decide exact expiry timing for QQQ Clean Fast Break signals, including same-session expiry, next-candle expiry, higher-base continuation behavior, and whether later same-session follow-through can expire or preserve the setup. |
| Stage transitions | missing decision; blocked by tests | `SAFE_FAST_PROJECT_PROOF_PIPELINE.md` requires transitions among watch, candidate, signal, spent, stale, invalidated, blocked, no-trade, and review. | Define project-wide and QQQ CFB-specific transition table, transition triggers, precedence, and regression fixtures. |
| Contract selection | missing decision; pending validation | Databento supports available contracts, expirations, strikes, side, and metadata, but the mapping doc says SAFE-FAST has not selected side, expiration, strike, DTE, spread width, or ranking. | Decide long/short direction or abstain rule, call/put selection, expiration/DTE range, strike or delta/moneyness rule, single-leg versus spread, spread width if any, and fallback when the target contract is missing or illiquid. |
| Entry rule | missing decision; pending validation | Databento quote timestamps support nearest-at-or-before-signal lookup; no accepted entry timing rule exists. | Decide exact entry timestamp, trigger condition, quote source, allowed quote age, whether entry is at signal close, next quote, next bar, breakout touch, or confirmation, and whether no quote means no trade. |
| Fill assumption | missing decision | `SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md` says an option quote is not a fill; normalizer refuses fill inference. | Decide whether fills use bid, ask, midpoint, midpoint plus slippage, limit rule, or no-fill if spread/quote conditions fail. Include partial/missing quote behavior. |
| Spread/liquidity limits | missing decision; pending validation | Databento supports bid, ask, bid/ask size, spread, spread percent, trades, volume, and open interest inspection fields. | Decide maximum spread, maximum spread percent, minimum bid/ask size, minimum volume/open interest, quote-age limit, minimum option price, and no-trade behavior when limits fail. |
| Exit rule | missing decision; blocked by data | Current Databento request window is signal-centered; mapping doc says no accepted exit rule exists. | Decide profit exit, target, trailing behavior if any, invalidation exit, time exit interaction, quote source, and required option quote window for exit replay. |
| Stop/invalidation rule | accepted/current for underlying trigger/invalidation; missing decision for option translation | Work rows record trigger `613.67` and invalidation `609.58`. | Decide how underlying invalidation maps to option exit/stop, whether stop triggers on candle close, touch, bid/ask quote, or timed review, and what happens if option quotes are missing at invalidation. |
| Time exit | missing decision; blocked by data | Trade-plan gate requires time exit or EOD rule if applicable; current OPRA window does not prove EOD handling. | Decide maximum hold time, same-session close behavior, EOD liquidation rule, stale/no-progress timeout, and required data window for replay. |
| Cost/slippage assumptions | missing decision; pending validation | Databento spread inspection can inform assumptions, but no assumption is accepted. | Decide commission/fees, slippage model, spread crossing model, minimum edge after costs, and how missing/abnormal quotes are treated. |
| Failure diagnosis labels | accepted/current at project level; missing decision for QQQ CFB label set | `SAFE_FAST_BUILD_STATE.md` and `SAFE_FAST_PROJECT_PROOF_PIPELINE.md` require diagnosis of weak, failed, unclear, missing, or unprofitable results. | Decide exact QQQ CFB backtest failure labels, including trigger failure, invalidation failure, stale/spent failure, blocker failure, late signal, insufficient remaining room, liquidity failure, fill failure, exit failure, cost/slippage failure, missing evidence, and no-trade. |
| Sample-size requirement | missing decision | `SAFE_FAST_PROJECT_RULE_INDEX.md` and `SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md` list sample-size requirements as not accepted. | Decide minimum QQQ CFB sample counts before promotion, including winners, failures, blocked/no-trade examples, missing-evidence examples, late-signal examples, wrong-winner examples, and boundary cases. |
| Promotion gate | accepted/current at high level; missing decision for exact gate | Proof pipeline says promotion requires accepted evidence, passing regressions, complete trade-plan rules, and no-hindsight review; exact criteria remain missing. | Decide exact criteria for moving QQQ CFB from evidence review to reconsideration-eligible, intake-ready, shadow planning, or rejection/narrowing. Include required tests, sample counts, and review signoff. |
| Option-context status | missing decision; pending validation | Databento supports raw option/liquidity inputs, but `SAFE_FAST_DAY41_DATABENTO_QQQ_EVIDENCE_FIELD_MAPPING.md` says label rules are missing. | Decide how raw chain, quote, spread, size, volume, open interest, and contract metadata classify `option_context_status`. |
| Execution-context status | missing decision; pending validation | Databento supports quote/trade inputs but not fills. | Decide how entry timing, quote age, bid/ask, spread, fill assumption, and liquidity classify `execution_context_status`. |
| Headline-context status | blocked by data; missing decision | Validated Databento OPRA files contain no headline, macro, news, or event feed. | Decide required source for headline/macro/event review, allowed statuses, no-data behavior, and whether missing headline context blocks the candidate. |
| Complete caution review status | missing decision; pending validation; partly blocked by data | Work package requests complete caution status; mapping says Databento only supports option/liquidity/execution slice. | Decide aggregation rule across gap, stale/spent, headline, option, execution, blocker, macro/IV/event, and complete caution fields, including precedence and no-trade overrides. |

## Smallest Ordered Implementation Plan

1. Accept QQQ CFB gap-threshold decision criteria and fixture set without using outcome hindsight.
2. Add regression cases for gap measurement, no-threshold unknown status, future-bar rejection, replay future rejection, missing inputs, wrong symbol, non-RTH contamination, source timestamp distinction, and threshold boundaries.
3. Implement the gap-context calculator only after those regression cases exist, then fill only the gap-context evidence fields if tests pass.
4. Decide QQQ CFB stale/spent and expiry lifecycle rules, then add lifecycle transition regression rows before any lifecycle fill.
5. Decide stage-transition precedence for watch, candidate, signal, spent, stale, invalidated, blocked, no-trade, and review states.
6. Decide the complete trade plan: contract selection, entry, fill, spread/liquidity thresholds, exit, stop/invalidation translation, time exit, costs, slippage, and failure labels.
7. Extend the read-only Databento path only as needed to produce inspection artifacts for the chosen contract and required entry/exit windows; do not infer fills or P&L from quotes.
8. Decide option, headline, execution, and complete caution label rules, including no-data behavior and aggregation precedence.
9. Add tests for each accepted label/trade-plan rule before using it in evidence fill or backtest.
10. Fill evidence only from source-backed calculated labels and accepted rule artifacts, then rerun the content validator and bridge.
11. Build a backtest path only after the trade-plan completeness gate is satisfied and the data window covers entry, exit, time exit, stop, costs, slippage, and failure cases.
12. Apply sample-size and promotion gates before any reconsideration-eligible, intake-ready, proof, profitability, or live/shadow status.

## Current Result

Evidence filled: NO.

Trade chosen: NO.

P&L calculated: NO.

Backtest authorized: NO.

QQQ candidate marked ready: NO.

Proof accepted: NO.

Profitability claimed: NO.
