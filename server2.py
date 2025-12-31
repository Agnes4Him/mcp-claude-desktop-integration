from mcp.server.fastmcp import FastMCP
from typing import List, Dict
import os
import base64
from email.mime.text import MIMEText

# Gmail imports (can be swapped for another provider)
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


app = FastMCP("email-mcp-server")

GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]

TOKEN_FILE = "src/auth/token.json"


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


def decode_body(payload: Dict) -> str:
    """
    Extracts text/plain content from a Gmail message payload.
    """
    if "body" in payload and payload["body"].get("data"):
        return base64.urlsafe_b64decode(
            payload["body"]["data"]
        ).decode("utf-8")

    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain":
            return base64.urlsafe_b64decode(
                part["body"]["data"]
            ).decode("utf-8")

    return ""


# Tool 1: Get unread emails

@app.tool()
def get_unread_emails(max_results: int = 10) -> List[Dict]:
    """
    Returns unread emails with sender, subject, snippet/body,
    message ID, and thread ID.
    """
    service = get_gmail_service()

    response = service.users().messages().list(
        userId="me",
        q="is:unread",
        maxResults=max_results
    ).execute()

    messages = response.get("messages", [])
    results = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        headers = msg_data["payload"]["headers"]
        header_map = {h["name"]: h["value"] for h in headers}

        body = decode_body(msg_data["payload"])

        results.append({
            "message_id": msg_data["id"],
            "thread_id": msg_data["threadId"],
            "from": header_map.get("From"),
            "subject": header_map.get("Subject"),
            "snippet": msg_data.get("snippet"),
            "body": body
        })

    return results


# Tool 2: Create a threaded draft reply

@app.tool()
def create_draft_reply(
    message_id: str,
    thread_id: str,
    reply_body: str
) -> Dict:
    """
    Creates a correctly threaded draft reply to an email.
    """
    service = get_gmail_service()

    # Fetch original message to extract headers
    original = service.users().messages().get(
        userId="me",
        id=message_id,
        format="metadata",
        metadataHeaders=["From", "Subject", "Message-ID", "References"]
    ).execute()

    headers = {h["name"]: h["value"] for h in original["payload"]["headers"]}

    mime_message = MIMEText(reply_body)
    mime_message["To"] = headers["From"]
    mime_message["Subject"] = f"Re: {headers.get('Subject', '')}"
    mime_message["In-Reply-To"] = headers.get("Message-ID")
    mime_message["References"] = headers.get("References", headers.get("Message-ID"))

    raw = base64.urlsafe_b64encode(
        mime_message.as_bytes()
    ).decode("utf-8")

    draft = service.users().drafts().create(
        userId="me",
        body={
            "message": {
                "raw": raw,
                "threadId": thread_id
            }
        }
    ).execute()

    return {
        "draft_id": draft["id"],
        "thread_id": thread_id,
        "status": "draft_created"
    }


# Entry point

if __name__ == "__main__":
    app.run()
