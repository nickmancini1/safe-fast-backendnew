# SAFE-FAST Day 55 Ready Downloaded Contracts Replay Result

## Decision

- Ready downloaded contracts evaluated: `8`.
- Valid entries: `0`.
- Evaluated exits: `0`.
- Net P&L results: `0`.
- Exact no-entry rejections: `8`.
- Profitability proof: `NO`.
- Paper/live eligibility: `NO`.

## Preserved SPY 670C Rejection

- Contract: `SPY   260330C00670000`.
- Preserved: `True`.
- First blocker: `target_contract_not_in_day55_download_manifest`.

## Contract Results

- `QQQ   260416C00585000`: entry `NO_ENTRY_EXACT_REJECTION`, exit `EXIT_BLOCKED`, gross P&L `None`, net P&L `None`, first blocker `open_interest_statistics_zero_rows`.
- `QQQ   260416C00590000`: entry `NO_ENTRY_EXACT_REJECTION`, exit `EXIT_BLOCKED`, gross P&L `None`, net P&L `None`, first blocker `trade_volume_below_1`.
- `QQQ   260501C00650000`: entry `NO_ENTRY_EXACT_REJECTION`, exit `EXIT_BLOCKED`, gross P&L `None`, net P&L `None`, first blocker `open_interest_statistics_zero_rows`.
- `QQQ   260501C00655000`: entry `NO_ENTRY_EXACT_REJECTION`, exit `EXIT_BLOCKED`, gross P&L `None`, net P&L `None`, first blocker `open_interest_statistics_zero_rows`.
- `SPY   260414C00645000`: entry `NO_ENTRY_EXACT_REJECTION`, exit `EXIT_BLOCKED`, gross P&L `None`, net P&L `None`, first blocker `trade_volume_below_1`.
- `SPY   260414C00650000`: entry `NO_ENTRY_EXACT_REJECTION`, exit `EXIT_BLOCKED`, gross P&L `None`, net P&L `None`, first blocker `trade_volume_below_1`.
- `SPY   260501C00702000`: entry `NO_ENTRY_EXACT_REJECTION`, exit `EXIT_BLOCKED`, gross P&L `None`, net P&L `None`, first blocker `spread_above_0_15`.
- `SPY   260501C00707000`: entry `NO_ENTRY_EXACT_REJECTION`, exit `EXIT_BLOCKED`, gross P&L `None`, net P&L `None`, first blocker `spread_above_0_15`.

## Guardrails

Local downloaded Day 55 Databento files only. No vendor download, definition request, Schwab, Railway/deploy, live backend, credential, `.env`, `main.py`, sizing, commit, profitability claim, or paper/live eligibility change was made.
