$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$target = Join-Path $projectRoot '.local\model_checkers'
New-Item -ItemType Directory -Path $target -Force | Out-Null
$archive = Join-Path $target 'NuSMV-2.7.1-win64.zip'
$checksum = "$archive.sha256sum"
Invoke-WebRequest -Uri 'https://nusmv.fbk.eu/distrib/2.7.1/NuSMV-2.7.1-win64.zip' -OutFile $archive
Invoke-WebRequest -Uri 'https://nusmv.fbk.eu/distrib/2.7.1/NuSMV-2.7.1-win64.zip.sha256sum' -OutFile $checksum
$expected = ((Get-Content -LiteralPath $checksum -Raw).Trim() -split '\s+')[0]
$observed = (Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash
if ($observed -ine $expected) { throw 'NuSMV checksum mismatch' }
Expand-Archive -LiteralPath $archive -DestinationPath (Join-Path $target 'NuSMV-2.7.1') -Force
Get-ChildItem -LiteralPath $target -Recurse -Filter NuSMV.exe | Select-Object -ExpandProperty FullName
