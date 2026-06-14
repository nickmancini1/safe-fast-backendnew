# SAFE-FAST Day 41 QQQ CFB Contract Selection Fixtures Review

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00`.

Baseline from task file: `362972a Accept QQQ CFB contract selection rule`.

This review records data-only regression fixtures for the accepted first QQQ Clean Fast Break contract-selection rule. It does not create selector code, fill evidence, backtest, choose a real trade, calculate P&L, claim proof or profitability, mark QQQ ready, or change intake-ready status.

## Artifact Created

Fixture file: `historical_signal_replay/fixtures/qqq_cfb_contract_selection_regression_fixtures.json`.

Fixture count: `18`.

Accepted rule source: `SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION.md`.

## Fixture Coverage

The fixture file covers:

- valid selected contract;
- wrong side rejected;
- DTE below `14` rejected;
- nearest valid expiration selected;
- strike below trigger `613.67` rejected;
- lowest strike greater than or equal to `613.67` selected;
- spread above `0.15` rejected;
- spread percent above `2.00%` rejected;
- missing bid rejected;
- missing ask rejected;
- bid size below `1` rejected;
- ask size below `1` rejected;
- through-setup trade volume below `1` rejected;
- open interest below `1` rejected;
- quote `ts_event` after signal rejected;
- statistics `ts_event` after signal rejected;
- no fallback when the top-ranked contract fails;
- abstain when no contract passes.

Each fixture includes:

- `fixture_id`;
- `signal_time`;
- `trigger_price`;
- `candidate_contracts`;
- `expected_selected_contract`;
- `expected_status`;
- `expected_rejection_reason`;
- `reason`.

## Rule Boundaries Preserved

The fixtures preserve the accepted first-rule boundaries:

- long calls only;
- nearest reviewed-universe expiration with DTE at least `14`;
- lowest reviewed-universe call strike greater than or equal to trigger `613.67`;
- nearest OTM-by-trigger moneyness;
- quote nearest at or before setup time by Databento `ts_event`;
- strict no-hindsight statistics timestamp handling;
- maximum absolute spread `0.15`;
- maximum spread percent `2.00%`;
- minimum bid size, ask size, trade volume, and open interest of `1`;
- missing-data abstain behavior;
- no fallback scan after a top-ranked contract fails a gate.

## Validation

JSON parse and required-field validation command:

`python - <<local required-field validator>>`

Result: PASS, `18` fixtures, required fields present.

Safe-check command:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`

Result: PASS, `3` checks.

## Still Not Authorized

Selector code created: NO.

Evidence filled: NO.

Backtest authorized: NO.

Real trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Proof accepted: NO.

Profitability claimed: NO.

## Next

The next bounded step, only when explicitly requested, is selector/calculator implementation against these fixtures. Entry, fill, exit, stop/invalidation translation, time exit, cost/slippage, failure labels, headline-source policy, sample-size requirements, and promotion gates remain blocked.
