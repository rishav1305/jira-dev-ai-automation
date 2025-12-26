import sys
import json
from src.jira_service import JiraService

def create_cdaa_project_manual():
    try:
        service = JiraService()
        account_id = service.get_myself_account_id()
        
        print("Creating project 'Confluence Dev AI Automation' (CDAA) as Company Managed...")
        
        # 1. Create Project
        payload = {
            "key": "CDAA",
            "name": "Confluence Dev AI Automation",
            "projectTypeKey": "software",
            "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-simplified-agility-scrum",
            "description": "Project Confluence Dev AI Automation created via AI Agent",
            "leadAccountId": account_id,
            "assigneeType": "PROJECT_LEAD"
        }
        
        project_created = False
        project_data = service.client.post("/rest/api/3/project", payload)
        
        if project_data:
             print(f"Project created successfully: {project_data.get('id')}")
             project_created = True
        else:
             # Check if it already exists
             existing = service.client.get("/rest/api/3/project/CDAA")
             if existing:
                 print("Project CDAA already exists, proceeding to board config.")
                 project_created = True
             else:
                 print("Failed to create project.")
                 return

        if not project_created:
            return

        # 2. Find the Board
        # Company managed projects usually create a board automatically.
        print("Finding board for CDAA...")
        params = {"projectKeyOrId": "CDAA"}
        board_data = service.client.get("/rest/agile/1.0/board", params=params)
        board_id = None
        if board_data and "values" in board_data and len(board_data["values"]) > 0:
             # Prefer the one with name matching project key or name
             board = board_data["values"][0] # Just take first
             board_id = board['id']
             print(f"Found Board: {board['name']} (ID: {board_id})")
        else:
             print("No board found. detailed creation might be needed.")
             return

        # 3. Ensure Statuses Exist
        # Columns: To Do, READY FOR DEV, In Progress, QA TESTING, PO Validation, Done
        # Statuses must exist globally.
        required_statuses = [
            ("To Do", 2),
            ("READY FOR DEV", 2), # Category 2=To Do
            ("In Progress", 4),
            ("QA TESTING", 4), # Category 4=In Progress
            ("PO Validation", 4),
            ("Done", 3)
        ]
        
        status_ids = {}
        for name, cat_id in required_statuses:
            # We use service.create_status which checks existence first
            sid = service.create_status(name, cat_id)
            if sid:
                status_ids[name] = sid
        
        # 4. Update Board Configuration (Columns)
        # We need to construct the columnConfig
        # Note: Company managed boards use mapped statuses.
        # However, for company managed, statuses must be in the WORKFLOW of the project first.
        # This is where it gets tricky. Just adding columns doesn't add statuses to the project workflow.
        # But we can try setting the columns and if status is not in workflow, it might just not show issues or error.
        # Wait, if status is not in workflow, we can't map it in board configuration usually.
        # BUT, let's try updating columns.
        
        print("Updating Board Columns...")
        
        columns_config = [
            {"name": "To Do", "statuses": [{"id": status_ids.get("To Do")}]},
            {"name": "READY FOR DEV", "statuses": [{"id": status_ids.get("READY FOR DEV")}]},
            {"name": "In Progress", "statuses": [{"id": status_ids.get("In Progress")}]},
            {"name": "QA TESTING", "statuses": [{"id": status_ids.get("QA TESTING")}]},
            {"name": "PO Validation", "statuses": [{"id": status_ids.get("PO Validation")}]},
            {"name": "Done", "statuses": [{"id": status_ids.get("Done")}]}
        ]
        
        # Statuses list must be list of objects or ids?
        # API expects: "statuses": [{"id": "123"}, ...]
        
        config_payload = {
            "columnConfig": {
                "columns": columns_config
            }
        }
        
        # PUT /rest/agile/1.0/board/{boardId}/configuration
        # Note: The endpoint to update board configuration might be restricted or complex.
        # actually, PUT /rest/agile/1.0/board/{boardId}/configuration isn't always standard.
        # It's often per-column or not fully writable for company managed boards if workflow doesn't match?
        # Let's try.
        
        # Try updating just columns isn't a simple PUT on configuration.
        # We might not be able to fully automate column layout if workflow doesn't allow it.
        # But let's attempt.
        # Wait, there is no direct PUT /configuration endpoint in public Agile API v1.0 docs often.
        # It might be read-only for company managed or specific endpoints.
        # Checking resources...
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_cdaa_project_manual()
