$ErrorActionPreference = "Stop"

function Convert-ToCompactLine {
    param(
        [AllowNull()][string]$Value,
        [int]$MaximumLength = 240
    )

    if ($null -eq $Value) {
        return ""
    }

    $oneLine = ($Value -replace '\s+', ' ').Trim()
    if ($oneLine.Length -le $MaximumLength) {
        return $oneLine
    }

    return $oneLine.Substring(0, $MaximumLength - 3) + "..."
}

try {
    $scriptPath = $MyInvocation.MyCommand.Path
    $scriptDir = Split-Path -Parent $scriptPath
    $repoRoot = Split-Path -Parent $scriptDir
    Set-Location $repoRoot

    $buildStatePath = Join-Path $repoRoot "SAFE_FAST_BUILD_STATE.md"
    if (-not (Test-Path -LiteralPath $buildStatePath)) {
        throw "SAFE_FAST_BUILD_STATE.md is missing."
    }

    $buildState = Get-Content -LiteralPath $buildStatePath -Raw
    $stateMatch = [regex]::Match(
        $buildState,
        '(?s)<!-- SAFE_FAST_CURRENT_STATE_BEGIN -->(.*?)<!-- SAFE_FAST_CURRENT_STATE_END -->'
    )
    if (-not $stateMatch.Success) {
        throw "The current-state section is missing from SAFE_FAST_BUILD_STATE.md."
    }

    $fields = @{}
    foreach ($line in ($stateMatch.Groups[1].Value -split "`r?`n")) {
        if ($line -match '^\s*-\s*([A-Z_]+):\s*(.*)\s*$') {
            $fields[$matches[1]] = $matches[2].Trim()
        }
    }

    $requiredFields = @(
        "PROJECT_DAY",
        "ACTIVE_TASK",
        "ACTIVE_OBJECTIVE",
        "CURRENT_TECHNICAL_RESULT",
        "NEXT_ACTION"
    )
    foreach ($field in $requiredFields) {
        if (-not $fields.ContainsKey($field) -or [string]::IsNullOrWhiteSpace($fields[$field])) {
            throw "Current-state field $field is missing."
        }
    }

    $branch = (& git --no-pager branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "Git could not read the current branch."
    }
    if ([string]::IsNullOrWhiteSpace($branch)) {
        $branch = "DETACHED_HEAD"
    }

    $head = (& git --no-pager rev-parse --short HEAD).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "Git could not read HEAD."
    }

    $statusLines = @(& git --no-pager status --short -- . ":(exclude)tmp2i57tguu" ":(exclude)tmpj8ei9a_f" ":(exclude)tmpra392qh0" ":(exclude)tmpt2fw63vq")
    if ($LASTEXITCODE -ne 0) {
        throw "Git could not read repository status."
    }
    $gitStatus = if ($statusLines.Count -eq 0) {
        "clean"
    }
    else {
        "dirty ($($statusLines.Count) changed paths)"
    }

    Write-Output "=== COPY BACK ==="
    Write-Output "PROJECT_DAY: $(Convert-ToCompactLine $fields['PROJECT_DAY'] 80)"
    Write-Output "BRANCH: $(Convert-ToCompactLine $branch 100)"
    Write-Output "HEAD: $(Convert-ToCompactLine $head 80)"
    Write-Output "GIT_STATUS: $gitStatus"
    Write-Output "ACTIVE_TASK: $(Convert-ToCompactLine $fields['ACTIVE_TASK'] 220)"
    Write-Output "ACTIVE_OBJECTIVE: $(Convert-ToCompactLine $fields['ACTIVE_OBJECTIVE'] 240)"
    Write-Output "CURRENT_RESULT: $(Convert-ToCompactLine $fields['CURRENT_TECHNICAL_RESULT'] 240)"
    Write-Output "NEXT_ACTION: $(Convert-ToCompactLine $fields['NEXT_ACTION'] 240)"
    Write-Output "=== END COPY BACK ==="
    exit 0
}
catch {
    Write-Output "=== COPY BACK ==="
    Write-Output "STATUS_ERROR: $(Convert-ToCompactLine $_.Exception.Message 500)"
    Write-Output "=== END COPY BACK ==="
    exit 1
}
