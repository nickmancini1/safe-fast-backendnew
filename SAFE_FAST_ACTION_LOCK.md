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
