# setup_venv.ps1
$ErrorActionPreference = "Stop"

# Aller à la racine du projet (2 niveaux au-dessus de .vscode\script)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Resolve-Path (Join-Path $ScriptDir "..\..")
Set-Location $Root

Write-Host "Racine du projet : $Root"

# ─────────────────────────────────────────────
# Vérifier si Python est dispo
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "[ERREUR] Python n'est pas installé ou introuvable dans PATH"
    exit 1
}

# ─────────────────────────────────────────────
# Créer le venv s'il n'existe pas
$VenvPath = Join-Path $Root ".venv"
if (-not (Test-Path $VenvPath)) {
    Write-Host "Création de l'environnement virtuel .venv..."
    python -m venv .venv
} else {
    Write-Host ".venv déjà présent"
}

# ─────────────────────────────────────────────
# Activer le venv
Write-Host "Activation de .venv"
. ".venv/Scripts/Activate.ps1"

# ─────────────────────────────────────────────
# Mise à jour pip/setuptools/wheel
Write-Host "Mise à jour de pip/setuptools/wheel"
pip install --upgrade pip setuptools wheel

# ─────────────────────────────────────────────
# Installer les dépendances
if (Test-Path "pyproject.toml") {
    Write-Host "Installation des dépendances via pyproject.toml (PEP 621)"
    pip install -e .
} elseif (Test-Path "requirements.txt") {
    Write-Host "Installation des dépendances via requirements.txt"
    pip install -r requirements.txt
} else {
    Write-Host "[ERREUR] Aucun pyproject.toml ou requirements.txt trouvé. Environnement vide."
}

Write-Host "`n Environnement prêt. Active-le avec :"
Write-Host "   . .venv/Scripts/Activate.ps1"
