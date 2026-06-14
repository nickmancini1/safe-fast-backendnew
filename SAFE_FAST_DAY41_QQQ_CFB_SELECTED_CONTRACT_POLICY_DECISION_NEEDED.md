# SAFE-FAST Day 41 QQQ CFB Selected-Contract Policy Decision Needed

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00`.

This document records the exact human decisions still needed after the first reviewed-universe and selected-contract eligibility policy. It does not choose a trade, backtest, calculate P&L, fill evidence, claim proof or profitability, mark QQQ ready, or change intake-ready status.

## Decision Still Needed

The repo evidence supports a bounded Databento-backed reviewed option universe and no-hindsight quote eligibility filter. It does not support an honest one-contract selection yet.

Exact human decisions needed:

1. Selected side: long calls, long puts, both sides with a ranking rule, debit spreads, or abstain/no-trade.
2. Expiration ranking: nearest available expiration, fixed target DTE, weekly/monthly preference, or explicit fallback behavior when the target expiration is unavailable.
3. Strike ranking: reference price and tie-breaker for one strike, including whether to use signal-day open, trigger, invalidation, nearest ATM, first ITM/OTM, or another side-aware rule.
4. Moneyness preference: ATM, ITM, OTM, or side-aware ranking.
5. Numeric spread rule: maximum absolute spread, maximum spread percent, caution band, and hard-block threshold.
6. Liquidity rule: minimum bid size, ask size, trade count, cleared volume, open interest, and missing-statistics behavior.
7. Statistics timestamp rule: whether Databento statistics with `ts_ref` or `ts_event` after setup time may represent setup-time open interest/cleared volume, or must be rejected for no-hindsight labels.
8. One-contract tie-breaker and fallback: how to choose among multiple eligible contracts and whether to abstain when the preferred contract is missing or rejected.
9. Whether rejected-contract behavior should be `unknown`, `caution`, `fail`, or no-trade for each rejection type.

## Blocked Until These Decisions Exist

- one selected contract;
- option-context clean/caution/fail labels;
- execution-context clean/caution/fail labels;
- contract-specific entry/fill regression fixtures;
- evidence fill beyond blocker-preserving unknowns;
- backtest;
- trade result counting;
- P&L;
- proof;
- profitability;
- readiness.

## Result

Decision needed documented: YES.

Evidence filled: NO.

Backtest authorized: NO.

Trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Proof accepted: NO.

Profitability claimed: NO.
