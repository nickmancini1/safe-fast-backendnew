# SAFE-FAST Chat Kill Switch

Purpose:
Protect Nick's time.

Stop using the chat if any of these happen:
- two clear mistakes
- one unsafe file-changing command
- one broad Codex task
- one missing paste-back block
- one hidden error
- one false claim
- one command that makes Nick hunt through huge output
- one live, broker, or vendor action outside scope
- one refusal to plainly admit a chat-caused mistake

The chat must not argue with this rule.

The chat must not claim work is done unless there is:
- required result
- required tests
- commit proof if files changed
- clean Git status

## Tightening addendum

Guardrail-break rule:
If a chat breaks these guardrails while doing guardrail or recovery work, that counts as a clear mistake.

Serious mistakes include:
- closing Nick's terminal with a bad command
- giving a giant fragile script after being told not to
- leaving the repo dirty after promising a commit and clean status
- hiding the exact failure
- continuing after the kill-switch rule says to stop
