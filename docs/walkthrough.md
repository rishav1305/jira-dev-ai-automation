# JIRA Integration Walkthrough

## Setup
The integration is configured in `/home/rishav/.gemini/antigravity/playground/photonic-halley`.
A virtual environment has been created to manage dependencies.

## Usage
To use the JIRA agent, first activate the virtual environment (if not already active):
```bash
source venv/bin/activate
```

### 1. Verify Connection
Check if your credentials are valid:
```bash
python jira_agent.py --verify
```

### 2. Fetch Open Tasks
List all tasks in the configured project with status "READY FOR DEVELOPEMENT":
```bash
python jira_agent.py --fetch
```

### 3. View Issue Details
Get details for a specific task:
```bash
python jira_agent.py --details DEV-2
```

### 4. Take Up a Task
To assign a task to yourself (the API user), use the task key (e.g., PROJ-123):
```bash
python jira_agent.py --assign PROJ-123
```

### 5. Move Task to In Progress
To update the status of a task:
```bash
python jira_agent.py --move PROJ-123
```
Note: This defaults to moving to "In Progress".

## Troubleshooting
- **401 Unauthorized**: Check your `JIRA_USER_EMAIL` and `JIRA_API_TOKEN` in `.env`.
- **404 Not Found**: Check the `JIRA_URL` and `JIRA_PROJECT_KEY`.
- **410 Gone**: Ensure you are using the correct API endpoint (script relies on `/rest/api/3/search/jql`).
