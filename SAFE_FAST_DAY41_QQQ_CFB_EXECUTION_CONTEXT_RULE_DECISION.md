# SAFE-FAST Day 41 QQQ CFB Execution Context Rule Decision

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00` (`2026-04-13T16:30:00Z`).

Selected contract: `QQQ   260427C00615000`.

Instrument id: `1023411456`.

Baseline from task file: `ebf7b99 Fill QQQ CFB option context with new contract OI exception`.

This document decides the first conservative QQQ Clean Fast Break execution-context rule. It does not fill evidence, backtest, choose a real trade, calculate P&L, claim proof or profitability, mark QQQ ready, or change intake-ready status.

## Decision Result

First conservative execution-context rule accepted: YES.

Evidence filled: NO.

Backtest authorized: NO.

Real trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Proof accepted: NO.

Profitability claimed: NO.

## Status Values

Accepted `execution_context_status` values:

- `clean`: required setup-time quote, spread, size, and volume inputs pass, and quote age is less than or equal to `60` seconds.
- `caution`: required setup-time quote, spread, size, and volume inputs pass, and quote age is greater than `60` seconds but less than or equal to `5` minutes.
- `fail`: required execution usability gates fail, including stale quote age above `5` minutes, spread failure, missing or invalid bid/ask, missing or invalid size, missing setup-time-safe trade volume, quote after signal, future data, or fallback.
- `unknown`: required source data, timestamps, rule inputs, identity fields, or no-hindsight proof are missing or unresolved.

Missing evidence remains a blocker. It must not be treated as clean, caution, proof, profitability, or readiness.

## Quote Age Thresholds

Quote event time source: Databento TCBBO `ts_event`.

Signal/setup boundary: `2026-04-13T16:30:00Z`.

Quote age formula: setup boundary minus selected quote `ts_event`.

Accepted thresholds:

- `clean`: quote at or before setup and quote age `<= 60` seconds.
- `caution`: quote at or before setup and quote age `> 60` seconds and `<= 5` minutes.
- `fail`: quote age `> 5` minutes.
- `fail`: quote `ts_event` after setup.
- `unknown`: missing or unparseable quote timestamp, missing setup timestamp, or unresolved timestamp basis.

`ts_recv` may be preserved as metadata, but it cannot make a post-signal `ts_event` valid.

## Bid, Ask, Spread, Size, And Volume Requirements

The first execution-context rule inherits the accepted QQQ CFB option/contract gates for setup-time usability:

- bid must be present and greater than or equal to `0`;
- ask must be present and greater than bid;
- midpoint must be positive;
- absolute spread must be less than or equal to `0.15`;
- spread percent must be less than or equal to `2.00%`;
- bid size must be at least `1`;
- ask size must be at least `1`;
- same-contract trade volume through setup time must be at least `1`;
- no fallback to another strike, expiration, side, or contract is allowed after the selected/top-ranked contract fails a gate.

Missing bid, ask, midpoint, spread, spread percent, bid size, ask size, or setup-time-safe trade volume is `fail` when the required source row is otherwise present and the rule can evaluate the failed gate. Missing source data or unresolved identity/timestamp proof is `unknown`.

## Fill Basis For Later Testing

For later long-call testing only, the accepted fill basis is the ask price from the selected setup-time-safe quote.

For this target quote, the later-test fill basis would be ask `7.80`.

This task does not fill evidence, simulate an entry, infer a fill, calculate slippage, calculate costs, calculate P&L, backtest, prove profitability, or mark readiness.

## Missing-Data Behavior

Return `unknown` when any required source/rule premise is missing or unresolved:

- wrong candidate id;
- wrong symbol;
- wrong setup type;
- missing selected contract identity;
- missing setup timestamp;
- missing or unparseable quote timestamp;
- missing source identity;
- missing bid/ask row;
- missing spread or spread-percent calculation;
- missing bid size or ask size;
- missing setup-time-safe same-contract trade volume source;
- missing no-hindsight boundary;
- unresolved future-data checks;
- unresolved fallback/no-fallback proof.

Unknown blocks complete-caution promotion.

## Future-Data Rejection

The execution-context rule must reject:

- option quotes with `ts_event` after setup;
- trade rows after setup when calculating setup-time-safe volume;
- future candles;
- future replay rows;
- outcome movement;
- broker/order/account data;
- fills;
- P&L;
- profitability;
- readiness.

Future or forbidden inputs must not improve an execution-context status.

## Expected QQQ Result

Known setup-safe quote:

| Field | Value |
| --- | --- |
| Quote `ts_event` | `2026-04-13T16:06:30.640301037Z` |
| Setup boundary | `2026-04-13T16:30:00Z` |
| Quote age | about `23` minutes `29.359699` seconds |
| Bid / ask | `7.76` / `7.80` |
| Spread | `0.04` |
| Spread percent | about `0.5141%` |
| Bid size / ask size | `3` / `31` |
| Setup-time-safe trade volume | `65` |

The quote passes bid/ask, spread, spread-percent, size, and setup-time-safe trade-volume requirements.

The quote fails the accepted execution quote-age gate because the quote age is greater than `5` minutes.

Expected target result after regression fixtures and implementation:

- `execution_context_status=fail`;
- no fallback;
- no fill evidence;
- no P&L;
- no proof;
- no profitability;
- QQQ remains not ready;
- complete caution remains not accepted.

## Regression Fixtures Needed Next

Required data-only regression fixture cases before implementation or evidence fill:

1. Clean quote age: quote at or before setup with age exactly `60` seconds passes as `clean` when spread, size, and volume pass.
2. Caution lower boundary: quote age greater than `60` seconds returns `caution` when otherwise passing.
3. Caution upper boundary: quote age exactly `5` minutes returns `caution` when otherwise passing.
4. Stale quote failure: quote age greater than `5` minutes returns `fail`.
5. Target QQQ stale quote: `2026-04-13T16:06:30.640301037Z` against `2026-04-13T16:30:00Z` returns `fail`.
6. Quote after signal returns `fail`.
7. Missing quote source returns `unknown`.
8. Missing or unparseable quote timestamp returns `unknown`.
9. Missing bid returns `fail` when quote row is otherwise present.
10. Missing ask returns `fail` when quote row is otherwise present.
11. Crossed or zero-midpoint quote returns `fail`.
12. Spread above `0.15` returns `fail`.
13. Spread percent above `2.00%` returns `fail`.
14. Bid size below `1` returns `fail`.
15. Ask size below `1` returns `fail`.
16. Setup-time-safe trade volume below `1` returns `fail`.
17. Missing trade-volume source returns `unknown`.
18. No-fallback case: failed selected/top-ranked contract does not select another contract.
19. Future quote, trade, candle, replay, fill, broker/order/account, outcome, P&L, profitability, and readiness inputs are rejected.
20. Later-test fill basis uses ask price only and does not calculate P&L.

## Safety Boundaries

Evidence filled: NO.

Backtest authorized: NO.

Real trade chosen: NO.

P&L calculated: NO.

Proof accepted: NO.

Profitability claimed: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Raw Databento files changed: NO.

`main.py`, live/engine trading logic, Railway/deploy files, broker/order/account files, `.env`, secrets, and generated live reports/logs changed: NO.
