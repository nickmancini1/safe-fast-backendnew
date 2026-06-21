# SAFE-FAST Day 50 Schwab Read-Only Auth and Capability Audit - Codex Task

## Required Startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DATA_SOURCE_REGISTRY.md`
2. `historical_signal_replay/config/safe_fast_data_source_registry.json`
3. `watcher_foundation/safe_fast_data_source_resolver.py`
4. `SAFE_FAST_DAY50_DATA_SOURCE_REGISTRY_AND_SCHWAB_QUEUE_RESULT.md`
5. `SAFE_FAST_PROJECT_DASHBOARD.md`
6. `SAFE_FAST_PROJECT_RULE_INDEX.md`
7. `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`

Expected branch: `main`.

This is read-only broker/source capability work.

## Restrictions

- Do not submit, replace, cancel, or preview an order.
- Do not call an order-submission endpoint.
- Do not modify `main.py`.
- Do not touch Railway or deployment files.
- Do not change frozen trading behavior.
- Do not download paid market data without exact cost check and explicit user approval.
- Do not print, document, commit, or save client secrets, access tokens, or refresh tokens.
- Store Schwab tokens outside Git and outside tracked repo files.
- Require explicit user action only when Schwab OAuth browser authorization is actually needed.

## Required Scope

1. Audit official Schwab Trader API requirements and existing repo support.
2. Implement OAuth authentication and token renewal in read-only mode.
3. Store tokens outside Git and outside tracked repo files.
4. Verify account-list access.
5. Verify balances, buying power, positions, and transaction-history access.
6. Verify quote access.
7. Verify option-chain access.
8. Verify price-history access.
9. Determine historical range, granularity, timestamp semantics, adjustments, option-history availability, rate limits, and entitlement limits.
10. Read existing order and fill records when safely available.
11. Compare bounded identical timestamps against Databento.
12. Compare bounded option-chain fields against tastytrade when available.
13. State which historical fields Schwab can replace, supplement, or cannot provide.
14. Define a future local Schwab market-data archive for forward replay.
15. Add focused tests and documentation.
16. Update the source registry and future-chat handoffs.
17. Keep production, Railway, live backend, and trading logic untouched.

## Required Output

- Schwab read-only audit implementation and tests, if OAuth can be completed safely.
- A result document stating exact capabilities verified, blocked, or not attempted.
- Registry updates only for proven Schwab capabilities.
- No order-submission behavior.
- No live-readiness, proof, profitability, promotion, or paper/live eligibility claim.

