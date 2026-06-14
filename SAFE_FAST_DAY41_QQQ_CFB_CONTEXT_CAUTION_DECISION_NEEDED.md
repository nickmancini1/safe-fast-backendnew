# SAFE-FAST Day 41 QQQ CFB Context/Caution Decision Needed

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00`.

This document names the exact missing decision after the context/caution rule review found no accepted honest rule.

## Exact Missing Decision

SAFE-FAST needs an accepted QQQ Clean Fast Break context/caution rule that defines all of the following before evidence fill:

- `option_context_status`: status vocabulary, raw option inputs, thresholds, no-data behavior, and setup-time timestamp rules.
- `headline_context_status`: required source type, status vocabulary, source-confirmation rule, no-data behavior, and setup-time timestamp rules.
- `execution_context_status`: entry timing, quote selection, quote-age limit, spread/liquidity limits, fill assumption, slippage/cost interaction, no-fill behavior, and setup-time timestamp rules.
- `complete_caution_review_status`: aggregation rule across gap context, lifecycle state, option context, headline context, execution context, and any 24H/macro/IV/event/room/blocker inputs that remain required for a complete QQQ CFB caution review.

## Required Status Vocabulary Decision

The rule must decide whether each component uses:

- `clean`, `caution`, `fail`, `unknown`; or
- a different explicit status vocabulary.

The rule must also decide whether `unknown` blocks evidence validation or can pass as an accepted no-data status. Until that decision is made, unresolved fields remain blockers.

## Required Raw Input Decision

The rule must decide the exact source-backed inputs for:

- Option context: contract identifier, side, expiration, strike, bid, ask, bid size, ask size, spread, spread percent, quote timestamp, quote age, volume, open interest, and contract metadata.
- Headline context: source-confirmed headline/news/event/macro payload, source status, source timestamp, and evidence references.
- Execution context: accepted entry timestamp, quote chosen for entry review, allowed quote age, bid/ask/mid/fill rule, spread/liquidity thresholds, and no-fill behavior.
- Complete caution review: prerequisite gap and lifecycle labels, plus any 24H, macro, IV, event, room, wall-thesis, blocker, option, headline, and execution fields that are required.

## Required Timestamp Decision

The rule must define:

- The latest allowed setup-time source timestamp for each component.
- How quote `ts_event`, quote `ts_recv`, statistics `ts_ref`, source export `source_as_of`, headline source time, and setup candle time interact.
- Whether nearest-at-or-before quote selection is required.
- Whether stale quote or stale headline evidence produces `unknown`, `caution`, `fail`, or no-trade.

## Required Forbidden-Data Decision

The rule must explicitly reject:

- future candles;
- future replay rows;
- post-signal option quotes or trades;
- post-signal statistics updates if not allowed by the timestamp rule;
- later headline/news/event changes;
- fills, broker/order/account fields, P&L, outcomes, profitability, readiness, and promotion labels.

## Required Missing-Data Decision

The rule must define whether each missing component produces:

- `unknown`;
- `caution`;
- `fail`;
- `blocked`;
- `no_trade`; or
- another accepted status.

It must also define aggregation precedence when some components are known and others are missing.

## Minimum Regression Package Needed Next

Before any calculator or evidence fill, create source-shaped regression rows for:

- option context clean/caution/fail/unknown cases;
- headline context source-confirmed clear/caution/block and missing/source-unconfirmed cases;
- execution context clean/caution/fail/unknown cases;
- complete caution aggregation all-clean, one-caution, one-fail/block, and missing-component cases;
- threshold boundary cases for spread, spread percent, quote age, bid/ask size, volume, open interest, and minimum option price;
- wrong-symbol and wrong-setup contamination;
- future option quote/trade rejection;
- future headline/event rejection;
- future candle and future replay row rejection;
- outcome/fill/P&L/profitability/readiness rejection.

## Current Result

Decision accepted: NO.

Evidence fill authorized: NO.

Backtest authorized: NO.

Trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Proof accepted: NO.

Profitability claimed: NO.
