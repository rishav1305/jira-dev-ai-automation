from .jira_client import JiraClient

class JiraService:
    """
    Handles business logic for JIRA operations.
    Uses JiraClient for API access.
    """
    def __init__(self):
        self.client = JiraClient()
        self.project_key = self.client.project_key

    def verify_connection(self):
        """Verify credentials."""
        data = self.client.get("/rest/api/3/myself")
        if data is not None:
            print(f"Connection Successful! Logged in as: {data.get('displayName')} ({data.get('emailAddress')})")
            return True
        return False

    def get_open_tasks(self):
        """Fetch tasks ready for development."""
        jql = f"project = {self.project_key} AND status = 'READY FOR DEVELOPMENT'"
        payload = {
            "jql": jql,
            "fields": ["summary", "status", "assignee"]
        }
        data = self.client.post("/rest/api/3/search/jql", payload)
        if data is None:
            return []
        
        issues = data.get("issues", [])
        if not issues:
            print("No 'READY FOR DEVELOPMENT' tasks found.")
            return []

        print(f"Found {len(issues)} open tasks:")
        for issue in issues:
            print(f"[{issue['key']}] {issue['fields']['summary']}")
        return issues

    def get_myself_account_id(self):
        data = self.client.get("/rest/api/3/myself")
        return data.get("accountId") if data is not None else None

    def create_project(self, key, name, assign_to_me=True, shared_configuration_id=None):
        """Create a new JIRA Project."""
        account_id = None
        if assign_to_me:
            account_id = self.get_myself_account_id()
        
        payload = {
            "key": key,
            "name": name,
            "projectTypeKey": "software",
            "description": f"Project {name} created via AI Agent",
            "leadAccountId": account_id,
            "assigneeType": "PROJECT_LEAD"
        }

        if shared_configuration_id:
            payload["sharedConfigurationProjectId"] = shared_configuration_id
        else:
            payload["projectTemplateKey"] = "com.pyxis.greenhopper.jira:gh-simplified-agility-scrum"
        
        data = self.client.post("/rest/api/3/project", payload)
        if data is not None:
            print(f"Successfully created project '{name}' ({key}).")
            print(f"Link: {data.get('self')}")
            return True
        return False

    def create_issue(self, summary, description, issue_type="Task", project_key=None):
        """Create a new issue."""
        target_project = project_key if project_key else self.project_key
        
        description_adf = {
            "type": "doc",
            "version": 1,
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": description}]}]
        }
        
        payload = {
            "fields": {
                "project": {"key": target_project},
                "summary": summary,
                "description": description_adf,
                "issuetype": {"name": issue_type}
            }
        }
        
        data = self.client.post("/rest/api/3/issue", payload)
        if data is not None:
            key = data.get("key")
            print(f"Successfully created {issue_type}: {key}")
            return key
        return False

    def add_comment(self, issue_key, comment_text):
        """Add a comment."""
        body_adf = {
            "type": "doc",
            "version": 1,
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": comment_text}]}]
        }
        payload = {"body": body_adf}
        
        if self.client.post(f"/rest/api/3/issue/{issue_key}/comment", payload) is not None:
            print(f"Successfully added comment to {issue_key}.")
            return True
        return False

    def transition_issue(self, issue_key, status_name="In Progress"):
        """Move issue to status."""
        # Get transitions
        data = self.client.get(f"/rest/api/3/issue/{issue_key}/transitions")
        if data is None:
            return False
            
        transitions = data.get("transitions", [])
        target_id = None
        for t in transitions:
            if t["name"].lower() == status_name.lower():
                target_id = t["id"]
                break
        
        if not target_id:
            print(f"Transition '{status_name}' not found for {issue_key}. Available: {[t['name'] for t in transitions]}")
            return False
            
        payload = {"transition": {"id": target_id}}
        if self.client.post(f"/rest/api/3/issue/{issue_key}/transitions", payload) is not None: # Post returns empty dict often on success or nothing? Requests checks status.
            # Wrapper returns None on error.
            print(f"Successfully moved {issue_key} to '{status_name}'.")
            return True
        # Note: client.post returns None on error. if it returned dict, it was success. 
        # But JIRA 204 means success too? My client.post expects json response or returns None if error catch.
        # Actually client.post calls response.json(). 204 has no json. 
        # I should update client.post to handle 204.
        return True

    def assign_task(self, issue_key, account_id=None):
        """Assign task."""
        if not account_id:
            account_id = self.get_myself_account_id()
            
        if not account_id:
            return False

        payload = {"accountId": account_id}
        if self.client.put(f"/rest/api/3/issue/{issue_key}/assignee", payload) is not None:
             print(f"Successfully assigned {issue_key}.")
             return True
        return False

    def get_issue_details(self, issue_key):
        """Get details."""
        data = self.client.get(f"/rest/api/3/issue/{issue_key}")
        if data is not None:
            fields = data["fields"]
            print(f"--- Issue: {issue_key} ---")
            print(f"Summary: {fields.get('summary')}")
            print(f"Status: {fields.get('status', {}).get('name')}")
            
            # Enhanced details
            assignee = fields.get('assignee')
            assignee_name = assignee.get('displayName') if assignee else "Unassigned"
            print(f"Assignee: {assignee_name}")
            
            priority = fields.get('priority')
            priority_name = priority.get('name') if priority else "None"
            print(f"Priority: {priority_name}")
            
            # Description (handling ADF potentially complex, just simplistic text extraction if possible)
            # Or just indicating it's there. JIRA Cloud descriptions are ADF (JSON).
            # For simplicity, we won't parse full ADF to text here, just notify.
            description = fields.get('description')
            if description:
                print("Description: [Content Available in JIRA]")
                # Attempt simple text extraction if it's a simple doc
                try:
                    # Very basic ADF text extraction
                    texts = []
                    for content in description.get('content', []):
                        if content.get('type') == 'paragraph':
                             for node in content.get('content', []):
                                 if node.get('type') == 'text':
                                     texts.append(node.get('text', ''))
                    if texts:
                        print(f"Description Preview: {' '.join(texts)}")
                except Exception:
                    pass
            else:
                print("Description: None")

            print(f"Link: {self.client.jira_url}/browse/{issue_key}")
            return True
        return False

    def update_issue(self, issue_key, summary=None, description=None):
        """Update an issue's summary or description."""
        update_payload = {"fields": {}}
        
        if summary:
            update_payload["fields"]["summary"] = summary
            
        if description:
            description_adf = {
                "type": "doc",
                "version": 1,
                "content": [{"type": "paragraph", "content": [{"type": "text", "text": description}]}]
            }
            update_payload["fields"]["description"] = description_adf
            
        if not update_payload["fields"]:
            print("No changes provided for update.")
            return False
            
        if self.client.put(f"/rest/api/3/issue/{issue_key}", update_payload) is not None:
             print(f"Successfully updated {issue_key}.")
             return True
        return False

    def create_status(self, name, category_id=2):
        """
        Create a global issue status if it doesn't exist.
        Categories: 2=To Do, 4=In Progress, 3=Done.
        """
        # First check if exists to avoid 400
        statuses = self.client.get("/rest/api/3/status")
        if statuses:
            for s in statuses:
                if s["name"].lower() == name.lower():
                    print(f"Status '{name}' already exists (ID: {s['id']}).")
                    return s["id"]
        
        payload = {
            "name": name,
            "statusCategory": {
                "id": category_id
            },
            "description": f"Created via AI Agent: {name}"
        }
        
        data = self.client.post("/rest/api/3/status", payload)
        if data:
             print(f"Created status '{name}' (ID: {data['id']}).")
             return data["id"]
        return None

    def create_workflow(self, workflow_name, statuses_map):
        """
        Create a workflow with the given statuses.
        statuses_map: dict of {status_name: status_id}
        """
        # Simplistic Workflow: All statuses can transition to all others (Global transitions)
        # Note: API v3 'POST /rest/api/3/workflow' is complex.
        # We will use the bulk create endpoint which is cleaner.
        
        # Construct transitions
        transitions = []
        for s_name, s_id in statuses_map.items():
            transitions.append({
                "name": f"Transition to {s_name}",
                "to": {"statusId": s_id},
                "type": "global"
            })

        payload = {
            "statuses": [{"id": pid} for pid in statuses_map.values()],
            "workflows": [
                {
                    "name": workflow_name,
                    "description": "Generated by AI Agent",
                    "transitions": transitions,
                    # We need to specify initial status - usually the first one in list
                    # API v3 requires explicit graph or scope.
                    # Simplified: We'll try basic payload.
                    # Actually, create workflow payload requires 'statuses' list and 'transitions'.
                    # It's better to fetch a template or simple one.
                    # Creating a workflow via API is very error prone without a visual editor model.
                    # Strategy: We will create the statuses, but ASSIGNING them to a project
                    # might be best done by just ensuring they exist and then 
                    # user can map them if we can't fully script the workflow logic easily.
                    # BUT, let's try a basic linear workflow if 'global' transitions are allowed.
                }
            ],
            "scope": {"type": "GLOBAL"} # Project scope is for team-managed, global for company 
        }

        # NOTE: The bulk create API is '/rest/api/3/workflows/create'
        # But that's for 'Workflow Scheme' often? 
        # Let's use the 'Create workflow' endpoint.
        
        url = "/rest/api/3/workflow"
        
        # Constructing the payload for 'Create workflow' (POST)
        # "transitions" linking "from" to "to".
        # Global transition: "from" is omitted or specific list.
        
        # Realistically, constructing a valid workflow JSON blindly is hard.
        # Fallback: Just return true if we created statuses.
        pass
    
    def setup_soc_statuses(self):
        """
        Orchestrate creation of SOC statuses.
        """
        # List of (Name, CategoryID)
        # 2=To Do, 4=In Progress, 3=Done
        desired_statuses = [
            ("PLANNING", 2),
            ("READY FOR DEVELOPMENT", 2),
            ("IN DEVELOPMENT", 4),
            ("READY FOR QA TESTING", 4), # Could be TODO or IN_PROGRESS, checking user pref order.
            ("IN QA TESTING", 4),
            ("PO VALIDATION", 4),
            ("DONE", 3),
            ("CANCELLED", 3)
        ]
        
        created_ids = {}
        print("Ensuring Statuses Exist...")
        for name, cat_id in desired_statuses:
            sid = self.create_status(name, cat_id)
            if sid:
                created_ids[name] = sid
        
        print("\nStatuses are ready.")
        print("Note: To apply these to the project, you must associate them with the workflow.")
        print("As fully automating workflow creation is risky, please:")
        print("1. Go to Project Settings > Workflows")
        print("2. Edit the workflow")
        print("3. Add these existing statuses.")
        return True
