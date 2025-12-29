from atlassian import Jira
import os
from dotenv import load_dotenv

class JiraClient:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv("JIRA_URL")
        self.username = os.getenv("JIRA_USER_EMAIL")
        self.api_token = os.getenv("JIRA_API_TOKEN")

        if not all([self.url, self.username, self.api_token]):
            raise ValueError("Missing JIRA configuration variables.")

        self.jira = Jira(
            url=self.url,
            username=self.username,
            password=self.api_token,
            cloud=True
        )

    def create_project(self, key, name):
        return self.jira.create_project(key, name)

    def create_issue(self, summary, description, issue_type="Task", project_key=None):
        fields = {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},
        }
        return self.jira.issue_create(fields)

    def update_issue(self, key, summary=None, description=None):
        fields = {}
        if summary:
            fields["summary"] = summary
        if description:
            fields["description"] = description
        return self.jira.issue_update(key, fields)

    def transition_issue(self, key, status):
        return self.jira.set_issue_status(key, status)

    def add_comment(self, key, body):
        return self.jira.issue_add_comment(key, body)

    def get_issue(self, key):
        return self.jira.issue(key)

    def search_tasks(self, jql):
        return self.jira.jql(jql)
