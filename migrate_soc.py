import sys
from src.jira_service import JiraService

def migrate_project_config():
    try:
        service = JiraService()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)

    # 1. Get LDS Project ID
    print("Fetching LDS Project ID...")
    lds_data = service.client.get("/rest/api/3/project/LDS")
    if not lds_data:
        print("Error: Could not find project LDS")
        sys.exit(1)
    
    lds_id = lds_data["id"] # Numeric ID
    print(f"LDS ID: {lds_id}")

    # 2. Delete SOC (if it exists)
    print("Checking for existing SOC project...")
    soc_data = service.client.get("/rest/api/3/project/SOC")
    if soc_data:
        print("Deleting existing SOC project to recreate it...")
        # DELETE /rest/api/3/project/{projectIdOrKey}
        service.client.session = None # Hack: The Client wrapper doesn't have delete, I should add it or use requests directly.
        # Adding delete support to client or using requests.
        # Quick fix: using the service.client credentials to make a raw delete call if method not generic
        # Wait, JiraClient doesn't have delete method. I'll use `requests` directly or add it.
        # Adding `delete` to JiraClient is cleaner. But for this script I'll just use requests with headers.
        import requests
        resp = requests.delete(f"{service.client.jira_url}/rest/api/3/project/SOC", headers=service.client.headers)
        if resp.status_code in [204, 200]:
            print("Successfully deleted SOC.")
        else:
            print(f"Error deleting SOC: {resp.text}")
            sys.exit(1)
    else:
        print("SOC project does not exist (clean slate).")

    # 3. Create SOC with shared config
    print("Creating SOC project with shared configuration from LDS...")
    success = service.create_project(
        key="SOC",
        name="Social Engagement",
        shared_configuration_id=int(lds_id)
    )
    
    if success:
        print("Successfully created SOC with LDS configuration!")
    else:
        print("Failed to create SOC.")

if __name__ == "__main__":
    migrate_project_config()
