# SAFE-FAST Day 46 Next Chat Handoff - Start Here

## Direct Answer

Start the next chat from local git, not memory. Local git is the source of truth if it differs from this handoff.

Latest known checkpoint when this handoff was created:

- Branch: `main`.
- Latest known local HEAD before committing this handoff: `59b2a03 Run first CFB backtest reference case`.
- Existing Day 46 review/expansion work was present locally before this handoff commit.
- Local git output controls.

## Plain-English Status

SAFE-FAST has its first useful Clean Fast Break reference result, but it is only one example. It is not proof, it is not a profitability claim, it is not a promotion decision, and it does not make any candidate ready.

The current state is:

- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` is the first positive CFB reference.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` is still a no-trade control because its quote came after the signal.
- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` is still a no-trade control because its quote was older than 5 minutes.
- Evidence cleanup reached `9` passed requests and `0` failed requests after the SPY Ideal batch.
- Intake-ready remains `0`.
- The project is moving from one reference result into grouped comparison and expansion.

## First CFB Backtest Result

The first actual CFB backtest reference was `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`.

- Result: completed profit target.
- Entry basis: `6.37`.
- Adjusted exit basis: `7.98`.
- Cost/slippage-adjusted result: `+1.61`.
- Exit reason: `profit_target`.

Meaning: this is one useful positive reference plus two rejection controls. Do not overreact to one good example. The next work is grouped comparison and expansion.

## What The Next Chat Should Do First

Ask the user to run this in PowerShell:

```powershell
Set-Location "C:\Users\nickm\Desktop\New folder\safe-fast-backendnew"
git --no-pager branch --show-current
git --no-pager log -1 --oneline
git --no-pager status --short
```

Then read, in order:

1. `SAFE_FAST_BUILD_STATE.md`
2. `SAFE_FAST_PROJECT_DASHBOARD.md`
3. `SAFE_FAST_PROJECT_RULE_INDEX.md`
4. `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`
5. `SAFE_FAST_DAY46_NEXT_CHAT_START_BLOCK.txt`

## Communication Rules

- Use plain English.
- Direct answer first.
- Do not make the user decode project jargon.
- Avoid filler.
- Avoid long safety disclaimers unless a direct boundary is needed.
- Explain what changed, what it means, and the next action.
- For build work, use:
  - `Baseline:`
  - `Fixed:`
  - `Blocked:`
  - `Next:`
  - `Command:`
- If the user asks yes/no/I-don't-know, answer that first.
- Be clear about timeline, cost, and uncertainty.

## PowerShell And Codex Workflow

- Repo path: `C:\Users\nickm\Desktop\New folder\safe-fast-backendnew`.
- Expected branch: `main`.
- Use PowerShell.
- Use local Codex task files.
- Do not pass huge prompts directly on the command line.
- Write a task file first.
- Then launch Codex against that task file.
- User pastes Codex output.
- Review output.
- Commit guarded checkpoints.
- Do not push unless the user explicitly asks.

Codex launch command:

```powershell
codex.cmd -c 'windows.sandbox="unelevated"' --sandbox workspace-write --ask-for-approval never
```

If Codex transport, WebSocket, or backend errors repeat: stop, restart the laptop, reopen PowerShell, verify git, and resume with a small bounded task.

## Budget And Data Rules

- Cheap starter data first.
- Full-window Databento data only after exact cost check and user approval.
- Do not broad-download data from guesses.
- Known cost warning: the SPY 3-candidate full-window cost check was about `$72.36`.
- Databento starter data is local-only and raw vendor files should stay ignored.
- If a Databento key appears in output, tell the user to rotate it.

## Batching Rule

Batching is already the rule.

Future chats must use grouped candidate passes, grouped rule packages, grouped validation, grouped cost checks, and grouped comparison. Avoid one-field loops unless a real blocker makes batching unsafe. If a blocker appears, batch the diagnosis where possible.

## Day 60 And Tier Transition

- Day 1: May 3, 2026.
- Day 45: June 16, 2026.
- Day 46: June 17, 2026.
- Day 60: July 1, 2026.
- Day 60 is a checkpoint and reporting date, not a forced finish.
- The build must be correct.
- The project must also be bounded.
- The next `$200` month is the final high-intensity build sprint before moving toward the `$20` tier.
- The final sprint must produce a decision package.

The decision package should say what works, what failed, what needs repair, what data costs remain, strongest and weakest candidate families, accepted and missing rules, what can continue on the `$20` tier, and what would require another serious spend or redesign.

## Recommended Next Grouped Task

Recommended next task:

- Review the first CFB backtest result.
- Build a grouped expansion plan.
- Compare `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`, `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`, and `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.
- Decide the next batch across CFB, Ideal, and Continuation without one-example grinding.
- Use `SAFE_FAST_DAY46_FIRST_BACKTEST_REVIEW_AND_EXPANSION_PLAN_CODEX_TASK.md` if present, or create a fresh grouped review/expansion task if local git says it is missing.

## Guardrails

- Do not download data.
- Do not run new backtests unless a later task explicitly authorizes it.
- Do not calculate new P&L.
- Do not change `main.py`.
- Do not touch live, engine, broker, order, account, Railway, `.env`, secrets, raw Databento files, evidence fills, backtest code, or P&L files.

## Day 46 handoff correction: prompt discipline and Codex transport failure

This correction exists because a new chat mishandled the Day 46 handoff and produced a bad first Codex attempt.

Future chats must follow this exactly:

1. Do not invent generic task files such as TASK_DAY46_GROUPED_BACKTEST_BATCH_REVIEW.md.

2. Use the task files already committed in the repo unless local git proves they are missing.

3. After checkpoint 239692f Add Day 46 first backtest expansion plan, the expected next grouped task is:
   SAFE_FAST_DAY46_NEXT_GROUPED_BACKTEST_BATCH_TASK.md

4. If that file exists, launch Codex with exactly this command:

   codex.cmd -c 'windows.sandbox="unelevated"' --sandbox workspace-write --ask-for-approval never "Read and execute .\SAFE_FAST_DAY46_NEXT_GROUPED_BACKTEST_BATCH_TASK.md exactly."

5. If the expected task file does not exist, create a proper SAFE_FAST_..._CODEX_TASK.md task file first.

6. Do not pass a huge task prompt directly into Codex as command-line text.

7. Do not create random task names.

8. Do not make the user correct the prompt format.

Correct PowerShell/Codex workflow:

Step 1:
Give the user one PowerShell block that writes the task file.

Step 2:
Stop.

Step 3:
After the user confirms the task file exists, give the Codex launch line separately.

Step 4:
User pastes Codex final output.

Step 5:
Review output and give guarded commit commands.

Correct startup check for the next chat:

   Set-Location "C:\Users\nickm\Desktop\New folder\safe-fast-backendnew"
   git --no-pager branch --show-current
   git --no-pager log -1 --oneline
   git --no-pager status --short

Expected checkpoint:
   main
   239692f Add Day 46 first backtest expansion plan
   clean status

If Codex shows WebSocket fallback failure, HTTPS fallback failure, backend-api/codex/responses 404, or repeated reconnect failure:

- Say plainly: Codex connection failed; repo is not the problem.
- Stop retrying the same Codex run.
- Ask only for git branch/log/status.
- Do not create new project tasks while Codex transport is failing.
- Do not tell the user to delete the chat as the first solution.

Plain English current state:

- First real CFB backtest reference ran.
- SPY CFB 002 hit the profit target.
- Adjusted result was +1.61.
- SPY CFB 003 stayed out because quote came after the signal.
- QQQ CFB 001 stayed out because quote was too old.
- Next work is grouped expansion/comparison.
- Do not grind one example.
- Do not invent new task names.

Next intended work:

Use SAFE_FAST_DAY46_NEXT_GROUPED_BACKTEST_BATCH_TASK.md if present.
If missing, create a fresh SAFE_FAST_DAY46_... grouped review/expansion task file first.
Keep batching.
Keep cost control.
Use plain English.

## End Day 46 handoff correction

