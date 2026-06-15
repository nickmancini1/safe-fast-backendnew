# SAFE-FAST Day 41 QQQ CFB Open-Interest Source Audit

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00` (`2026-04-13T16:30:00Z`).

Top-ranked contract: `QQQ   260427C00615000`.

Instrument id: `1023411456`.

Baseline from task file: `4666e96 Accept QQQ CFB open interest gate decision`.

This audit checks whether timestamp-safe same-contract open interest exists anywhere in the local QQQ OPRA source files. It does not change the open-interest gate, fill evidence, backtest, calculate P&L, choose a real trade, claim proof or profitability, mark QQQ ready, or change intake-ready status.

## Local Files Inspected

Folder: `historical_signal_replay/source_data/external_option_data_drop/`.

| File | Rows | Role |
| --- | ---: | --- |
| `QQQ_OPRA_2026-04-13_download_manifest.json` | n/a | Original Databento request manifest. |
| `QQQ_OPRA_definitions_full_day.csv` | `10,244` | Full-day definitions / contract metadata. |
| `QQQ_OPRA_definitions_full_day.dbn.zst` | n/a | Raw DBN source for definitions. |
| `QQQ_OPRA_statistics_full_day.csv` | `809,952` | Full-day statistics, including open-interest-like `stat_type=9` rows for other contracts. |
| `QQQ_OPRA_statistics_full_day.dbn.zst` | n/a | Raw DBN source for full-day statistics. |
| `QQQ_OPRA_tcbbo_1225_1235_et.csv` | `28,388` | Ten-minute quote/trade-with-BBO window. |
| `QQQ_OPRA_tcbbo_1225_1235_et.dbn.zst` | n/a | Raw DBN source for TCBBO. |
| `QQQ_OPRA_trades_1225_1235_et.csv` | `28,388` | Ten-minute trades window. |
| `QQQ_OPRA_trades_1225_1235_et.dbn.zst` | n/a | Raw DBN source for trades. |
| `QQQ_OPRA_top_contract_1023411456_tcbbo_0930_1230_et.csv` | `28` | Wider setup-window TCBBO for the top contract. |
| `QQQ_OPRA_top_contract_1023411456_tcbbo_0930_1230_et.dbn.zst` | n/a | Raw DBN source for top-contract TCBBO. |
| `QQQ_OPRA_top_contract_1023411456_tcbbo_0930_1230_et_manifest.json` | n/a | Top-contract TCBBO manifest. |
| `QQQ_OPRA_top_contract_1023411456_trades_0930_1230_et.csv` | `28` | Wider setup-window trades for the top contract. |
| `QQQ_OPRA_top_contract_1023411456_trades_0930_1230_et.dbn.zst` | n/a | Raw DBN source for top-contract trades. |
| `QQQ_OPRA_top_contract_1023411456_statistics_0930_1230_et.csv` | `0` | Wider setup-window statistics for the top contract; header-only. |
| `QQQ_OPRA_top_contract_1023411456_statistics_0930_1230_et.dbn.zst` | n/a | Raw DBN source for top-contract statistics; no CSV rows exported. |
| `QQQ_OPRA_top_contract_1023411456_trades_statistics_0930_1230_et_manifest.json` | n/a | Top-contract trades/statistics manifest. |
| `README.md` | n/a | Drop-folder request instructions. |

The `.dbn.zst` files were not modified. Their corresponding CSV exports and manifests were used as the local inspectable source files for this audit.

## Open-Interest-Like Fields Found

Definitions file:

- Header does not contain `open_interest`, `interest`, `quantity`, or `stat_type`.
- The exact top-contract definition is present at CSV line `10022`.
- Definition row fields identify the contract but do not provide open interest:
  - `instrument_id=1023411456`;
  - `symbol=QQQ   260427C00615000`;
  - `expiration=2026-04-27T00:00:00.000000000Z`;
  - `instrument_class=C`;
  - `strike_price=615.000000000`.

Statistics files:

- `QQQ_OPRA_statistics_full_day.csv` has `quantity` and `stat_type` columns.
- `historical_signal_replay/databento_opra_normalizer.py` maps `stat_type=9` to `open_interest` and `stat_type=6` to `cleared_volume`.
- Full-day statistics `stat_type` counts:
  - `1`: `78,933`;
  - `4`: `78,933`;
  - `5`: `78,933`;
  - `6`: `78,933`;
  - `7`: `78,933`;
  - `8`: `78,933`;
  - `9`: `178,488`;
  - `11`: `78,933`;
  - `12`: `78,933`.
- Therefore, local full-day statistics do contain open-interest rows for other QQQ option contracts.

Trades and TCBBO files:

- Trade files have `size`, but no open-interest field.
- TCBBO files have bid/ask price and size fields, but no open-interest field.
- Quote size and trade size remain non-substitutes under the accepted open-interest gate.

## Same-Contract Search Result

Exact local same-contract identity:

- `instrument_id=1023411456`;
- `symbol=QQQ   260427C00615000`.

Full-day statistics result for the same contract:

| Field | Result |
| --- | ---: |
| Same-contract statistics rows | `88` |
| Same-contract statistics rows at or before `2026-04-13T16:30:00Z` | `0` |
| Same-contract statistics rows after `2026-04-13T16:30:00Z` | `88` |
| Same-contract `stat_type=9` open-interest rows | `0` |
| Same-contract `stat_type=9` rows at or before setup | `0` |
| Same-contract `stat_type=9` rows after setup | `0` |

Nearest same-contract statistics row in the full-day file:

| Field | Value |
| --- | --- |
| CSV line | `204434` |
| `ts_recv` | `2026-04-13T20:40:35.573660839Z` |
| `ts_event` | `2026-04-13T20:40:35.574100224Z` |
| `ts_ref` | blank |
| `stat_type` | `1` |
| `price` | `8.730000000` |
| `quantity` | `9223372036854775807` |
| `symbol` | `QQQ   260427C00615000` |

This row is after the setup boundary and is not open interest. It cannot satisfy the accepted open-interest gate.

Top-contract setup-window statistics result:

| File | Result |
| --- | --- |
| `QQQ_OPRA_top_contract_1023411456_statistics_0930_1230_et.csv` | Header-only CSV with `0` rows. |
| `QQQ_OPRA_top_contract_1023411456_statistics_0930_1230_et.dbn.zst` | Present, `99` bytes, corresponding to the empty exported statistics result. |
| `QQQ_OPRA_top_contract_1023411456_trades_statistics_0930_1230_et_manifest.json` | Confirms a `statistics_0930_1230_et` request for `instrument_id=1023411456` with `csv_bytes=139` and `estimated_cost_usd=0.0`. |

Result: no timestamp-safe same-contract open-interest row exists in the local QQQ OPRA files.

## Quote And Trade Cross-Check

The local files still support the previously cured quote and trade gates:

- `QQQ_OPRA_top_contract_1023411456_tcbbo_0930_1230_et.csv` has `28` rows for `instrument_id=1023411456`, all at or before setup time.
- Nearest setup-time-safe TCBBO row is CSV line `29`, `ts_event=2026-04-13T16:06:30.640301037Z`, bid `7.760000000`, ask `7.800000000`, bid size `3`, ask size `31`.
- `QQQ_OPRA_top_contract_1023411456_trades_0930_1230_et.csv` has `28` rows for `instrument_id=1023411456`, all at or before setup time.
- Setup-time-safe trade volume remains `65`.

Those facts do not change the open-interest result because the accepted gate rejects volume-only liquidity and quote-size substitution.

## Current Schema/File Conclusion

Databento statistics schema support exists locally in general: `QQQ_OPRA_statistics_full_day.csv` contains `178,488` `stat_type=9` open-interest rows.

However, the current local Databento files do not provide open interest for the required same contract:

- no `stat_type=9` row for `instrument_id=1023411456`;
- no `stat_type=9` row for `QQQ   260427C00615000`;
- no same-contract statistics row of any type at or before `2026-04-13T16:30:00Z`;
- the targeted setup-window statistics request returned `0` rows.

Therefore, the blocker is a source-coverage blocker for the selected contract in the current local files, not a symbol-mapping blocker, quote blocker, trade-volume blocker, or normalizer-column blocker.

## Next Source Request Needed

Exact next source request needed before the current open-interest gate can pass:

- dataset/source: Databento OPRA statistics or another accepted historical option source that explicitly returns open interest;
- underlying: `QQQ`;
- exact contract: `QQQ   260427C00615000`;
- instrument id: `1023411456`;
- required field: explicit open interest, not volume, quote size, bid size, ask size, or nearby-contract data;
- required value: numeric same-contract open interest;
- required timestamp condition: accepted event/reference timestamp at or before `2026-04-13T16:30:00Z`;
- preferred Databento filter if available: `schema=statistics`, `instrument_id=1023411456`, `stat_type=9`, start early enough to include the prior/open-interest publication for the contract, end `2026-04-13T16:30:00Z`;
- cost check first if a new vendor request is made;
- no full download without accepted cost check.

If Databento cannot provide a same-contract `stat_type=9` row for `1023411456` at or before setup time, the exact decision needed is still the same later human rule decision documented in `SAFE_FAST_DAY41_QQQ_CFB_OPEN_INTEREST_GATE_DECISION.md`: either keep the blocker, or explicitly change the open-interest gate with regression fixtures before any selector behavior changes.

## Current QQQ Classification

- Quote gate: pass.
- Spread gate: pass.
- Spread-percent gate: pass.
- Bid-size gate: pass.
- Ask-size gate: pass.
- Trade-volume gate: pass.
- Same-contract setup-time-safe open-interest gate: `unknown`.
- Selector result remains `abstain`.
- `option_context_status` remains `unknown`.
- No fallback to another strike or expiration is allowed.

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
