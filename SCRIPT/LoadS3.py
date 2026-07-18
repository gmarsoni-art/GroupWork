# -*- coding: utf-8 -*-
"""
Carica le tabelle finali (DATA/tables) sul bucket S3 del progetto.
RAW_DATA e CLEAN_DATA restano fuori: si condividono via git, S3 serve solo Athena.
Sovrascrive i file esistenti (comportamento normale per aggiornare le tabelle).

Uso:
    python LoadS3.py             # carica DATA/tables
    python LoadS3.py --nuovi     # carica solo i file non ancora presenti sul bucket

Requisiti: credenziali in ~/.aws/credentials (da AWS Details del Learner Lab).
"""
import sys
from pathlib import Path

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

BUCKET = "groupworksistemascolastico"   # <-- nome del vostro bucket

DATA = Path(__file__).resolve().parent.parent / "DATA"
TABLES = DATA / "tables"          # si carica solo questa cartella


def check_error(e):
    code = e.response["Error"]["Code"]
    if code in ("ExpiredToken", "InvalidToken", "InvalidAccessKeyId"):
        sys.exit("Credenziali scadute: riavvia il lab e aggiorna ~/.aws/credentials")
    if code == "AccessDenied":
        sys.exit(f"Accesso negato al bucket {BUCKET}: controlla la bucket policy")
    raise e


def main():
    solo_nuovi = "--nuovi" in sys.argv
    if not TABLES.is_dir():
        sys.exit(f"Cartella non trovata: {TABLES}")

    s3 = boto3.client("s3")
    try:
        esistenti = set()
        if solo_nuovi:
            pages = s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="tables/")
            for page in pages:
                for obj in page.get("Contents", []):
                    esistenti.add(obj["Key"])

        n, saltati = 0, 0
        for f in TABLES.rglob("*"):
            if f.is_dir():
                continue
            key = "tables/" + f.relative_to(TABLES).as_posix()   # DATA/tables/x.csv -> tables/x.csv
            if key in esistenti:
                saltati += 1
                continue
            s3.upload_file(str(f), BUCKET, key)
            print(f"  -> {key}")
            n += 1
    except NoCredentialsError:
        sys.exit(
            "Credenziali mancanti. Avvia il Learner Lab, apri 'AWS Details' -> "
            "'AWS CLI: Show' e incolla il blocco in ~/.aws/credentials"
        )
    except ClientError as e:
        check_error(e)

    msg = f"Caricati {n} file su s3://{BUCKET}"
    if solo_nuovi:
        msg += f" (saltati {saltati} già presenti)"
    print(msg)


if __name__ == "__main__":
    main()
