from api.imap_api import fetch_emails
from api.openai_api import OpenAIClient
from api.tmanager_api import check_availability


emails = fetch_emails()

for email_data in emails:

    # extract dates and flat name
    print("bla")

    # check availability

    # create response

    # move response to drafts folder


# client = OpenAIClient()
# response = client.call_openai("write a haiku about ai")
# print(response)
