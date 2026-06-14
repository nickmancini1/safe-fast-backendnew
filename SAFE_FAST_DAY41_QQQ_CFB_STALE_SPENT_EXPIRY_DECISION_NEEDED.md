# SAFE-FAST Day 41 QQQ CFB Stale/Spent Expiry Decision Needed

## Scope

Candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Symbol/setup: QQQ / Clean Fast Break.

Setup/signal time: `2026-04-13T12:30:00-04:00`.

Baseline: `17d433e Fill QQQ CFB gap context evidence`.

This document records the exact missing lifecycle decision. It does not fill evidence, add regression rows, backtest, choose a trade, calculate P&L, mark QQQ ready, accept proof, or claim profitability.

## Decision Needed

SAFE-FAST needs an accepted QQQ Clean Fast Break lifecycle rule that defines:

- when the initial-break candidate is fresh;
- how long the initial-break candidate stays fresh;
- when an untriggered or delayed setup becomes stale;
- when a completed break becomes spent;
- when a setup expires;
- whether expiry is candle-based, same-session, next-session, session-boundary, or higher-base dependent;
- whether a higher-base/fresh-break can create a new eligible trigger path after a prior completed break;
- precedence among fresh, stale, spent, expired, invalidated, blocked, and unknown states.

## Exact Missing Choice

Choose one accepted rule family before fixture or evidence work:

- Same-candle expiry: the initial-break signal is fresh only at the signal candle decision timestamp and becomes expired afterward unless a separately defined higher-base/fresh-break rule creates a new setup.
- Same-session expiry: the initial-break signal can remain fresh through a defined same-session window, but becomes spent after same-session follow-through or by session close.
- Next-candle expiry: the initial-break signal remains fresh until the next completed review candle, then becomes stale/expired if no accepted entry or confirmation rule fires.
- Higher-base refresh: a prior completed Clean Fast Break is spent, but a later higher base may create a new fresh setup only when a new trigger/invalidation pair and fresh completed breakout are source-backed.
- No accepted rule yet: lifecycle fields remain `unknown` or blocked and the QQQ CFB row stays parked.

## Required Regression Decisions

The decision must also specify:

- the controlling timestamp for each lifecycle decision;
- whether the timestamp is setup candle time, review candle time, first follow-through time, or session close;
- boundary behavior at exactly the expiry timestamp;
- missing-data behavior;
- wrong-symbol and wrong-setup contamination behavior;
- future-data rejection behavior;
- precedence when a row could be both spent and expired, or blocked and stale.

## Current Recommended Next Action

Create data-only lifecycle regression fixtures for the QQQ replay rows after the lifecycle rule is chosen. Do not fill `clean_fast_break_stale_spent_expiry_rule` or `clean_fast_break_expiry_regression_rows` until those fixtures exist and pass.

## Current Result

Decision accepted: NO.

Evidence filled: NO.

Backtest authorized: NO.

Trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Proof accepted: NO.

Profitability claimed: NO.
