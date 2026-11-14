param(
    [string[]]$Tasks = @('pilot'),
    [string]$SourceDir,
    [string]$OutDir,
    [string]$Python,
    [ValidateSet('star','codex_cli')][string]$Driver = 'star',
    [string]$Model = 'deepseek-v4.1-flash-1017',
    [string]$Condition,
    [int]$Workers = 2,
    [string[]]$Stages = @('compile', 'functional', 'formal'),
    [int]$FormalTimeout = 60,
    [switch]$ReuseTraces,
    [switch]$Recompile,
    [switch]$RetryInfra,
    [switch]$KeepGoing,
    [switch]$GenerateMissing,
    [switch]$AllowModelApi,
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
if (-not $Python) {
    $Python = Join-Path $projectRoot '.venv\Scripts\python.exe'
    $localPython = Join-Path $projectRoot '.local\batch_python.txt'
    if (-not (Test-Path -LiteralPath $Python) -and (Test-Path -LiteralPath $localPython)) {
        $Python = (Get-Content -LiteralPath $localPython -Raw -Encoding UTF8).Trim()
    }
    if (-not (Test-Path -LiteralPath $Python)) {
        $Python = (Get-Command python -ErrorAction Stop).Source
    }
}
if ($GenerateMissing -and -not $AllowModelApi) {
    throw 'Obtain explicit owner approval before generation, then use -GenerateMissing -AllowModelApi.'
}
$batchArgs = @('--tasks', ($Tasks -join ','), '--workers', "$Workers", '--formal-timeout', "$FormalTimeout", '--driver', $Driver, '--model', $Model)
if ($Condition) { $batchArgs += @('--condition', $Condition) }
if ($SourceDir) { $batchArgs += @('--source-dir', $SourceDir) }
if ($OutDir) { $batchArgs += @('--out-dir', $OutDir) }
foreach ($item in @(
    @($ReuseTraces, '--reuse-traces'), @($Recompile, '--recompile'),
    @($RetryInfra, '--retry-infra'), @($KeepGoing, '--keep-going'),
    @($GenerateMissing, '--generate-missing'), @($AllowModelApi, '--allow-model-api'),
    @($DryRun, '--dry-run')
)) { if ($item[0]) { $batchArgs += $item[1] } }
$batchArgs += @('--stages') + $Stages
$env:PYTHONIOENCODING = 'utf-8'
& $Python -X utf8 -u (Join-Path $PSScriptRoot 'run_batch.py') @batchArgs
exit $LASTEXITCODE
