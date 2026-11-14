$ErrorActionPreference = "Stop"
$Project = Split-Path -Parent $PSScriptRoot
$RunDir = Join-Path $Project "results/raw/four_group_20261114"
$CourseRoot = Split-Path -Parent (Split-Path -Parent $Project)
$Python = Get-ChildItem -Path (Join-Path $CourseRoot "PLC_Agent_*") -Directory |
    ForEach-Object { Join-Path $_.FullName ".venv/Scripts/python.exe" } |
    Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $Python) { throw "Project virtualenv Python was not found." }
$SummaryPath = Join-Path $RunDir "matrix_summary.json"
$RetryConfig = Join-Path $RunDir "matrix_config_codex_retry.json"
$Log = Join-Path $RunDir "codex_retry.log"

while ($true) {
    if (Test-Path -LiteralPath (Join-Path $RunDir "STOP")) {
        Add-Content -LiteralPath $Log -Value "STOP marker found; Codex retry was not started."
        exit 2
    }
    $state = & $Python -X utf8 -c "import json,sys; print(json.load(open(sys.argv[1],encoding='utf-8'))['state'])" $SummaryPath
    if ($LASTEXITCODE -eq 0 -and $state -in @("COMPLETE", "COMPLETE_WITH_RECORDED_ERRORS")) { break }
    Start-Sleep -Seconds 20
}

& $Python -X utf8 scripts/prepare_codex_retry.py *>> $Log
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Add-Content -LiteralPath $Log -Value "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Starting corrected Codex groups."
& $Python -X utf8 -u scripts/run_fullflow_matrix.py --run --allow-model-api --config $RetryConfig --only codex_deepseek,codex_terra *>> $Log
exit $LASTEXITCODE
