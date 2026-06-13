# SAFE-FAST Day 41 Databento QQQ Cost/Access Test

## Scope

Goal: test Databento access and estimate cost only for the smallest useful QQQ OPRA historical option request around `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

No market data download was requested. No API key was printed or written. No trading, broker, order, account, live engine, evidence, calculator, test, Railway, or deploy files were touched.

## Baseline

| Field | Result |
| --- | --- |
| Branch | `main` |
| HEAD | `f460e91 Record QQQ external option data request package` |
| Dataset target | `OPRA.PILLAR` |
| Candidate | `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` |
| Signal time | `2026-04-13T12:30:00-04:00` |
| Initial test window | `2026-04-13 12:25:00 America/New_York` through `2026-04-13 12:35:00 America/New_York` |
| UTC request window used for cost candidates | `2026-04-13T16:25:00Z` through `2026-04-13T16:35:00Z` |

## Local Access Check

| Check | Result |
| --- | --- |
| `DATABENTO_API_KEY` | `PRESENT` |
| Python `databento` package installed | `YES` |
| Python `databento` package version | `0.79.0` |

Only key presence was checked. The key value was not printed, logged, copied, or written.

## Exact Request Candidates Checked

The bounded request candidates came from `SAFE_FAST_DAY41_QQQ_EXTERNAL_OPTION_DATA_REQUEST_PACKAGE.md`:

- Dataset: `OPRA.PILLAR`.
- Underlying: `QQQ`.
- Symbol input type for cost candidates: `parent`.
- Date: `2026-04-13`.
- Quote window: `2026-04-13T12:25:00-04:00` through `2026-04-13T12:35:00-04:00`.
- Expirations requested by the package: `2026-04-27` through `2026-05-13`, inclusive, or all QQQ expirations if Databento cannot filter by DTE at request time.
- Strikes requested by the package: `590` through `640`, inclusive, or full chain if Databento cannot filter by strike at request time.
- Option types: calls and puts.
- Needed data: historical option quotes/NBBO plus chain/security definition metadata.

Metadata/cost-only calls attempted:

| Call type | Candidate |
| --- | --- |
| Schema listing | `metadata.list_schemas(dataset="OPRA.PILLAR")` |
| Field listing | `metadata.list_fields(schema="definition", encoding="dbn")` |
| Field listing | `metadata.list_fields(schema="cbbo-1s", encoding="dbn")` |
| Field listing | `metadata.list_fields(schema="cbbo-1m", encoding="dbn")` |
| Field listing | `metadata.list_fields(schema="mbp-1", encoding="dbn")` |
| Field listing | `metadata.list_fields(schema="trades", encoding="dbn")` |
| Field listing | `metadata.list_fields(schema="ohlcv-1d", encoding="dbn")` |
| Field listing | `metadata.list_fields(schema="statistics", encoding="dbn")` |
| Unit prices | `metadata.list_unit_prices(dataset="OPRA.PILLAR")` |
| Dataset range | `metadata.get_dataset_range(dataset="OPRA.PILLAR")` |
| Dataset condition | `metadata.get_dataset_condition(dataset="OPRA.PILLAR", start_date="2026-04-13", end_date="2026-04-13")` |
| Cost estimate | `metadata.get_cost(dataset="OPRA.PILLAR", start="2026-04-13T16:25:00Z", end="2026-04-13T16:35:00Z", symbols="QQQ", schema="definition", stype_in="parent")` |
| Cost estimate | same ten-minute parent-symbol cost call for `cbbo-1s`, `cbbo-1m`, `mbp-1`, `trades`, `ohlcv-1d`, and `statistics` |
| Cost estimate | full-day parent-symbol `definition` cost call for `2026-04-13T04:00:00Z` through `2026-04-14T04:00:00Z` |

## Metadata / Cost Call Result

All Databento metadata/cost calls failed before reaching a Databento response because the local environment routes HTTPS through a refused proxy:

`ProxyError: HTTPSConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [WinError 10061]`

This is an environment/network access blocker, not a Databento package blocker and not a vendor field-availability result.

## Estimated Cost

Estimated cost: `NOT_AVAILABLE_PROXY_BLOCKED`.

Paid/full download requested: `NO`.

Market data download requested: `NO`.

Proceed-with-download threshold met: `NO`.

## Schema / Missing Field Availability

Schema and field availability could not be confirmed because the metadata calls were blocked by the local proxy before returning API responses.

Required field mapping remains unconfirmed:

| Missing field need | Databento availability from this test |
| --- | --- |
| option chain / definitions | `UNCONFIRMED_PROXY_BLOCKED` |
| bid | `UNCONFIRMED_PROXY_BLOCKED` |
| ask | `UNCONFIRMED_PROXY_BLOCKED` |
| quote timestamp | `UNCONFIRMED_PROXY_BLOCKED` |
| spread | `UNCONFIRMED_PROXY_BLOCKED`; may be derivable later from bid/ask if quotes are available |
| expiration | `UNCONFIRMED_PROXY_BLOCKED` |
| strike | `UNCONFIRMED_PROXY_BLOCKED` |
| volume | `UNCONFIRMED_PROXY_BLOCKED` |
| open interest if available | `UNCONFIRMED_PROXY_BLOCKED` |

Databento appears able to provide the missing QQQ option fields: `UNKNOWN_FROM_THIS_TEST`.

## Next Step

Exact package step needed: `NONE_PACKAGE_INSTALLED`.

Exact next access command: rerun the same metadata/cost-only check from an environment where HTTPS access to `hist.databento.com` is not routed through the refused `127.0.0.1:9` proxy.

Do not download market data until Databento returns an estimated cost of `0.00` or a clearly tiny cost under available free credits.

## Proceed With Download

Proceed with download: `NO`.

Reason: cost was not confirmed as `0.00` or clearly tiny under free credits, and schema availability was not confirmed.

## Result

Cost/access test reached the installed Databento client and attempted metadata/cost-only calls, but API access was blocked by local proxy/network configuration.

Blocked by missing Python package: `NO`.

Blocked by local proxy/network access: `YES`.

Proof accepted: `NO`.

Profitability claim made: `NO`.
