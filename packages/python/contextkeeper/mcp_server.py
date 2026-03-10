"""contextkeeper MCP server -- expose CLI tools via Model Context Protocol."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from contextkeeper import api

mcp = FastMCP(
    name="contextkeeper",
    instructions="Zero model drift between AI agents. Universal session continuity for Claude, GPT, Gemini, and any LLM.",
)


@mcp.tool()
def contextkeeper_init(
    project: str | None = None,
    bridge: str | None = None,
    project_type: str | None = None,
) -> dict:
    """Initialize contextkeeper state files in the current project directory.

    Creates STATE_VECTOR.json, HANDOFF.md, and a .workbench config file.
    Auto-detects project type (web_app, library, ml_pipeline, etc.).

    Args:
        project: Project slug (default: current directory name)
        bridge: GitHub bridge repo e.g. 'username/workbench'
        project_type: Override auto-detected project type
    """
    return api.init(project=project, bridge=bridge, project_type=project_type)


@mcp.tool()
def contextkeeper_sync(
    bridge: str | None = None,
    dry_run: bool = False,
) -> dict:
    """Sync project state files to the GitHub bridge repo.

    Validates STATE_VECTOR.json, clones the bridge repo, copies state files,
    commits, and pushes. Requires a GitHub PAT token.

    Args:
        bridge: GitHub bridge repo e.g. 'username/workbench'
        dry_run: If true, preview what would be synced without pushing
    """
    return api.sync(bridge=bridge, dry_run=dry_run)


@mcp.tool()
def contextkeeper_status(bridge: str | None = None) -> dict:
    """Get status of all projects tracked in the bridge repo.

    Clones the bridge repo and reads STATE_VECTOR.json from each project
    directory. Returns project names, types, statuses, active tasks, and blockers.

    Args:
        bridge: GitHub bridge repo e.g. 'username/workbench'
    """
    return api.status(bridge=bridge)


@mcp.tool()
def contextkeeper_bootstrap(
    project: str = "",
    bridge: str | None = None,
    clipboard: bool = False,
) -> str:
    """Generate a paste-ready bootstrap prompt for any AI chat.

    Builds a prompt containing raw GitHub URLs to PROFILE.md, HANDOFF.md,
    and STATE_VECTOR.json. Paste this into any AI chat to restore full
    project context in under 60 seconds.

    Args:
        project: Project slug (required)
        bridge: GitHub bridge repo e.g. 'username/workbench'
        clipboard: If true, copy the prompt to the system clipboard
    """
    return api.bootstrap(project=project, bridge=bridge, clipboard=clipboard)


@mcp.tool()
def contextkeeper_doctor() -> dict:
    """Run the contextkeeper environment health check.

    Checks: Python version, git on PATH, git user config, GitHub token,
    GitHub API reachability, STATE_VECTOR.json presence and validity.
    """
    return api.doctor()


def main():
    """Entry point for contextkeeper-mcp command."""
    mcp.run()


if __name__ == "__main__":
    main()
