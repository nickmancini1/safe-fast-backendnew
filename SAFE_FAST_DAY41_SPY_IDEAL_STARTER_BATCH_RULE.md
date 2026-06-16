# SAFE-FAST Day 41 SPY Ideal Starter Batch Rule

## Scope

- Candidate: `SPY-REAL-HISTORICAL-IDEAL-001`.
- Setup family: Ideal.
- Data used: local cheap starter Databento files plus existing SPY source/replay rows.
- Full-window data used: NO.
- Backtest, P&L, proof, profitability, readiness, real trade choice: NO.

## Lifecycle Rule

The first conservative SPY Ideal lifecycle rule is source-backed by `historical_signal_replay/reports/second_real_spy_ideal_replay_v1_signal_log.jsonl` lines 5-6 and source CSV line 291.

- `fresh`: only the exact completed SPY Ideal trigger-stage signal timestamp, `2026-05-13T11:30:00-04:00`, with matching symbol, setup type, trigger `740.75`, invalidation `731.83`, `trigger_state=triggered`, source-backed row ordering, and unspent trigger path.
- `spent`: later same-trigger Ideal follow-through/no-fresh-trigger context with explicit prior completed Ideal trigger spent blocker.
- `expired`: a later review of a previously fresh signal when no spent evidence applies.
- `unknown`: missing or wrong identity, timestamps, trigger, invalidation, stage, trigger state, prior-state, rule metadata, row ordering, or no-hindsight boundary.
- Future option/fill/P&L/proof/profitability/readiness inputs must not change lifecycle state.

Fixture file: `historical_signal_replay/fixtures/spy_ideal_lifecycle_regression_fixtures.json`.

## Starter Option Rule

The first conservative SPY Ideal starter option-context rule is a starter-only inspection rule, not a trade choice:

- Long calls only.
- Nearest reviewed expiration with DTE at least `14`.
- Lowest reviewed-universe call strike at or above the candidate trigger.
- Quote must be nearest at or before setup by Databento `ts_event`.
- Spread cap `0.15`; spread percent cap `2.00%`.
- Minimum bid size `1`, ask size `1`, setup-time trade volume `1`.
- Setup-time-safe same-contract OI is used only when it exists in the starter data.
- No fallback after the top-ranked contract fails a gate.

Applied to SPY Ideal, the top-ranked contract is `SPY   260527C00745000`, `instrument_id=1224739213`, expiration `2026-05-27`, strike `745`. Its only local starter quote/trade row is `2026-05-13T15:30:34.836555549Z`, after the `2026-05-13T15:30:00Z` setup boundary, so option context is `unknown`.

Fixture file: `historical_signal_replay/fixtures/spy_ideal_contract_selection_regression_fixtures.json`.

## Execution And Caution Rule

The existing setup-time execution-context thresholds are reused only after a selected setup-time-safe quote exists:

- Quote age `<= 60` seconds is `clean`.
- Quote age `> 60` and `<= 300` seconds is `caution`.
- Quote age `> 300` seconds, future quote, spread/size/volume gate failure, or no-fallback selected-contract failure is `fail`.
- Missing selected setup-time-safe quote data is `unknown`.

For SPY Ideal, no selected setup-time-safe quote exists, so execution context is `unknown`.

Gap context remains `unknown` because no accepted Ideal gap threshold exists. Headline context remains `unknown` because no accepted historical headline/no-headline source policy exists. Complete caution review remains `unknown` by accepted precedence because required components are unknown.

Fixture files:

- `historical_signal_replay/fixtures/spy_ideal_execution_context_regression_fixtures.json`
- `historical_signal_replay/fixtures/spy_ideal_context_caution_regression_fixtures.json`

## Non-Goals

- No raw Databento files were modified.
- No full-window data was used or requested.
- No backtest, entry, fill, exit, P&L, proof, profitability, readiness, live, broker, order, account, `main.py`, or Railway behavior is authorized.
