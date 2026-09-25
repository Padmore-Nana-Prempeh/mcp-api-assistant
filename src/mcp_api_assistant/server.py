from mcp.server import MCPServer

from mcp_api_assistant.github_client import (
    GitHubAPIError,
    get_issue,
)


mcp = MCPServer("MCP API Assistant")


@mcp.tool()
def get_github_issue(
    owner: str,
    repo: str,
    issue_number: int,
) -> dict:
    """
    Retrieve an issue from a public GitHub repository.

    Args:
        owner: GitHub username or organization that owns the repository.
        repo: Repository name.
        issue_number: GitHub issue number.
    """

    try:
        return get_issue(
            owner=owner,
            repo=repo,
            issue_number=issue_number,
        )

    except GitHubAPIError as exc:
        return {
            "error": str(exc),
            "owner": owner,
            "repo": repo,
            "issue_number": issue_number,
        }
