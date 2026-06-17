# SAFE-FAST Day 46 PowerShell And Codex Workflow

## First Command For A New Chat

Ask the user to run:

```powershell
Set-Location "C:\Users\nickm\Desktop\New folder\safe-fast-backendnew"
git --no-pager branch --show-current
git --no-pager log -1 --oneline
git --no-pager status --short
```

Local git output controls. If it differs from this handoff, trust local git and then reconcile the docs.

## Required Reading Order

1. `SAFE_FAST_BUILD_STATE.md`
2. `SAFE_FAST_PROJECT_DASHBOARD.md`
3. `SAFE_FAST_PROJECT_RULE_INDEX.md`
4. `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`
5. `SAFE_FAST_DAY46_NEXT_CHAT_HANDOFF_START_HERE.md`
6. Relevant candidate packets in `historical_signal_replay/candidate_packets/`

## Codex Workflow

Use PowerShell and local task files.

Do not pass huge prompts directly on the command line. Write a task file first, then launch Codex against the task file.

Codex command:

```powershell
codex.cmd -c 'windows.sandbox="unelevated"' --sandbox workspace-write --ask-for-approval never
```

Working pattern:

1. Create or update a bounded task file.
2. Run Codex against that task file.
3. User pastes Codex output.
4. Review the output against repo state.
5. Run safe local checks when appropriate.
6. Commit guarded checkpoints.
7. Do not push unless the user explicitly asks.

If repeated Codex transport, WebSocket, or backend errors appear, stop and restart the laptop, reopen PowerShell, verify git, and resume with a small bounded task.

## Safe Checks

Use:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
python -m watcher_foundation.source_evidence_work_package_content_validator
python -m watcher_foundation.source_evidence_package_to_intake_bridge
```

Only run checks that are safe and local for the current task. Do not run new backtests unless explicitly authorized.

## Communication Format

Use plain English. Direct answer first.

Default build-work format:

```text
Baseline:
Fixed:
Blocked:
Next:
Command:
```

Explain what changed, what it means, and the next action. Be direct about timeline, cost, and uncertainty.

## Guardrails

- Do not download data without explicit approval.
- Do not run broad Databento downloads.
- Full-window Databento data requires exact cost check and user approval.
- Known cost warning: SPY 3-candidate full-window cost check was about `$72.36`.
- Do not run new backtests unless the task explicitly authorizes it.
- Do not calculate new P&L unless the task explicitly authorizes it.
- Do not change `main.py`, live, engine, broker, order, account, Railway, `.env`, secrets, raw Databento files, generated live reports/logs, or P&L files.

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

