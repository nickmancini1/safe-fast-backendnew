# SAFE-FAST Day 41 QQQ CFB Option-Context Rerun With Trades/Statistics Review

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00` (`2026-04-13T16:30:00Z`).

Baseline from task file: `2842cbd Rerun QQQ option context with wider quotes`.

This review reruns the existing QQQ CFB option-context selector using the local wider top-contract TCBBO file plus the newly downloaded top-contract trades/statistics files. It does not change selector rules, backtest, calculate P&L, choose a real trade, claim proof or profitability, mark QQQ ready, or change intake-ready status.

## Inputs Used

- Definitions: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_definitions_full_day.csv`.
- Prior quote window: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_tcbbo_1225_1235_et.csv`.
- Wider top-contract quote file: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_top_contract_1023411456_tcbbo_0930_1230_et.csv`.
- New top-contract trades file: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_top_contract_1023411456_trades_0930_1230_et.csv`.
- New top-contract statistics file: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_top_contract_1023411456_statistics_0930_1230_et.csv`.
- Trades/statistics manifest: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_top_contract_1023411456_trades_statistics_0930_1230_et_manifest.json`.
- Normalizer: `historical_signal_replay/databento_opra_normalizer.py`.
- Selector: `historical_signal_replay/cfb_contract_selector.py`.

The new top-contract files are local-only raw vendor data and were not modified. The top-contract files omit a `symbol` column, so the rerun joined them in memory to the already-audited definition mapping for `instrument_id=1023411456`, `QQQ   260427C00615000`.

## New Trades Coverage

The new trades CSV exists: YES.

Exact trade coverage for `instrument_id=1023411456`:

| Field | Value |
| --- | --- |
| Row count | `28` |
| Rows at or before signal time | `28` |
| Rows after signal time | `0` |
| Total setup-time-safe trade size | `65` |
| Instrument id | `1023411456` |
| Contract | `QQQ   260427C00615000` |

First setup-time-safe trade row:

| Field | Value |
| --- | --- |
| CSV line | `2` |
| `ts_event` | `2026-04-13T13:34:26.747067064Z` |
| `ts_recv` | `2026-04-13T13:34:26.747272432Z` |
| Price | `7.100000000` |
| Size | `1` |

Nearest setup-time-safe trade at or before signal time:

| Field | Value |
| --- | --- |
| CSV line | `29` |
| `ts_event` | `2026-04-13T16:06:30.640301037Z` |
| `ts_recv` | `2026-04-13T16:06:30.640503901Z` |
| Price | `7.760000000` |
| Size | `3` |

Result: the previous through-setup trade-volume blocker is cured for the top-ranked contract. The accepted minimum trade volume gate requires at least `1`, and the new file provides `65` setup-time-safe contracts.

## New Statistics Coverage

The new statistics CSV exists: YES.

Exact statistics coverage for `instrument_id=1023411456`:

| Field | Value |
| --- | --- |
| Row count | `0` |
| Rows at or before signal time | `0` |
| Rows after signal time | `0` |
| Setup-time-safe open-interest rows | `0` |

The new statistics request returned a header-only CSV. It does not provide any setup-time-safe open-interest row for the top-ranked contract.

## Selector Rerun

Reviewed-universe definitions loaded: `280`.

Reviewed symbols with setup-time-safe quotes after adding the wider top-contract rows: `76`.

The accepted ranking rule again identifies the top-ranked reviewed-universe contract as:

- contract: `QQQ   260427C00615000`;
- instrument id: `1023411456`;
- expiration: `2026-04-27`;
- strike: `615`;
- side: call;
- DTE: `14`.

Top-ranked contract inputs used by the existing selector:

| Field | Value |
| --- | --- |
| Quote timestamp gate | PASS |
| Nearest setup-time-safe quote | `2026-04-13T16:06:30.640301037Z` |
| Absolute spread gate | PASS, `0.04 <= 0.15` |
| Spread-percent gate | PASS, about `0.5141% <= 2.00%` |
| Bid-size gate | PASS, `3 >= 1` |
| Ask-size gate | PASS, `31 >= 1` |
| Through-setup trade volume from the new trades file | PASS, `65 >= 1` |
| Timestamp-safe same-contract open interest/statistics from the new statistics file | MISSING |

Existing selector result:

| Field | Value |
| --- | --- |
| `contract_selection_status` | `abstain` |
| `selected_contract` | `None` |
| `rejection_reason` | `top_ranked_contract_failed_no_fallback` |

The immediate remaining accepted-rule blocker is timestamp-safe same-contract open interest. The new statistics file has no rows, so the selector cannot satisfy `open_interest >= 1`. The accepted no-fallback rule then preserves the selector abstain instead of selecting another strike or expiration.

## Evidence Fill

`option_context_status` remains `unknown`.

Reason: the wider TCBBO file provides a setup-time-safe quote and the new trades file provides setup-time-safe trade volume, but the new statistics file provides no setup-time-safe same-contract open-interest row. Under the accepted selector, missing open interest is a blocker, not a clean/caution/fail option-context label.

Unchanged fields:

- `headline_context_status=unknown`;
- `execution_context_status=unknown`;
- `complete_caution_review_status=unknown`.

## Safety Boundaries

Backtest authorized: NO.

Trade chosen: NO.

P&L calculated: NO.

Proof accepted: NO.

Profitability claimed: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Raw Databento files changed: NO.

Selector code changed: NO.

`main.py`, live/engine trading logic, Railway/deploy files, broker/order/account files, `.env`, secrets, and generated live reports/logs changed: NO.

## Validation

Focused test command:

`python -m unittest tests.test_cfb_contract_selector`

Result: PASS.

Safe-check command:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`

Result: PASS, `3` checks.

Content validator command:

`python -B -m watcher_foundation.source_evidence_work_package_content_validator`

Result: PASS command; `3` passed requests, `6` failed requests, `6` partial rows, `0` header-only rows.

Bridge command:

`python -B -m watcher_foundation.source_evidence_package_to_intake_bridge`

Result: PASS command; QQQ reconsideration-eligible count `1`, intake-ready count `0`, proof allowed `NO`.

## Next

Option context still cannot move from `unknown` under the accepted selector. A later bounded task would need accepted setup-time-safe same-contract open-interest/statistics support, or a new accepted rule decision changing that gate, before `option_context_status` can honestly move to a clean, caution, or fail value.
