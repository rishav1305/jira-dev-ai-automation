# Using the Unified MCP Server

This project now uses a **Unified MCP Server** that provides both JIRA and Confluence capabilities.

## Server Details
- **Location**: `src/server.py`
- **Clients**: Wrappers around `atlassian-python-api` in `src/clients/`.
- **Default Port**: 8080 (SSE)

## Configuration
Ensure your `.env` file contains the following:

```ini
# JIRA Configuration
JIRA_URL=https://your-domain.atlassian.net
JIRA_USER_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-api-token

# Confluence Configuration
CONFLUENCE_URL=https://your-domain.atlassian.net
CONFLUENCE_USER_EMAIL=your-email@example.com
CONFLUENCE_API_TOKEN=your-api-token

# Server
MCP_SERVER_URL=http://localhost:8080/sse
```

## Running the Server
```bash
python src/server.py --transport sse --port 8080
```

## Tools Available
### Confluence
- `get_page(page_id)`
- `create_page(space_key, title, body)`
- `update_page(page_id, title, body, version_number)`
- `search_pages(cql)`
- `get_page_id(title, space_key)`
- `create_space(key, name)`

### JIRA
- `create_project(key, name)`
- `create_issue(summary, description, ...)`
- `update_issue(key, ...)`
- `transition_issue(key, status)`
- `add_comment(key, body)`
- `get_issue(key)`
- `search_tasks(jql)`
