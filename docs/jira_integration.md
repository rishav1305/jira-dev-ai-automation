# JIRA Integration Documentation

## Overview
This module facilitates interaction with the JIRA API to automate task management, issue creation, and project setup.

## Architecture
The integration follows a modular design compliant with SOLID principles:

- **`src/jira_client.py`**: Handles raw HTTP requests and authentication.
- **`src/jira_service.py`**: Contains higher-level business logic and agent capabilities.
- **`jira_agent.py`**: CLI entry point.

## Features
- **Project Creation**: Create Scrum projects programmatically.
- **Issue Management**: Create tasks, stories, spikes, etc.
- **Workflow Automation**: Transition issues and assign tasks.
- **Updates**: Add comments and details to issues.

## Usage

### CLI Commands
```bash
# Verify Connection
python3 jira_agent.py --verify

# Create Issue
python3 jira_agent.py --create-issue "Story:Title:Description"


# Move Issue
python3 jira_agent.py --move "KEY-1" --status "Done"
```

### Desktop Automation
The `create_desktop_boards.py` script automates the creation of JIRA projects for directories on the Desktop.

**Usage:**
```bash
python3 create_desktop_boards.py
```
This script:
1.  Scans `/home/rishav/Desktop` for directories.
2.  Generates a project key (e.g., `gemini-cli` -> `GC`).
3.  Creates a new JIRA project for each directory using the `JiraService`.

## Testing
Run unit tests using:
```bash
python3 -m unittest discover tests
```

