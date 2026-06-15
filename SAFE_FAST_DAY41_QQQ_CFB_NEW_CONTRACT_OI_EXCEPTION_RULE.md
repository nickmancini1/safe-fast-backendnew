# SAFE-FAST Day 41 QQQ CFB New-Contract Open-Interest Exception Rule

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00` (`2026-04-13T16:30:00Z`).

Target contract: `QQQ   260427C00615000`.

Instrument id: `1023411456`.

Baseline from task file: `6befebd Audit QQQ CFB target contract listing open interest`.

This document decides the conservative listing-aware open-interest exception for newly listed contracts. It does not fill evidence, change selector code, backtest, calculate P&L, choose a real trade, claim proof or profitability, mark QQQ ready, or change intake-ready status.

## Decision

Conservative new-contract open-interest exception accepted: YES.

The accepted exception is narrow:

- If the already selected top-ranked contract was not listed on the prior trading day, prior-day same-contract open interest is not required.
- The contract must still be listed before the setup/signal time.
- The setup-time-safe quote, spread, spread percent, bid size, ask size, and trade-volume gates must pass.
- No future data is allowed.
- No fallback to another strike, expiration, side, or contract is allowed after the top-ranked contract fails a required gate.
- The result is `caution`, not `clean`, because open interest is unavailable.

This is a liquidity-context rule decision only. It does not prove trade quality, fills, entry, exit, P&L, readiness, or profitability.

## Allowed Statuses

Allowed option open-interest component statuses under this exception:

- `pass`: same-contract open interest is numeric, at least `1`, and setup-time-safe under the accepted statistics timestamp rule.
- `fail`: same-contract open interest is numeric, setup-time-safe, and below `1`.
- `caution`: same-contract setup-time-safe open interest is unavailable only because the selected contract was not listed on the prior trading day, while all required listing, quote, spread, size, volume, no-future-data, and no-fallback checks pass.
- `unknown`: required listing, prior-day definition, quote, spread, size, volume, timestamp, identity, or no-hindsight evidence is missing, ambiguous, unparseable, or not same-contract.

Allowed option-context result for the exception:

- `caution` when the exception passes.
- `unknown` when required data is missing or ambiguous.
- `fail` when an accepted hard-fail gate has timestamp-safe evidence of failure.
- `clean` is not allowed from this exception because same-contract open interest is unavailable.

## Required Raw Inputs

Required raw inputs for the exception:

- selected contract identity by `instrument_id` and/or exact option symbol;
- selected contract definition row showing listing before setup;
- prior-trading-day parent definitions source for the same underlying and contract universe;
- proof that the selected exact contract was absent from prior-trading-day definitions;
- setup-time-safe TCBBO quote for the same selected contract;
- bid, ask, bid size, ask size, midpoint, absolute spread, and spread percent;
- setup-time-safe same-contract trade rows or calculated through-setup trade volume;
- accepted setup/signal timestamp boundary;
- source timestamps that can be compared to the setup boundary;
- no use of future option rows, future candles, future replay rows, fills, broker/order/account data, P&L, proof, profitability, or readiness.

## Listing-Before-Signal Rule

The selected contract must have an accepted definition/listing row before or at the setup boundary.

For the target QQQ case:

- Apr 13 definition line: `10022`.
- `security_update_action=A`.
- `ts_event=2026-04-13T12:00:00.445628903Z`.
- setup boundary: `2026-04-13T16:30:00Z`.
- listing-before-signal result: PASS.

If the listing timestamp is after setup, missing, ambiguous, wrong-contract, or unparseable, the exception cannot apply and the status is `unknown` or `fail` under the accepted gate being evaluated.

## Prior-Day-Not-Listed Rule

The selected contract must be absent from an accepted prior-trading-day parent definition source.

For the target QQQ case:

- prior trading day checked: `2026-04-10`;
- file: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_definitions_2026_04_10_parent.csv`;
- row count: `10,212`;
- target instrument matches: `0`;
- target symbol matches: `0`;
- same `2026-04-27` call `615` contract-shape rows: `0`;
- prior-day-not-listed result: PASS.

If the prior-day source is missing or does not cover the needed definition universe, the exception cannot apply. Missing prior-day source is `unknown`, not `caution`.

## Quote, Spread, Size, And Volume Requirements

The exception does not relax the existing setup-time option liquidity gates other than prior-day open-interest availability for a newly listed contract.

Required gates:

- same-contract setup-time-safe quote exists;
- quote `ts_event` is at or before setup time;
- bid/ask are parseable and not crossed;
- midpoint is positive;
- absolute spread is at or below the accepted cap;
- spread percent is at or below the accepted cap;
- bid size is at least the accepted minimum;
- ask size is at least the accepted minimum;
- same-contract trade volume through setup is at least the accepted minimum.

For the target QQQ case:

- nearest setup-time-safe quote: `2026-04-13T16:06:30.640301037Z`;
- bid `7.76`;
- ask `7.80`;
- spread `0.04`, passing the `0.15` cap;
- spread percent about `0.5141%`, passing the `2.00%` cap;
- bid size `3`, passing minimum `1`;
- ask size `31`, passing minimum `1`;
- setup-time-safe trade volume `65`, passing minimum `1`.

## Missing-Data Behavior

Missing, ambiguous, unparseable, timestamp-unsafe, wrong-contract, or wrong-symbol data cannot be used to pass the exception.

The exception does not allow:

- inferring open interest from trade volume;
- inferring open interest from quote size;
- using nearby-contract open interest;
- using after-signal statistics;
- using a prior-day definition file that does not cover the relevant universe;
- using a same-day listing row after setup;
- using future candles, future replay rows, outcome data, fills, P&L, proof, profitability, or readiness.

If required exception inputs are missing, classify the relevant component as `unknown` and keep option context from passing.

## No-Fallback Behavior

The no-fallback rule remains unchanged.

If the top-ranked selected contract fails listing, quote, spread, size, volume, timestamp, identity, or exception requirements, the rule abstains or returns the accepted blocked status. It must not scan to another strike, expiration, side, or contract to find a cleaner result.

## Expected QQQ Result

Expected result for `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` under this accepted exception:

- contract listed before setup: PASS;
- absent from prior trading day definitions: PASS;
- setup-time-safe quote: PASS;
- spread gate: PASS;
- spread-percent gate: PASS;
- bid-size gate: PASS;
- ask-size gate: PASS;
- setup-time-safe trade volume: PASS, `65`;
- setup-time-safe same-contract open interest: unavailable because the contract was not listed on the prior trading day;
- open-interest exception component: `caution`;
- expected option-context status after regression fixtures and selector/rule implementation: `caution`;
- expected complete-caution status remains `unknown` unless headline and execution context rules also pass under accepted rules.

This expected result is not an evidence fill and does not choose a real trade.

## Regression Fixtures Needed Next

Before selector or calculator behavior changes, add regression fixtures for:

1. Newly listed contract with listing before setup, prior-day absence, passing quote/spread/size/volume, and missing open interest returns `caution`.
2. Same inputs with prior-day contract present and missing open interest returns `unknown` or blocked under the ordinary open-interest gate.
3. Missing prior-day definitions source returns `unknown`.
4. Prior-day source present but wrong underlying or insufficient universe returns `unknown`.
5. Same-day listing after setup rejects the exception.
6. Setup-time quote missing rejects the exception.
7. Spread above accepted cap rejects the exception.
8. Spread percent above accepted cap rejects the exception.
9. Bid size or ask size below accepted minimum rejects the exception.
10. Setup-time trade volume below accepted minimum rejects the exception.
11. After-signal quote, trade, or statistics rows are rejected.
12. Nearby-contract open interest cannot satisfy the selected contract.
13. Trade volume and quote size cannot be converted into open interest.
14. Top-ranked contract exception failure still does not allow fallback.
15. Wrong symbol, wrong setup, future candle, future replay row, fill, broker/order/account data, outcome, P&L, profitability, and readiness inputs are ignored or rejected.

## Safety Boundaries

Evidence filled: NO.

Selector code changed: NO.

Regression fixtures created now: NO.

Backtest authorized: NO.

Real trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Proof accepted: NO.

Profitability claimed: NO.

Raw Databento files changed: NO.
