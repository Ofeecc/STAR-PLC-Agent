param([switch]$Render)
$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
$taskTex = Join-Path $taskRoot 'report\latex'
$taskBuild = Join-Path $taskTex 'build'
New-Item -ItemType Directory -Path $taskBuild -Force | Out-Null
Push-Location $taskTex
try {
    foreach ($taskPass in 1..2) {
        & pdflatex -interaction=nonstopmode -halt-on-error -no-shell-escape -output-directory=build main.tex *> (Join-Path $taskBuild "pass_$taskPass.log")
        if ($LASTEXITCODE -ne 0) { throw "LaTeX compilation failed; inspect $taskBuild\pass_$taskPass.log" }
    }
    $taskLog = Get-Content -LiteralPath (Join-Path $taskBuild 'main.log') -Raw
    if ($taskLog -match 'Overfull \\[hv]box') { throw 'The report has overfull boxes; resolve layout before release.' }
    if ($taskLog -match 'There were undefined references') { throw 'The report has unresolved citations or references.' }
    Copy-Item -LiteralPath (Join-Path $taskBuild 'main.pdf') -Destination (Join-Path $taskRoot 'report\report.pdf') -Force
} finally { Pop-Location }
if ($Render) {
    $taskRendered = Join-Path $taskRoot 'report\rendered'
    New-Item -ItemType Directory -Path $taskRendered -Force | Out-Null
    & pdftoppm -r 100 -png (Join-Path $taskRoot 'report\report.pdf') (Join-Path $taskRendered 'page')
    if ($LASTEXITCODE -ne 0) { throw 'PDF rendering failed.' }
}
& pdfinfo (Join-Path $taskRoot 'report\report.pdf') | Select-String 'Pages:|Page size:|File size:'
