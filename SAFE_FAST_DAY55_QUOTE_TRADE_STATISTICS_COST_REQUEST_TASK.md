# SAFE_FAST_DAY55_QUOTE_TRADE_STATISTICS_COST_REQUEST_TASK

Read .\SAFE_FAST_BUILD_STATE.md first.

Objective:
Create the exact Day 55 Databento quote/trade/statistics cost-only request for the selected contract in:
historical_signal_replay/results/day55_definition_contract_selection_for_replay_ready_candidates.json

Baseline:
- Branch main, commit 7d7683c.
- Repo started clean.
- Day 55 contract selection is complete.
- Preserve profitability_proof NO and paper_live_eligibility NO.
- Do not claim entry, exit, gross P&L, net P&L, paper eligibility, or live eligibility.

Allowed work:
- Add or update the smallest replay/request builder needed.
- Produce a machine-readable cost-request result under historical_signal_replay/results/.
- Add a short result markdown only if it records the completed machine result.
- Add focused regression coverage for the cost-request builder.

Required request constraints:
- Cost-only first.
- No vendor download.
- No live backend, Schwab, Railway, broker, account, order, fill, credential, .env, or production work.
- Use selected contract identity from the Day 55 selected-contract JSON.
- Request only quote/trade/statistics evidence needed for economic replay.
- Include schemas cmbp-1, tcbbo, trades, statistics when required by existing repo conventions.
- Do not include definition schema in the quote/trade/statistics request.

Required Codex report:
Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:
Commit proof:

Required checks before reporting:
- focused new/changed tests
- affected Day 55 replay regression tests
- validators for any produced machine result
- safe checks available in repo
- git diff --check

Do not commit. Operator review and commit are required.
