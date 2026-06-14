# SAFE-FAST Day 41 QQQ CFB Context/Caution Calculator Review

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00`.

Baseline from task file: `c1877a4 Accept QQQ CFB context caution blocker defaults`.

This review records the fixture-driven context/caution calculator. It does not fill evidence, backtest, choose a trade, calculate P&L, claim proof or profitability, mark QQQ ready, or change intake-ready status.

## Created

Calculator: `historical_signal_replay/context_caution_calculator.py`.

Focused tests: `tests/test_context_caution_calculator.py`.

Fixture source: `historical_signal_replay/fixtures/qqq_cfb_context_caution_regression_fixtures.json`.

## Calculator Behavior

- Classifies `option_context_status`, `headline_context_status`, and `execution_context_status` from the accepted framework fixtures.
- Classifies `complete_caution_review_status` with precedence `fail`, then `unknown`, then `caution`, then `clean`.
- Preserves accepted blocker defaults:
  - no selected contract or reviewed universe keeps option context `unknown`;
  - no source-confirmed historical headline/no-headline source keeps headline context `unknown`;
  - no accepted entry/fill rule keeps execution context `unknown`;
  - any required unknown component keeps complete caution review `unknown`.
- Rejects wrong candidate identity, wrong symbol, and wrong setup type.
- Ignores future option quotes and future headlines for setup-time context.
- Ignores fill, broker/order/account, outcome, P&L, profitability, and readiness fields.
- Returns clear rejection reasons for missing required component data.
- Provides explicit refusal helpers for trade choice, P&L, proof, and readiness inference.

## Validation

Focused test command: `python -m unittest tests.test_context_caution_calculator`.

Focused test result: PASS, 7 tests covering all 22 accepted context/caution fixtures.

Safe-check command: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`.

Safe-check result: PASS, 3 checks.

## Result

Context/caution calculator created: YES.

Evidence filled: NO.

Backtest authorized: NO.

Trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Proof accepted: NO.

Profitability claimed: NO.
