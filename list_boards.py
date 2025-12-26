import sys
from src.jira_service import JiraService

def list_boards():
    try:
        service = JiraService()
        # Fetch all boards
        data = service.client.get("/rest/agile/1.0/board")
        if data and "values" in data:
            for board in data["values"]:
                print(f"ID: {board['id']}, Name: {board['name']}, Type: {board['type']}")
        else:
            print("No boards found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_boards()
