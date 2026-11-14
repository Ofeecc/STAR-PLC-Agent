$ErrorActionPreference = 'Stop'
$Project = Split-Path -Parent $PSScriptRoot
$RunDir = Join-Path $Project 'results/raw/four_group_20261114'
$Log = Join-Path $RunDir 'resume_then_codex_retry.log'
Set-Location $Project
& (Join-Path $PSScriptRoot 'run_fullflow_until_done.ps1')
$matrixExit = $LASTEXITCODE
Add-Content -LiteralPath $Log -Value "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Original matrix supervisor exit=$matrixExit"
if ($matrixExit -ne 0) { exit $matrixExit }
& (Join-Path $PSScriptRoot 'run_codex_retry_after_full_matrix.ps1')
$retryExit = $LASTEXITCODE
Add-Content -LiteralPath $Log -Value "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Corrected Codex retry exit=$retryExit"
exit $retryExit
