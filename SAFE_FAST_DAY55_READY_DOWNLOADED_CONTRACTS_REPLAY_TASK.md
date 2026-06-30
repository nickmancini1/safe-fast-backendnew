# SAFE-FAST Day 55 Ready Downloaded Contracts Replay Task

Read SAFE_FAST_BUILD_STATE.md first.

Goal:
Create the next economic replay using only the 8 Day 55 contracts already downloaded with cmbp-1, tcbbo, trades, and statistics.

Do not use the missing SPY 670C target as the replay target.
Preserve SPY 670C as exact rejection: target_contract_not_in_day55_download_manifest.

Allowed contracts:
- QQQ   260416C00585000
- QQQ   260416C00590000
- QQQ   260501C00650000
- QQQ   260501C00655000
- SPY   260414C00645000
- SPY   260414C00650000
- SPY   260501C00702000
- SPY   260501C00707000

Required output:
- valid entry + exit + gross/net P&L, or exact no-entry rejection for each ready contract.
- machine-readable JSON result.
- markdown result summary.
- validator.
- focused tests.

Rules:
No vendor download. No definition request. No Schwab. No Railway. No live backend. No paper/live eligibility claim unless replay proves it.
