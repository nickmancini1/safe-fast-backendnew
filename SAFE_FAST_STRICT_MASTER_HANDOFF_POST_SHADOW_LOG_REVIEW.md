# SAFE-FAST Strict Master Handoff Post Shadow Log Review

## 1. Current Source Priority

Use this source priority exactly:

1. `SAFE_FAST_BUILD_STATE.md`
2. `SAFE_FAST_STRICT_MASTER_HANDOFF_POST_SHADOW_LOG_REVIEW.md`
3. `SAFE_FAST_TRIGGER_CARD_CONTRACT_SCHEMA_REVIEW.md`
4. `SAFE_FAST_WATCHER_STATE_SCHEMA_DESIGN_REVIEW.md`
5. `SAFE_FAST_SHADOW_LOG_SCHEMA_REVIEW.md`
6. `SAFE_FAST_POST_GLD_WATCHER_TRANSITION_HARDENING_PLAN.md`
7. `SAFE_FAST_ALL_SYMBOL_CURRENT_DEPTH_CLOSEOUT_REVIEW.md`
8. older Day 60 / project handoff docs as background only

Older docs such as `SAFE_FAST_DAY60_PRODUCT_BUSINESS_HANDOFF_ADDENDUM.md` and `SAFE_FAST_PROJECT_MASTER_HANDOFF.md` are historical/product context only if they disagree with build-state or this strict handoff.

## 2. Current Baseline

- Baseline: `patch8`
- Repo: `nickmancini1/safe-fast-backendnew`
- Branch: `main`
- Current completed milestone: Continuous Watcher foundation shadow log schema review
- Latest completed milestone commit: `b8b63a4 Add shadow log schema review`
- Active objective: duplicate suppression design review only
- Work mode: build work only, not live trade chat

## 3. Current Completed State

- SPY / QQQ / IWM / GLD current-depth closeout complete.
- All-symbol current-depth closeout/readiness complete.
- Post-GLD hardening plan PASS.
- Watcher shadow architecture plan PASS.
- Trigger-card contract/schema review PASS.
- Watcher state schema/design review PASS.
- Shadow log schema review PASS and committed at `b8b63a4 Add shadow log schema review`.

## 4. Current Active Objective

- Duplicate suppression design review only.
- No implementation yet.

## 5. Strict NO-GO Boundaries

- no Railway
- no production
- no deploy files
- no live backend
- no `main.py` / engine changes
- no watcher runtime code
- no auto-trading
- no broker/order execution
- no option P&L
- no account sizing
- no live trade decisions
- no generated replay reports
- no generated chart outcome reports
- no invented headlines/news
- no live data fetches

## 6. Stale-Handoff Conflict Prevention

- Any old text saying QQQ closeout commit `5d33edc` is current is stale.
- Any old text saying IWM/GLD are future broader targets is stale.
- Any old text saying GLD is incomplete is stale.
- Any old text saying shadow log schema review is uncommitted/index-lock blocked is stale.
- Current build-state wins.

## 7. Build-State Bookkeeping Convention

- Milestone commit and bookkeeping HEAD are separate.
- Bookkeeping-only commits are not conflicts.
- Do not create repeated sync loops.
- Only sync build-state when active objective, milestone status, no-go boundaries, or accepted handoff status are stale.
- If a docs task is committed, update stale "local/pending" wording once, then continue.

## 8. PowerShell/Codex Mistakes To Avoid

- Keep PowerShell blocks short.
- Avoid giant command blocks when a small Codex task is enough.
- Avoid PowerShell double-quoted replacement strings containing backticks.
- Prefer single quotes or Codex edits for markdown with backticks.
- If PowerShell shows `>>`, tell user to press Ctrl+C and recover.
- If `.git/index.lock` appears, stop and remove only if safe / confirm no Git process is running.
- If accidental untracked files appear, stop and clean them first.
- Use:

```powershell
& "$env:APPDATA\npm\codex.cmd" -a never -s workspace-write
```

- Do not use bare `codex`.
- Codex should not commit/push unless explicitly told.

## 9. User/Assistant Workflow

- Assistant starts with baseline, fixed, unproven/NO-GO, active objective.
- Do not ask user to re-explain.
- If repo/build-state/handoff disagree, stop and name exact conflict.
- Give one bounded Codex task at a time.
- After Codex output, give direct commit/push block.
- Be succinct.
- If user is on phone, do not give laptop commands unless requested.

## 10. Watcher Foundation Status And Next Sequence

Current next task sequence:

1. duplicate suppression design review only
2. best-current-candidate / focus ranking design review
3. diagnostics explanation design review
4. headline/news source policy design review
5. only then bounded watcher implementation tasks

Do not skip into watcher implementation.

## 11. Trigger-Card / State / Shadow-Log Dependency Summary

- Trigger-card contract controls card fields and phone/full-card wording.
- Watcher state schema controls lifecycle state.
- Shadow log schema controls append-only review records.
- Duplicate suppression design must use trigger-card and state fields.

## 12. Phone/Laptop Interaction

- Laptop runs watcher first.
- Phone gets short alerts later.
- Phone does not run full watcher first.
- ChatGPT reviews watcher logs/cards after the fact.
- ChatGPT does not call live trades.

## 13. Future Chat First Message

Ready-to-paste first message for a future chat:

```text
You are working on SAFE-FAST build work only, not live trade chat.

Read SAFE_FAST_BUILD_STATE.md first.
Then read SAFE_FAST_STRICT_MASTER_HANDOFF_POST_SHADOW_LOG_REVIEW.md.

Repo: nickmancini1/safe-fast-backendnew
Branch: main
Baseline: patch8
Latest completed milestone commit: b8b63a4 Add shadow log schema review
Latest completed milestone: Continuous Watcher foundation shadow log schema review
Active objective: duplicate suppression design review only

Continuous Watcher implementation remains deferred.
Do not touch Railway, production, deploy files, old repos, main.py, engine logic, live backend, broker/order execution, auto-trading, option P&L, account sizing, generated reports, watcher runtime code, or live trade logic.
Do not fetch live data, make live trade decisions, or fabricate headlines/news, signals, trigger levels, outcomes, P&L, or trade facts.

Current next task: duplicate suppression design review only, no watcher implementation.
```

## 14. Next Task After Strict Handoff

- Duplicate suppression design review only.
- No watcher implementation.
