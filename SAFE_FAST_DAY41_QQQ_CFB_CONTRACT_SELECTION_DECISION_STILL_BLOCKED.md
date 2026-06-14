# SAFE-FAST Day 41 QQQ CFB Contract Selection Decision Still Blocked

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00`.

This document records what remains blocked after accepting the first conservative QQQ Clean Fast Break contract-selection rule for regression work.

## No Longer Blocked For First Contract-Selection Regression

The following first-rule decisions are now defined in `SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION.md`:

- side: long calls only;
- expiration: nearest reviewed-universe expiration with DTE at least `14`;
- strike: lowest reviewed-universe call strike greater than or equal to trigger `613.67`;
- moneyness: nearest out-of-the-money call by trigger reference;
- ranking: deterministic side, expiration, strike, quote, spread, and liquidity ordering;
- maximum spread: `0.15` absolute and `2.00%` spread percent;
- minimum liquidity: bid size `>= 1`, ask size `>= 1`, through-setup trade volume `>= 1`, open interest `>= 1`;
- quote timestamp: nearest TCBBO quote at or before setup time by `ts_event`;
- statistics timestamp: same-contract statistics only when `ts_event` is at or before setup time, and `ts_ref` is also at or before setup time when available;
- missing-data behavior: abstain/unknown;
- rejected top-ranked contract behavior: abstain with no fallback scan.

## Still Blocked Before Evidence Fill Or Trade-Plan Counting

The accepted contract-selection decision does not by itself authorize evidence fill, backtest, trade result counting, P&L, proof, profitability, or readiness.

Still blocked:

1. Regression fixture package for the accepted contract-selection rule.
2. Calculator or selector implementation for the accepted rule.
3. Normalizer support for preserving Databento statistics `ts_ref` if the next implementation wants to test the stricter `ts_ref` branch directly.
4. Option-context clean/caution/fail label thresholds beyond this one-contract selection gate.
5. Execution entry timing.
6. Fill assumption.
7. Exit rule.
8. Stop/invalidation-to-option handling.
9. Time exit or end-of-day handling.
10. Cost and slippage assumptions.
11. Failure/no-trade diagnosis labels.
12. Historical headline/no-headline source and category policy.
13. Sample-size requirements.
14. Promotion gates.

## Exact Human Decisions Still Needed

The first contract-selection rule is sufficient for regression fixture work, but these human decisions remain needed before a complete trade plan can count:

- whether the first-rule spread and liquidity thresholds remain test-only or become promotion-grade thresholds;
- whether Databento open-interest rows with post-setup `ts_event` but pre-setup or prior-date `ts_ref` may be used in a later less restrictive rule;
- exact entry quote time and fill assumption;
- exact exit, stop, time-exit, cost, and slippage rules;
- whether a rejected top-ranked contract should remain an abstain/no-trade or allow fallback scanning in later versions;
- headline/no-headline source policy and category mapping;
- sample-size and promotion thresholds.

## Result

First contract-selection regression rule unblocked: YES.

Evidence fill authorized: NO.

Backtest authorized: NO.

Trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Proof accepted: NO.

Profitability claimed: NO.
