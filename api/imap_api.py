import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import os

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
                        From = decode_header(msg.get("From"))[0][0]
                        if isinstance(From, bytes):
                            From = From.decode()

                        # Dekodiere den Betreff
                        Subject = decode_header(msg.get("Subject"))[0][0]
                        if isinstance(Subject, bytes):
                            Subject = Subject.decode()

                        # Füge die E-Mail in die Liste ein
                        # Initialisiere das E-Mail-Dictionary
                        email_data = {
                            "From": From,
                            "Subject": Subject,
                            "Body": None,
                        }

                        # Überprüfe, ob die E-Mail mehrere Teile hat
                        if msg.is_multipart():
                            for part in msg.walk():
                                # Ignoriere Anhänge und berücksichtige nur Text/HTML-Teile
                                if part.get_content_type() in [
                                    "text/plain",
                                    "text/html",
                                ]:
                                    try:
                                        email_data["Body"] = part.get_payload(
                                            decode=True
                                        ).decode(part.get_content_charset())
                                        break
                                    except Exception as e:
                                        print(
                                            f"Fehler beim Dekodieren des E-Mail-Inhalts: {e}"
                                        )
                        else:
                            # Wenn die E-Mail nicht multipart ist
                            try:
                                email_data["Body"] = msg.get_payload(
                                    decode=True
                                ).decode(msg.get_content_charset())
                            except Exception as e:
                                print(f"Fehler beim Dekodieren des E-Mail-Inhalts: {e}")

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
