# SAFE-FAST Paste-Back Contract

Purpose:
Nick should never have to hunt through huge output.

Every PowerShell or Codex task must end with exactly this small block:

=== PASTE BACK TO CHAT ===
ACTION:
RESULT:
COMMIT:
TESTS:
STATUS:
=== END PASTE BACK ===

Rules:
- Ask Nick to paste only that block.
- Long logs go to files.
- Failed tests print only a short failure summary, log path, and status.
- No giant terminal walls unless Nick explicitly asks.
- Do not hide errors.
- Do not continue from partial output without saying what is missing.

## Tightening addendum

Partial-output rule:
If output is partial, ask only for the missing lines.
Do not ask Nick to rerun the whole command unless there is a specific reason.

Tiny-output rule:
The paste-back block must be the only output Nick needs to copy.
If a command cannot produce a tiny paste-back block, the command is not ready.
