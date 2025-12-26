import sys
import json
from src.jira_service import JiraService

def inspect_cdaa_board():
    try:
        service = JiraService()
        board_id = 45 # From previous output
        print(f"Fetching Configuration for Board {board_id}...")
        
        config = service.client.get(f"/rest/agile/1.0/board/{board_id}/configuration")
        if config:
            print(json.dumps(config, indent=2))
        else:
            print("Could not fetch board configuration.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_cdaa_board()
