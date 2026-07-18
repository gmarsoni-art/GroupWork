@echo off
REM ============================================================
REM  INIZIA LAVORO: allinea il tuo PC allo stato del progetto
REM  (git pull; S3 non serve: i dati arrivano già da git)
REM  Da lanciare dalla root del repo o da SCRIPT\
REM ============================================================
cd /d "%~dp0.."

echo === git pull ===
git pull
if errorlevel 1 (
    echo.
    echo !!! ATTENZIONE: git pull fallito - probabile conflitto.
    echo !!! NON proseguire: risolvi il conflitto o chiedi al gruppo.
    pause
    exit /b 1
)

echo.
echo === download tabelle da S3 ===
py SCRIPT\DownloadS3.py
if errorlevel 1 (
    echo.
    echo Avviso: download S3 non riuscito (lab spento o credenziali scadute?).
    echo Git e' comunque allineato: puoi lavorare e riprovare piu' tardi con:
    echo    py SCRIPT\DownloadS3.py
)

echo.
echo Tutto allineato. Buon lavoro!
pause
