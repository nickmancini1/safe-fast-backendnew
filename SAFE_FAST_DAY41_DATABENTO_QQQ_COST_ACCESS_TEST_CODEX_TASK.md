# SAFE-FAST Day 41 Databento QQQ cost/access test task

Baseline:
- Branch: main
- HEAD: f460e91 Record QQQ external option data request package

First action:
- Read SAFE_FAST_BUILD_STATE.md first.

Goal:
- Test Databento access and estimate cost only.
- Do not download paid/full data yet.
- Do not print the API key.
- Do not write the API key anywhere.
- Do not call trading/broker/order/account code.

Use:
- Environment variable only: DATABENTO_API_KEY
- Dataset target: OPRA.PILLAR
- Candidate: QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001
- Signal time: 2026-04-13T12:30:00-04:00
- Initial test window: 2026-04-13 12:25:00 America/New_York through 2026-04-13 12:35:00 America/New_York

Task:
1. Verify DATABENTO_API_KEY is present, but print only PRESENT/MISSING.
2. Check whether the Python databento package is installed.
3. If missing, do not install automatically. Say the exact install command needed.
4. If installed, use safe metadata/cost calls only.
5. Estimate cost for the smallest useful QQQ OPRA historical option request around the signal window.
6. Check which schemas are available for the missing fields:
   - option chain / definitions
   - bid
   - ask
   - quote timestamp
   - spread
   - expiration
   - strike
   - volume
   - open interest if available
7. Do not request a full download unless cost is confirmed as 0.00 or clearly tiny under the free credits.
8. Create:
   - SAFE_FAST_DAY41_DATABENTO_QQQ_COST_ACCESS_TEST.md
9. The doc must say:
   - API key: PRESENT or MISSING only
   - package installed: YES/NO
   - exact request candidates checked
   - estimated cost
   - whether Databento appears able to provide the missing QQQ option fields
   - exact next command/package step
   - whether we should proceed with download: YES/NO
10. Append a short note to:
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_DATABENTO_QQQ_COST_ACCESS_TEST_CODEX_TASK.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_COST_ACCESS_TEST.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- API keys
- .env files
- downloaded market data files
- calculator code
- tests
- evidence files
- main.py
- live/engine/broker/order/account/Railway files

Final response:
Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:
