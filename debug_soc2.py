import sys
from src.jira_service import JiraService

def check_soc2_status():
    try:
        service = JiraService()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)

    project_key = "SOC2"
    print(f"\n--- Statuses for Project: {project_key} ---")
    data = service.client.get(f"/rest/api/3/project/{project_key}/statuses")
    
    if not data:
        print(f"Could not fetch statuses for {project_key}")
        return
        
    for issue_type in data:
        type_name = issue_type.get("name")
        statuses = issue_type.get("statuses", [])
        print(f"Issue Type: {type_name}")
        for status in statuses:
            print(f"  - {status.get('name')} (ID: {status.get('id')})")

if __name__ == "__main__":
    check_soc2_status()
