# Issue: JDAA-3

**Summary**: Attach the CONFLUENCE MCP Server to this and make proper documentation
**Status**: IN PROGRESS
**Assignee**: Rishav Chatterjee
**Priority**: Medium
**Link**: https://rishavchatterjee.atlassian.net/browse/JDAA-3

## Description
Setup the CONFLUENCE MCP server for the following tasks. All of this should be done using the MCP Server `http://unified-mcp-server:8080` with the least lines of code.

## Implementation Details
The Unified MCP Server has been re-implemented in `src/server.py` to support both JIRA and Confluence.

### Components
- `src/server.py`: Unified FastMCP Server.
- `src/clients/confluence_client.py`: Confluence API wrapper.
- `src/clients/jira_client.py`: JIRA API wrapper.

### Usage
See [Using Unified Server](using_unified_server.md) for details.
