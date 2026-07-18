# -*- coding: utf-8 -*-
"""
Scarica le tabelle dal bucket S3 del progetto in DATA/tables del repo.

Uso:
    python DownloadS3.py                     # scarica tutte le tabelle
    python DownloadS3.py tables/province/    # scarica solo un prefix

Requisiti: credenziali in ~/.aws/credentials (da AWS Details del Learner Lab).
"""
import sys
from pathlib import Path

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

BUCKET = "groupworksistemascolastico"   # <-- nome del vostro bucket

# DATA sta accanto a SCRIPT, qualunque sia la cartella da cui lanci lo script
DATA = Path(__file__).resolve().parent.parent / "DATA"


def check_error(e):
    code = e.response["Error"]["Code"]
    if code in ("ExpiredToken", "InvalidToken", "InvalidAccessKeyId"):
        sys.exit("Credenziali scadute: riavvia il lab e aggiorna ~/.aws/credentials")
    if code == "AccessDenied":
        sys.exit(f"Accesso negato al bucket {BUCKET}: controlla la bucket policy")
    raise e


def main():
    prefix = sys.argv[1] if len(sys.argv) > 1 else "tables/"
    s3 = boto3.client("s3")
    n = 0
    try:
        pages = s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix)
        for page in pages:
            for obj in page.get("Contents", []):
                key = obj["Key"]
                if key.endswith("/"):
                    continue
                dest = DATA / key
                dest.parent.mkdir(parents=True, exist_ok=True)
                s3.download_file(BUCKET, key, str(dest))
                print(f"  <- {key}")
                n += 1
    except NoCredentialsError:
        sys.exit(
            "Credenziali mancanti. Avvia il Learner Lab, apri 'AWS Details' -> "
            "'AWS CLI: Show' e incolla il blocco in ~/.aws/credentials"
        )
    except ClientError as e:
        check_error(e)
    print(f"Scaricati {n} file in {DATA}")


if __name__ == "__main__":
    main()
