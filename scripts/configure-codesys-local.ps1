param(
    [Parameter(Mandatory=$true)][string]$CodesysExe,
    [Parameter(Mandatory=$true)][string]$Profile,
    [string]$AdditionalFolder = ''
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$exe = (Resolve-Path -LiteralPath $CodesysExe).Path
if ([IO.Path]::GetFileName($exe) -ne 'CODESYS.exe') {
    throw 'Select Development System V3 CODESYS.exe, not CODESYS-4.exe or a Control Win runtime.'
}
$configPath = Join-Path $projectRoot 'configs\runtime.local.json'
$config = Get-Content -LiteralPath $configPath -Raw -Encoding UTF8 | ConvertFrom-Json
$config.codesys_exe = $exe
$config.codesys_profile = $Profile
$config.codesys_template = Join-Path $projectRoot 'codesys\templates\benchmark.project'
$config | Add-Member -NotePropertyName additional_folder -NotePropertyValue $AdditionalFolder -Force
$json = $config | ConvertTo-Json -Depth 20
[IO.File]::WriteAllText($configPath, $json, [Text.UTF8Encoding]::new($false))
Write-Output 'Local paths saved. Run scripts\run.ps1 compiler-smoke to verify the actual compiler and Scripting installation.'
