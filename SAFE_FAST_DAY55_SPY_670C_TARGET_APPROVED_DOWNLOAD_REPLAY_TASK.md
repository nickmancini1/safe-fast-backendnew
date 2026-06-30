# SAFE-FAST Day 55 SPY 670C Target Approved Download Replay Task

Read SAFE_FAST_BUILD_STATE.md first.

Goal:
Download only the approved SPY 670C target-only Databento evidence, then replay entry, exit, and P&L.

Approved:
- Symbol: SPY   260330C00670000
- Cost: 0.006495481730 USD
- Schemas: cmbp-1, tcbbo, trades, statistics
- No definition
- Destination: historical_signal_replay/source_data/external_option_data_drop/day55_spy_670c_target_only

Rules:
Use the exact requests/windows from historical_signal_replay/results/day55_spy_670c_target_cost_only_request.json.
No broad download. No Schwab. No Railway. No live backend.
Final result must be valid entry/exit/P&L or exact no-entry rejection.
