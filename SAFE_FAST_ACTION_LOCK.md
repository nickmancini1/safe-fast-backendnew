# SAFE-FAST Action Lock

Purpose:
Stop the chat from doing whatever it wants.

No command is allowed unless the action is sealed first.

Every command must state:
- command type
- exact goal
- exact files allowed
- exact files forbidden
- allowed actions
- forbidden actions
- done condition
- stop condition
- required tests
- commit proof if files change
- clean status proof

Command types:
- read-only: checks files only
- this can change files: creates, edits, stages, or commits named files only
- vendor/paid: calls or prepares a paid/vendor request
- dangerous/destructive: deletes, resets, overwrites broadly, touches credentials, touches broker APIs, or affects live systems

Dangerous/destructive commands are forbidden unless Nick explicitly approves them in plain English.

Hard stops:
- no files outside the sealed file list
- no broad cleanup
- no Railway unless Nick explicitly says to
- no live backend unless Nick explicitly says to
- no Schwab unless Nick explicitly approves it and the current task says Schwab is in scope
- no paid Databento unless cost and scope are approved first
- no candidate work while replay work is active
- no proof claim without tests, commit proof, and clean Git status

## Tightening addendum

Pre-change gate:
Before any command that can change files, the command must first verify the repo folder, branch, clean status, active task when needed, and allowed dirty files during recovery.
If any check fails, stop before changing files.

Small-command rule:
Use one-purpose PowerShell blocks.
Do not use giant fragile scripts when a smaller step can do the job.

Codex sealed-ticket rule:
No Codex task is allowed unless the ticket states one objective, exact files, forbidden work, tests, done condition, commit proof, and clean status proof.

Build-state rule:
Before any Codex or code task, read `SAFE_FAST_BUILD_STATE.md` first.
If `SAFE_FAST_BUILD_STATE.md` is missing, stop before touching engine logic.

No terminal-closing rule:
Do not use `exit` in Nick's PowerShell commands unless Nick explicitly approves it in plain English.
