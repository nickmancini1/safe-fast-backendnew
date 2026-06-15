# SAFE-FAST Day 41 QQQ CFB New-Contract OI Exception Fixtures Review

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00` (`2026-04-13T16:30:00Z`).

Target contract: `QQQ   260427C00615000`.

Instrument id: `1023411456`.

Baseline from task file: `63a4748 Accept QQQ CFB new contract OI exception rule`.

This review records data-only regression fixtures for the accepted new-contract open-interest exception. It does not change selector code, fill evidence, backtest, choose a real trade, calculate P&L, claim proof or profitability, mark QQQ ready, or change intake-ready status.

## Artifact Created

Fixture file: `historical_signal_replay/fixtures/qqq_cfb_new_contract_oi_exception_regression_fixtures.json`.

Fixture count: `13`.

Accepted rule source: `SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_RULE.md`.

## Fixture Coverage

The fixture file covers:

- valid new-contract open-interest exception returns `caution`;
- contract listed after signal rejected;
- contract existed prior day but open interest missing rejected as `unknown`;
- missing listing timestamp rejected as `unknown`;
- missing setup-time-safe quote rejected as `unknown`;
- quote after signal rejected;
- spread above `0.15` rejected;
- spread percent above `2.00%` rejected;
- bid size below `1` rejected;
- ask size below `1` rejected;
- setup-time trade volume below `1` rejected;
- fallback after top-ranked contract failure rejected;
- future data rejected.

Each fixture includes:

- `fixture_id`;
- `signal_time`;
- `contract`;
- `instrument_id`;
- `listed_before_signal`;
- `existed_prior_trading_day`;
- `has_setup_safe_quote`;
- `spread`;
- `spread_percent`;
- `bid_size`;
- `ask_size`;
- `setup_time_trade_volume`;
- `has_setup_safe_open_interest`;
- `expected_option_context_status`;
- `expected_rejection_reason`;
- `reason`.

## Rule Boundaries Preserved

The fixtures preserve the accepted exception boundaries:

- the exception applies only to the already selected top-ranked contract;
- prior-day same-contract open interest is not required only when that selected contract was not listed on the prior trading day;
- the contract must be listed before setup;
- setup-time-safe quote, spread, spread percent, bid size, ask size, and trade volume must still pass;
- no future data is allowed;
- no fallback to another strike, expiration, side, or contract is allowed;
- the passing exception result is `caution`, not `clean`, because open interest is unavailable.

## Validation

JSON parse and required-field validation command:

`python -c "<local required-field validator>"`

Result: PASS, `13` fixtures, required fields present.

Safe-check command:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`

Result: PASS, `3` checks.

## Still Not Authorized

Selector code changed: NO.

Evidence filled: NO.

Backtest authorized: NO.

Real trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Proof accepted: NO.

Profitability claimed: NO.

Raw Databento files changed: NO.

## Next

The next bounded step, only when explicitly requested, is selector/rule implementation against these fixtures. Evidence fill, entry, fill, exit, cost/slippage, proof, profitability, readiness, and intake-ready changes remain blocked.
