import os
import sys
import requests
import json
from base64 import b64encode
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_USER_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_API_TOKEN")
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

if not all([JIRA_URL, JIRA_EMAIL, JIRA_TOKEN, PROJECT_KEY]):
    print("Error: Missing JIRA configuration. Please check your .env file.")
    sys.exit(1)

AUTH_STRING = f"{JIRA_EMAIL}:{JIRA_TOKEN}"
AUTH_HEADER = {
    "Authorization": f"Basic {b64encode(AUTH_STRING.encode('utf-8')).decode('utf-8')}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def get_open_tasks():
    """Fetch tasks with status 'READY FOR DEVELOPMENT' for the configured project."""
    jql = f"project = {PROJECT_KEY} AND status = 'READY FOR DEVELOPMENT'"
    url = f"{JIRA_URL}/rest/api/3/search/jql"
    
    payload = {
        "jql": jql,
        "fields": ["summary", "status", "assignee"]
    }

    try:
        response = requests.post(url, headers=AUTH_HEADER, json=payload)
        response.raise_for_status()
        data = response.json()
        
        issues = data.get("issues", [])
        if not issues:
            print("No 'READY FOR DEVELOPMENT' tasks found.")
            return []
            
        print(f"Found {len(issues)} open tasks:")
        for issue in issues:
            key = issue["key"]
            summary = issue["fields"]["summary"]
            print(f"[{key}] {summary}")
        return issues
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tasks: {e}")
        if response.text:
             print(f"Response: {response.text}")
        return []

def assign_task(issue_key):
    """Assign the task to the authenticated user."""
    # First get the user's account ID (myself)
    # Actually, for Atlassian Cloud, we assign by accountId. 
    # Let's get "myself" first.
    
    myself_url = f"{JIRA_URL}/rest/api/3/myself"
    try:
        r = requests.get(myself_url, headers=AUTH_HEADER)
        r.raise_for_status()
        account_id = r.json()["accountId"]
    except Exception as e:
        print(f"Error getting user info: {e}")
        return False

    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}/assignee"
    payload = {
        "accountId": account_id
    }
    
    try:
        response = requests.put(url, headers=AUTH_HEADER, json=payload)
        response.raise_for_status()
        print(f"Successfully assigned {issue_key} to me.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error assigning task: {e}")
        return False

def transition_task(issue_key, status_name="In Progress"):
    """Move the task to a new status."""
    # First need to find the transition ID for "In Progress"
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}/transitions"
    try:
        r = requests.get(url, headers=AUTH_HEADER)
        r.raise_for_status()
        transitions = r.json().get("transitions", [])
        
        target_id = None
        for t in transitions:
            if t["name"].lower() == status_name.lower():
                target_id = t["id"]
                break
        
        if not target_id:
            print(f"Transition '{status_name}' not found for {issue_key}. Available: {[t['name'] for t in transitions]}")
            return False
            
        payload = {
            "transition": {
                "id": target_id
            }
        }
        
        r = requests.post(url, headers=AUTH_HEADER, json=payload)
        r.raise_for_status()
        print(f"Successfully moved {issue_key} to '{status_name}'.")
        return True

    except Exception as e:
         print(f"Error transitioning task: {e}")
         return False

def verify_connection():
    """Verify credentials by fetching the current user's profile."""
    url = f"{JIRA_URL}/rest/api/3/myself"
    try:
        response = requests.get(url, headers=AUTH_HEADER)
        response.raise_for_status()
        data = response.json()
        print(f"Connection Successful! Logged in as: {data['displayName']} ({data['emailAddress']})")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Connection Failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
             print(f"Status Code: {e.response.status_code}")
             print(f"Response: {e.response.text}")
        return False

def get_issue_details(issue_key):
    """Fetch and print details for a specific issue."""
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}"
    try:
        response = requests.get(url, headers=AUTH_HEADER)
        response.raise_for_status()
        issue = response.json()
        
        fields = issue["fields"]
        summary = fields["summary"]
        status = fields["status"]["name"]
        description = fields.get("description")
        # Description in API v3 is often a rich text structure (Atlassian Document Format)
        # We'll just print that it exists or try to extract text if simple, 
        # but for now printing the raw repr or just summary/status is enough for verification.
        
        print(f"--- Issue: {issue_key} ---")
        print(f"Summary: {summary}")
        print(f"Status: {status}")
        print(f"Link: {JIRA_URL}/browse/{issue_key}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error fetching issue {issue_key}: {e}")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="JIRA Agent Script")
    parser.add_argument("--fetch", action="store_true", help="Fetch open tasks")
    parser.add_argument("--assign", type=str, help="Assign task ID to me")
    parser.add_argument("--move", type=str, help="Move task ID to 'In Progress'")
    parser.add_argument("--verify", action="store_true", help="Verify connection credentials")
    parser.add_argument("--details", type=str, help="Get details for a specific issue key")
    
    args = parser.parse_args()
    
    if args.verify:
        verify_connection()
    elif args.fetch:
        get_open_tasks()
    elif args.details:
        get_issue_details(args.details)
    elif args.assign:
        assign_task(args.assign)
    elif args.move:
        transition_task(args.move)
    else:
        parser.print_help()
