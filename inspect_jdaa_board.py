import sys
import json
from src.jira_service import JiraService

def inspect_board_config(board_id):
    try:
        service = JiraService()
        print(f"Fetching Configuration for Board {board_id}...")
        config = service.client.get(f"/rest/agile/1.0/board/{board_id}/configuration")
        if config:
            print(json.dumps(config, indent=2))
        else:
            print("Could not fetch board configuration.")
            
        # Also let's see the board metadata to find the project
        board_info = service.client.get(f"/rest/agile/1.0/board/{board_id}")
        if board_info:
             print("\nBoard Info:")
             print(json.dumps(board_info, indent=2))
             
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_board_config(11)
