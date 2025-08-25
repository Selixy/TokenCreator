@echo off
cls

rem Écran vide temporaire (évite affichage résiduel)
for /L %%i in (1,1,100) do echo.
cls
setlocal

REM === Aller à la racine du projet ===
set "ROOT=%~dp0..\.."
pushd "%ROOT%" || (echo [ERREUR] Impossible d'acceder a "%ROOT%" & exit /b 1)

set "APPNAME=TokenCreator"
set "OUTBASE=%ROOT%\build"
set "WORKDIR=%OUTBASE%\build"
set "DISTDIR=%OUTBASE%\dist"
set "SPECFILE=%OUTBASE%\%APPNAME%.spec"
set "EGGINFO=%ROOT%\app\tokencreator.egg-info"

REM Vérif/creation du venv via setup_venv.bat
call ".vscode\script\setup_venv.bat"

REM Activer le venv
call ".venv\Scripts\activate.bat"

REM Installer pyinstaller si absent
pip show pyinstaller >nul 2>&1 || pip install pyinstaller

REM Nettoyage ancien build
if exist "%OUTBASE%" (
  echo [CLEAN] suppression de %OUTBASE%
  rmdir /s /q "%OUTBASE%"
)
mkdir "%WORKDIR%"
mkdir "%DISTDIR%"

REM Options communes PyInstaller
set "COMMON_OPTS=app\main.py -n %APPNAME% --noconsole --clean --collect-all PySide6 --collect-all PySide6.QtSvgWidgets"
if exist "assets\app.ico" (
  set "COMMON_OPTS=%COMMON_OPTS% --icon=assets\app.ico"
)

echo === Build (one-folder + one-file) ===
call pyinstaller %COMMON_OPTS% ^
  --distpath "%DISTDIR%" ^
  --workpath "%WORKDIR%" ^
  --specpath "%OUTBASE%"
set EXITCODE=%ERRORLEVEL%


REM === Nettoyage final ===
echo [CLEAN] suppression des dossier
del /f /q "%OUTBASE%\%APPNAME%.spec"
rmdir /s /q "%WORKDIR%"
rmdir /s /q "%EGGINFO%"

REM === Déplacer contenu de dist -> OUTBASE ===
echo [MOVE] Déplacement du contenu de %DISTDIR% vers %OUTBASE%
xcopy "%DISTDIR%\*" "%OUTBASE%\" /E /I /H /Y >nul

REM === Supprimer dist ===
if exist "%DISTDIR%" (
  echo [CLEAN] Suppression de %DISTDIR%
  rmdir /s /q "%DISTDIR%"
)

REM === Mettre à jour DISTDIR pour pointer sur l'appli finale ===
set "DISTDIR=%OUTBASE%\%APPNAME%\%APPNAME%.exe"


echo.
echo ============================================
echo  Build termine avec succes
echo    Sortie finale : %DISTDIR%
echo ============================================
%DISTDIR%

popd
exit /b 0
