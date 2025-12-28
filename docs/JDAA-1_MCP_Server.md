# JDAA-1: JIRA MCP Server Implementation Guide

## Overview
This document details the implementation of the JIRA Model Context Protocol (MCP) Server. The server allows AI agents and external applications to interact with the JIRA instance programmatically using standardized MCP tools.

## Features
The following JIRA capabilities are exposed as MCP tools:
- **Project Management**: `create_project`
- **Issue Handling**: `create_issue`, `update_issue`, `get_issue`
- **Workflow**: `transition_issue`
- **Collaboration**: `add_comment`
- **Search**: `search_tasks` (JQL support)

## Installation & Setup

### Prerequisites
- Python 3.10+
- `mcp` python package
- `requests` python package
- A valid `.env` file with JIRA credentials (`JIRA_URL`, `JIRA_API_TOKEN`, `JIRA_EMAIL`).

### Running the Server

#### 1. Local Mode (Stdio)
For use with local AI agents (e.g., Claude Desktop, local scripts).
```bash
python -m src.mcp_server
```

#### 2. Remote Mode (SSE)
For access from different servers or networked agents.
```bash
# Default: Runs on 0.0.0.0:8000
python -m src.mcp_server --transport sse

# Custom Host/Port
python -m src.mcp_server --transport sse --host 0.0.0.0 --port 8080
```

## Client Implementation

### How to call from a separate project
To interact with this server from another Python project, use the `mcp` client library.

#### Example Code (`client_sse_test.py`)
```python
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def run_client():
    # URL of your running SSE server
    sse_url = "http://<SERVER_IP>:8000/sse"

    print(f"Connecting to {sse_url}...")
    
    # Connect using sse_client context manager
    async with sse_client(sse_url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print(f"Connected to server with tools: {[t.name for t in tools.tools]}")
            
            # Call a tool (e.g., Get Issue Details)
            result = await session.call_tool("get_issue", {"issue_key": "JDAA-1"})
            
            # Process result
            for content in result.content:
                if content.type == "text":
                    print(f"Result: {content.text}")

if __name__ == "__main__":
    asyncio.run(run_client())
```

### Tool Reference

| Tool Name | Arguments | Description |
|-----------|-----------|-------------|
| `create_project` | `key` (str), `name` (str) | Creates a new software project. |
| `create_issue` | `summary` (str), `description` (str), `issue_type` (str, default="Task"), `project_key` (str, opt) | Creates a new issue. |
| `update_issue` | `issue_key` (str), `summary` (str, opt), `description` (str, opt) | Updates summary or description. |
| `transition_issue` | `issue_key` (str), `status_name` (str) | Moves issue to a new status (e.g., "In Progress"). |
| `add_comment` | `issue_key` (str), `comment_text` (str) | Adds a comment to the issue. |
| `get_issue` | `issue_key` (str) | Returns JSON details of an issue. |
| `search_tasks` | `jql` (str) | Returns a list of issues matching the JQL query. |
