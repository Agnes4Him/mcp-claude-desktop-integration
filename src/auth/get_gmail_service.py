from utils.path_bootstrap import ensure_src_on_path
ensure_src_on_path()

import os

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]

# Resolve paths relative to THIS FILE
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")


def get_gmail_service():
    if not os.path.exists(TOKEN_FILE):
        raise RuntimeError(
            "token.json not found. Run one-time auth locally first."
        )

    creds = Credentials.from_authorized_user_file(
        TOKEN_FILE,
        scopes=GMAIL_SCOPES
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return build("gmail", "v1", credentials=creds)