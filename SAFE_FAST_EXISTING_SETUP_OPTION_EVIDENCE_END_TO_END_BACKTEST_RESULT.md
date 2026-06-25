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

- Status: `CONTRACT_RESOLVED_FROM_EXISTING_LOCAL_DEFINITION_EVIDENCE`.
- Rejected contract: `SPY   260330C00669000`; reason `CONTRACT_UNLISTED`.
- Selected contract: `SPY   260330C00670000`; expiration `2026-03-30`; strike `670`; side `C`; instrument ID `1241515301`; publisher ID `30`.
- Rejection reason: SPY   260330C00669000 is rejected as CONTRACT_UNLISTED; SPY   260330C00670000 is the lowest listed call strike greater than or equal to the accepted trigger under the frozen rule.

## Entry Window

- Status: `BLOCKED_COMPLETE_OPTION_PRICE_WINDOW_MISSING`.
- Accepted window: `2026-03-16T13:31:00Z` through `2026-03-16T13:36:00Z`.
- Price basis: ask plus `0.02` entry slippage.
- First valid price: `None`.
- Rejection reason: no complete local March 16 SPY OPRA quote stream exists for the selected 670C contract; the complete accepted entry window cannot be evaluated.

## Vendor Results

- Tastytrade: `FIELD_LIMITATION_BLOCKED`; historical option bid/ask evidence was not proven by the local helper.
- Databento: `NETWORK_EXECUTION_BLOCKED`; use operator script `scripts/safe_fast_day52_existing_setup_databento_cost_request.py`.
- Expected operator output: `historical_signal_replay/results/day52_existing_setup_databento_cost_request_operator_output.json`.

## P&L

No entry, exit, or net P&L was recorded. Stage reached: `EXACT_EVIDENCE_REQUEST`.

## Exact Request

Definition evidence is complete from the committed local contract-resolution JSON. Dataset: `OPRA.PILLAR`. Remaining schemas: `cmbp-1`, `tcbbo`, `trades`, and `statistics`. Numerical cost is `PENDING_OPERATOR_COST_OUTPUT` until the operator-run script succeeds. Current blocker: complete 670C economic evidence.

## Guardrails

No `main.py`, Railway/deploy, production/live backend, broker/account/order/alert code, credentials, `.env`, sizing, paid download, proof, profitability claim, paper eligibility, or live eligibility was changed or created.
