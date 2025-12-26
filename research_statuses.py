import sys
from src.jira_service import JiraService

def research_statuses():
    try:
        service = JiraService()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return

    projects = ["LDS", "SOC"]
    
    for project_key in projects:
        print(f"\n--- Statuses for Project: {project_key} ---")
        # Endpoint: /rest/api/3/project/{projectIdOrKey}/statuses
        data = service.client.get(f"/rest/api/3/project/{project_key}/statuses")
        
        if not data:
            print(f"Could not fetch statuses for {project_key}")
            continue
            
        # Data is a list of issue types, each containing a list of statuses
        for issue_type in data:
            type_name = issue_type.get("name")
            statuses = issue_type.get("statuses", [])
            print(f"Issue Type: {type_name}")
            for status in statuses:
                print(f"  - {status.get('name')} (ID: {status.get('id')})")

if __name__ == "__main__":
    research_statuses()
