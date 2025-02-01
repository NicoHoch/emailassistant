from api.imap_api import fetch_emails
from api.openai_api import OpenAIClient


emails = fetch_emails()

for email_data in emails:
    print(f"Absender: {email_data['From']}")
    print(f"Betreff: {email_data['Subject']}")
    print(
        f"Inhalt: {email_data['Body'][:100]}..."
    )  # Zeige nur die ersten 100 Zeichen des Inhalts


client = OpenAIClient()
response = client.call_openai("write a haiku about ai")
print(response)
