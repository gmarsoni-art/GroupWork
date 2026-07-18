#!/bin/bash
# PUBBLICA LAVORO (Mac/Linux): commit + push su git, poi tabelle su S3
# Uso: ./pubblica_lavoro.sh "messaggio di commit"
cd "$(dirname "$0")/.." || exit 1

MSG="$1"
if [ -z "$MSG" ]; then
    read -r -p "Messaggio di commit: " MSG
fi
if [ -z "$MSG" ]; then
    echo "Nessun messaggio: annullato."
    exit 1
fi

echo "=== git pull (prima di pushare si integra il lavoro altrui) ==="
git pull || { echo "!!! Conflitto o errore git: risolvi manualmente."; exit 1; }

echo
echo "=== commit e push ==="
git add -A
git commit -m "$MSG"
git push || { echo "!!! Push rifiutato: git pull e riprova."; exit 1; }

echo
echo "=== pubblicazione tabelle su S3 ==="
if ! python3 SCRIPT/LoadS3.py; then
    echo
    echo "!!! Upload S3 fallito (credenziali scadute?). Git e' comunque a posto."
    echo "!!! Aggiorna ~/.aws/credentials e rilancia: python3 SCRIPT/LoadS3.py"
    exit 1
fi

echo
echo "Fatto: git aggiornato e tabelle pubblicate su S3."
