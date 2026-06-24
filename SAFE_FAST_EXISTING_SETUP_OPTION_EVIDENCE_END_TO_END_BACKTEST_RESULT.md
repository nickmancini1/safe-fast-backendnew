# SAFE-FAST Existing-Setup Option Evidence and End-to-End Backtest Result

## Decision

- Selected winner: `DAY52-SPY-2026-03-16-CLEAN-FAST-BREAK-20260316T133000Z-P39`.
- Economic family: `Clean Fast Break`.
- Direction: bullish long call.
- Trigger timestamp: `2026-03-16T13:31:00Z`.
- Accepted trigger: `668.360000000`.
- Accepted invalidation: `667.870000000`.
- Duplicate handling: one economic winner only; Ideal and Continuation remain suppressed.

## Contract Selection

- Status: `BLOCKED_DEFINITION_EVIDENCE_MISSING`.
- Deterministic candidate if OPRA definition confirms listing: `SPY   260330C00669000`; expiration `2026-03-30`; strike `669`; side `C`.
- Selected contract: `None`.
- Rejection reason: local March 16 SPY OPRA definition evidence is absent, so the candidate raw symbol cannot be confirmed as a listed contract with instrument_id and setup-safe liquidity.

## Entry Window

- Status: `BLOCKED_COMPLETE_OPTION_PRICE_WINDOW_MISSING`.
- Accepted window: `2026-03-16T13:31:00Z` through `2026-03-16T13:36:00Z`.
- Price basis: ask plus `0.02` entry slippage.
- First valid price: `None`.
- Rejection reason: no local March 16 SPY OPRA quote stream exists for the deterministic candidate contract; the complete accepted entry window cannot be evaluated.

## Vendor Results

- Tastytrade: `FIELD_LIMITATION_BLOCKED`; historical option bid/ask evidence was not proven by the local helper.
- Databento: `NETWORK_EXECUTION_BLOCKED`; use operator script `scripts/safe_fast_day52_existing_setup_databento_cost_request.py`.
- Expected operator output: `historical_signal_replay/results/day52_existing_setup_databento_cost_request_operator_output.json`.

## P&L

No entry, exit, or net P&L was recorded. Stage reached: `EXACT_EVIDENCE_REQUEST`.

## Exact Request

Dataset: `OPRA.PILLAR`. Schemas: `definition`, `cmbp-1`, `tcbbo`, `trades`, and `statistics`. Numerical cost is `PENDING_OPERATOR_COST_OUTPUT` until the operator-run script succeeds.

## Guardrails

No `main.py`, Railway/deploy, production/live backend, broker/account/order/alert code, credentials, `.env`, sizing, paid download, proof, profitability claim, paper eligibility, or live eligibility was changed or created.
