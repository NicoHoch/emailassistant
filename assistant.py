from api.imap_api import fetch_emails

emails = fetch_emails()
for email_data in emails:
    print(f"Absender: {email_data['From']}")
    print(f"Betreff: {email_data['Subject']}")
    print(
        f"Inhalt: {email_data['Body'][:100]}..."
    )  # Zeige nur die ersten 100 Zeichen des Inhalts
