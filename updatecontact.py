import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/contacts"]

CREDENTIALS_FILE_PATH = r'/home/ken/Desktop/bilaltest/contactsmanager/api/credentials.json'

def update_contact_information(names, new_name, phone_number):
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          CREDENTIALS_FILE_PATH, SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("people", "v1", credentials=creds)
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=100,
        personFields='names,emailAddresses').execute()
    
    connections = results.get('connections', [])
    for contact in connections:
        if contact["names"][0]["displayName"] == names:
            service.people().updateContact(resourceName=contact['resourceName'],
                                        updatePersonFields="names",
                                        personFields="names, phoneNumbers", 
                                        body={
                                            "etag": contact["etag"],
                                            "names": [
                                                {
                                                "familyName": new_name,
                                                
                                                }
                                            ],
                                            "phoneNumbers": [{'value': phone_number}],
                                          
                                            }
                                        ).execute() 
  except HttpError as err:
    print(err)
