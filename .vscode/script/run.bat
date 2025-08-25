@echo off
setlocal
cls

REM === Aller à la racine du projet (2 niveaux au-dessus de .vscode\script) ===
pushd "%~dp0..\.."

REM Vérif venv
if not exist ".venv\Scripts\activate.bat" (
  echo [ERREUR] venv introuvable dans %cd%
  echo Lance d'abord setup_venv.bat
  exit /b 1
)

REM Activer venv
call ".venv\Scripts\activate.bat"

echo === Lancement de l'application ===
python -m tokencreator
set EXITCODE=%ERRORLEVEL%

popd
exit /b %EXITCODE%
