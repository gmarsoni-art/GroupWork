#!/bin/bash
# INIZIA LAVORO (Mac/Linux): allinea il tuo PC allo stato del progetto
cd "$(dirname "$0")/.." || exit 1

echo "=== git pull ==="
if ! git pull; then
    echo
    echo "!!! git pull fallito - probabile conflitto. NON proseguire:"
    echo "!!! risolvi il conflitto o chiedi al gruppo."
    exit 1
fi

echo
echo "=== download tabelle da S3 ==="
if ! python3 SCRIPT/DownloadS3.py; then
    echo
    echo "Avviso: download S3 non riuscito (lab spento o credenziali scadute?)."
    echo "Git e' comunque allineato: puoi lavorare e riprovare con:"
    echo "   python3 SCRIPT/DownloadS3.py"
fi

echo
echo "Tutto allineato. Buon lavoro!"
