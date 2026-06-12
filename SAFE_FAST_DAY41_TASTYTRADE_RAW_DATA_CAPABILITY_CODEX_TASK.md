# SAFE-FAST Day 41 tastytrade raw data capability review task

You are working in repo: safe-fast-backendnew.

Mode:
- Build-only.
- This is not live trade chat.
- No live trading.
- No proof claim.
- No profitability claim.
- No broker/order/account work.
- No Railway/production/deploy work.
- No engine/live trading patching.
- No main.py changes.
- No sizing.
- No alerts.
- No option P&L.
- No fake proof.
- No hindsight filling.

Current verified local baseline before this task:
- Branch: main
- HEAD: 6f1fff4 Add Day 41 raw tastytrade handoff
- Prior commit 46c0a92 is an ancestor of HEAD.
- SAFE_FAST_BUILD_STATE.md exists.
- Current validator state before tastytrade proof: 0 passed requests, 9 failed requests.
- Proof accepted: NO.
- Profitability claim made: NO.

Primary objective:
Run a read-only raw-data capability review for tastytrade / dxLink, focused first on:

Candidate:
- QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001

First evidence target:
- QQQ CFB gap context

Needed SAFE-FAST labels to calculate from raw data:
- gap_context_status
- gap_context_as_of
- gap_context_reviewed_before_signal

Raw data needed:
- previous session close
- signal-day open
- intraday OHLC through the signal time only
- timestamped bars or quotes
- evidence available before or at signal time
- option quote / chain / spread data around signal time if tastytrade can provide it

Critical correction:
- Do not ask whether tastytrade provides SAFE-FAST labels.
- tastytrade is expected to provide raw market / option data only.
- SAFE-FAST must calculate labels from raw data.

Required first reads:
1. SAFE_FAST_BUILD_STATE.md
2. SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md
3. SAFE_FAST_DAY41_RAW_TASTYTRADE_NEXT_CHAT_HANDOFF.md
4. Any Day 41 / tastytrade / raw-data files referenced by latest git history
5. historical_signal_replay/source_data/richer_export_package_work/
6. dxlink_candles.py
7. historical_signal_replay/export_dxlink_source_csv.py
8. Any current tastytrade / dxLink helper files and tests

Safety rules:
- This task is read-only market-data capability testing only.
- Do not place orders.
- Do not preview orders.
- Do not route orders.
- Do not access balances.
- Do not access positions.
- Do not access account history.
- Do not access account numbers.
- Do not print tokens.
- Do not print client secrets.
- Do not print refresh tokens.
- Do not print credentials.
- Do not write .env files.
- Do not expose secrets.
- Do not use broker/order/account endpoints.
- Do not create option P&L.
- Do not create sizing logic.
- Do not create trade recommendations.
- Do not create live trade decisions.
- If checking environment variables or credentials, report only present / missing.

Task:
Create or update exactly this review doc:
- SAFE_FAST_DAY41_TASTYTRADE_RAW_DATA_CAPABILITY_REVIEW.md

The review must answer:

1. Can current local tastytrade / dxLink helpers fetch historical underlying candles for QQQ around the target window?
2. Can they fetch previous session close and signal-day open?
3. Can they fetch intraday bars through signal time only?
4. Can they fetch historical option chain data for that window?
5. Can they fetch historical option bid/ask quotes around signal time?
6. Can they fetch spread and quote timestamps?
7. Can they fetch expiration / strike metadata?
8. Can they fetch option volume / open interest, if available?
9. Which fields are unavailable from current helpers?
10. Which fields may be available from tastytrade but require a different endpoint/helper?
11. Which fields are not available from tastytrade historical access and require another data source?

Required review format:
- Baseline
- Files inspected
- Helpers found
- Safe commands run
- Environment variable presence check, present/missing only
- Candidate metadata found for QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001
- Signal timestamp or target window found
- Raw underlying candle capability
- Previous close / signal-day open capability
- Intraday-through-signal-only capability
- Historical option chain capability
- Historical option bid/ask quote capability
- Spread and quote timestamp capability
- Expiration / strike metadata capability
- Option volume / open interest capability
- Exact raw fields found, with source timestamps if available
- Missing fields
- Whether each missing field is:
  - unavailable from current helper,
  - possibly available from tastytrade through another endpoint/helper,
  - or not available from tastytrade historical access and requiring another source
- Whether QQQ CFB gap-context evidence can be filled now
- If fillable, provide a proposed evidence-fill patch in the doc only
- If not fillable, name the exact blocker and next evidence-backed source path
- Proof accepted: NO
- Profitability claim made: NO
- Intake-ready candidates: 0 unless existing validators prove otherwise

Allowed writes for this task:
- SAFE_FAST_DAY41_TASTYTRADE_RAW_DATA_CAPABILITY_REVIEW.md
- SAFE_FAST_BUILD_STATE.md only to append a compact Day 41 capability-review status note
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md only if a compact handoff/status note is needed

Not allowed in this task:
- Do not edit historical_signal_replay/source_data/richer_export_package_work/ evidence files.
- Do not edit engine/live trading code.
- Do not edit main.py.
- Do not edit Railway/deploy/production files.
- Do not edit broker/order/account code.
- Do not edit .env or secrets files.
- Do not create generated live reports/logs.
- Do not mark proof accepted.
- Do not mark profitability proven.
- Do not mark intake-ready unless existing validators and exact raw evidence prove it, which is not expected in this task.

Code-change rule:
- This is intended as a docs/capability-review task.
- Do not patch helper/source code.
- If a code/helper change appears necessary, stop and document the needed change, required tests, and doc updates instead of making the code change.

Required checks:
- Run git --no-pager status --short before changes.
- Run git --no-pager log -1 --oneline.
- Run safe file discovery only.
- Run existing validators/bridge only if they are local, safe, and do not require live/broker/account/order access.
- If validators/bridge are not run, state exactly why.
- Run git --no-pager status --short after changes.
- Final Codex output must list changed files and tests/checks run.

Final Codex response format:
Baseline:
Fixed:
Blocked:
Still unproven:
Active build objective:
Tests/checks:
Files changed:
Next:
