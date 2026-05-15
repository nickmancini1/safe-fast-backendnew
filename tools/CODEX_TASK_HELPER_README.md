# SAFE-FAST Codex Task Helper

`tools/safe_fast_codex_task.ps1` is a local workflow helper for starting Codex with a prepared prompt.

## Usage

```powershell
powershell -ExecutionPolicy Bypass -File tools/safe_fast_codex_task.ps1 codex_prompts\my_task.md
```

For help:

```powershell
powershell -ExecutionPolicy Bypass -File tools/safe_fast_codex_task.ps1 -Help
```

## Behavior

- Runs from the SAFE-FAST repo root: `%USERPROFILE%\Desktop\safe-fast-backendnew`
- Checks `git status --short`
- Stops if the working tree is dirty
- Prints the latest local commit
- Copies the prompt file contents to the clipboard
- Opens Codex interactively with:

```powershell
codex.cmd -C "$env:USERPROFILE\Desktop\safe-fast-backendnew" -s workspace-write -a on-request
```

After Codex opens, press `Ctrl+V`, then `Enter`.

## Non-Interactive Codex Note

`codex.cmd --help` documents non-interactive support through `codex exec` and also shows an optional `[PROMPT]` argument for starting a session. This helper intentionally does not submit prompts non-interactively yet.

## Scope

This helper is workflow-only. It does not change engine code, trading logic, replay logic, backtesting logic, schemas, fixtures, reports, or deployment files.
