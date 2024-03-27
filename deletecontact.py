import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/contacts"]

CREDENTIALS_FILE_PATH = r'/home/ken/Desktop/bilaltest/contactsmanager/api/credentials.json'

def delete_contacts_with_resourceName(number_of_contact):
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
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=number_of_contact,
        personFields='names,emailAddresses,phoneNumbers').execute()
    
    connections = results.get('connections', [])
    
    for person in connections:
        abcd = person.get('resourceName')
        print(abcd)
        service.people().deleteContact(resourceName=abcd).execute()
    
  except HttpError as err:
    print(err)

