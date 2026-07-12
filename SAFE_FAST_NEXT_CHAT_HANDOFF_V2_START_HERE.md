# SAFE-FAST Next Chat Handoff — V2

## Read this first

This handoff is designed not to become stale.

The user says the project is at the end of Day 70. The exact technical state must come from the user’s local repository. GitHub may be behind. Do not use an older Day 55, Day 68, or other historical section as the current state merely because it appears in a file.

Use GPT-5.6 Pro for this work.

Read `SAFE_FAST_PROJECT_INSTRUCTIONS_V2.txt` before doing anything else.

## First rule

The local repository wins over GitHub, old handoffs, saved chat memory, and assumptions.

Do not ask the user to explain the project again.

Do not choose a task until the compact local status is available in the current chat.

If fresh compact status is already in the current chat, use it. Do not ask for it again.

## First response format

Before any explanation or command, write these four plain lines:

Priority check: YES or NO.
Current priority: one simple sentence.
This step is: Substance or busy work.
Why allowed: one simple sentence.

If the priority check is NO, stop and correct course.

Use simple English. Avoid jargon. Give one action at a time.

Do not use a code block, quote block, table, or boxed text unless the user must copy and paste its contents.

## Compact startup status

When fresh local status is not already present, ask the user to paste only this:

```powershell
Set-Location "C:\Users\nickm\Desktop\New folder\safe-fast-backendnew"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\safe_fast_new_chat_status_compact.ps1"
```

Put the label `PASTE INTO POWERSHELL` directly above that block.

The compact script must return no more than these items:

- current project day;
- branch;
- HEAD;
- clean or dirty Git status;
- active task;
- active objective;
- current result;
- next action.

Do not ask for a full build-state file, full Git log, full JSON file, registry dump, or broad search output.

## After status is returned

State the baseline in simple English.

Resolve conflicts this way:

1. Fresh local compact status.
2. Current machine-readable result named by that status.
3. Current local build-state block.
4. GitHub.
5. Historical handoffs.

Never move down this list when a higher source already answers the question.

If local status says the work is terminal, the source is exhausted, or no valid next action exists, say that plainly and stop. Do not invent work.

If local status shows a valid active task, give the smallest step that directly advances that task.

## PowerShell output rules

Every command must be obvious to copy.

When the user must paste a command:

- write `PASTE INTO POWERSHELL` immediately above the block;
- put only the command inside the block;
- use one block per reply unless two are truly required;
- keep the block at 8 lines or fewer and 1,200 characters or fewer;
- prefer one or two commands;
- never send a large inline script, base64 payload, huge here-string, or full file contents;
- make output bounded to 3–8 decisive lines;
- print `=== COPY BACK ===` before the requested output and `=== END COPY BACK ===` after it.

When output would be long, have the command write it to a file and ask the user to attach the file. Do not make the user paste a giant terminal transcript.

Never use a broad text search across current and historical sections when an exact file, marker, field, or result is known.

## Open Codex in PowerShell

Use ordinary, non-Administrator PowerShell unless elevated access is specifically required and explained.

When Codex is needed, give exactly this:

```powershell
Set-Location "C:\Users\nickm\Desktop\New folder\safe-fast-backendnew"
codex.cmd --sandbox workspace-write -c 'windows.sandbox="unelevated"'
```

Put the label `PASTE INTO POWERSHELL` directly above that block.

Do not replace `codex.cmd` with `codex` unless the user asks.

After Codex opens, give the user one sealed task to paste into Codex. Put the label `PASTE INTO CODEX` above that block. The sealed task must contain:

- one objective;
- exact files Codex may change;
- work Codex must not do;
- exact tests;
- the done condition;
- whether commit is allowed;
- the required final proof.

Do not put explanation inside the paste block.

## Safety and time protection

Do not repeat a completed download, paid request, test batch, Codex task, or vendor call merely because output was quiet.

If a command appears stuck:

1. check whether it is waiting for input;
2. if not, press Ctrl+C once;
3. do not rerun;
4. inspect the existing log, partial output, expected file, and Git status with one small read-only command.

No paid data, vendor call, download, credential use, broker action, order, or live change without clear user approval.

Never claim success from an echoed label or a chat statement. Check the real file, tests, commit, and Git status.

## End-of-Day-70 warning

The only safe fixed fact in this handoff is that the user says this is the end of Day 70.

Do not treat the previously seen Day 68 terminal source result as the current Day 70 state unless the fresh local status confirms it.

Do not revive Day 55 SPY 670C or any other old task unless the fresh local status explicitly makes it current.

## Completion standard

A valid response either:

- advances the current active task with one small, direct action;
- asks for required approval;
- or closes the exact blocker and stops.

It must not create busy work merely to keep the conversation moving.
