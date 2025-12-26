import sys
import json
from src.jira_service import JiraService

def update_board_config():
    try:
        service = JiraService()
        board_id = 45 
        
        # IDs from inspection and creation
        # Default ones for CDAA:
        todo_id = "10082" 
        inprogress_id = "10083"
        done_id = "10084"
        
        # Global ones we verified:
        ready_dev_id = "10074"
        qa_testing_id = "10081"
        po_valid_id = "10080"
        
        # Construct config
        columns_config = [
            {"name": "To Do", "statuses": [{"id": todo_id}]},
            {"name": "READY FOR DEV", "statuses": [{"id": ready_dev_id}]},
            {"name": "In Progress", "statuses": [{"id": inprogress_id}]},
            {"name": "QA TESTING", "statuses": [{"id": qa_testing_id}]},
            {"name": "PO Validation", "statuses": [{"id": po_valid_id}]},
            {"name": "Done", "statuses": [{"id": done_id}]}
        ]
        
        payload = {
            "columnConfig": {
                "columns": columns_config
            }
        }
        
        print("Updating Board 45 Configuration...")
        print(json.dumps(payload, indent=2))
        
        # Note: PUT to configuration might fail if statuses are not in workflow.
        # But for Simplified Workflow, it might auto-add them.
        # Check standard endpoint: PUT /rest/agile/1.0/board/{boardId}/configuration
        # Docs say: "Update board configuration" is not available in Cloud Agile API PUBLICLY usually?
        # Use PUT /rest/agile/1.0/board/{boardId} is for metadata.
        # Actually, there is NO public endpoint to update board configuration in Jira Cloud Agile API.
        
        # However, we can try using the internal Greenhopper API or just try the endpoint in case it works (sometimes it does for specific apps).
        # OR, we verify if we can do it.
        # If not, we fall back to notifying user.
        
        # Let's try the PUT anyway.
        # If 404 or 405, we know.
        
        resp = service.client.put(f"/rest/agile/1.0/board/{board_id}/configuration", payload)
        
        if resp:
            print("Update Successful!")
            print(json.dumps(resp, indent=2))
        else:
            print("Update Failed (Likely not supported via Public API).")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_board_config()
