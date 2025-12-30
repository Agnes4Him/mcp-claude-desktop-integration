from utils.path_bootstrap import ensure_src_on_path
ensure_src_on_path()

from typing import List, Dict

from auth.get_gmail_service import get_gmail_service
from utils.decode_message_body import decode_message_body


def list_unread_messages(max_results: int = 10) -> List[Dict]:
    """
    Fetch unread Gmail messages and return parsed metadata.
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

        headers = {
            h["name"]: h["value"]
            for h in msg_data["payload"]["headers"]
        }

        results.append({
            "message_id": msg_data["id"],
            "thread_id": msg_data["threadId"],
            "from": headers.get("From"),
            "subject": headers.get("Subject"),
            "snippet": msg_data.get("snippet"),
            "body": decode_message_body(msg_data["payload"])
        })

    return results