import base64
from typing import Dict
from email.mime.text import MIMEText

from auth.get_gmail_service import get_gmail_service


def create_threaded_draft(
    message_id: str,
    thread_id: str,
    reply_body: str
) -> Dict:
    """
    Create a properly threaded Gmail draft reply.
    """
    service = get_gmail_service()

    original = service.users().messages().get(
        userId="me",
        id=message_id,
        format="metadata",
        metadataHeaders=["From", "Subject", "Message-ID", "References"]
    ).execute()

    headers = {
        h["name"]: h["value"]
        for h in original["payload"]["headers"]
    }

    mime_message = MIMEText(reply_body)
    mime_message["To"] = headers["From"]
    mime_message["Subject"] = f"Re: {headers.get('Subject', '')}"
    mime_message["In-Reply-To"] = headers.get("Message-ID")
    mime_message["References"] = headers.get(
        "References",
        headers.get("Message-ID")
    )

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