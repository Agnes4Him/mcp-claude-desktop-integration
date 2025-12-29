import base64
from typing import Dict


def decode_message_body(payload: Dict) -> str:
    """
    Extract text/plain body from Gmail message payload.
    """
    if payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(
            payload["body"]["data"]
        ).decode("utf-8")

    for part in payload.get("parts", []):
        if (
            part.get("mimeType") == "text/plain"
            and part.get("body", {}).get("data")
        ):
            return base64.urlsafe_b64decode(
                part["body"]["data"]
            ).decode("utf-8")

    return ""