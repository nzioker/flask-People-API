import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/contacts"]

CREDENTIALS_FILE_PATH = r'/home/ken/Desktop/bilaltest/contactsmanager/api/credentials.json'


def create_new_contact(first_name, phone_number, job_title, company, email, city, primaryNumberCC):
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          CREDENTIALS_FILE_PATH, SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("people", "v1", credentials=creds)
    service.people().createContact(body={
      "names": [{"givenName": first_name}], 
      "phoneNumbers": [{'value': phone_number}],
      "occupations":[{'value':job_title}],
      "organizations":[{'title':company}],
      "emailAddresses":[{'value':email}],
      "addresses": [{"city": city}], 
      "addresses": [{"countryCode": primaryNumberCC}], 
      }).execute()
    
  except HttpError as err:
    print(err)

