@echo off
REM ============================================================
REM  PUBBLICA LAVORO: commit + push su git, poi tabelle su S3
REM  Uso:  pubblica_lavoro.bat "messaggio di commit"
REM ============================================================
cd /d "%~dp0.."

set "MSG=%~1"
if "%MSG%"=="" set /p MSG=Messaggio di commit:
if "%MSG%"=="" (
    echo Nessun messaggio: annullato.
    pause
    exit /b 1
)

echo === git pull (prima di pushare si integra il lavoro altrui) ===
git pull
if errorlevel 1 goto :conflitto

echo.
echo === commit e push ===
git add -A
git commit -m "%MSG%"
git push
if errorlevel 1 goto :conflitto

echo.
echo === pubblicazione tabelle su S3 ===
py SCRIPT\LoadS3.py
if errorlevel 1 (
    echo.
    echo !!! Upload S3 fallito (credenziali scadute?). Git e' comunque a posto.
    echo !!! Aggiorna ~/.aws/credentials e rilancia: py SCRIPT\LoadS3.py
    pause
    exit /b 1
)

echo.
echo Fatto: git aggiornato e tabelle pubblicate su S3.
pause
exit /b 0

:conflitto
echo.
echo !!! Operazione git fallita - probabile conflitto o push rifiutato.
echo !!! Risolvi manualmente (git status per capire) o chiedi al gruppo.
pause
exit /b 1
