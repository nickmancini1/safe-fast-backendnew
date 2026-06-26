$ErrorActionPreference = "Stop"

$scriptPath = $MyInvocation.MyCommand.Path
$scriptDir = Split-Path -Parent $scriptPath
$repoRoot = Split-Path -Parent $scriptDir
Set-Location $repoRoot

$buildStatePath = Join-Path $repoRoot "SAFE_FAST_BUILD_STATE.md"
$handoffPath = "SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md"
$introPath = "SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt"
$operatingLoopPath = "SAFE_FAST_SOURCE_TO_DECISION_OPERATING_LOOP.md"

function Fail-Conflict {
    param([string]$Message)
    Write-Host "CONFLICT: $Message"
    exit 1
}

if (-not (Test-Path -LiteralPath $buildStatePath)) {
    Fail-Conflict "SAFE_FAST_BUILD_STATE.md is missing"
}

$buildState = Get-Content -LiteralPath $buildStatePath -Raw
$match = [regex]::Match(
    $buildState,
    '(?s)<!-- SAFE_FAST_CURRENT_STATE_BEGIN -->(.*?)<!-- SAFE_FAST_CURRENT_STATE_END -->'
)
if (-not $match.Success) {
    Fail-Conflict "SAFE_FAST current-state section is missing"
}

$fields = @{}
$sectionLines = $match.Groups[1].Value -split "`r?`n"
foreach ($line in $sectionLines) {
    if ($line -match '^\s*-\s*([A-Z_]+):\s*(.*)\s*$') {
        $fields[$matches[1]] = $matches[2].Trim()
    }
}

$requiredFields = @(
    "PROJECT_DAY",
    "PROJECT_DATE",
    "ACTIVE_OBJECTIVE",
    "ACTIVE_TASK",
    "ACTIVE_TASK_PURPOSE",
    "PROVEN_SUMMARY",
    "UNPROVEN_SUMMARY",
    "CURRENT_FUNNEL_TOTALS",
    "CURRENT_TECHNICAL_PACKAGE",
    "CURRENT_TECHNICAL_RESULT",
    "SCHWAB_STATUS",
    "DATA_SOURCE_REGISTRY",
    "NEXT_ACTION"
)

foreach ($field in $requiredFields) {
    if (-not $fields.ContainsKey($field) -or [string]::IsNullOrWhiteSpace($fields[$field])) {
        Fail-Conflict "Current-state field $field is missing"
    }
}

$activeTask = $fields["ACTIVE_TASK"]
$activeTaskPath = Join-Path $repoRoot $activeTask
$activeTaskExists = Test-Path -LiteralPath $activeTaskPath

$branch = (& git --no-pager branch --show-current).Trim()
$head = (& git --no-pager rev-parse --short HEAD).Trim()
$latestCommits = @(& git --no-pager log -3 --oneline)
$statusLines = @(& git --no-pager status --short -- . ":(exclude)tmp2i57tguu" ":(exclude)tmpj8ei9a_f" ":(exclude)tmpra392qh0" ":(exclude)tmpt2fw63vq")
if ($statusLines.Count -eq 0) {
    $statusText = "clean"
}
else {
    $statusText = "dirty ($($statusLines.Count) changed paths)"
}

Write-Host "SAFE_FAST_NEW_CHAT_STATUS"
Write-Host "PROJECT_DAY: $($fields["PROJECT_DAY"])"
Write-Host "PROJECT_DATE: $($fields["PROJECT_DATE"])"
Write-Host "BRANCH: $branch"
Write-Host "HEAD: $head"
Write-Host "LATEST_COMMITS:"
foreach ($commit in $latestCommits) {
    Write-Host "  $commit"
}
Write-Host "GIT_STATUS: $statusText"
Write-Host "CANONICAL_HANDOFF: $handoffPath"
Write-Host "CANONICAL_INTRO_BLOCK: $introPath"
Write-Host "CANONICAL_OPERATING_LOOP: $operatingLoopPath"
Write-Host "OPENING_REPORT_REQUIRED: Baseline; Active objective; Raw-data source; SAFE-FAST translation required; Blocker category; Candidate state; Next executable step; Why this is the fastest safe path; Required tests; Commit proof."
Write-Host "BLOCKER_CATEGORIES: RAW_DATA_GAP; RULE_DEFINITION_GAP; CALCULATOR_OR_IMPLEMENTATION_GAP; CANDIDATE_QUALITY_GAP; ECONOMIC_EVIDENCE_GAP; REGRESSION_OR_PROOF_GAP"
Write-Host "SOURCE_OWNERSHIP: Vendors provide evidence; SAFE-FAST provides labels and decisions."
Write-Host "ACTIVE_OBJECTIVE: $($fields["ACTIVE_OBJECTIVE"])"
Write-Host "ACTIVE_TASK: $activeTask"
Write-Host "ACTIVE_TASK_EXISTS: $activeTaskExists"
Write-Host "PROVEN_SUMMARY: $($fields["PROVEN_SUMMARY"])"
Write-Host "UNPROVEN_SUMMARY: $($fields["UNPROVEN_SUMMARY"])"
Write-Host "CURRENT_FUNNEL_TOTALS: $($fields["CURRENT_FUNNEL_TOTALS"])"
Write-Host "CURRENT_TECHNICAL_PACKAGE: $($fields["CURRENT_TECHNICAL_PACKAGE"])"
Write-Host "CURRENT_TECHNICAL_RESULT: $($fields["CURRENT_TECHNICAL_RESULT"])"
Write-Host "SCHWAB_STATUS: $($fields["SCHWAB_STATUS"])"
Write-Host "NEXT_ACTION: $($fields["NEXT_ACTION"])"
Write-Host "FREEZE_RULE: If PowerShell stops progressing, press Ctrl+C once. Do not rerun. First inspect logs, partial files, output, manifest, and Git status."
Write-Host "FREEZE_RECOVERY: First determine whether PowerShell is waiting for hidden input; if not, press Ctrl+C once; do not assume success or failure; inspect process status, logs, partial files, output, manifest, sizes, hashes, parseability, and Git status; rerun only for a specific verified missing or failed result; never repeat a paid request or completed schema merely because output was quiet."

if (-not $activeTaskExists) {
    Fail-Conflict "Active task is missing: $activeTask"
}

exit 0
