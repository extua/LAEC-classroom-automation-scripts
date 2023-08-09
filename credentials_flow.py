import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
apiurl = 'https://www.googleapis.com/auth/'
SCOPES = [apiurl + 'classroom.courses',
          apiurl + 'classroom.announcements',
          apiurl + 'admin.directory.user']

# Define project path here
projectPath = os.path.join(os.path.expanduser('~'),'python')

def getcreds():
    # Get API authorisation
    creds = None
    credFile = os.path.join(projectPath,'credentials.json')
    tokenFile = os.path.join(projectPath,'token.json')
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(credFile) and os.path.exists(tokenFile):
        creds = Credentials.from_authorized_user_file(tokenFile, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credFile, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokenFile, 'w') as token:
            token.write(creds.to_json())
    return creds
