@echo off
cls

rem ─────────────────────────────────────────────
rem Aller à la racine du projet (2 niveaux au-dessus de .vscode\script)
set "ROOT=%~dp0..\.."
pushd "%ROOT%" || (echo [ERREUR] Impossible d'accéder à "%ROOT%" & exit /b 1)

rem ─────────────────────────────────────────────
rem Vérifier que le venv existe
if not exist ".venv\Scripts\activate.bat" (
  echo [ERREUR] Aucun venv trouvé dans %ROOT%
  echo Lance d'abord setup_venv.bat
  popd
  exit /b 1
)

rem ─────────────────────────────────────────────
rem Activer le venv
call ".venv\Scripts\activate.bat"

rem ─────────────────────────────────────────────
rem Lancer ton application Python
python -m app

rem ─────────────────────────────────────────────
rem Conserver le code de sortie
set EXITCODE=%ERRORLEVEL%

popd
exit /b %EXITCODE%
