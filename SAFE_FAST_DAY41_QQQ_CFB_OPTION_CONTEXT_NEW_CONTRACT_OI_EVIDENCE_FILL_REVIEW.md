# SAFE-FAST Day 41 QQQ CFB Option-Context New-Contract OI Evidence Fill Review

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00` (`2026-04-13T16:30:00Z`).

Baseline from task file: `aec19d8 Update QQQ CFB selector for new contract OI exception`.

This review records the bounded evidence fill for the accepted new-contract open-interest exception. It does not backtest, choose a real trade, calculate P&L, claim proof or profitability, mark QQQ ready, or change intake-ready status.

## Inputs Used

- Definitions: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_definitions_full_day.csv`.
- Prior-day definitions: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_definitions_2026_04_10_parent.csv`.
- Wider top-contract quote file: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_top_contract_1023411456_tcbbo_0930_1230_et.csv`.
- Top-contract trades file: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_top_contract_1023411456_trades_0930_1230_et.csv`.
- Top-contract statistics file: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_top_contract_1023411456_statistics_0930_1230_et.csv`.
- Selector: `historical_signal_replay/cfb_contract_selector.py`.

The raw Databento files were read only and were not modified.

## Selector Rerun

Reviewed-universe candidate count: `280`.

Selected/top-ranked contract identity:

| Field | Value |
| --- | --- |
| Contract | `QQQ   260427C00615000` |
| Instrument id | `1023411456` |
| Expiration | `2026-04-27` |
| Strike | `615` |
| Side | call |

Base selector result without the exception:

| Field | Value |
| --- | --- |
| `contract_selection_status` | `abstain` |
| `selected_contract` | `None` |
| `rejection_reason` | `top_ranked_contract_failed_no_fallback` |

This preserves the original open-interest gate and no-fallback behavior.

## New-Contract OI Exception Evidence

Exception inputs for the target contract:

| Field | Value |
| --- | --- |
| Apr 13 listing `ts_event` | `2026-04-13T12:00:00.445628903Z` |
| Listed before setup | YES |
| Apr 10 target instrument matches | `0` |
| Apr 10 target symbol matches | `0` |
| Apr 10 same `2026-04-27` call `615` contract-shape rows | `0` |
| Nearest setup-time-safe quote | `2026-04-13T16:06:30.640301037Z` |
| Bid / ask | `7.76` / `7.80` |
| Spread | `0.04` |
| Spread percent | about `0.5141%` |
| Bid size / ask size | `3` / `31` |
| Setup-time-safe trade rows | `28` |
| Setup-time-safe trade volume | `65` |
| Setup-time-safe statistics rows | `0` |

Exception selector result:

| Field | Value |
| --- | --- |
| `option_context_status` | `caution` |
| `rejection_reason` | `None` |

Reason: the already top-ranked contract was listed before setup, was absent from the Apr 10 prior-trading-day parent definitions, and passed the setup-time-safe quote, spread, spread-percent, bid-size, ask-size, trade-volume, no-future-data, and no-fallback gates. Same-contract open interest is unavailable because the contract was newly listed, so the accepted exception returns `caution`, not `clean`.

## Evidence Fill

Updated file:

- `historical_signal_replay/source_data/richer_export_package_work/qqq_cfb_complete_context_caution_fields.jsonl`.

Updated field:

- `option_context_status`: `unknown` -> `caution`.

Unchanged fields:

- `headline_context_status=unknown`;
- `execution_context_status=unknown`;
- `complete_caution_review_status=unknown`.

Complete caution remains `unknown` because headline and execution context remain unsupported by accepted source/rule decisions.

## Validation

Focused test command:

`python -m unittest tests.test_cfb_contract_selector`

Result: PASS, `12` tests.

Safe-check command:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`

Result: PASS, `3` checks.

Content validator command:

`python -B -m watcher_foundation.source_evidence_work_package_content_validator`

Result: PASS command; `3` passed requests, `6` failed requests, `6` partial rows, `0` header-only rows.

Bridge command:

`python -B -m watcher_foundation.source_evidence_package_to_intake_bridge`

Result: PASS command; QQQ remains reconsideration-eligible, intake-ready count `0`, proof allowed `NO`.

## Safety Boundaries

Backtest authorized: NO.

Trade chosen: NO.

P&L calculated: NO.

Proof accepted: NO.

Profitability claimed: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Raw Databento files changed: NO.

`main.py`, live/engine trading logic, Railway/deploy files, broker/order/account files, `.env`, secrets, and generated live reports/logs changed: NO.
