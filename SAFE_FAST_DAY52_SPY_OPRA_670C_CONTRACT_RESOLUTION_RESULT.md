# SAFE-FAST Day 52 SPY OPRA 670C Contract Resolution Result

## Result

- Status: CONTRACT_RESOLVED_FROM_EXISTING_LOCAL_DEFINITION_EVIDENCE
- Dataset: OPRA.PILLAR
- Schema: definition
- Parent symbol: SPY.OPT
- Coverage: 2026-03-16T00:00:00Z through 2026-03-17T00:00:00Z
- Definition request cost: 0.022584199905 USD
- Definition records: 13472
- March 30 SPY calls found: 30
- Final DBN path: historical_signal_replay/results/day52_spy_opra_parent_definition_20260316.dbn.zst
- Final DBN storage: local-only; excluded from Git
- Final DBN bytes: 485786
- Final DBN SHA-256: 2dfabeaae6eef16f752ef105daf8d469bf932d1e9ee11b7d560ff824bf24011f
- Final resolution JSON path: historical_signal_replay/results/day52_spy_opra_contract_resolution.json
- Final resolution JSON SHA-256: f6dc9ee03907ff5b01da7ec99e27631559f26c1340e9f64afb6d09dd668845ff

## Frozen contract decision

Accepted trigger:

- 668.360000

Accepted invalidation:

- 667.870000

Rejected:

- Raw symbol: SPY   260330C00669000
- Expiration: 2026-03-30
- Strike: 669
- Side: call
- Reason: CONTRACT_UNLISTED

Selected:

- Raw symbol: SPY   260330C00670000
- Expiration: 2026-03-30
- Strike: 670
- Side: call
- Instrument ID: 1241515301
- Publisher ID: 30
- Definition match rows: 1
- Reason: nearest listed expiration with DTE at least 14 and lowest listed call strike greater than or equal to trigger

## Preservation

- The existing paid definition download was reused.
- No second definition request or charge was made during recovery.
- The raw DBN remains local-only.
- The derived contract-resolution JSON and this result document are the committed repository evidence.
- Future chats must not redownload the SPY parent definition chain.

## Accepted entry window

- Start: 2026-03-16T13:31:00Z
- End: 2026-03-16T13:36:00Z

## Remaining economic blockers

- exact 670C quote-request cost
- complete accepted 670C entry quote window
- valid entry or exact rejection
- exit replay
- spread
- slippage
- commissions and fees
- gross P&L
- net P&L

## Proof state

- Complete end-to-end backtest: NO
- Complete 670C quote window: NO
- Valid entry: NO
- Exit: NO
- Net P&L: NO
- Profitability proof: NO
- Paper eligibility: NO
- Live eligibility: NO
