# mcp-claude-desktop-integration
A project to demonstarte the integration of MCP server with Claude Desktop 

## Solutions
* Prompt:
I want you to fetch unread emails from my mail and output their summaries, ordering them based on recency. Then create drafts of replies to the email.

## `claude_desktop_config.json` file
{
    "mcpServers": {
        "Emails": {
            "command": "uv",
            "args": [
                "--directory",
                "/home/agnes/Documents/personal/projects/mcp-claude-desktop-integration/",
                "run",
                "server.py"
            ]
        }
    }
}

## Steps to run:



