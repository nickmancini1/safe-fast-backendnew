# SAFE-FAST Day 41 QQQ gap-context calculation task

Repo:
- safe-fast-backendnew

Current baseline:
- Branch: main
- HEAD: 0f3d706 Record Day 41 tastytrade raw data capability review
- Repo should be clean except this task file before Codex starts.

First required action:
- Read SAFE_FAST_BUILD_STATE.md before touching anything else.

Goal:
- Build a separate data-only way to calculate QQQ gap context from existing QQQ price candles.
- Do not fill evidence yet.
- Do not mark QQQ ready.
- Do not change engine/live files.

Candidate:
- QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001

Fields needed:
- gap_context_status
- gap_context_as_of
- gap_context_reviewed_before_signal

Use only:
- previous session close
- signal-day open
- QQQ candles through signal time only
- timestamps / source_as_of already in repo data

Work:
1. Verify repo status and latest commit.
2. Read:
   - SAFE_FAST_BUILD_STATE.md
   - SAFE_FAST_DAY41_TASTYTRADE_RAW_DATA_CAPABILITY_REVIEW.md
   - SAFE_FAST_DAY41_RAW_TASTYTRADE_NEXT_CHAT_HANDOFF.md
   - SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md
   - historical_signal_replay/source_data/richer_export_package_work/
   - QQQ source CSV / replay files tied to QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001
3. Find the exact QQQ candidate date and signal time.
4. Find any existing repo rule for gap context.
5. If no clear rule exists, do not invent one. Write only:
   - SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_RULE_GAP.md
   and explain the exact missing rule.
6. If a clear rule exists, create a small data-only calculator and tests.
   Preferred files:
   - historical_signal_replay/gap_context_calculator.py
   - tests/test_gap_context_calculator.py
   Use repo naming/path style if different.
7. Tests must prove:
   - no candle after signal time is used
   - previous close is found correctly
   - signal-day open is found correctly
   - missing rows fail clearly
   - gap_context_reviewed_before_signal is true only when source data is available before or at signal time
8. Create:
   - SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_CALCULATION_REVIEW.md
9. Append a short status note to:
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_CALCULATION_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_CALCULATION_REVIEW.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_RULE_GAP.md only if needed
- SAFE_FAST_BUILD_STATE.md
- historical_signal_replay/gap_context_calculator.py only if rule exists
- tests/test_gap_context_calculator.py only if rule exists

Do not edit:
- main.py
- engine/live trading files
- Railway/deploy files
- broker/order/account files
- evidence package files
- .env or secrets
- generated live reports/logs

Final response format:
Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:
