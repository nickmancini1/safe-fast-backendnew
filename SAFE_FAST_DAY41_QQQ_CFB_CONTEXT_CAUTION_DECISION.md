# SAFE-FAST Day 41 QQQ CFB Context/Caution Decision

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00`.

Baseline from task file: `5dec718 Record QQQ CFB context caution decision needed`.

This decision defines the first conservative QQQ Clean Fast Break context/caution label framework for regression work. It does not fill evidence, backtest, choose a trade, calculate P&L, accept proof, claim profitability, or mark QQQ ready.

## Decision Result

First framework decision accepted: YES, for regression and later calculator design only.

Complete field evidence fill authorized: NO.

Still blocked decisions: YES. The exact blocked decisions are recorded in `SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION_STILL_BLOCKED.md`.

The accepted part is the reusable status vocabulary, source/timestamp/no-hindsight guardrails, missing-data behavior, and complete-caution aggregation precedence. The blocked part is the human/business choice of option thresholds, execution trade-plan thresholds, and a historical headline/news/event source policy.

## Shared Status Vocabulary

All four fields use the same status vocabulary:

| Status | Meaning |
| --- | --- |
| `clean` | Required source-backed setup-time inputs are present and pass the accepted component rule. |
| `caution` | Required source-backed setup-time inputs are present, no fail condition is triggered, but one or more accepted caution conditions are present. |
| `fail` | Required source-backed setup-time inputs are present and an accepted hard-block/no-trade condition is triggered. |
| `unknown` | Required input, accepted threshold, source confirmation, timestamp proof, or no-hindsight proof is missing or ambiguous. |

Accepted missing-data behavior: `unknown` is a valid component status for regression purposes, but it does not pass complete evidence validation unless a later task explicitly accepts an unknown-as-pass policy. For this QQQ CFB path, unknown components block `complete_caution_review_status=clean`.

## `option_context_status`

Allowed statuses: `clean`, `caution`, `fail`, `unknown`.

Required raw inputs:

- candidate id, symbol, setup type, and setup timestamp;
- reviewed option contract universe or selected contract rule;
- option contract identifier, side, expiration, strike, and multiplier;
- bid, ask, bid size, ask size, quote event timestamp, quote receive timestamp, and quote age versus setup time;
- derived midpoint, spread, and spread percent;
- volume or cleared volume where available;
- open interest where available;
- source references for Databento definitions, TCBBO quote rows, trade rows, statistics rows, and normalizer behavior.

Allowed timestamps:

- Definitions and contract metadata must be available for `2026-04-13`.
- Quote rows must be selected nearest-at-or-before `2026-04-13T12:30:00-04:00` using `ts_event`.
- `ts_recv` may be preserved as receive-time metadata, but cannot override a post-signal `ts_event`.
- Statistics rows may be used only if their accepted `ts_ref` or rule-defined reference time is at or before setup time, or if a later decision explicitly accepts prior-session/opening statistics for setup-time review.
- Source export times such as `source_as_of` prove file provenance only; they do not make post-signal market data valid.

Forbidden future data:

- post-signal option quotes, trades, or statistics not allowed by the timestamp rule;
- future candles, future replay rows, outcome movement, fills, P&L, profitability, readiness, or promotion labels.

Missing-data behavior:

- missing contract universe or selected contract rule: `unknown`;
- missing quote, missing bid/ask, missing quote timestamp, missing side/expiration/strike, or missing no-hindsight clip: `unknown`;
- missing volume or open interest: `unknown` until minimum-liquidity policy is accepted.

Caution behavior:

- caution requires accepted numeric or categorical thresholds for spread, spread percent, quote age, bid/ask size, volume, open interest, minimum option price, or contract availability.
- Those thresholds are still blocked, so regression rows may describe caution fixtures but must not fill live evidence from them yet.

Fail behavior:

- fail requires accepted hard-block thresholds, such as crossed/locked/invalid quote, zero or negative bid/ask, quote too stale, contract missing, spread too wide, liquidity too low, or selected contract unavailable.
- Hard-block thresholds are still blocked.

Unknown behavior:

- any unsupported threshold, ambiguous timestamp, wrong symbol/setup, or missing source-backed raw input produces `unknown`.

Exact regression fixture cases needed next:

1. Clean option context with source-backed contract metadata, bid/ask, quote age, spread, size, volume, and open interest under accepted thresholds.
2. Caution boundary cases for spread, spread percent, quote age, bid/ask size, volume, open interest, and minimum option price.
3. Fail cases for crossed quote, zero/negative bid, stale quote, unavailable selected contract, excessive spread, and insufficient liquidity.
4. Unknown cases for missing contract selection, missing quote, missing statistics, ambiguous timestamp, wrong symbol, wrong setup, and missing threshold metadata.
5. Future option quote, future trade, future statistic, outcome, fill, P&L, profitability, and readiness rejection.

## `headline_context_status`

Allowed statuses: `clean`, `caution`, `fail`, `unknown`.

Required raw inputs:

- source-confirmed headline, news, macro, event, calendar, or explicit no-headline payload;
- source name and source reference;
- source timestamp;
- mapping from source payload to clear/caution/fail categories.

Allowed timestamps:

- the latest usable headline/event source timestamp must be at or before `2026-04-13T12:30:00-04:00`;
- later headline updates, later macro/event interpretations, and post-outcome labels are forbidden.

Forbidden future data:

- post-signal news/headline/event updates;
- future candles, future replay rows, outcomes, fills, P&L, profitability, readiness, or promotion labels.

Missing-data behavior:

- no source-confirmed historical headline/news/event payload produces `unknown`.
- Existing unconfirmed or runtime default text is not enough to label the historical row clean, caution, or fail.

Caution behavior:

- caution requires an accepted source-backed category such as source-confirmed pending event, macro caution, material headline risk, scheduled release, or confirmed adverse but non-blocking news.

Fail behavior:

- fail requires an accepted source-backed hard-block category such as source-confirmed major event, halt-like risk, earnings-style blocker if applicable, or other human-accepted no-trade headline blocker.

Unknown behavior:

- missing source, source-unconfirmed payload, ambiguous event timing, or missing category mapping produces `unknown`.

Exact regression fixture cases needed next:

1. Source-confirmed no-material-headline clear case.
2. Source-confirmed caution headline/event case.
3. Source-confirmed hard-block headline/event case.
4. Missing headline source returns `unknown`.
5. Source-unconfirmed headline text returns `unknown`.
6. Future headline/event rejection.
7. Wrong-symbol and wrong-date headline rejection.

## `execution_context_status`

Allowed statuses: `clean`, `caution`, `fail`, `unknown`.

Required raw inputs:

- accepted entry timing rule;
- selected option contract or accepted review contract rule;
- selected quote at or before the entry/setup timestamp;
- bid, ask, midpoint if used, spread, spread percent, quote age, bid/ask size;
- accepted fill assumption;
- accepted slippage and cost interaction if execution status depends on tradability;
- no-fill behavior.

Allowed timestamps:

- quote selection must be nearest-at-or-before the accepted entry/setup timestamp unless a later entry rule explicitly allows a later timestamp;
- for this setup-time context decision, post-`2026-04-13T12:30:00-04:00` option quotes cannot prove setup-time execution context.

Forbidden future data:

- post-signal quote selection unless later entry timing is explicitly accepted before evidence fill;
- actual broker/order/account/fill data;
- future candles, future replay rows, outcomes, P&L, profitability, readiness, or promotion labels.

Missing-data behavior:

- missing entry rule, selected contract, fill assumption, quote, quote-age rule, spread threshold, or slippage/cost policy produces `unknown`.

Caution behavior:

- caution requires an accepted execution threshold, such as near-limit spread, near-limit quote age, limited size, or other tradability warning.

Fail behavior:

- fail requires an accepted execution hard-block, such as no valid quote, too-stale quote, crossed/invalid quote, spread too wide, no-fill rule triggered, or liquidity below hard minimum.

Unknown behavior:

- missing accepted entry/fill/threshold decisions produce `unknown` even if raw Databento quotes are structurally present.

Exact regression fixture cases needed next:

1. Clean execution context with accepted entry timing, selected quote, fill rule, spread/age/liquidity thresholds, and no-hindsight proof.
2. Caution execution boundary cases for quote age, spread, spread percent, size, and slippage/cost interaction.
3. Fail cases for no quote, stale quote, crossed/invalid quote, no-fill rule, excessive spread, and insufficient liquidity.
4. Unknown cases for missing entry rule, contract selection, fill assumption, quote-age threshold, or spread/liquidity thresholds.
5. Future quote, actual fill, broker/order/account data, outcome, P&L, profitability, and readiness rejection.

## `complete_caution_review_status`

Allowed statuses: `clean`, `caution`, `fail`, `unknown`.

Required raw inputs:

- accepted `gap_context_status`;
- accepted lifecycle status from the QQQ CFB stale/spent/expiry rule;
- `option_context_status`;
- `headline_context_status`;
- `execution_context_status`;
- any additional required 24H room, wall-thesis, macro, IV, event, or blocker fields if a later QQQ CFB rule keeps them in the complete caution gate;
- source references and no-hindsight proof for every component.

Allowed timestamps:

- each component must use its own accepted setup-time timestamp rule;
- the complete review timestamp cannot be later than the latest allowed setup-time component timestamp and cannot use post-signal evidence to improve or downgrade the status.

Forbidden future data:

- future candles, future replay rows, post-signal option data unless explicitly allowed by a pre-accepted entry rule, post-signal headlines/events, actual fills, P&L, outcomes, profitability, readiness, and promotion labels.

Missing-data behavior:

- if any required component is `unknown`, the complete status is `unknown`;
- if any required component is missing, source-unconfirmed, or lacks no-hindsight proof, the complete status is `unknown`.

Caution behavior:

- if all required components are known and at least one component is `caution`, while none is `fail`, the complete status is `caution`.

Fail behavior:

- if any required component is `fail`, the complete status is `fail`.

Unknown behavior:

- `unknown` has precedence over `clean` and `caution` when any required component is undecided or unsupported;
- `fail` has highest precedence when a source-backed hard-block is accepted and present.

Accepted aggregation precedence:

1. `fail`
2. `unknown`
3. `caution`
4. `clean`

Exact regression fixture cases needed next:

1. All required components clean produces complete `clean`.
2. One caution and no fail/unknown produces complete `caution`.
3. One fail produces complete `fail`.
4. One unknown and no fail produces complete `unknown`.
5. Missing option/headline/execution/gap/lifecycle component produces complete `unknown`.
6. Wrong symbol, wrong setup, future candle, future replay row, future option quote, future headline, fill, P&L, outcome, profitability, and readiness rejection.

## Current QQQ Target Implication

The target QQQ row remains blocked for context/caution evidence fill because:

- option numeric thresholds and selected-contract policy are not accepted;
- execution entry, fill, quote-age, spread/liquidity, slippage/cost, and no-fill rules are not accepted;
- no source-confirmed historical headline/news/event payload exists for the row;
- complete caution aggregation cannot produce `clean` while required components remain `unknown`.

## Result

Decision framework accepted: YES.

Still-blocked doc created: `SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION_STILL_BLOCKED.md`.

Evidence filled: NO.

Backtest authorized: NO.

Trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Proof accepted: NO.

Profitability claimed: NO.
