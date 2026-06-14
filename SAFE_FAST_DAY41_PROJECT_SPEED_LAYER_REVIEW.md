# SAFE-FAST Day 41 Project Speed Layer Review

## What Was Added

- Added a safe local check runner at `scripts/safe_fast_run_safe_checks.ps1`.
- Added reusable bounded task templates at `SAFE_FAST_CODEX_TASK_TEMPLATES.md`.
- Added the project dashboard at `SAFE_FAST_PROJECT_DASHBOARD.md`.
- Added candidate-packet guidance at `historical_signal_replay/candidate_packets/README.md`.
- Added a QQQ Clean Fast Break packet at `historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md`.
- Updated the next-chat intro so future chats read build state, dashboard, rule index, templates, safe checks, and candidate packets before doing new work.
- Updated the rule index to record the speed layer as accepted/current.
- Updated build state with this speed-layer result.

## What Was Already Partly Covered

- `SAFE_FAST_BUILD_STATE.md` already preserved the full chronological state.
- `SAFE_FAST_PROJECT_RULE_INDEX.md` already separated accepted/current, missing, pending, superseded, and conflicting rules.
- `SAFE_FAST_PROJECT_PROOF_PIPELINE.md` and `SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md` already defined the broad proof path and trade-plan gate.
- Existing Day 41 docs already recorded Databento validation, Databento field mapping, the OPRA normalizer, the QQQ rule decision package, QQQ threshold fixture decision, and QQQ gap regression fixtures.

## What Was Redundant

- Broad project-control facts were already present across several docs, so the dashboard does not replace them.
- Candidate facts for QQQ already existed in several Day 41 files; the new candidate packet centralizes them for speed rather than creating a new decision.
- The safe-check runner does not replace focused test commands documented in task reviews; it provides a repeatable local pre/post check.

## What Was Clarified

- Future chats should not repeat old discovery when build state, the dashboard, the rule index, or a candidate packet already records the answer.
- The next single action is QQQ gap-context calculator plus focused tests only after a future task explicitly authorizes calculator code.
- The current QQQ gap fixture status is not proof, not evidence fill, not backtest authorization, not P&L, and not readiness.
- Weak, failed, unclear, missing, or unprofitable results mean diagnose and repair, not project-dead language.

## What Was Intentionally Not Deleted

- No old handoff, review, planning, rule, or validation docs were deleted.
- No historical source files were removed.
- No raw Databento files were touched.
- No evidence rows were filled.
- No calculator, backtest, trade-selection, P&L, live, broker, order, account, Railway, `main.py`, `.env`, or secrets files were changed.

## What Future Chats Should Read First

1. `SAFE_FAST_BUILD_STATE.md`.
2. `SAFE_FAST_PROJECT_DASHBOARD.md`.
3. `SAFE_FAST_PROJECT_RULE_INDEX.md`.
4. `historical_signal_replay/candidate_packets/README.md`.
5. The relevant candidate packet, currently `historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md`.
6. `SAFE_FAST_CODEX_TASK_TEMPLATES.md`.

## Safe Check Command

Run:

```powershell
.\scripts\safe_fast_run_safe_checks.ps1
```

Use it before and after code changes. Documentation-only tasks may run it once after changes if no code was edited.
