# SAFE-FAST Day 46 handoff and next-chat start task

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.
- Then read SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt.
- Then read SAFE_FAST_DAY45_BOUNDED_FINAL_SPRINT_UPDATE.md.
- Then read SAFE_FAST_DAY45_200_TO_20_TIER_TRANSITION_PLAN.md.
- Then read SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_WITH_EXIT_PATH_RESULT.md.
- Then read SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_WITH_EXIT_PATH_REVIEW.md.

Goal:
- Create a committed repo handoff for the next chat.
- Make the next chat able to start without the user holding its hand.
- Put the current state, next work, communication rules, PowerShell/Codex workflow, budget controls, batching rule, and final sprint framing in one obvious place.
- This is a handoff/control task only.
- Do not download data.
- Do not run new backtests.
- Do not calculate new P&L.
- Do not change trading/live/deploy files.

Known current checkpoint:
- Latest known commit before this handoff: 59b2a03 Run first CFB backtest reference case.
- Local git output still controls if it differs.

Known first actual CFB backtest result:
- Candidate: SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002.
- Result: completed profit target.
- Entry: 6.37.
- Adjusted exit: 7.98.
- Adjusted result: +1.61.
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003 stayed out because quote came after signal.
- QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001 stayed out because quote was too old.
- Meaning: one useful positive reference plus two rejection controls.
- Do not overreact to one good example.
- Next work is grouped comparison/expansion.

Day/timeline rules:
- Day 1 is May 3, 2026.
- June 16, 2026 was Day 45.
- June 17, 2026 is Day 46.
- Day 60 is July 1, 2026.
- Day 60 is a checkpoint/reporting date.
- Day 60 does not force rushed proof.
- The build must be correct.
- The project must also be bounded.
- The next  month is the final high-intensity build sprint before moving toward the  tier.
- The final sprint must produce a decision package.

Communication rules for future chats:
- Use plain English.
- Direct answer first.
- Do not make the user decode project jargon.
- Avoid filler.
- Avoid repeating long safety disclaimers to the user.
- Avoid user-facing “not/not/not” recaps unless a direct refusal/safety boundary is actually needed.
- Explain what changed, what it means, and the next action.
- The default format for build work:
  - Baseline:
  - Fixed:
  - Blocked:
  - Next:
  - Command:
- If the user asks a simple yes/no/I-don’t-know question, answer that first.
- Do not talk around timeline, cost, or uncertainty.

PowerShell/Codex workflow:
- Local repo output controls.
- Start every new chat with git status/log/branch check.
- Repo path:
  - C:\Users\nickm\Desktop\New folder\safe-fast-backendnew
- Branch expected:
  - main
- Use PowerShell and local Codex task files.
- Use Codex command:
  - codex.cmd -c 'windows.sandbox="unelevated"' --sandbox workspace-write --ask-for-approval never
- Do not pass huge prompts directly on the command line.
- Write a task file first.
- Then launch Codex against the task file.
- User pastes Codex output.
- Review output.
- Commit guarded checkpoints.
- Do not push unless user explicitly asks.
- If Codex transport/WebSocket/backend errors repeat, stop, restart laptop, reopen PowerShell, verify git, and resume with a small bounded task.

Budget/data rules:
- Cheap starter data first.
- Full-window Databento data only after exact cost check and user approval.
- No broad data download from guesses.
- Known cost warning: SPY 3-candidate full-window cost check was about .36. Record this clearly. 
- Databento starter data is local-only and raw vendor files should stay ignored.
- If Databento key ever appears in output, tell the user to rotate it.

Batching rule:
- Batching/grouped progress is already the rule.
- Future chats must follow it.
- Use grouped candidate passes, grouped rule packages, grouped validation, grouped cost checks, and grouped comparison.
- Avoid one-field loops unless a real blocker makes batching unsafe.
- If a blocker appears, batch the diagnosis where possible.

Current build status to preserve:
- Evidence cleanup reached 9 passed / 0 failed after SPY Ideal batch.
- First CFB backtest reference case ran.
- SPY CFB 002 is the first positive reference.
- SPY CFB 003 is a quote-after-signal no-trade control.
- QQQ CFB 001 is a stale-quote no-trade control.
- Intake-ready remains 0 until the readiness gate supports more.
- Current work is moving from first reference case into grouped comparison/expansion.

Create these repo artifacts:
- SAFE_FAST_DAY46_NEXT_CHAT_HANDOFF_START_HERE.md
- SAFE_FAST_DAY46_NEXT_CHAT_START_BLOCK.txt
- SAFE_FAST_DAY46_HANDOFF_CURRENT_STATE_AND_FINAL_SPRINT_PLAN.md
- SAFE_FAST_DAY46_HANDOFF_POWER_SHELL_CODEX_WORKFLOW.md

Update these front-door files:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt

The handoff must include:
1. Exact latest known checkpoint and instruction that local git controls.
2. Plain-English project status.
3. First CFB backtest result.
4. What the result means.
5. What the next chat should do first.
6. Exact PowerShell command for the next chat to request from the user.
7. Exact Codex workflow.
8. Budget/data rule.
9. Batching rule.
10. Final sprint / -to- transition rule.
11. Communication rules.
12. Next grouped task recommendation.

Create the next-chat start block as copy/paste text for a new chat.
It should begin:

"Start here. You are continuing SAFE-FAST build work. Use local git as source of truth. Speak plain English. Day 46 context: first CFB backtest reference ran; SPY CFB 002 hit target with adjusted result +1.61; SPY CFB 003 and QQQ CFB 001 stayed out correctly. Day 60 is a checkpoint, not a forced finish. The next  month is the final high-intensity sprint before moving toward the  tier. Work must stay batched, cost-controlled, and evidence-backed."

Then it should tell the next chat to ask for:

Set-Location "C:\Users\nickm\Desktop\New folder\safe-fast-backendnew"
git --no-pager branch --show-current
git --no-pager log -1 --oneline
git --no-pager status --short

Recommended next grouped task:
- Review first CFB backtest result.
- Build grouped expansion plan.
- Compare SPY CFB 002, SPY CFB 003, QQQ CFB 001.
- Decide the next batch across CFB, Ideal, and Continuation without one-example grinding.
- Use SAFE_FAST_DAY46_FIRST_BACKTEST_REVIEW_AND_EXPANSION_PLAN_CODEX_TASK.md if present, or create a fresh grouped review/expansion task if local git says it is missing.

Run checks:
- powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
- content validator if safe/local
- bridge if safe/local

Allowed writes:
- SAFE_FAST_DAY46_HANDOFF_AND_NEXT_CHAT_START_CODEX_TASK.md
- SAFE_FAST_DAY46_NEXT_CHAT_HANDOFF_START_HERE.md
- SAFE_FAST_DAY46_NEXT_CHAT_START_BLOCK.txt
- SAFE_FAST_DAY46_HANDOFF_CURRENT_STATE_AND_FINAL_SPRINT_PLAN.md
- SAFE_FAST_DAY46_HANDOFF_POWER_SHELL_CODEX_WORKFLOW.md
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt

Excluded writes:
- raw Databento files
- evidence fills
- backtest code
- P&L changes beyond summarizing existing result
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
