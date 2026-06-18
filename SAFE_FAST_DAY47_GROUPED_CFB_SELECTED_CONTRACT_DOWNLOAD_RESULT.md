# SAFE-FAST Day 47 Grouped CFB Selected-Contract Download Result

## Baseline

- Task file executed: `SAFE_FAST_DAY47_GROUPED_CFB_SELECTED_CONTRACT_DOWNLOAD_CODEX_TASK.md`.
- Baseline branch and commit: `main`, `5a818d8`.
- User approval recorded by task: grouped selected-contract download approved.
- Approved request shape: Databento `OPRA.PILLAR`, `raw_symbol`, `SPY   260429C00700000`.
- Failed shape not used: local starter `instrument_id=1333784938`, which previously returned Databento `422 symbology_invalid_request`.

## Preflight

- Branch verified: `main`.
- Commit verified: `5a818d8`.
- Pre-existing uncommitted file allowed by task: `SAFE_FAST_DAY47_GROUPED_CFB_SELECTED_CONTRACT_DOWNLOAD_CODEX_TASK.md`.
- Databento credential available: YES; key was not printed or written.
- Raw data target: `historical_signal_replay/source_data/external_option_data_drop/`.
- Raw data ignore rule verified through `historical_signal_replay/source_data/external_option_data_drop/.gitignore`.

## Repeat Cost Check

The exact approved `raw_symbol` requests were checked immediately before download.

| Request | Schema | UTC start | UTC end | Checked cost |
| --- | --- | --- | --- | --- |
| setup quotes, open to signal | `tcbbo` | `2026-04-15T13:30:00Z` | `2026-04-15T18:30:00Z` | `$0.001204758883` |
| setup trades, open to signal | `trades` | `2026-04-15T13:30:00Z` | `2026-04-15T18:30:00Z` | `$0.000963807106` |
| signal-day statistics/open-interest diagnosis | `statistics` | `2026-04-15T04:00:00Z` | `2026-04-16T04:00:00Z` | `$0.000057697296` |
| conditional TCBBO exit path | `tcbbo` | `2026-04-15T18:30:00Z` | `2026-04-15T19:45:00Z` | `$0.000422447920` |
| conditional trades exit path | `trades` | `2026-04-15T18:30:00Z` | `2026-04-15T19:45:00Z` | `$0.000337958336` |

- Setup-window subtotal: `$0.002226263285`.
- Conditional exit-path subtotal: `$0.000760406256`.
- Pre-download checked total: `$0.002986669541`.
- Cap enforced by task: `$0.01`.
- Actual billed cost: `NOT_AVAILABLE`.

## Downloaded Ignored Raw Files

All files are local-only and ignored by git.

| Request | CSV path | Rows | CSV bytes | CSV SHA-256 | DBN path | DBN bytes | DBN SHA-256 |
| --- | --- | ---: | ---: | --- | --- | ---: | --- |
| setup `tcbbo` | `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_003_selected_contract_tcbbo_open_to_signal.csv` | 77 | 12697 | `8a5cb4eea6ab53074d1deb4dfdbb9dafcac78b2716643d869e7b1e6e510808e7` | `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_003_selected_contract_tcbbo_open_to_signal.dbn.zst` | 2713 | `46688ea9d93b5891fced974561573bb44957c31cf87967fc54401e34c489d4ed` |
| setup `trades` | `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_003_selected_contract_trades_open_to_signal.csv` | 77 | 10583 | `90d17edd7a6cedf4f3c2c552054aebca473defe816158750c763e605e8003d24` | `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_003_selected_contract_trades_open_to_signal.dbn.zst` | 1886 | `7eb975e788b4eb1811e9b5539687b715c0b56b5e9ed25bf9447126a78b4d5e7a` |
| setup support `statistics` | `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_003_selected_contract_statistics_signal_day.csv` | 88 | 13582 | `362360a2a53d0f7091f4a65df00b68d0e2726fd1df35a1a5dd2d3a698e82e130` | `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_003_selected_contract_statistics_signal_day.dbn.zst` | 840 | `b2166adeb81870b94b704a9a11b0f41f29eaad9398302d2993b2432ac1851e28` |
| conditional exit `tcbbo` | `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_003_selected_contract_tcbbo_signal_to_1545_et.csv` | 25 | 4215 | `7623a21e6edce3ccc138e649fec6c889e1b3b1a342ebd71785a4a80566957d06` | `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_003_selected_contract_tcbbo_signal_to_1545_et.dbn.zst` | 954 | `4cca25e4843c25985e621dbb64294941f8891806d884c4303af3c1ee6124814c` |
| conditional exit `trades` | `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_003_selected_contract_trades_signal_to_1545_et.csv` | 25 | 3529 | `fb27d0814755d123253436fd8060a74490df6f82e1be7c66a5a6db06efc93f7b` | `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_003_selected_contract_trades_signal_to_1545_et.dbn.zst` | 687 | `1af714b29a8f5c3aaf41d6855885c90102f4fd8cb5769be9d6bede0ecdc81515` |
| local manifest | `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_003_selected_contract_download_manifest.json` | n/a | n/a | n/a | n/a | n/a | n/a |

Databento request identifiers were not available from the local client metadata.

## Validation

- Expected setup and conditional exit windows remain separated.
- Expected schemas are identifiable from DBN metadata and CSV headers: `tcbbo`, `trades`, and `statistics`.
- CSV files are readable and nonempty.
- DBN files are readable through `databento.DBNStore.from_file`.
- All downloaded rows use raw symbol `SPY   260429C00700000`.
- All downloaded rows returned Databento row-level `instrument_id=1258293278`.
- Mapping finding: this differs from the earlier local starter mapping `instrument_id=1333784938`; replay work must use the downloaded raw-symbol evidence deliberately and must not replace it with the failed instrument-id request.
- Raw files and manifest are ignored and unstaged.
- No credential was printed, documented, or committed.

## What Remains Unproven

- Downloaded files do not prove that `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` is tradeable, profitable, ready, or promotion eligible.
- Conditional exit-path data remains conditional on later grouped replay finding a valid entry under accepted no-hindsight rules.
- Headline/no-headline policy, complete caution, sample-size, positive expectancy, and promotion blockers remain unresolved.
- No new backtest, P&L, proof, profitability, readiness, promotion, real-trade selection, or intake-ready change is made by this download.

## Next

- Exact next grouped replay task: `SAFE_FAST_DAY47_GROUPED_CFB_SELECTED_CONTRACT_REPLAY_BACKTEST_CODEX_TASK.md`.
- Mandatory queued audit task immediately after the current grouped data/replay path: `SAFE_FAST_DAY47_TO_DAY90_CONSOLIDATED_AUDIT_AND_COMPLETION_PLAN_CODEX_TASK.md`.
