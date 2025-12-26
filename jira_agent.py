import sys
import argparse
from src.jira_service import JiraService

def main():
    parser = argparse.ArgumentParser(description="JIRA Agent CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Verify
    parser_verify = subparsers.add_parser("verify", help="Verify connection credentials")

    # Fetch
    parser_fetch = subparsers.add_parser("fetch", help="Fetch open tasks ready for development")

    # Details
    parser_details = subparsers.add_parser("details", help="Get details for a specific issue")
    parser_details.add_argument("key", type=str, help="Issue Key (e.g., JDAA-1)")

    # Assign
    parser_assign = subparsers.add_parser("assign", help="Assign an issue")
    parser_assign.add_argument("key", type=str, help="Issue Key")
    parser_assign.add_argument("--user", type=str, help="Account ID (Optional, defaults to self)")

    # Move (Transition)
    parser_move = subparsers.add_parser("move", help="Transition an issue to a new status")
    parser_move.add_argument("key", type=str, help="Issue Key")
    parser_move.add_argument("status", type=str, help="Target Status (e.g., 'In Progress')")

    # Comment
    parser_comment = subparsers.add_parser("comment", help="Add a comment to an issue")
    parser_comment.add_argument("key", type=str, help="Issue Key")
    parser_comment.add_argument("text", type=str, help="Comment text")

    # Create Issue
    parser_create = subparsers.add_parser("create", help="Create a new issue")
    parser_create.add_argument("summary", type=str, help="Issue Summary")
    parser_create.add_argument("description", type=str, help="Issue Description")
    parser_create.add_argument("--type", type=str, default="Task", help="Issue Type (default: Task)")
    parser_create.add_argument("--project", type=str, help="Project Key (Optional)")

    # Create Project
    parser_project = subparsers.add_parser("create-project", help="Create a new project")
    parser_project.add_argument("key", type=str, help="Project Key")
    parser_project.add_argument("name", type=str, help="Project Name")

    # Update
    parser_update = subparsers.add_parser("update", help="Update an issue")
    parser_update.add_argument("key", type=str, help="Issue Key")
    parser_update.add_argument("--summary", type=str, help="New Summary")
    parser_update.add_argument("--description", type=str, help="New Description")

    # Promote (Composite Action)
    parser_promote = subparsers.add_parser("promote", help="Promote an issue to a status and comment")
    parser_promote.add_argument("key", type=str, help="Issue Key")
    parser_promote.add_argument("status", type=str, help="Target Status")
    parser_promote.add_argument("--comment", type=str, required=True, help="Comment text")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        service = JiraService()
    except Exception as e:
        print(f"Error initializing JiraService: {e}")
        sys.exit(1)

    if args.command == "verify":
        service.verify_connection()
    elif args.command == "fetch":
        service.get_open_tasks()
    elif args.command == "details":
        service.get_issue_details(args.key)
    elif args.command == "assign":
        service.assign_task(args.key, args.user)
    elif args.command == "move":
        service.transition_issue(args.key, args.status)
    elif args.command == "comment":
        service.add_comment(args.key, args.text)
    elif args.command == "create":
        service.create_issue(args.summary, args.description, args.type, args.project)
    elif args.command == "create-project":
        service.create_project(args.key, args.name)
    elif args.command == "update":
        if not args.summary and not args.description:
            print("Error: Provide --summary or --description to update.")
        else:
            service.update_issue(args.key, args.summary, args.description)
    elif args.command == "promote":
        print(f"Promoting {args.key} to '{args.status}'...")
        if service.add_comment(args.key, args.comment):
            service.transition_issue(args.key, args.status)
        service.get_issue_details(args.key)

if __name__ == "__main__":
    main()
