# SAFE-FAST Source Historical Data

This folder is reserved for real source historical market data used to prepare future Historical Signal Replay v1 signal/stage/lifecycle fixtures.

Do not add invented, synthetic, placeholder, or example market rows here. If source data is not available, stop and request real source data.

## Allowed Symbols

- `SPY`
- `QQQ`
- `IWM`
- `GLD`

## Boundary

Source data in this folder is for signal/stage/lifecycle replay preparation only.

It must not include trade outcome backtesting, option P&L, account sizing, broker/order execution, live trade decisions, production behavior, or Continuous Watcher implementation data.

## Template

Use the header-only template:

```text
historical_signal_replay/source_data/templates/first_real_historical_replay_v1_source_template.csv
```

Recommended first source file path:

```text
historical_signal_replay/source_data/<symbol>_<YYYY-MM-DD>_<timeframe>_source.csv
```

Recommended naming shape:

```text
SPY_YYYY-MM-DD_1h_rth_source.csv
```

## Intake Rules

- Use one allowed symbol per first source file.
- Use timezone-aware ISO 8601 timestamps.
- Use `America/New_York` for RTH session interpretation.
- Include only real sourced OHLCV values.
- Include source, `source_as_of`, and data vendor metadata.
- Mark unavailable 24H/daily, macro, IV, or event context explicitly unconfirmed.
- Do not use future candles or later outcomes to label rows.
- Do not include outcome, profit, option P&L, account sizing, broker, or execution fields.

See `historical_signal_replay/SOURCE_HISTORICAL_DATA_INTAKE_SPEC.md` before adding any real source file.
