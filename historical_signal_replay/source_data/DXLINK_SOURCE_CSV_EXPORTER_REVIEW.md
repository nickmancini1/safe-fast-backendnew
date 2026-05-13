# SAFE-FAST Historical Signal Replay v1 dxLink Source CSV Exporter Review

## Status

- **Status:** PASS
- **Baseline:** patch8
- **Exporter script:** `historical_signal_replay/export_dxlink_source_csv.py`
- **Default output target:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- **Real source CSV created:** no

## Boundary

- Read-only market-data only.
- Uses existing `dxlink_candles.get_1h_ema50_snapshot` candle tooling.
- Does not import `main.py`.
- Does not call order, execution, option-chain, quote-order, or broker execution paths.
- Does not place trades.
- Does not modify `main.py`.
- Does not change order/execution logic.

## Data Rules

- Writes the exact header columns from `historical_signal_replay/source_data/templates/first_real_historical_replay_v1_source_template.csv`.
- Uses only real returned dxLink candle rows when run without `--dry-run`.
- Validates numeric finite OHLC values, non-negative volume, high/low consistency, and open/close inside the high/low range before writing.
- Filters rows to weekday regular-session bar timestamps from 9:30 AM through before 4:00 PM America/New_York when returned candle timestamps allow it.
- Marks unavailable 24H/daily, macro, IV, and event context as unconfirmed.
- Does not fabricate timestamps, OHLCV, volume, source metadata, context, setup labels, trigger labels, blocker labels, lifecycle labels, trade outcomes, option P&L, or account sizing fields.

## CLI Review

- `--help` is available through argparse and does not fetch data.
- `--dry-run` validates local setup without making a network request or writing a file.
- Normal execution is read-only market-data retrieval through tastytrade OAuth token refresh and dxLink candle subscription.

## Validation Notes

- The requested task did not fetch data, so the real source CSV was not created.
- The next task should run the read-only exporter command to create the first real SPY source CSV.
