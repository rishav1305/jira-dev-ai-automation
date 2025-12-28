import sys
import os

# Ensure current directory is in python path
sys.path.append(os.getcwd())

try:
    from src.jira_service import JiraService
    service = JiraService()
    service.get_issue_details('JDAA-4')
except Exception as e:
    print(f"Error: {e}")
