# SAFE-FAST Day 41 QQQ CFB Target Contract Listing / Open-Interest Audit

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00` (`2026-04-13T16:30:00Z`).

Target contract: `QQQ   260427C00615000`.

Instrument id: `1023411456`.

Baseline from task file: `feb2e74 Audit QQQ CFB open interest source`.

This audit checks listing timing and same-contract open-interest availability for the already top-ranked QQQ CFB contract. It does not change the open-interest gate, fill evidence, backtest, calculate P&L, choose a real trade, claim proof or profitability, mark QQQ ready, or change intake-ready status.

## Local Files Inspected

Folder: `historical_signal_replay/source_data/external_option_data_drop/`.

| File | Result |
| --- | --- |
| `QQQ_OPRA_definitions_full_day.csv` | Apr 13 full-day definitions contain the target contract. |
| `QQQ_OPRA_definitions_2026_04_10_parent.csv` | Apr 10 parent definitions exist and contain `10,212` rows, but no target match. |
| `QQQ_OPRA_statistics_full_day.csv` | Apr 13 full-day statistics contain same-contract rows, all after setup, with no `stat_type=9`. |
| `QQQ_OPRA_top_contract_1023411456_statistics_0930_1230_et.csv` | Header-only setup-window statistics CSV with `0` rows. |
| `QQQ_OPRA_top_contract_1023411456_trades_statistics_0930_1230_et_manifest.json` | Confirms the setup-window statistics request for `instrument_id=1023411456` returned `csv_bytes=139` and cost `0.0`. |

The raw Databento `.dbn.zst` files were not modified.

## Apr 13 Definition Result

Exact Apr 13 definition match:

| Field | Value |
| --- | --- |
| CSV line | `10022` |
| `ts_recv` | `2026-04-13T12:00:00.445830893Z` |
| `ts_event` | `2026-04-13T12:00:00.445628903Z` |
| `instrument_id` | `1023411456` |
| `raw_symbol` / `symbol` | `QQQ   260427C00615000` |
| `security_update_action` | `A` |
| `expiration` | `2026-04-27T00:00:00.000000000Z` |
| `instrument_class` | `C` |
| `strike_price` | `615.000000000` |
| `asset` / `underlying` | `QQQ` / `QQQ` |

Definition timing result:

- The definition `ts_event` is `2026-04-13T12:00:00.445628903Z`.
- The setup boundary is `2026-04-13T16:30:00Z`.
- Therefore, the target contract was listed before the signal/setup time in the Apr 13 local definitions.

## Apr 10 Parent Definition Result

Apr 10 parent definition file:

- Path: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_definitions_2026_04_10_parent.csv`.
- Row count: `10,212`.
- Matches for `instrument_id=1023411456`: `0`.
- Matches for `QQQ   260427C00615000`: `0`.
- Matches for same expiration/call/strike (`2026-04-27`, call, `615.000000000`): `0`.

Prior-day listing result:

- The target contract is not present in the local Apr 10 parent definitions.
- Based on the current local Apr 10 parent definition source, the target contract did not exist on the prior trading day.

## Apr 13 Same-Contract Statistics Result

Exact same-contract statistics rows in `QQQ_OPRA_statistics_full_day.csv`:

| Field | Result |
| --- | ---: |
| Same-contract statistics rows | `88` |
| Rows at or before `2026-04-13T16:30:00Z` | `0` |
| Rows after `2026-04-13T16:30:00Z` | `88` |
| Same-contract `stat_type=9` open-interest rows | `0` |

Same-contract stat type counts:

| `stat_type` | Count | First `ts_event` | Last `ts_event` |
| ---: | ---: | --- | --- |
| `1` | `11` | `2026-04-13T20:40:35.574100224Z` | `2026-04-13T21:44:56.145209064Z` |
| `4` | `11` | `2026-04-13T20:40:35.574100224Z` | `2026-04-13T21:44:56.145209064Z` |
| `5` | `11` | `2026-04-13T20:40:35.574100224Z` | `2026-04-13T21:44:56.145209064Z` |
| `6` | `11` | `2026-04-13T20:40:35.574100224Z` | `2026-04-13T21:44:56.145209064Z` |
| `7` | `11` | `2026-04-13T20:40:35.574100224Z` | `2026-04-13T21:44:56.145209064Z` |
| `8` | `11` | `2026-04-13T20:40:35.574100224Z` | `2026-04-13T21:44:56.145209064Z` |
| `11` | `11` | `2026-04-13T20:40:35.574100224Z` | `2026-04-13T21:44:56.145209064Z` |
| `12` | `11` | `2026-04-13T20:40:35.574100224Z` | `2026-04-13T21:44:56.145209064Z` |

Nearest same-contract statistics row:

| Field | Value |
| --- | --- |
| CSV line | `204434` |
| `ts_recv` | `2026-04-13T20:40:35.573660839Z` |
| `ts_event` | `2026-04-13T20:40:35.574100224Z` |
| `stat_type` | `1` |
| `price` | `8.730000000` |
| `quantity` | `9223372036854775807` |
| `symbol` | `QQQ   260427C00615000` |

Latest same-contract statistics row:

| Field | Value |
| --- | --- |
| CSV line | `788713` |
| `ts_recv` | `2026-04-13T21:44:56.145410441Z` |
| `ts_event` | `2026-04-13T21:44:56.145209064Z` |
| `stat_type` | `6` |
| `quantity` | `16` |
| `symbol` | `QQQ   260427C00615000` |

Setup-window target statistics result:

- `QQQ_OPRA_top_contract_1023411456_statistics_0930_1230_et.csv` contains only the header.
- Row count: `0`.
- Setup-time-safe same-contract open-interest rows: `0`.

## Audit Answers

Was the contract listed before signal time?

- Yes. The Apr 13 definition row exists with `security_update_action=A` and `ts_event=2026-04-13T12:00:00.445628903Z`, before the `2026-04-13T16:30:00Z` setup boundary.

Did it exist on the prior trading day?

- No in the current local source. The Apr 10 parent definitions file has `target_matches=0` for both `instrument_id=1023411456` and `QQQ   260427C00615000`, and also has `0` rows for the same `2026-04-27` call `615` contract shape.

Is prior-day open interest unavailable because the contract was not listed?

- The local evidence supports that conclusion for the current files: the target contract is absent from the Apr 10 parent definitions, so a prior-day same-contract open-interest row for that exact contract is not available from the current local Apr 10 source. This does not create a passing substitute under the accepted rule.

Does the current open-interest gate still block option context?

- Yes. The accepted gate still requires same-contract setup-time-safe open interest. The Apr 13 target definition is setup-time-safe, and quote/trade gates remain cured, but the same-contract statistics rows are all after setup and none are `stat_type=9`; the setup-window statistics file has `0` rows. `open_interest_status` remains `unknown`, selector result remains `abstain`, and `option_context_status` remains `unknown`.

What exact next human decision is needed?

- Decide whether to keep blocking newly listed contracts that have no setup-time-safe same-contract open-interest row, or explicitly accept a new listing-aware open-interest rule with regression fixtures before any selector/rule behavior changes.
- If the current gate is kept, the exact source needed remains a same-contract open-interest/statistics row for `QQQ   260427C00615000` / `instrument_id=1023411456`, with accepted timestamp fields at or before `2026-04-13T16:30:00Z`.
- If an exception is desired, it must be a separate human rule decision that defines how same-day-listed contracts are handled, what source proves first listing, what status vocabulary is used, and what regression cases prevent volume, quote size, after-signal statistics, or nearby contracts from becoming hidden substitutes.

## Current QQQ Classification

- Contract listed before setup: YES.
- Contract existed on prior trading day in local Apr 10 definitions: NO.
- Setup-time-safe quote: PASS.
- Setup-time-safe trade volume: PASS, `65`.
- Setup-time-safe same-contract open interest: `unknown`.
- Selector result: `abstain`.
- `option_context_status`: `unknown`.
- QQQ candidate ready: NO.

## Safety Boundaries

Open-interest gate changed: NO.

Evidence filled: NO.

Selector code changed: NO.

Raw Databento files changed: NO.

Backtest authorized: NO.

Real trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Proof accepted: NO.

Profitability claimed: NO.
