param(
    [string]$NarrationPath = (Join-Path $PSScriptRoot '..\presentation\narration.json'),
    [string]$OutputDirectory = (Join-Path $PSScriptRoot '..\video\audio'),
    [string]$Voice = 'Microsoft Zira Desktop',
    [ValidateRange(-10,10)][int]$Rate = 0
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$narrationFile = (Resolve-Path -LiteralPath $NarrationPath).Path
$entries = ConvertFrom-Json -InputObject (Get-Content -LiteralPath $narrationFile -Raw -Encoding UTF8)
if ($entries.Count -lt 6 -or $entries.Count -gt 8) {
    throw 'Expected 6-8 slide narration entries.'
}
$slideNumbers = @($entries | ForEach-Object { [int]$_.slide })
for ($i = 0; $i -lt $entries.Count; $i++) {
    if ($slideNumbers[$i] -ne ($i + 1) -or [string]::IsNullOrWhiteSpace([string]$entries[$i].text)) {
        throw 'Narration entries must have sequential slide numbers starting at 1 and non-empty text.'
    }
}
$destination = [System.IO.Path]::GetFullPath($OutputDirectory)
[System.IO.Directory]::CreateDirectory($destination) | Out-Null
$synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer
$records = @()
try {
    $synthesizer.SelectVoice($Voice)
    $synthesizer.Rate = $Rate
    $synthesizer.Volume = 100
    foreach ($entry in $entries) {
        $filename = 'slide_{0:00}.wav' -f [int]$entry.slide
        $target = Join-Path $destination $filename
        $synthesizer.SetOutputToWaveFile($target)
        $synthesizer.Speak([string]$entry.text)
        $synthesizer.SetOutputToNull()
        if ((Get-Item -LiteralPath $target).Length -le 44) {
            throw "Speech synthesis produced an empty WAV: $filename"
        }
        $records += [ordered]@{
            slide = [int]$entry.slide
            path = $filename
            sha256 = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant()
            text = [string]$entry.text
        }
        Write-Output "Narration created: $filename"
    }
} finally {
    $synthesizer.Dispose()
}
$manifest = [ordered]@{
    schema_version = 1
    created_utc = [DateTime]::UtcNow.ToString('o')
    backend = 'Windows System.Speech / SAPI'
    voice = $Voice
    rate = $Rate
    synthetic_narration = $true
    disclosure = 'Computer-generated narration from the saved English slide notes; no human voice recording or voice cloning.'
    narration_sha256 = (Get-FileHash -LiteralPath $narrationFile -Algorithm SHA256).Hash.ToLowerInvariant()
    slides = $records
}
$manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $destination 'narration_manifest.json') -Encoding UTF8
