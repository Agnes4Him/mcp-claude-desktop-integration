import sys
import os
from pathlib import Path
from typing import List, Dict

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# bootstrap src/ onto sys.path
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from src.services.list_unread_messages import list_unread_messages
from src.services.get_email_style_guide import get_email_style_guide
from src.services.create_threaded_draft import create_threaded_draft

# Load environment variables from .env
load_dotenv()


mcp = FastMCP(
    name="email-mcp-server"
    )

EMAIL_STYLE_GUIDE_DOC_ID = os.getenv("EMAIL_STYLE_GUIDE_DOC_ID")

if not EMAIL_STYLE_GUIDE_DOC_ID:
    raise RuntimeError(
        "EMAIL_STYLE_GUIDE_DOC_ID is not set. "
        "Add it to your .env file."
    )

'''@mcp.tool()
def health_check() -> str:
    """
    MCP tool: health check.
    """
    return "OK"  '''

@mcp.tool()
def get_unread_emails(max_results: int = 10) -> List[Dict]:
    """
    MCP tool: fetch unread emails.
    """
    return list_unread_messages(max_results=max_results)


@mcp.tool()
def fetch_email_style_guide(doc_id: str | None = None) -> str:
    """
    Fetches an email style guide from Google Docs to guide email replies.
    """
    return get_email_style_guide(doc_id or EMAIL_STYLE_GUIDE_DOC_ID)

@mcp.tool()
def create_draft_reply(
    message_id: str,
    thread_id: str,
    reply_body: str
) -> Dict:
    """
    MCP tool: create a threaded draft reply.
    """
    return create_threaded_draft(
        message_id=message_id,
        thread_id=thread_id,
        reply_body=reply_body
    )


if __name__ == "__main__":
    mcp.run()