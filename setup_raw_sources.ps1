# Klont alle 4 Quell-Repositories vollständig nach raw_sources/ (inkl. Windows Longpaths-Fix)
$ErrorActionPreference = "Stop"
$rawDir = Join-Path $PSScriptRoot "raw_sources"
New-Item -ItemType Directory -Force -Path $rawDir | Out-Null
Set-Location $rawDir

git config --global core.longpaths true

$repos = @(
    "https://github.com/Junkz3/wrench-board.git",
    "https://github.com/theEmbeddedGeorge/theEmbeddedNewTestament.github.io.git",
    "https://github.com/aKaReZa75/Repair.git",
    "https://github.com/Vitorbnc/electronics-datasheets.git"
)

foreach ($url in $repos) {
    $name = [System.IO.Path]::GetFileNameWithoutExtension($url)
    if (-not (Test-Path (Join-Path $rawDir $name))) {
        Write-Host "Klone $url ..."
        git -c core.longpaths=true clone $url
    } else {
        Write-Host "$name existiert bereits – prüfe Checkout..."
        git -C (Join-Path $rawDir $name) config core.longpaths true
        git -C (Join-Path $rawDir $name) checkout -f HEAD
    }
}
Write-Host "Alle Quell-Repositories in raw_sources/ sind vollständig eingerichtet."
