param(
    [switch]$Quiet
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

$results = New-Object System.Collections.Generic.List[object]

function Add-Result {
    param(
        [string]$Name,
        [string]$Status,
        [string]$Detail
    )
    $results.Add([pscustomobject]@{
        Name = $Name
        Status = $Status
        Detail = $Detail
    }) | Out-Null
}

function Run-Check {
    param(
        [string]$Name,
        [scriptblock]$Command,
        [string]$SkipReason = ""
    )

    if ($SkipReason) {
        Add-Result -Name $Name -Status "SKIPPED" -Detail $SkipReason
        if (-not $Quiet) { Write-Host "SKIPPED $Name - $SkipReason" }
        return
    }

    if (-not $Quiet) { Write-Host "RUN $Name" }

    try {
        & $Command
        Add-Result -Name $Name -Status "PASS" -Detail ""
        if (-not $Quiet) { Write-Host "PASS $Name" }
    }
    catch {
        Add-Result -Name $Name -Status "FAIL" -Detail $_.Exception.Message
        Write-Host "FAIL $Name - $($_.Exception.Message)"
    }
}

Write-Host "SAFE-FAST safe local checks"
Write-Host "Scope: local tests, JSON fixture parsing, and Python compile checks only."
Write-Host "Excluded: live, broker, order, account, Railway, secrets, paid/vendor calls, raw-data mutation."
Write-Host ""

$normalizerTest = Join-Path $repoRoot "tests\test_databento_opra_normalizer.py"
if (Test-Path -LiteralPath $normalizerTest) {
    Run-Check -Name "Databento OPRA normalizer tests" -Command {
        $oldNoByteCode = $env:PYTHONDONTWRITEBYTECODE
        $env:PYTHONDONTWRITEBYTECODE = "1"
        try {
            python -m unittest tests.test_databento_opra_normalizer
            if ($LASTEXITCODE -ne 0) { throw "python unittest exited with code $LASTEXITCODE" }
        }
        finally {
            $env:PYTHONDONTWRITEBYTECODE = $oldNoByteCode
        }
    }
}
else {
    Run-Check -Name "Databento OPRA normalizer tests" -Command {} -SkipReason "tests\test_databento_opra_normalizer.py not present"
}

$fixtureDir = Join-Path $repoRoot "historical_signal_replay\fixtures"
$jsonFixtures = @()
if (Test-Path -LiteralPath $fixtureDir) {
    $jsonFixtures = @(Get-ChildItem -LiteralPath $fixtureDir -Filter "*.json" -File)
}

if ($jsonFixtures.Count -gt 0) {
    Run-Check -Name "JSON fixture validation" -Command {
        foreach ($fixture in $jsonFixtures) {
            python -m json.tool $fixture.FullName | Out-Null
            if ($LASTEXITCODE -ne 0) { throw "json validation failed for $($fixture.FullName) with code $LASTEXITCODE" }
        }
    }
}
else {
    Run-Check -Name "JSON fixture validation" -Command {} -SkipReason "No JSON fixtures found in historical_signal_replay\fixtures"
}

$compileTargets = @(
    "historical_signal_replay\databento_opra_normalizer.py",
    "historical_signal_replay\signal_replay.py",
    "historical_signal_replay\metrics.py",
    "watcher_foundation\source_evidence_work_package_content_validator.py",
    "watcher_foundation\source_evidence_package_to_intake_bridge.py"
)

$presentCompileTargets = @()
foreach ($target in $compileTargets) {
    $path = Join-Path $repoRoot $target
    if (Test-Path -LiteralPath $path) {
        $presentCompileTargets += $path
    }
}

if ($presentCompileTargets.Count -gt 0) {
    Run-Check -Name "Python helper compile checks" -Command {
        $compileScript = @'
import sys
from pathlib import Path

for target in sys.argv[1:]:
    path = Path(target)
    source = path.read_text(encoding="utf-8")
    compile(source, str(path), "exec")
'@
        $compileScript | python - @presentCompileTargets
        if ($LASTEXITCODE -ne 0) { throw "python compile checks exited with code $LASTEXITCODE" }
    }
}
else {
    Run-Check -Name "Python helper compile checks" -Command {} -SkipReason "No configured helper modules present"
}

Write-Host ""
Write-Host "Summary"
$passCount = @($results | Where-Object { $_.Status -eq "PASS" }).Count
$failCount = @($results | Where-Object { $_.Status -eq "FAIL" }).Count
$skipCount = @($results | Where-Object { $_.Status -eq "SKIPPED" }).Count

foreach ($result in $results) {
    if ($result.Detail) {
        Write-Host "$($result.Status) $($result.Name) - $($result.Detail)"
    }
    else {
        Write-Host "$($result.Status) $($result.Name)"
    }
}

Write-Host ""
Write-Host "PASS: $passCount"
Write-Host "FAIL: $failCount"
Write-Host "SKIPPED: $skipCount"

if ($failCount -gt 0) {
    exit 1
}

exit 0
