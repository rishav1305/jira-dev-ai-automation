from mcp.server.fastmcp import FastMCP
import sys
import os

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.clients.jira_client import JiraClient
from src.clients.confluence_client import ConfluenceClient
import json
import os
import argparse

# Initialize Server
mcp = FastMCP("Unified Atlassian MCP")

# Initialize Clients
# We wrap them in try-except to allow partial functionality if env vars are missing for one
try:
    jira = JiraClient()
    jira_available = True
except Exception as e:
    print(f"JIRA Unavailable: {e}")
    jira_available = False

try:
    confluence = ConfluenceClient()
    confluence_available = True
except Exception as e:
    print(f"Confluence Unavailable: {e}")
    confluence_available = False

# --- JIRA Tools ---
if jira_available:
    @mcp.tool()
    def create_project(key: str, name: str) -> str:
        """Create a new JIRA Project."""
        try:
            res = jira.create_project(key, name)
            return json.dumps(res, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"

    @mcp.tool()
    def create_issue(summary: str, description: str, issue_type: str="Task", project_key: str=None) -> str:
        """Create JIRA Issue."""
        try:
            res = jira.create_issue(summary, description, issue_type, project_key)
            return f"Created: {res.get('key')}"
        except Exception as e:
            return f"Error: {str(e)}"

    @mcp.tool()
    def update_issue(key: str, summary: str=None, description: str=None) -> str:
        """Update JIRA Issue."""
        try:
            jira.update_issue(key, summary, description)
            return f"Updated {key}"
        except Exception as e:
            return f"Error: {str(e)}"

    @mcp.tool()
    def transition_issue(key: str, status: str) -> str:
        """Transition JIRA Issue."""
        try:
            jira.transition_issue(key, status)
            return f"Transitioned {key} to {status}"
        except Exception as e:
            return f"Error: {str(e)}"

    @mcp.tool()
    def add_comment(key: str, body: str) -> str:
        """Add Comment to JIRA Issue."""
        try:
            jira.add_comment(key, body)
            return f"Comment added to {key}"
        except Exception as e:
            return f"Error: {str(e)}"

    @mcp.tool()
    def get_issue(key: str) -> str:
        """Get JIRA Issue Details."""
        try:
            res = jira.get_issue(key)
            return json.dumps(res, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"

    @mcp.tool()
    def search_tasks(jql: str) -> str:
        """Search JIRA Tasks."""
        try:
            res = jira.search_tasks(jql)
            return json.dumps(res, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"

# --- Confluence Tools ---
if confluence_available:
    @mcp.tool()
    def get_page(page_id: str) -> str:
        """Get Confluence Page."""
        try:
            res = confluence.get_page(page_id)
            return json.dumps(res, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"

    @mcp.tool()
    def create_page(space_key: str, title: str, body: str, parent_id: str = None) -> str:
        """Create Confluence Page."""
        try:
            res = confluence.create_page(space_key, title, body, parent_id)
            return json.dumps(res, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"

    @mcp.tool()
    def update_page(page_id: str, title: str, body: str, version_number: int) -> str:
        """Update Confluence Page."""
        try:
            res = confluence.update_page(page_id, title, body, version_number)
            return json.dumps(res, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"

    @mcp.tool()
    def search_pages(cql: str) -> str:
        """Search Confluence Pages."""
        try:
            res = confluence.search_pages(cql)
            return json.dumps(res, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"

    @mcp.tool()
    def get_page_id(title: str, space_key: str = None) -> str:
        """Get Confluence Page ID."""
        try:
            res = confluence.get_page_id(title, space_key)
            return str(res) if res else "Not Found"
        except Exception as e:
            return f"Error: {str(e)}"

    @mcp.tool()
    def create_space(key: str, name: str, description: str = None) -> str:
        """Create Confluence Space."""
        try:
            res = confluence.create_space(key, name, description)
            return json.dumps(res, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unified MCP Server")
    parser.add_argument("--transport", default=os.environ.get("MCP_TRANSPORT", "stdio"), choices=["stdio", "sse"], help="Transport protocol")
    parser.add_argument("--host", default=os.environ.get("MCP_HOST", "0.0.0.0"), help="Host for SSE")
    parser.add_argument("--port", type=int, default=int(os.environ.get("MCP_PORT", "8080")), help="Port for SSE") # Default to 8080 as per user requirement
    
    args = parser.parse_args()
    
    if args.transport == "sse":
        print(f"Starting Unified SSE server on {args.host}:{args.port}")
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        if args.host not in ("127.0.0.1", "localhost", "::1"):
             mcp.settings.transport_security = None
        mcp.run(transport="sse")
    else:
        mcp.run(transport="stdio")
