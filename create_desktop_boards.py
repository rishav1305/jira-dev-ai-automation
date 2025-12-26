import os
import re
from src.jira_service import JiraService

DESCRIPTION = "Creating JIRA boards for Desktop items"
DESKTOP_PATH = "/home/rishav/Desktop"

def generate_project_key(name):
    """
    Generates a JIRA project key from a directory name.
    Heuristic:
    - Split by '-' or '_'
    - If multiple parts: Take first letter of each part (e.g., 'jira-dev-ai' -> 'JDA').
    - If one part: Take first 4 characters upper-cased.
    - If resulting key < 2 chars, append 'X' or take more chars.
    """
    clean_name = re.sub(r'[^\w\s-]', '', name) # Remove special chars
    parts = re.split(r'[-_ ]+', clean_name)
    parts = [p for p in parts if p] # Filter empty
    
    if not parts:
        return "UNK"
        
    key = ""
    if len(parts) > 1:
        # Acronym
        for p in parts:
            if p:
                key += p[0].upper()
        # If acronym is too short (e.g. 2 chars), maybe add 2nd char of first word?
        # But 'CC' for 'claude-code' is valid.
    else:
        # Single word, take up to 4 chars
        key = parts[0][:4].upper()
        
    if len(key) < 2:
        key = (key + "PRJ")[:3]
        
    return key

def main():
    print(f"--- {DESCRIPTION} ---")
    
    if not os.path.exists(DESKTOP_PATH):
        print(f"Error: Path {DESKTOP_PATH} does not exist.")
        return

    try:
        service = JiraService()
    except Exception as e:
        print(f"Failed to initialize JiraService: {e}")
        return

    print("Verifying connection...")
    if not service.verify_connection():
        print("Failed to verify JIRA connection.")
        return

    items = os.listdir(DESKTOP_PATH)
    directories = []
    
    for item in items:
        full_path = os.path.join(DESKTOP_PATH, item)
        if os.path.isdir(full_path) and not item.startswith('.'):
            directories.append(item)
            
    print(f"Found {len(directories)} directories on Desktop: {directories}")
    
    for dir_name in directories:
        key = generate_project_key(dir_name)
        project_name = dir_name.replace("-", " ").replace("_", " ").title()
        
        print(f"\nProcessing '{dir_name}' -> Key: {key}, Name: {project_name}")
        
        # Check if project exists (heuristic via create_project handled by service/JIRA usually)
        # We'll just try to create it.
        try:
            # We don't have a check_exists method easily exposed without searching, 
            # create_project prints error if fails.
            service.create_project(key, project_name)
        except Exception as e:
            print(f"Error creating project for {dir_name}: {e}")

if __name__ == "__main__":
    main()
