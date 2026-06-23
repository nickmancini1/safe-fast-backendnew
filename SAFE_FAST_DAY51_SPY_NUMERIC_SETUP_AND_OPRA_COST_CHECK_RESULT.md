# SAFE-FAST Day 51 SPY Numeric Setup and OPRA Cost Check Result

## Scope

- Task executed: `SAFE_FAST_DAY51_SPY_NUMERIC_SETUP_AND_OPRA_COST_CHECK_CODEX_TASK.md`.
- Machine-readable result: `historical_signal_replay/results/day51_spy_numeric_setup_and_opra_cost_check.json`.
- Implementation: `historical_signal_replay/day51_spy_numeric_setup_and_opra_cost_check.py`.
- Validator: `watcher_foundation/day51_spy_numeric_setup_and_opra_cost_check_validator.py`.
- Focused tests: `tests/test_day51_spy_numeric_setup_and_opra_cost_check.py`.
- Covered setup families: Ideal, Clean Fast Break, and Continuation for SPY on `2026-03-16` only.

## Numeric Setup Contract

- Ideal: trigger numeric `None` (RULE_GAP_NOT_NUMERICALLY_ESTABLISHED), invalidation numeric `None` (RULE_GAP_NOT_NUMERICALLY_ESTABLISHED); setup evidence VWAP `668.1674118288091935803447593`.
- Clean Fast Break: trigger numeric `None` (RULE_GAP_NOT_NUMERICALLY_ESTABLISHED), invalidation numeric `None` (RULE_GAP_NOT_NUMERICALLY_ESTABLISHED); setup evidence VWAP `668.1674118288091935803447593`.
- Continuation: trigger numeric `None` (RULE_GAP_NOT_NUMERICALLY_ESTABLISHED), invalidation numeric `None` (RULE_GAP_NOT_NUMERICALLY_ESTABLISHED); setup evidence VWAP `668.1674118288091935803447593`.

The exact rule gap remains: the accepted Day 50 mapper names family trigger and invalidation contracts but does not bind those contracts to a numeric OHLCV field. Raw setup-minute high/low/open/close values are recorded as evidence only and were not promoted into trigger or invalidation thresholds.

## Exact OPRA Specification

One grouped request specification was produced for Databento `OPRA.PILLAR` schemas `definition`, `tcbbo`, `trades`, and `statistics`. It is constrained to SPY parent definitions at the setup timestamp, nearest DTE >= 14 expiration (`2026-03-30`), entry evidence from `13:30Z` to `13:35Z`, and selected-contract exit evidence through `19:45Z` only after a selected raw symbol exists.

## Cost Check

- Status: `NOT_AVAILABLE`.
- Grouped total: `NOT_AVAILABLE` `USD`.
- API/local command used: `python -m historical_signal_replay.day51_spy_numeric_setup_and_opra_cost_check`.
- Credential used: `False`.
- Estimate sufficient for explicit approval: `False`.
- Download created: `False`.

## Replay

- Ideal: selected contract `None`; entry `None`; exit `None`; net P&L `None`; status `APPROVAL_REQUIRED_BEFORE_COSTED_BACKTEST`.
- Clean Fast Break: selected contract `None`; entry `None`; exit `None`; net P&L `None`; status `APPROVAL_REQUIRED_BEFORE_COSTED_BACKTEST`.
- Continuation: selected contract `None`; entry `None`; exit `None`; net P&L `None`; status `APPROVAL_REQUIRED_BEFORE_COSTED_BACKTEST`.

No costed backtest was run because numeric trigger/invalidation remain rule-gapped and local March 16 SPY OPRA selected-contract evidence is absent.

## Final Status

`APPROVAL_REQUIRED_COST_ESTIMATE_BLOCKED` grouped cost `NOT_AVAILABLE` `USD`. The precise data it unlocks is the exact grouped SPY OPRA definition, selected-contract quote, trade, statistics, and conditional exit evidence listed in the JSON result.

## Guardrails

No `main.py`, Railway/deploy, production/live backend, broker/account/order code, credentials, `.env`, sizing, alerts, frozen `patch8` thresholds, paid download, proof, paper/live eligibility, or profitability claim was changed or created.
