from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os

SCOPES = [
    "https://www.googleapis.com/auth/documents.readonly",
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")


def get_docs_service():
    creds = Credentials.from_authorized_user_file(
        TOKEN_FILE,
        scopes=SCOPES
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return build("docs", "v1", credentials=creds)