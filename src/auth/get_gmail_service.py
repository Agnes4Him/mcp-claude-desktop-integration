from utils.path_bootstrap import ensure_src_on_path
ensure_src_on_path()

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]

def get_gmail_service():
    """
    Authenticate and return a Gmail API service client.
    """
    creds = Credentials.from_authorized_user_file(
        "token.json",
        scopes=GMAIL_SCOPES
    )
    return build("gmail", "v1", credentials=creds)