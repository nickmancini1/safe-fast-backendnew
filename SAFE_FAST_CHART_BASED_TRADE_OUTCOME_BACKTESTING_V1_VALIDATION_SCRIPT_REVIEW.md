# SAFE-FAST Chart-Based Trade Outcome Backtesting v1 Validation Script Review

## Status

- **Validation script task:** PASS
- **Baseline:** patch8
- **Latest local commit before task:** `d4330cf Add chart outcome sample schema validation`
- **Script created:** `chart_trade_outcome_backtesting/validate_chart_outcome_fixtures.py`
- **Scope:** minimal chart-only schema validation for the existing chart outcome sample input fixture and expected output fixture

## Files validated by script

- **Input fixture:** `chart_trade_outcome_backtesting/fixtures/first_spy_continuation_chart_outcome_input_v1.json`
- **Input schema:** `chart_trade_outcome_backtesting/schemas/chart_outcome_backtest_input_v1.schema.json`
- **Expected output fixture:** `chart_trade_outcome_backtesting/fixtures/first_spy_continuation_chart_outcome_expected_output_v1.json`
- **Output schema:** `chart_trade_outcome_backtesting/schemas/chart_outcome_backtest_output_v1.schema.json`

## Boundary review

- **Backtesting implementation started:** no
- **Outcome calculation implemented:** no
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Watcher implementation started:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Fixtures changed:** no
- **Historical replay runner changed:** no

## Expected command

```powershell
python -B chart_trade_outcome_backtesting/validate_chart_outcome_fixtures.py
```

## Expected behavior

- Prints `PASS chart outcome fixture schema validation` when both fixtures validate.
- Prints `FAIL chart outcome fixture schema validation` plus validation details when either fixture fails.
- Exits nonzero on validation failure.
