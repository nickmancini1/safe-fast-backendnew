# SAFE-FAST Day 41 QQQ CFB Top-Contract Quote Coverage Audit

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00` (`2026-04-13T16:30:00Z`).

Top-ranked contract under the accepted first selector rule: `QQQ   260427C00615000`.

This audit inspects local Databento QQQ OPRA files only. It does not download more data, change the selector rule, fill evidence, backtest, calculate P&L, claim proof or profitability, or mark QQQ ready.

## Files Inspected

- Definitions: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_definitions_full_day.csv`.
- TCBBO: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_tcbbo_1225_1235_et.csv`.
- Trades: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_trades_1225_1235_et.csv`.
- Statistics: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_statistics_full_day.csv`.
- Manifest: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_2026-04-13_download_manifest.json`.
- Normalizer: `historical_signal_replay/databento_opra_normalizer.py`.
- Selector: `historical_signal_replay/cfb_contract_selector.py`.

## Exact Contract Mapping

The exact top-ranked contract appears in definitions.

| Field | Value |
| --- | --- |
| Symbol | `QQQ   260427C00615000` |
| Definition line | `10022` |
| Instrument id | `1023411456` |
| Expiration | `2026-04-27` |
| Side | `C` |
| Strike | `615.000000000` |
| Definition `ts_event` | `2026-04-13T12:00:00.445628903Z` |
| Definition `ts_recv` | `2026-04-13T12:00:00.445830893Z` |

The same `instrument_id` and symbol are used in the local TCBBO, trades, and statistics rows found for the contract. No symbol/instrument-id mismatch was found for `1023411456` in the inspected files.

## Exact TCBBO Coverage

Local TCBBO rows for `QQQ   260427C00615000`: `2`.

Rows at or before signal time: `0`.

Rows after signal time: `2`.

Nearest TCBBO row before signal: NONE.

Nearest TCBBO row after signal:

| Field | Value |
| --- | --- |
| CSV line | `18631` |
| Instrument id | `1023411456` |
| `ts_event` | `2026-04-13T16:31:13.931412942Z` |
| `ts_recv` | `2026-04-13T16:31:13.931613555Z` |
| Bid | `8.560000000` |
| Ask | `8.630000000` |
| Bid size | `22` |
| Ask size | `25` |
| TCBBO trade price | `8.580000000` |
| TCBBO trade size | `1` |

Second local TCBBO row:

| Field | Value |
| --- | --- |
| CSV line | `19923` |
| Instrument id | `1023411456` |
| `ts_event` | `2026-04-13T16:31:44.749496767Z` |
| `ts_recv` | `2026-04-13T16:31:44.749700528Z` |
| Bid | `8.480000000` |
| Ask | `8.540000000` |
| Bid size | `10` |
| Ask size | `22` |
| TCBBO trade price | `8.480000000` |
| TCBBO trade size | `1` |

## Trades And Statistics Coverage

Exact trade rows for `QQQ   260427C00615000`: `2`.

Trade rows at or before signal time: `0`.

Trade rows after signal time: `2`.

Nearest trade row before signal: NONE.

Nearest trade row after signal: line `18631`, `ts_event=2026-04-13T16:31:13.931412942Z`, `ts_recv=2026-04-13T16:31:13.931613555Z`, price `8.580000000`, size `1`.

Exact statistics rows for `QQQ   260427C00615000`: `88`.

Statistics rows at or before signal time: `0`.

Statistics rows after signal time: `88`.

Nearest statistics row before signal: NONE.

Nearest statistics row after signal: line `204434`, `ts_event=2026-04-13T20:40:35.574100224Z`, `ts_recv=2026-04-13T20:40:35.573660839Z`, `stat_type=1`, price `8.730000000`.

The statistics rows do not cure the selector blocker because the accepted rule requires timestamp-safe same-contract statistics, and these local statistics rows are all after setup time.

## Nearby Contract Coverage

Definitions include the nearby `2026-04-27` contracts at strikes `610`, `615`, and `620`.

| Contract | Instrument id | Side | Local TCBBO rows | TCBBO rows at/before signal | First local TCBBO `ts_event` |
| --- | --- | --- | ---: | ---: | --- |
| `QQQ   260427C00610000` | `1023411534` | C | `2` | `0` | `2026-04-13T16:31:11.951379332Z` |
| `QQQ   260427P00610000` | `1090520399` | P | `5` | `1` | `2026-04-13T16:29:20.551383589Z` |
| `QQQ   260427C00615000` | `1023411456` | C | `2` | `0` | `2026-04-13T16:31:13.931412942Z` |
| `QQQ   260427P00615000` | `1090520409` | P | `0` | `0` | NONE |
| `QQQ   260427C00620000` | `1023411522` | C | `0` | `0` | NONE |
| `QQQ   260427P00620000` | `1090520375` | P | `0` | `0` | NONE |

This nearby scan shows the local file can contain pre-signal TCBBO rows for adjacent same-expiration contracts, as seen in the `610P`. It also shows the nearest same-expiration calls at `610C` and `615C` both first appear after the signal in the local ten-minute TCBBO file.

## Classification

Symbol/instrument mapping problem: unlikely.

Reason: definitions map the top contract to `instrument_id=1023411456`, and all local TCBBO, trade, and statistics rows for that instrument id retain the same `QQQ   260427C00615000` symbol.

Downloaded time-window problem: possible and likely worth testing with a narrow cost-checked wider pull.

Reason: the local TCBBO/trades window is only `2026-04-13T16:25:00Z` through `2026-04-13T16:35:00Z`. The selector accepts the nearest quote at or before signal time, so a same-day quote before `16:25:00Z` could be setup-time-safe but is outside the local TCBBO file.

Real no-quote blocker in the downloaded ten-minute window: YES.

Reason: inside the local downloaded TCBBO window, the exact top-ranked contract has no TCBBO row at or before `2026-04-13T16:30:00Z`; its first local TCBBO row is about `73.931412942` seconds after the signal.

Selector rule needs a future human decision: still possible, but not required to explain this audit result.

Reason: the current selector is behaving according to the accepted no-hindsight and no-fallback rule. A human decision would be needed only to change quote-age limits, fallback behavior, statistics timestamp handling, or accepted data-request scope.

## Exact Next Databento Request

If a wider quote pull is justified, the next request should be cost-checked first and should not perform a full download until the cost is accepted.

Recommended cost-check request:

| Field | Value |
| --- | --- |
| Vendor | Databento |
| Dataset | `OPRA.PILLAR` |
| Schema | `tcbbo` |
| Symbol | `QQQ   260427C00615000` |
| Instrument id | `1023411456` |
| Start | `2026-04-13T13:30:00Z` (`09:30:00 ET`) |
| End | `2026-04-13T16:30:00Z` (`12:30:00 ET`) |
| Purpose | Determine whether any setup-time-safe TCBBO quote exists for the already top-ranked contract before the signal. |
| Required guardrail | Cost-check first; no full download without accepted cost check. |

If Databento historical symbol filtering cannot use the raw OPRA symbol directly, use the validated instrument id `1023411456` for the same interval. Do not request the full QQQ chain for this audit step unless a later task explicitly authorizes a broader cost-checked pull.

## Result

The local blocker is real for the downloaded ten-minute TCBBO file: the top-ranked `QQQ   260427C00615000` contract has no TCBBO quote at or before signal time in that file.

The blocker is not explained by a symbol/instrument mapping error.

The audit cannot prove the top contract had no quote earlier in the same day, because local TCBBO coverage starts at `2026-04-13T16:25:00Z`. A cost-checked, single-contract wider TCBBO pull from the regular-session open through the setup time is the smallest justified follow-up if more data is allowed.

## Safety Boundaries

Evidence filled: NO.

Selector changed: NO.

Backtest authorized: NO.

Real trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Proof accepted: NO.

Profitability claimed: NO.

Raw Databento files changed: NO.

## Validation

Safe-check command:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`

Result: PASS, `3` checks.
