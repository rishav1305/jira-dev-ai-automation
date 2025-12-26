import sys
import argparse
from src.jira_service import JiraService

def main():
    parser = argparse.ArgumentParser(description="JIRA Agent Script")
    
    # Existing commands
    parser.add_argument("--fetch", action="store_true", help="Fetch open tasks")
    parser.add_argument("--assign", type=str, help="Assign task ID to me")
    parser.add_argument("--move", type=str, help="Move task ID to a new status") 
    parser.add_argument("--status", type=str, default="In Progress", help="Target status for move command (default: 'In Progress')")
    parser.add_argument("--verify", action="store_true", help="Verify connection credentials")
    parser.add_argument("--details", type=str, help="Get details for a specific issue key")
    
    # New commands
    parser.add_argument("--create-project", type=str, help="Create a new project. Format: 'KEY:Project Name'")
    parser.add_argument("--create-issue", type=str, help="Create a new issue. Format: 'Type:Summary:Description'")
    parser.add_argument("--comment", type=str, help="Add comment to issue. Format: 'KEY:Comment Text'")

    # Update commands
    parser.add_argument("--update", type=str, help="Update an issue. Provide KEY.")
    parser.add_argument("--summary", type=str, help="New summary for the issue (used with --update)")
    parser.add_argument("--description", type=str, help="New description for the issue (used with --update)")

    args = parser.parse_args()
    
    try:
        service = JiraService()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)

    if args.verify:
        service.verify_connection()
    elif args.fetch:
        service.get_open_tasks()
    elif args.details:
        service.get_issue_details(args.details)
    elif args.assign:
        service.assign_task(args.assign)
    elif args.move:
        service.transition_issue(args.move, args.status)
    elif args.create_project:
        parts = args.create_project.split(":", 1)
        if len(parts) == 2:
            service.create_project(parts[0], parts[1])
        else:
            print("Invalid format for --create-project. Use 'KEY:Project Name'")
    elif args.create_issue:
        parts = args.create_issue.split(":", 2)
        if len(parts) == 3:
            service.create_issue(parts[1], parts[2], parts[0])
        else:
            print("Invalid format for --create-issue. Use 'Type:Summary:Description'")
    elif args.comment:
        parts = args.comment.split(":", 1)
        if len(parts) == 2:
            service.add_comment(parts[0], parts[1])
        else:
            print("Invalid format for --comment. Use 'KEY:Comment Text'")
    elif args.update:
        if not args.summary and not args.description:
            print("Error: Please provide --summary or --description with --update.")
        else:
            service.update_issue(args.update, args.summary, args.description)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
