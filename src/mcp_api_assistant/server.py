from mcp.server import MCPServer


# Create our MCP server
mcp = MCPServer("MCP API Assistant")


@mcp.tool()
def get_demo_issue(issue_number: int) -> dict:
    """
    Return information about a demo GitHub issue.

    This is currently fake data.
    Later, this tool will call the real GitHub REST API.
    """
    return {
        "issue_number": issue_number,
        "title": "Demo MCP issue",
        "status": "open",
        "repository": "mcp-api-assistant",
        "description": "This result came from our first MCP tool.",
    }
