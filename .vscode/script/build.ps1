# .vscode/script/build.ps1
$ErrorActionPreference = "Stop"

# Aller à la racine du projet
$root = Resolve-Path "$PSScriptRoot/../.."
Set-Location $root

# ─────────────────────────────────────────────
# Vérifier que le venv existe et l'activer
$VenvActivate = Join-Path $Root ".venv\Scripts\Activate.ps1"
if (-Not (Test-Path $VenvActivate)) {
    & Join-Path $PSScriptRoot "setup_venv.ps1"
    if (-Not (Test-Path $VenvActivate)) {
        Write-Error "[ERREUR] Aucun venv trouvé dans $Root"
        exit 1
    }
}
. $VenvActivate

# ─────────────────────────────────────────────
# Lancer le build
python ".vscode/script/build.py"
if ($LASTEXITCODE -ne 0) {
    Write-Error "[ERREUR] Build échoué avec code $LASTEXITCODE"
    exit $LASTEXITCODE
}

# ─────────────────────────────────────────────
# lancer l’appli compilée
$exe = "$root/build/dist/TokenCreator/TokenCreator.exe"
if (Test-Path $exe) {
    Write-Host "Lancement de l'application : $exe ..."
    & $exe
} else {
    Write-Warning "[ERREUR] Impossible de trouver $exe"
}
