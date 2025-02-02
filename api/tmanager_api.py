import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import os

from service import preprocessing

# Lade Umgebungsvariablen
load_dotenv()


def check_availability(date_from, date_to, flat_name):

    tmanager_base_url = os.getenv("TMANAGER_BASE_URL")
    tmanager_api_key = os.getenv("TMANAGER_API_KEY")

    result = ""

    if not tmanager_base_url or not tmanager_api_key:
        raise ValueError(
            "TMANAGER_BASE_URL oder TMANAGER_API_KEY Umgebungsvariable ist nicht gesetzt"
        )
    else:
        result = "available"

    return result
