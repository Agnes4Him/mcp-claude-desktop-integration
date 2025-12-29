from typing import List, Dict
from mcp.server.fastmcp import FastMCP

from src.services.list_unread_messages import list_unread_messages
from src.services.create_threaded_draft import create_threaded_draft


app = FastMCP("email-mcp-server")


@app.tool()
def get_unread_emails(max_results: int = 10) -> List[Dict]:
    """
    MCP tool: fetch unread emails.
    """
    return list_unread_messages(max_results=max_results)


@app.tool()
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
    app.run()