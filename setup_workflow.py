from src.jira_service import JiraService
import sys

def main():
    try:
        service = JiraService()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
        
    service.setup_soc_statuses()

if __name__ == "__main__":
    main()
