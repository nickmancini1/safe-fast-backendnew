param(
    [Parameter(Position = 0)]
    [string]$PromptFile,

    [switch]$Help
)

$ErrorActionPreference = "Stop"

$RepoRoot = Join-Path $env:USERPROFILE "Desktop\safe-fast-backendnew"

function Show-Help {
    Write-Host "SAFE-FAST Codex task helper"
    Write-Host ""
    Write-Host "Usage:"
    Write-Host "  powershell -ExecutionPolicy Bypass -File tools/safe_fast_codex_task.ps1 <prompt-file>"
    Write-Host "  powershell -ExecutionPolicy Bypass -File tools/safe_fast_codex_task.ps1 -Help"
    Write-Host ""
    Write-Host "What it does:"
    Write-Host "  - Checks git status --short from the SAFE-FAST repo root."
    Write-Host "  - Stops if the working tree is dirty."
    Write-Host "  - Prints the latest local commit."
    Write-Host "  - Copies the prompt file contents to the clipboard."
    Write-Host "  - Opens Codex interactively from the repo root."
    Write-Host ""
    Write-Host "After Codex opens, press Ctrl+V, then Enter."
}

if ($Help) {
    Show-Help
    exit 0
}

if ([string]::IsNullOrWhiteSpace($PromptFile)) {
    Show-Help
    exit 1
}

if (-not (Test-Path -LiteralPath $RepoRoot -PathType Container)) {
    throw "Repo root not found: $RepoRoot"
}

Push-Location $RepoRoot
try {
    $Status = git status --short
    if ($Status) {
        Write-Host "Working tree is dirty. Stop before opening Codex."
        Write-Host ""
        $Status | ForEach-Object { Write-Host $_ }
        exit 1
    }

    $LatestCommit = git log -1 --oneline
    Write-Host "Latest commit: $LatestCommit"

    $ResolvedPromptFile = Resolve-Path -LiteralPath $PromptFile
    $PromptText = Get-Content -LiteralPath $ResolvedPromptFile -Raw
    Set-Clipboard -Value $PromptText

    Write-Host "Copied prompt to clipboard: $ResolvedPromptFile"
    Write-Host "Opening Codex from: $RepoRoot"
    Write-Host "Inside Codex, press Ctrl+V, then Enter."

    & codex.cmd -C "$env:USERPROFILE\Desktop\safe-fast-backendnew" -s workspace-write -a on-request
}
finally {
    Pop-Location
}
