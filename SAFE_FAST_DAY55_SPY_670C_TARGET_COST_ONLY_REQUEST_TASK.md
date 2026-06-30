# SAFE-FAST Day 55 SPY 670C Target Cost-Only Request Task

Read SAFE_FAST_BUILD_STATE.md first.

Goal:
Create the exact Databento cost-only request for the missing selected target:
SPY   260330C00670000

Rules:
- Cost check only.
- No download.
- No definition request.
- Schemas only: cmbp-1, tcbbo, trades, statistics.
- Derive exact windows from repo evidence.
- If exact windows cannot be proven, write EXACT_WINDOW_NOT_FOUND and stop.
- Do not invent windows.
- Do not use Schwab, Railway, live backend, broker, credentials, or .env.

Required output:
- Exact symbol.
- Exact schemas.
- Exact windows.
- Exact estimated cost.
- Destination for approved download.
- Operator approval text.
- Machine-readable result.
- Markdown result.
- Focused tests or validator if code is added.
