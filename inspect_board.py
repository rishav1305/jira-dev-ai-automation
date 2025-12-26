import sys
import json
from src.jira_service import JiraService

def inspect_board():
    try:
        service = JiraService()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)

    # 1. Get Board
    print("Fetching Board for SOC2...")
    # This requires the Agile API which might be under a different path convention in our client?
    # Our client base URL is standard. We just append endpoint.
    data = service.client.get("/rest/agile/1.0/board?projectKeyOrId=SOC2")
    
    if not data or "values" not in data or not data["values"]:
        print("No board found for SOC2.")
        return

    board = data["values"][0] # Assume first board
    board_id = board["id"]
    print(f"Found Board: {board['name']} (ID: {board_id}, Type: {board['type']})")

    # 2. Get Configuration
    print(f"Fetching Configuration for Board {board_id}...")
    config = service.client.get(f"/rest/agile/1.0/board/{board_id}/configuration")
    if config:
        print(json.dumps(config, indent=2))
    else:
        print("Could not fetch board configuration.")

if __name__ == "__main__":
    inspect_board()
