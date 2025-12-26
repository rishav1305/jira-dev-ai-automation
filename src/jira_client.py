import os
import requests
from base64 import b64encode
from dotenv import load_dotenv

class JiraClient:
    """
    Handles low-level authentications and HTTP requests to JIRA API.
    Single Responsibility: API Communication.
    """
    def __init__(self):
        load_dotenv()
        self.jira_url = os.getenv("JIRA_URL")
        self.email = os.getenv("JIRA_USER_EMAIL")
        self.token = os.getenv("JIRA_API_TOKEN")
        self.project_key = os.getenv("JIRA_PROJECT_KEY")

        if not all([self.jira_url, self.email, self.token, self.project_key]):
            raise ValueError("Missing JIRA configuration in environment variables.")

        auth_string = f"{self.email}:{self.token}"
        self.headers = {
            "Authorization": f"Basic {b64encode(auth_string.encode('utf-8')).decode('utf-8')}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def get(self, endpoint, params=None):
        """Execute GET request."""
        url = f"{self.jira_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"GET Error {url}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return None

    def post(self, endpoint, payload):
        """Execute POST request."""
        url = f"{self.jira_url}{endpoint}"
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            if response.status_code == 204:
                return {} # Return empty dict for success with no content
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"POST Error {url}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return None

    def put(self, endpoint, payload):
        """Execute PUT request."""
        url = f"{self.jira_url}{endpoint}"
        try:
            response = requests.put(url, headers=self.headers, json=payload)
            response.raise_for_status()
            # PUT responses vary, sometimes 204 No Content
            if response.status_code == 204:
                return True
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"PUT Error {url}: {e}")
            return None
