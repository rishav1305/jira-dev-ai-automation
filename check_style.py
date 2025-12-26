import sys
import json
from src.jira_service import JiraService

def check_jdaa_style():
    try:
        service = JiraService()
        print("Fetching JDAA Project Info...")
        project = service.client.get("/rest/api/3/project/JDAA")
        if project:
            print(f"Name: {project['name']}")
            print(f"Style: {project.get('style')}")
            print(f"Properties: {project.get('properties')}")
            print(json.dumps(project, indent=2))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_jdaa_style()
