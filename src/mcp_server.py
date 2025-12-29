from mcp.server.fastmcp import FastMCP
from .jira_service import JiraService
import json
import argparse
import os

# Initialize the MCP Server
mcp = FastMCP("Jira Automation")

# Initialize Jira Service
# We initialize it globally or lazily. 
# For FastMCP, we can just instantiate it.
jira_service = JiraService()

@mcp.tool()
def create_project(key: str, name: str) -> str:
    """Create a new JIRA Project."""
    if jira_service.create_project(key, name):
        return f"Project {name} ({key}) created successfully."
    return f"Failed to create project {name} ({key})."

@mcp.tool()
def create_issue(summary: str, description: str, issue_type: str = "Task", project_key: str = None) -> str:
    """Create a new JIRA Issue."""
    key = jira_service.create_issue(summary, description, issue_type, project_key)
    if key:
        return f"Created {issue_type}: {key}"
    return "Failed to create issue."

@mcp.tool()
def update_issue(issue_key: str, summary: str = None, description: str = None) -> str:
    """Update an issue's summary or description."""
    if jira_service.update_issue(issue_key, summary, description):
        return f"Updated {issue_key}."
    return f"Failed to update {issue_key}."

@mcp.tool()
def transition_issue(issue_key: str, status_name: str) -> str:
    """Move an issue to a new status."""
    if jira_service.transition_issue(issue_key, status_name):
        return f"Moved {issue_key} to {status_name}."
    return f"Failed to transition {issue_key}."

@mcp.tool()
def add_comment(issue_key: str, comment_text: str) -> str:
    """Add a comment to an issue."""
    if jira_service.add_comment(issue_key, comment_text):
        return f"Comment added to {issue_key}."
    return f"Failed to add comment to {issue_key}."

@mcp.tool()
def get_issue(issue_key: str) -> str:
    """Get issue details."""
    # JiraService prints to stdout, we need to capture it or modify JiraService to return data.
    # Current JiraService prints. We should modify JiraService to return dict or text, 
    # OR we capture stdout.
    # For a robust tool, it's better if JiraService returns data.
    # But as per "Strictly wrap", we might need to rely on what we have or modify JiraService (refactoring).
    # Since I cannot easily verify if I can refactor JiraService deeply without user approval (though I have broad approval),
    # I will assume I can refactor JiraService slightly or just use it.
    # The current JiraService.get_issue_details prints.
    # I will modify this tool to return a message saying "Check stdout" or usage of a new method if I add one.
    # Let's try to capture logic.
    
    # Actually, looking at JiraService, it returns True/False.
    # I will stick to basic success/fail for now, or maybe reads the print? No.
    # I'll implement a new method in JiraService via `src/jira_service_extension.py` or just add it here
    # accessing client directly?
    
    # Best approach: Use `jira_service.client` to get data again? 
    # Or just say "Details fetched (check logs)"? 
    # The requirement is "Expose capabilities". The Agent using this tool wants the data back.
    # So I MUST return the data.
    
    data = jira_service.client.get(f"/rest/api/3/issue/{issue_key}")
    if data:
        fields = data.get("fields", {})
        summary = fields.get("summary")
        status = fields.get("status", {}).get("name")
        return json.dumps({"key": issue_key, "summary": summary, "status": status}, indent=2)
    return "Issue not found."

@mcp.tool()
def search_tasks(jql: str) -> str:
    """Search tasks using JQL."""
    payload = {
        "jql": jql,
        "fields": ["summary", "status", "assignee"]
    }
    data = jira_service.client.post("/rest/api/3/search/jql", payload)
    if data:
        issues = data.get("issues", [])
        return json.dumps([{"key": i["key"], "summary": i["fields"]["summary"]} for i in issues], indent=2)
    return "No issues found or error."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jira MCP Server")
    parser.add_argument("--transport", default=os.environ.get("MCP_TRANSPORT", "stdio"), choices=["stdio", "sse"], help="Transport protocol")
    parser.add_argument("--host", default=os.environ.get("MCP_HOST", "0.0.0.0"), help="Host for SSE")
    parser.add_argument("--port", type=int, default=int(os.environ.get("MCP_PORT", "8000")), help="Port for SSE")
    
    args = parser.parse_args()
    
    if args.transport == "sse":
        print(f"Starting SSE server on {args.host}:{args.port}")
        # Configure host/port on the instance
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        
        # If binding to non-local host, we must adjust transport security
        # properly or disable it, otherwise remote requests will be blocked (403/421).
        if args.host not in ("127.0.0.1", "localhost", "::1"):
            print("Binding to non-local host, disabling DNS rebinding protection.")
            mcp.settings.transport_security = None
            
        mcp.run(transport="sse")
    else:
        mcp.run(transport="stdio")
