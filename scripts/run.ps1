param([switch]$AllowModelApi, [Parameter(ValueFromRemainingArguments=$true)][string[]]$AgentArgs)
$ErrorActionPreference='Stop'
$projectRoot=Split-Path -Parent $PSScriptRoot
$projectPython=Join-Path $projectRoot '.venv\Scripts\python.exe'
if(-not (Test-Path -LiteralPath $projectPython)){throw 'Local Python environment missing.'}
if ((($AgentArgs -contains 'run') -or ($AgentArgs -contains 'probe-models')) -and -not $AllowModelApi) {
    throw 'Model API access blocked. Obtain the owner approval for this invocation before using -AllowModelApi.'
}
$env:PYTHONPATH=Join-Path $projectRoot 'src'
$env:PYTHONIOENCODING='utf-8'
$taskTemp=Join-Path $projectRoot '.local_tmp'
New-Item -ItemType Directory -Path $taskTemp -Force | Out-Null
$env:TEMP=$taskTemp
$env:TMP=$taskTemp
$localConfig=Join-Path $projectRoot 'configs\runtime.local.json'
if (-not ($AgentArgs -contains '--config')) { $AgentArgs=@('--config', $localConfig) + $AgentArgs }
& $projectPython -X utf8 -m plc_agent.cli @AgentArgs
exit $LASTEXITCODE
