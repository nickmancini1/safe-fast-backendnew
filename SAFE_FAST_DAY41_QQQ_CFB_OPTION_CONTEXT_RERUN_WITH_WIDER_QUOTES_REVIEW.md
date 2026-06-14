# SAFE-FAST Day 41 QQQ CFB Option-Context Rerun With Wider Quotes Review

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00` (`2026-04-13T16:30:00Z`).

Baseline from task file: `3c754f1 Audit QQQ CFB top contract quote coverage`.

This review reruns the existing QQQ CFB option-context selector using the newly downloaded wider top-contract TCBBO file. It does not change selector rules, backtest, calculate P&L, choose a real trade, claim proof or profitability, mark QQQ ready, or change intake-ready status.

## Inputs Used

- Definitions: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_definitions_full_day.csv`.
- Prior quote window: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_tcbbo_1225_1235_et.csv`.
- Wider top-contract quote file: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_top_contract_1023411456_tcbbo_0930_1230_et.csv`.
- Trades: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_trades_1225_1235_et.csv`.
- Statistics: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_statistics_full_day.csv`.
- Normalizer: `historical_signal_replay/databento_opra_normalizer.py`.
- Selector: `historical_signal_replay/cfb_contract_selector.py`.

The wider top-contract TCBBO file is local-only raw vendor data and was not modified. The file omits a `symbol` column, so the rerun joined it in memory to the already-audited definition mapping for `instrument_id=1023411456`, `QQQ   260427C00615000`.

## Wider Quote Coverage

The wider quote CSV exists: YES.

The wider quote CSV contains TCBBO rows for `instrument_id=1023411456`: YES.

Exact wider TCBBO coverage for the top-ranked contract:

| Field | Value |
| --- | --- |
| Row count | `28` |
| Rows at or before signal time | `28` |
| Rows after signal time | `0` |
| Instrument id | `1023411456` |
| Contract | `QQQ   260427C00615000` |

Nearest wider TCBBO quote at or before signal time:

| Field | Value |
| --- | --- |
| CSV line | `29` |
| `ts_event` | `2026-04-13T16:06:30.640301037Z` |
| `ts_recv` | `2026-04-13T16:06:30.640503901Z` |
| Bid | `7.760000000` |
| Ask | `7.800000000` |
| Bid size | `3` |
| Ask size | `31` |
| Midpoint | `7.780000000` |
| Spread | `0.040000000` |
| Spread percent | about `0.5141%` |

Result: the prior quote timestamp blocker is cured for the top-ranked contract. A setup-time-safe TCBBO quote now exists in the local wider quote file.

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
| Absolute spread gate | PASS, `0.04 <= 0.15` |
| Spread-percent gate | PASS, about `0.5141% <= 2.00%` |
| Bid-size gate | PASS, `3 >= 1` |
| Ask-size gate | PASS, `31 >= 1` |
| Through-setup trade volume from the existing trade file | FAIL, `0 < 1` |
| Timestamp-safe same-contract open interest/statistics | MISSING under accepted rule |

Existing selector result:

| Field | Value |
| --- | --- |
| `contract_selection_status` | `abstain` |
| `selected_contract` | `None` |
| `rejection_reason` | `top_ranked_contract_failed_no_fallback` |

The immediate gate after quote, spread, and quote-size checks is the accepted through-setup trade-volume requirement. The existing trade file still has no same-contract trade rows at or before setup time for `QQQ   260427C00615000`, so `trade_volume_through_setup=0`. The accepted no-fallback rule then preserves the selector abstain instead of selecting another strike or expiration.

The statistics blocker also remains: the existing statistics file has `88` rows for the same contract, but `0` are at or before signal time. The first same-contract statistics row is still after setup time at `2026-04-13T20:40:35.574100224Z`, so it cannot provide timestamp-safe open interest under the accepted rule.

## Evidence Fill

`option_context_status` remains `unknown`.

Reason: although the wider TCBBO file provides a setup-time-safe quote for the top-ranked contract, the existing accepted selector still abstains because the top-ranked contract fails required through-setup trade volume and timestamp-safe statistics/open-interest support, with no fallback allowed.

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

The prior quote-only blocker is resolved, but option context still cannot move from `unknown` under the accepted selector. A later bounded task would need accepted setup-time-safe support for the same-contract trade-volume and open-interest/statistics gates, or a new accepted rule decision changing those gates, before `option_context_status` can honestly move to a clean, caution, or fail value.
