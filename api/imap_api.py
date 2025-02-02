import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import os

from service import preprocessing

# Lade Umgebungsvariablen
load_dotenv()


# Funktion, um sich mit dem IMAP-Server zu verbinden und E-Mails zu holen
def fetch_emails():
    # E-Mail-Server und Anmeldedaten aus der .env-Datei
    imap_server = os.getenv("IMAP_SERVER", "imap.t-online.de")
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASSWORD")

    try:
        # Verbindung zum IMAP-Server
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_user, email_pass)

        # Wählen Sie den Posteingang aus
        mail.select("inbox")

        # Suche nach ungelesenen E-Mails
        status, messages = mail.search(None, "UNSEEN")

        if status == "OK":
            # Nachrichten-ID(s) abrufen
            email_ids = messages[0].split()
            emails = []

            for email_id in email_ids:
                # Holen Sie sich die E-Mail-Daten
                status, msg_data = mail.fetch(email_id, "(RFC822)")

                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])

                        # Dekodiere den Absender
                        email_sender = decode_header(msg.get("From"))[0][0]
                        if isinstance(email_sender, bytes):
                            email_sender = email_sender.decode()

                        # Dekodiere den Betreff
                        email_subject = decode_header(msg.get("Subject"))[0][0]
                        if isinstance(email_subject, bytes):
                            email_subject = email_subject.decode()

                        # Holen Sie sich den E-Mail-Inhalt
                        email_content = preprocessing.get_email_content(msg)

                        email_data = {
                            "From": email_sender,
                            "Subject": email_subject,
                            "Body": email_content,
                        }

                        # Füge die E-Mail in die Liste ein
                        emails.append(email_data)

            # Verbindung beenden
            mail.logout()

            return emails
        else:
            print("Keine neuen E-Mails gefunden.")
            return []

    except Exception as e:
        print(f"Fehler beim Abrufen der E-Mails: {e}")
        return []
