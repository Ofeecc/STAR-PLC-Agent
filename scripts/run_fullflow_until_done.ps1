param(
    [string]$Python = "",
    [int]$MaxInfraRetries = 4
)

$ErrorActionPreference = "Stop"
$Project = Split-Path -Parent $PSScriptRoot
$RunDir = Join-Path $Project "results/raw/four_group_20261114"
$Config = Join-Path $RunDir "matrix_config_resume.json"
$Log = Join-Path $RunDir "auto_resume.log"
$CourseRoot = Split-Path -Parent (Split-Path -Parent $Project)
if ([string]::IsNullOrWhiteSpace($Python)) {
    $Python = Get-ChildItem -Path (Join-Path $CourseRoot "PLC_Agent_*") -Directory |
        ForEach-Object { Join-Path $_.FullName ".venv/Scripts/python.exe" } |
        Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
}
if (-not $Python -or -not (Test-Path -LiteralPath $Python)) { throw "Project virtualenv Python was not found." }
Set-Location $Project

for ($attempt = 0; $attempt -le $MaxInfraRetries; $attempt++) {
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -LiteralPath $Log -Value "[$stamp] Starting four-group evaluation pass $($attempt + 1)."
    & $Python -X utf8 -u scripts/run_fullflow_matrix.py --run --allow-model-api --config $Config *>> $Log
    $exitCode = $LASTEXITCODE
    if ($exitCode -eq 0) {
        Add-Content -LiteralPath $Log -Value "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Matrix completed."
        exit 0
    }

    $summaryPath = Join-Path $RunDir "matrix_summary.json"
    if (-not (Test-Path -LiteralPath $summaryPath)) {
        Add-Content -LiteralPath $Log -Value "Matrix stopped with exit code $exitCode and no summary."
        exit $exitCode
    }
    $summaryState = & $Python -X utf8 -c "import json,sys; print(json.load(open(sys.argv[1], encoding='utf-8'))['state'])" $summaryPath
    if ($LASTEXITCODE -ne 0 -or $summaryState -notlike "BLOCKED *" -or $attempt -ge $MaxInfraRetries) {
        Add-Content -LiteralPath $Log -Value "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Stop: state=$summaryState, exit=$exitCode, retries=$attempt."
        exit $exitCode
    }
    if (Test-Path -LiteralPath (Join-Path $RunDir "STOP")) {
        Add-Content -LiteralPath $Log -Value "Operator STOP marker found; exiting."
        exit 2
    }
    Add-Content -LiteralPath $Log -Value "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Retrying blocked infrastructure stages; cached successful stages remain reused."
    Start-Sleep -Seconds 20
}

exit 2
