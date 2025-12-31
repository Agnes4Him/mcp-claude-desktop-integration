from google_auth_oauthlib.flow import InstalledAppFlow

GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]

TOKEN_FILE = "token.json"
CLIENT_SECRETS_FILE = "credentials.json"

flow = InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    GMAIL_SCOPES
)

creds = flow.run_local_server(port=0)

with open(TOKEN_FILE, "w") as f:
    f.write(creds.to_json())

print("token.json created successfully")