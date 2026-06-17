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
