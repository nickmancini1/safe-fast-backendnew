# SAFE-FAST Day 46 First CFB Backtest Run With Exit Path Review

## Direct Answer

The first local Clean Fast Break backtest path was rerun using the new local SPY CFB 002 selected-contract exit-path option data.

`SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` now completes as a review-only first reference case. The accepted bid-minus-slippage exit path hits the profit target before the `15:45 ET` time exit. The two control candidates remain rejected for their original named reasons.

## Local File Check

The required local files exist:

- `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_002_selected_contract_tcbbo_entry_to_1545_et.csv`.
- `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_002_selected_contract_trades_entry_to_1545_et.csv`.
- `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_002_selected_contract_exit_path_manifest.json`.

The runner used the TCBBO file for `instrument_id=1258293281`. No data was downloaded and no raw Databento file was changed.

## Local Run Result

| Candidate | Local runner result | Named reason |
| --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | `completed_review_only` | `completed_profit_target` |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | `no_trade` | `quote_after_signal` |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | `no_trade` | `quote_age_above_5_minutes` |

## SPY CFB 002 Completed Review Output

- Entry time: `2026-04-13T16:30:00+00:00`.
- Entry quote time: `2026-04-13T16:29:04.514819+00:00`.
- Selected contract: `SPY   260427C00685000`.
- Instrument id: `1258293281`.
- Entry ask: `6.35`.
- Entry price after accepted slippage: `6.37`.
- Profit target adjusted exit threshold: `7.9625`.
- Option stop adjusted exit threshold: `5.4145`.
- Exit time: `2026-04-13T19:37:14.335714+00:00`.
- Exit reason: `profit_target`.
- Exit bid: `8.00`.
- Exit price after accepted slippage: `7.98`.
- Gross result: `+1.65` option premium points.
- Cost/slippage-adjusted result: `+1.61` option premium points.
- Named success reason: `completed_profit_target`.

## Guardrails

- Existing local data only: YES.
- Databento downloaded: NO.
- Raw Databento files changed: NO.
- Backtest path rerun locally: YES.
- Review-only completed CFB example produced: YES.
- Promotion decision made: NO.
- Proof accepted: NO.
- Profitability claimed: NO.
- Candidate marked ready: NO.
- Intake-ready count changed: NO.
- Live trading, broker/order/account, Railway, `main.py`, and secrets changed: NO.
