@echo off
setlocal

REM === Aller à la racine du projet (2 niveaux au-dessus du script) ===
set "ROOT=%~dp0..\.."
pushd "%ROOT%" || (echo [ERREUR] Impossible d'acceder a "%ROOT%" & exit /b 1)

echo === Setup de l'environnement virtuel pour TokenCreator ===

REM === Option --force pour recréer le venv ===
if /I "%~1"=="--force" (
    if exist ".venv" (
        echo [INFO] Suppression de l'ancien venv...
        rmdir /s /q ".venv"
    )
)

REM === Chercher Python (priorité 3.11) ===
set "PYTHON_CMD="
for %%P in ("py -3.11" "py -3" "python3.11" "python") do (
    call %%~P -V >nul 2>&1 && set "PYTHON_CMD=%%~P" && goto :found
)
:found

if not defined PYTHON_CMD (
    echo [ERREUR] Python 3 introuvable. Installe Python 3.11 puis relance.
    popd & exit /b 1
)

echo [OK] Python trouve :
%PYTHON_CMD% -V

REM === Créer le venv si absent ===
if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Creation du venv...
    %PYTHON_CMD% -m venv ".venv"
) else (
    echo [OK] venv deja present
)

REM === Mise a jour pip ===
echo [INFO] Mise a niveau de pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip

REM === Installer le projet (editable mode) ===
echo [INFO] Installation du projet via pyproject.toml...
".venv\Scripts\python.exe" -m pip install -e .

echo.
echo [OK] Environnement pret dans %CD%\.venv
echo     Active-le avec: call .venv\Scripts\activate.bat

popd
exit /b 0
