# SAFE-FAST OPRA 670C Recovery Codex Task

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_OPRA_670C_RECOVERY_HANDOFF_START_HERE.md`
2. `historical_signal_replay/results/day52_spy_opra_contract_resolution.json`
3. `SAFE_FAST_DAY52_SPY_OPRA_670C_CONTRACT_RESOLUTION_RESULT.md`
4. `historical_signal_replay/day52_existing_setup_option_evidence_end_to_end_backtest.py`
5. `scripts/safe_fast_day52_existing_setup_databento_cost_request.py`
6. directly affected tests and validators

## Verified evidence

- 669C is unlisted.
- Frozen-rule selection is `SPY   260330C00670000`.
- Instrument ID: `1241515301`.
- Publisher ID: `30`.
- Entry window: 2026-03-16T13:31:00Z through 2026-03-16T13:36:00Z.
- The raw definition DBN is local-only.
- Do not redownload definitions.

## Objective

1. Remove the nonexistent 669C assumption.
2. Implement deterministic definition-driven contract selection.
3. Select 670C from the committed derived resolution evidence.
4. Correct the Databento cost-only request script.
5. Use `SAFE_FAST_DB_AUTH`.
6. Never print the credential.
7. Make no vendor call from Codex.
8. Prepare the exact complete 670C entry/exit evidence cost request.
9. Add focused tests and affected regression protection.
10. Update factual canonical state.

## Required tests

Cover:

- 669C rejection
- 670C selection
- expiration rule
- strike rule
- input-order invariance
- no future option performance
- exact raw symbol
- complete entry window
- output-path validation
- parseable success JSON
- parseable failure JSON
- credential-name enforcement
- no credential leakage
- no data download in cost-only mode
- no-hindsight
- no-trade
- legal stage transitions
- session boundaries
- duplicate suppression
- stable winner selection
- deterministic reruns

Run only affected bounded Day 50, Day 51, Day 52, Ideal, Clean Fast Break, and Continuation regressions.

Run affected validators.

Run:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`

Run:

`git diff --check`

## Guardrails

Do not modify:

- `main.py`
- production/live backend
- Railway/deploy
- broker/account/order/fill/alert code
- credentials, secrets, tokens, or `.env`
- sizing
- frozen patch8 thresholds

Do not buy or download data.

Do not stage or commit from Codex.

Finish with:

- `READY_FOR_OPERATOR_COMMIT`
- exact baseline
- exact changed files
- contract-selection result
- corrected cost-request behavior
- exact operator command
- exact output path
- focused tests passed
- affected regressions passed
- validators passed
- safe checks passed
- remaining blocker
- complete backtest: NO
- profitability proof: NO
- paper/live eligibility: NO
