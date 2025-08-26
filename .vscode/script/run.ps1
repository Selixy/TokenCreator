# Nettoyage de l'écran
Clear-Host
for ($i = 0; $i -lt 100; $i++) { Write-Output "" }
Clear-Host

# ─────────────────────────────────────────────
# Aller à la racine du projet (2 niveaux au-dessus de .vscode\script)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Resolve-Path (Join-Path $ScriptDir "..\..")
Set-Location $Root

# ─────────────────────────────────────────────
# Vérifier que le venv existe et l'activer
$VenvActivate = Join-Path $Root ".venv\Scripts\Activate.ps1"
if (-Not (Test-Path $VenvActivate)) {
    & Join-Path $PSScriptRoot "setup_venv.ps1"
    if (-Not (Test-Path $VenvActivate)) {
        Write-Error "[ERREUR] Aucun venv trouvé dans $Root"
        Write-Output "Lance d'abord setup_venv.bat"
        exit 1
    }
}
. $VenvActivate

# ─────────────────────────────────────────────
# Lancer ton application Python
python -m app
$ExitCode = $LASTEXITCODE

# ─────────────────────────────────────────────
# Rétablir le dossier précédent et sortir avec le même code
Set-Location $ScriptDir
exit $ExitCode
