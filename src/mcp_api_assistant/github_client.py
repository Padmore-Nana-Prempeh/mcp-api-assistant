from typing import Any

import httpx


GITHUB_API_BASE = "https://api.github.com"
GITHUB_API_VERSION = "2026-03-10"


class GitHubAPIError(RuntimeError):
    """Raised when the GitHub API request fails."""


def get_issue(
    owner: str,
    repo: str,
    issue_number: int,
) -> dict[str, Any]:
    """
    Retrieve one issue from a public GitHub repository.
    """

    url = (
        f"{GITHUB_API_BASE}/repos/"
        f"{owner}/{repo}/issues/{issue_number}"
    )

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": GITHUB_API_VERSION,
        "User-Agent": "mcp-api-assistant",
    }

    try:
        response = httpx.get(
            url,
            headers=headers,
            timeout=10.0,
        )

        response.raise_for_status()

    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code

        if status_code == 404:
            raise GitHubAPIError(
                f"Issue #{issue_number} was not found in "
                f"{owner}/{repo}."
            ) from exc

        raise GitHubAPIError(
            f"GitHub API returned HTTP {status_code}."
        ) from exc

    except httpx.RequestError as exc:
        raise GitHubAPIError(
            f"Could not connect to GitHub: {exc}"
        ) from exc

    data = response.json()

    return {
        "issue_number": data["number"],
        "title": data["title"],
        "state": data["state"],
        "body": data.get("body"),
        "author": data["user"]["login"],
        "labels": [
            label["name"]
            for label in data.get("labels", [])
        ],
        "comments": data["comments"],
        "created_at": data["created_at"],
        "updated_at": data["updated_at"],
        "url": data["html_url"],
        "is_pull_request": "pull_request" in data,
    }
