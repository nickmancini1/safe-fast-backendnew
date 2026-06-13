# SAFE-FAST Day 41 Databento QQQ download validation task

First action:
- Read SAFE_FAST_BUILD_STATE.md first.

Goal:
- Validate the Databento QQQ option files already downloaded.
- Do not download more data.
- Do not commit raw vendor data.
- Do not fill evidence yet.

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_DAY41_QQQ_EXTERNAL_OPTION_DATA_REQUEST_PACKAGE.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_COST_ACCESS_TEST.md
- historical_signal_replay/source_data/external_option_data_drop/README.md
- all QQQ_OPRA files in historical_signal_replay/source_data/external_option_data_drop/

Task:
1. Confirm the downloaded files exist.
2. Record file names and sizes.
3. Read CSV headers and row counts.
4. Confirm whether files contain:
   - option definitions / chain
   - bid
   - ask
   - quote timestamp
   - spread-calculable fields
   - expiration
   - strike
   - option side
   - trade volume
   - open interest / statistics if present
5. Confirm the timestamp window covers 2026-04-13 12:25-12:35 ET.
6. Identify any contracts near the QQQ signal-day open price 609.455.
7. Do not choose a trade.
8. Do not calculate P&L.
9. Do not mark QQQ ready.
10. Create:
   - SAFE_FAST_DAY41_DATABENTO_QQQ_DOWNLOAD_VALIDATION.md
11. Add or update:
   - historical_signal_replay/source_data/external_option_data_drop/.gitignore
   so raw CSV/DBN/manifest files stay local-only.
12. Append a short note to SAFE_FAST_BUILD_STATE.md.

Allowed writes:
- SAFE_FAST_DAY41_DATABENTO_QQQ_DOWNLOAD_VALIDATION_CODEX_TASK.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_DOWNLOAD_VALIDATION.md
- historical_signal_replay/source_data/external_option_data_drop/.gitignore
- SAFE_FAST_BUILD_STATE.md

Do not write:
- evidence files
- calculator code
- tests
- raw data edits
- main.py
- live/engine/broker/order/account/Railway files
- .env or secrets

Final response:
Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:
