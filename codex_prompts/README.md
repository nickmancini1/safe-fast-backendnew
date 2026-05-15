# Codex Prompts

Store local Codex prompt files here when using `tools/safe_fast_codex_task.ps1`.

Example:

```powershell
powershell -ExecutionPolicy Bypass -File tools/safe_fast_codex_task.ps1 codex_prompts\example_task.md
```

The helper copies the prompt file to the clipboard, opens Codex interactively from the repo root, and waits for you to paste with `Ctrl+V`, then press `Enter`.
