# SAFE-FAST Day 47 Codex Task — Grouped CFB Expansion / Data-Needed Planning

You are working in the SAFE-FAST local repo.

Repo source of truth:
C:\Users\nickm\Desktop\New folder\safe-fast-backendnew

Branch:
main

Checkpoint:
021bead Add Day 46 grouped backtest batch decision

Today:
June 18, 2026
Project Day 47

## Hard rules

- Read SAFE_FAST_BUILD_STATE.md first.
- Do not touch main.py.
- Do not touch Railway, production, broker, order, account, credentials, .env, or secrets.
- Do not download raw Databento data.
- Do not make any Databento request.
- Do not run a new backtest.
- Do not patch live trading logic.
- Do not change frozen baseline logic.
- Keep this as a planning / comparison / data-needed package only.
- Use batching. Do not return to one-example loops.
- If repo docs disagree, stop and report the conflict.
- Every changed file must be documentation or task/planning only unless a stronger repo instruction already exists.

## Read first

Read these files in this order:

1. SAFE_FAST_BUILD_STATE.md
2. SAFE_FAST_PROJECT_DASHBOARD.md
3. SAFE_FAST_PROJECT_RULE_INDEX.md
4. SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt
5. SAFE_FAST_DAY46_NEXT_GROUPED_BACKTEST_BATCH_DECISION.md
6. SAFE_FAST_DAY46_NEXT_CHAT_HANDOFF_START_HERE.md, background only because it may be stale
7. Candidate packets changed by commit 021bead:
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CONTINUATION_001.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_IDEAL_001.md
   - historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_002.md
   - historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_003.md
   - historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CONTINUATION_001.md
   - historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_IDEAL_001.md

Also search the repo for latest committed grouped task, grouped decision, cost-check, replay, backtest, or intake files that are directly referenced by those docs.

## Known current state to preserve

The first real Clean Fast Break backtest reference ran.

- SPY Clean Fast Break 002 hit the profit target.
- Entry was 6.37.
- Adjusted exit was 7.98.
- Adjusted result was +1.61.
- SPY Clean Fast Break 003 stayed out because its option quote came after the signal.
- QQQ Clean Fast Break 001 stayed out because its option quote was too old.

This is one useful positive reference, not enough to trust the whole plan.

## Objective

Create the next grouped expansion / data-needed planning package.

The package must:

1. Review the first CFB backtest result without treating it as proof.
2. Compare SPY CFB 002, SPY CFB 003, and QQQ CFB 001 as a grouped result:
   - positive tradable reference
   - quote-after-signal no-entry reference
   - stale-quote no-entry reference
3. Compare what is currently known across:
   - Clean Fast Break
   - Ideal
   - Continuation
4. Decide the next grouped candidate batch needed for broader comparison.
5. Identify exact data-needed categories before any Databento request.
6. Keep data spending controlled.
7. Build toward the Day 60 decision package.
8. Preserve no-trade discipline.

## Required output files

Create or update only these files unless the repo docs prove a different exact file is required:

1. SAFE_FAST_DAY47_GROUPED_CFB_EXPANSION_DATA_NEEDED_PLAN.md

This file must include:

- Baseline
- Fixed
- Still unproven
- Active build objective
- Grouped comparison table:
  - SPY CFB 002
  - SPY CFB 003
  - QQQ CFB 001
  - SPY Ideal 001
  - QQQ Ideal 001
  - SPY Continuation 001
  - QQQ Continuation 001
- What the first positive CFB result supports
- What it does not prove
- Weak-result / no-entry diagnosis
- Next grouped candidate batch recommendation
- Data needed before backtest
- Cost-control rule
- Promotion blockers
- Day 60 decision-package relevance
- Exact next action

2. SAFE_FAST_DAY47_NEXT_GROUPED_DATA_NEEDED_COST_CHECK_CODEX_TASK.md

This must be a follow-up Codex task file only. It must not perform the cost check itself.

It must instruct the next Codex run to:

- Read SAFE_FAST_BUILD_STATE.md first.
- Read the Day 47 grouped data-needed plan.
- Identify exact Databento symbols/windows needed for the next grouped batch.
- Cost-check the grouped batch before download.
- Print the exact checked price.
- Require user approval before any full-window download unless the checked cost is clearly tiny.
- Keep raw Databento files local and ignored.
- Do not download data unless the task has explicit approval language.
- Do not touch live/production/broker/order/account/Railway/.env/secrets/main.py.

3. Update SAFE_FAST_PROJECT_DASHBOARD.md only if needed to point to the Day 47 plan and next task.

4. Update SAFE_FAST_BUILD_STATE.md only if needed to record that the active next package has moved from Day 46 grouped decision review to Day 47 grouped data-needed cost-check planning.

5. Update SAFE_FAST_PROJECT_RULE_INDEX.md only if needed to preserve discoverability of the new Day 47 plan/task.

## Tests / checks

Run:

1. .\scripts\safe_fast_run_safe_checks.ps1
2. python -m watcher_foundation.source_evidence_work_package_content_validator
3. python -m watcher_foundation.source_evidence_package_to_intake_bridge

If a test is impossible because the environment is missing something, report that directly and do not fake a pass.

## Final response format

Respond in plain English using exactly:

Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:

Do not push.
Do not create a commit.
