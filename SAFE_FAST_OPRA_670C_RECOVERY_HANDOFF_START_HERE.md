# SAFE-FAST OPRA 670C Recovery Handoff — Start Here

## Authority

The local repository is the only source of truth.

Read `SAFE_FAST_BUILD_STATE.md` first.

## Verified recovery evidence

The existing paid SPY OPRA parent-definition DBN has been independently verified:

- Dataset: OPRA.PILLAR
- Schema: definition
- Local-only DBN path: `historical_signal_replay/results/day52_spy_opra_parent_definition_20260316.dbn.zst`
- Bytes: `485786`
- SHA-256: `2dfabeaae6eef16f752ef105daf8d469bf932d1e9ee11b7d560ff824bf24011f`
- Definition records: `13472`
- March 30 SPY calls: `30`

The raw DBN remains local-only and must not be staged or committed.

Committed derived evidence:

- `historical_signal_replay/results/day52_spy_opra_contract_resolution.json`
- `SAFE_FAST_DAY52_SPY_OPRA_670C_CONTRACT_RESOLUTION_RESULT.md`

## Contract resolution

Rejected:

- `SPY   260330C00669000`
- Reason: `CONTRACT_UNLISTED`

Selected under the frozen rule:

- `SPY   260330C00670000`
- Expiration: `2026-03-30`
- Strike: `670`
- Side: call
- Instrument ID: `1241515301`
- Publisher ID: `30`

Do not redownload the SPY parent definition chain.

## Accepted setup state

- Setup timestamp: 2026-03-16T13:30:00Z
- Trigger: 668.360000
- Invalidation: 667.870000
- Winner: DAY52-SPY-2026-03-16-CLEAN-FAST-BREAK-20260316T133000Z-P39
- Entry window: 2026-03-16T13:31:00Z through 2026-03-16T13:36:00Z

## Active task

Read and execute:

`SAFE_FAST_OPRA_670C_RECOVERY_CODEX_TASK.md`

The next bounded implementation must:

1. replace the nonexistent 669C assumption with definition-driven selection;
2. preserve deterministic 670C selection;
3. fix the exact Databento cost-only request;
4. make no vendor call from Codex;
5. prepare the complete accepted 670C evidence request;
6. preserve no-hindsight, no-trade, stage, session, duplicate, and stable-winner protections.

## Workflow

- Codex handles code and bounded offline tests.
- Normal local PowerShell handles credentials, vendor calls, approval, and final commits.
- Databento credential variable: `SAFE_FAST_DB_AUTH`.
- Never print the credential.
- No nonzero-cost request without explicit approval.

## No-go

- no definition redownload
- no broad candidate hunting
- no provisional recognition layer
- no documentation-only loop
- no `main.py`
- no production/live backend
- no Railway/deploy
- no broker/account/order/fill work
- no alerts
- no sizing
- no frozen threshold changes
- no secrets or `.env` changes
- no proof or profitability claim

## Current proof state

- Complete backtest: NO
- Complete 670C quote window: NO
- Valid entry: NO
- Exit: NO
- Net P&L: NO
- Profitability proof: NO
- Paper eligibility: NO
- Live eligibility: NO
