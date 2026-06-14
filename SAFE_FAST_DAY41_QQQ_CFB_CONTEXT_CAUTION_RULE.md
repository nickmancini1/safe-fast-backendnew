# SAFE-FAST Day 41 QQQ CFB Context/Caution Rule Review

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00`.

Baseline from task file: `f984e35 Fill QQQ CFB lifecycle evidence`.

This review identifies whether the repo already supports a complete QQQ Clean Fast Break context/caution rule for the remaining evidence checks. It does not fill evidence, backtest, choose a trade, calculate P&L, accept proof, claim profitability, or mark QQQ ready.

## Remaining Failed QQQ CFB Request

Current content validation after the QQQ gap-context and lifecycle fills:

- Passed requests: `2`.
- Failed requests: `7`.
- QQQ failed request remaining: `QQQ CFB complete context/caution fields`.
- Work file: `historical_signal_replay/source_data/richer_export_package_work/qqq_cfb_complete_context_caution_fields.jsonl`.
- Row status: `partial_missing_required_evidence`.
- Blocker fields:
  - `option_context_status`.
  - `headline_context_status`.
  - `execution_context_status`.
  - `complete_caution_review_status`.

## Existing Evidence Found

Supported setup identity and no-hindsight context:

- Candidate id: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.
- Symbol: `QQQ`.
- Setup type: `Clean Fast Break`.
- Setup candle: `2026-04-13T12:30:00-04:00`.
- Trigger: `613.67`.
- Invalidation: `609.58`.
- Source row: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` line 132.
- Replay row: `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl` line 3.
- No-hindsight boundary: setup-time row and replay log line 3 only.

Supported prerequisite labels:

- QQQ CFB gap-context evidence is filled and content-validator passed.
- QQQ CFB stale/spent/expiry lifecycle evidence is filled and content-validator passed.

Supported raw option/liquidity inputs:

- `SAFE_FAST_DAY41_DATABENTO_QQQ_EVIDENCE_FIELD_MAPPING.md` records that local Databento OPRA files support raw option definitions, bid/ask quotes, quote timestamps, sizes, trades, volume, open interest, and derived inspection fields.
- `SAFE_FAST_DAY41_DATABENTO_QQQ_OPRA_NORMALIZER_REVIEW.md` records that the Databento normalizer can parse and inspect these raw fields without inferring fills, trade choice, P&L, proof, profitability, or readiness.

## Rule Search Result

The repo does not yet support an honest complete QQQ CFB context/caution rule.

Reasons:

- `option_context_status` is raw-data supported but not label-supported. Databento supplies option, quote, spread, volume, and open-interest inputs, but no accepted SAFE-FAST thresholds or status rule maps those inputs to a label.
- `execution_context_status` is raw-data supported but not label-supported. Databento supplies quote and trade inputs, but no accepted entry timing, quote-age, spread, fill, slippage, or failure rule exists.
- `headline_context_status` is not source-supported for this historical row. The validated OPRA files contain no headline, macro, event, or news feed, and the QQQ source/replay row does not contain a source-confirmed headline status.
- `complete_caution_review_status` cannot be honestly derived until the option, execution, headline, aggregation, and no-data precedence rules are accepted.
- Existing runtime/watcher headline defaults such as unconfirmed headline state are not a QQQ historical evidence-fill rule for `headline_context_status`.
- Existing live/current `main.py` caution heuristics are not allowed evidence for this task and were not used as accepted historical context/caution rules.

## Rule Status

Accepted complete context status: not accepted.

Accepted caution context status: not accepted.

Required raw inputs: not finalized. Candidate raw input categories that still need a decision are option chain/contract metadata, quote timestamp/age, bid/ask/spread/size, volume/open interest, headline/news/event source payload, accepted entry/fill assumptions, and prerequisite gap/lifecycle labels.

Allowed timestamps: not finalized. A future rule must use only setup-time or earlier source evidence at or before `2026-04-13T12:30:00-04:00`, with explicit quote-age and source-as-of rules.

Forbidden future data: future candles, future replay rows, post-signal option quotes/trades, later headline/news/event updates, fills, P&L, outcomes, profitability, readiness, and promotion labels.

Missing-data behavior: not accepted for final labels. Until a rule is accepted, missing or unproven option, headline, execution, or aggregation inputs remain blockers and must not be converted into clean/caution/fail/pass labels.

## Exact Regression Cases Needed Next

Before any context/caution evidence fill, create regression cases covering:

1. Happy-path option context from source-backed contract metadata, quote, spread, size, volume, and open interest.
2. Option context missing contract metadata returns `unknown` or an accepted blocker status.
3. Option context missing quote, stale quote, crossed quote, zero/negative bid, or missing spread inputs.
4. Option context boundary cases for accepted spread, spread-percent, bid/ask size, volume, open-interest, and minimum price thresholds.
5. Execution context happy path after accepted entry timing, quote selection, fill, slippage, and quote-age rules.
6. Execution context rejected for post-signal quote use.
7. Execution context rejected for missing fill assumption or missing accepted entry rule.
8. Headline context source-confirmed clear/caution/block cases.
9. Headline context missing or source-unconfirmed behavior.
10. Complete caution aggregation when all components are clean.
11. Complete caution aggregation precedence when one component is caution.
12. Complete caution aggregation precedence when one component is fail/block/no-trade.
13. Missing component behavior for option, headline, execution, gap, and lifecycle inputs.
14. Wrong-symbol and wrong-setup contamination rejection.
15. Future candle, future replay row, future option quote, future headline, outcome, fill, P&L, profitability, and readiness rejection.

## Result

Context/caution rule accepted: NO.

Decision-needed doc created: `SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION_NEEDED.md`.

Evidence filled: NO.

Backtest authorized: NO.

Trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Proof accepted: NO.

Profitability claimed: NO.
