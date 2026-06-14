# SAFE-FAST Day 41 QQQ gap-context evidence fill task

Baseline:
- Latest commit before this task: 1e4e7f2 Add QQQ gap context calculator

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Fill only the QQQ CFB gap-context evidence fields if the new calculator and source-backed data support them.
- Do not fill unrelated evidence.
- Do not mark QQQ ready.
- Do not backtest.
- Do not choose a trade.
- Do not calculate P&L.
- Do not claim proof or profitability.

Candidate:
- QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001

Fields allowed to fill only if source-backed:
- gap_context_status
- gap_context_as_of
- gap_context_reviewed_before_signal

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_CALCULATOR_REVIEW.md
- SAFE_FAST_DAY41_QQQ_GAP_THRESHOLD_FIXTURE_DECISION.md
- historical_signal_replay/gap_context_calculator.py
- historical_signal_replay/fixtures/qqq_gap_context_regression_fixtures.json
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- historical_signal_replay/source_data/richer_export_package_work/

Known QQQ values:
- previous close: 611.02
- signal-day open: 609.455
- signal time: 2026-04-13T12:30:00-04:00
- expected gap status from accepted rule: clean, only if no-hindsight timing passes

Task:
1. Use the calculator and accepted fixtures to verify the QQQ gap-context result.
2. Find the exact QQQ CFB evidence request rows/files in historical_signal_replay/source_data/richer_export_package_work/.
3. Fill only the three gap-context fields if supported.
4. Add clear source notes showing previous close, signal-day open, signal time, calculator rule, and no-hindsight timing.
5. Do not alter unrelated fields.
6. Run the relevant content validator and bridge if safe/local.
7. Create:
   - SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_EVIDENCE_FILL_REVIEW.md
8. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_EVIDENCE_FILL_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_EVIDENCE_FILL_REVIEW.md
- historical_signal_replay/source_data/richer_export_package_work/
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- backtest code
- trade-selection code
- P&L
- raw Databento files
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
