# .vscode/script/build.ps1
$ErrorActionPreference = "Stop"
$root = Resolve-Path "$PSScriptRoot/../.."
Set-Location $root

# Synchroniser avant build (assure que tout est installé)
uv sync

# Lancer PyInstaller via uv
uv run python .vscode/script/build.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "[ERREUR] Build échoué avec code $LASTEXITCODE"
    exit $LASTEXITCODE
}

# Lancer l’exécutable si présent
$exe = "$root/build/dist/TokenCreator/TokenCreator.exe"
if (Test-Path $exe) {
    Write-Host "Lancement de l'application : $exe"
    & $exe
}
