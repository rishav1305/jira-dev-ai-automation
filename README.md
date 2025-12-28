# JIRA Dev AI Automation

Automation scripts for interacting with JIRA tasks using an AI agent.

## Setup

1.  Clone this repository.
2.  Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install requests python-dotenv
    ```
4.  Copy `.env.example` to `.env` and fill in your JIRA credentials.

## Usage

Fetch tasks ready for development:
```bash
python jira_agent.py --fetch
```

## MCP Server (Model Context Protocol)
This project includes an MCP server to allow AI agents to interact with JIRA programmatically.

### Running the Server
**Local Mode (Stdio)**:
```bash
python -m src.mcp_server
```

**Remote Mode (SSE)**:
```bash
python -m src.mcp_server --transport sse --host 0.0.0.0 --port 8000
```

### Documentation
See [docs/jira_mcp_server.md](docs/jira_mcp_server.md) for detailed implementation and usage guide.
