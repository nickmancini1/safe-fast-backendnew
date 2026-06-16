# SAFE-FAST Day 41 SPY Batch Databento Cost-Check Result

## Scope

- Task: grouped SPY Databento cost-check and source-availability preflight.
- Dataset: Databento `OPRA.PILLAR`.
- Schemas checked for cost-estimate path: `definition`, `tcbbo`, `trades`, and `statistics`.
- Candidates covered in one pass:
  - `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`.
  - `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`.
  - `SPY-REAL-HISTORICAL-IDEAL-001`.
- Databento data downloaded: NO.
- Raw vendor files written: NO.
- Evidence filled: NO.
- Backtest/P&L/proof/readiness: NO.

## Local Access Check

| Check | Result |
| --- | --- |
| `DATABENTO_API_KEY` | `PRESENT`; value not printed or written |
| Python `databento` package | `YES` |
| Python `databento` version | `0.79.0` |
| Databento client created | `YES` |
| Metadata/cost calls reached Databento response | `NO_PROXY_BLOCKED` |

All attempted metadata and cost-estimate calls failed before receiving a Databento response because HTTPS was routed through the refused local proxy `127.0.0.1:9`.

## Grouped Candidate Result

| Candidate | Setup ET | Setup UTC | Trigger | Cost-check schemas/windows | Symbol/filtering approach | Estimated cost | Local SPY OPRA files | Immediate local checks | Still blocked |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | `2026-04-13T12:30:00-04:00` | `2026-04-13T16:30:00Z` | `682.03` | `definition`, `tcbbo`, `trades`, `statistics`; RTH-to-setup `2026-04-13T13:30:00Z` to `2026-04-13T16:30:00Z`; prior definition day `2026-04-10T04:00:00Z` to `2026-04-11T04:00:00Z` | `symbols="SPY"`, `stype_in="parent"` for cost check; later narrow by accepted expiration/strike/instrument rules | `NOT_AVAILABLE_PROXY_BLOCKED` | `NO`; only QQQ OPRA files are local | Source CSV line 138, replay lines 2-3, trigger/invalidation, and work-package row presence can be checked now | Databento cost/source coverage unconfirmed; SPY CFB initial-break lifecycle rule/regressions missing; contract-selection, headline, execution, entry/exit/cost/slippage rules missing |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | `2026-04-15T14:30:00-04:00` | `2026-04-15T18:30:00Z` | `698.65` | `definition`, `tcbbo`, `trades`, `statistics`; RTH-to-setup `2026-04-15T13:30:00Z` to `2026-04-15T18:30:00Z`; prior definition day `2026-04-14T04:00:00Z` to `2026-04-15T04:00:00Z` | `symbols="SPY"`, `stype_in="parent"` for cost check; later narrow by accepted expiration/strike/instrument rules | `NOT_AVAILABLE_PROXY_BLOCKED` | `NO`; only QQQ OPRA files are local | Source CSV line 154, replay lines 5-6, trigger/invalidation, and work-package row presence can be checked now | Databento cost/source coverage unconfirmed; SPY CFB higher-base fresh-break lifecycle rule/regressions missing; contract-selection, headline, execution, entry/exit/cost/slippage rules missing |
| `SPY-REAL-HISTORICAL-IDEAL-001` | `2026-05-13T11:30:00-04:00` | `2026-05-13T15:30:00Z` | `740.75` | `definition`, `tcbbo`, `trades`, `statistics`; RTH-to-setup `2026-05-13T13:30:00Z` to `2026-05-13T15:30:00Z`; prior definition day `2026-05-12T04:00:00Z` to `2026-05-13T04:00:00Z` | `symbols="SPY"`, `stype_in="parent"` for cost check; later narrow only after Ideal-specific rules exist | `NOT_AVAILABLE_PROXY_BLOCKED` | `NO`; only QQQ OPRA files are local | Source CSV line 291, replay lines 5-6, trigger/invalidation, and work-package row presence can be checked now | Databento cost/source coverage unconfirmed; SPY Ideal lifecycle/gap/context rules missing; Ideal contract-selection, headline, execution, entry/exit/cost/slippage rules missing |

## Calls Attempted

Metadata/cost-only calls were attempted for:

- `metadata.list_schemas(dataset="OPRA.PILLAR")`.
- `metadata.list_unit_prices(dataset="OPRA.PILLAR")`.
- `metadata.get_dataset_range(dataset="OPRA.PILLAR")`.
- `metadata.get_dataset_condition(dataset="OPRA.PILLAR", start_date="2026-04-13", end_date="2026-04-13")`.
- `metadata.get_cost(...)` for each candidate, each schema, and each RTH-to-setup window in the table above.
- `metadata.get_cost(...)` for prior-trading-day parent `SPY` `definition` windows.

Result for all Databento metadata/cost calls: `ProxyError` before a Databento API response.

## Local File Availability

Matching local SPY files found:

- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`.
- SPY work-package templates and work rows in `historical_signal_replay/source_data/richer_export_package_template/` and `historical_signal_replay/source_data/richer_export_package_work/`.

Matching local SPY OPRA files found: `NO`.

Local OPRA files found are QQQ-only files in `historical_signal_replay/source_data/external_option_data_drop/`.

## Source / Rule Availability Review

Checks that can be attempted immediately from local source/replay/work-package rows:

- Confirm each SPY source CSV row exists.
- Confirm each SPY replay signal row and later lifecycle-context row exists.
- Confirm trigger and invalidation values.
- Confirm current work-package rows remain partial/missing.
- Draft rule/regression needs for SPY CFB initial-break, SPY CFB higher-base fresh-break, and SPY Ideal lifecycle/context.

Checks blocked until a later authorized Databento pull:

- SPY OPRA definition coverage.
- SPY option quote coverage.
- SPY same-contract trade-volume coverage.
- SPY statistics/open-interest coverage.
- Selected-contract quote freshness, spread, size, and setup-time-safe execution inputs.

Checks blocked by missing SAFE-FAST decisions before evidence fill:

- SPY CFB lifecycle/regression decisions for initial break and higher-base fresh break.
- SPY Ideal lifecycle, gap, and context decisions.
- SPY CFB and SPY Ideal reviewed-universe and contract-selection rules.
- Headline/no-headline source policy.
- Entry, fill, exit, stop/invalidation, time exit, costs, slippage, sample-size, and promotion gates.

## Decision

Next authorized step for the grouped Databento path: `STOP_COST_SOURCE_COVERAGE_NOT_ACCEPTABLE_YET`.

Do not download SPY OPRA data from this result. The estimated cost is unavailable, Databento schema/source coverage was not confirmed, and there are no local SPY OPRA files to inspect. The cost-check should be rerun from an environment where HTTPS access to `hist.databento.com` is not routed through the refused `127.0.0.1:9` proxy. A separate later task may authorize rule/regression fixture work from local SPY source/replay rows, but that is not a data-download or evidence-fill authorization.
