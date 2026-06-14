# SAFE-FAST Day 41 QQQ CFB Contract Selector Review

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00`.

Baseline from task file: `3115468 Add QQQ CFB contract selection fixtures`.

This review records the selector implementation for the accepted first QQQ Clean Fast Break contract-selection regression fixtures. It does not fill evidence, backtest, choose a real trade, calculate P&L, claim proof or profitability, mark QQQ ready, or change intake-ready status.

## Artifacts Created

- Selector: `historical_signal_replay/cfb_contract_selector.py`.
- Tests: `tests/test_cfb_contract_selector.py`.
- Fixture source: `historical_signal_replay/fixtures/qqq_cfb_contract_selection_regression_fixtures.json`.

## Implemented Rule

The selector applies the accepted first one-contract rule:

- long calls only;
- nearest reviewed-universe expiration with DTE at least `14`;
- lowest call strike greater than or equal to trigger `613.67`;
- quote nearest at or before setup time by `ts_event`;
- maximum spread `0.15`;
- maximum spread percent `2.00%`;
- minimum bid size `1`;
- minimum ask size `1`;
- minimum through-setup trade volume `1`;
- minimum open interest `1`;
- statistics `ts_event` at or before setup time and `ts_ref` at or before setup time when present;
- missing or unsafe required data causes abstain;
- if the top-ranked contract fails a gate, the selector abstains and does not fall back to a later strike or expiration.

## Fixture Coverage

Focused tests prove all `18` accepted fixtures pass, including valid selection, rejection gates, timestamp rejection, no fallback after top-ranked failure, and abstain when no contract passes.

## Safety Boundaries

The selector returns only contract-selection status, selected contract symbol when selected, rejection reason, and parsing errors.

It includes explicit refusal helpers for trade choice, P&L, proof, and readiness inference.

Evidence filled: NO.

Backtest authorized: NO.

Real trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Proof accepted: NO.

Profitability claimed: NO.

## Validation

Focused test command:

`python -m unittest tests.test_cfb_contract_selector`

Result: PASS, `6` tests, all `18` fixtures covered.

Safe-check command:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`

Result: PASS, `3` checks.

## Next

The selector is now implemented for regression work only. Entry, fill, exit, stop/invalidation translation, time exit, cost/slippage, failure labels, headline-source policy, sample-size requirements, promotion gates, evidence fill, backtest, trade choice, P&L, proof, profitability, readiness, and intake-ready status remain blocked until explicitly authorized by later tasks.
