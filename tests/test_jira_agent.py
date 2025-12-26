import unittest
from unittest.mock import MagicMock, patch
from src.jira_service import JiraService

class TestJiraService(unittest.TestCase):
    
    @patch('src.jira_service.JiraClient')
    def setUp(self, MockJiraClient):
        self.mock_client = MockJiraClient.return_value
        self.mock_client.jira_url = "https://test.atlassian.net"
        self.mock_client.project_key = "TEST"
        self.service = JiraService()

    def test_verify_connection_success(self):
        self.mock_client.get.return_value = {
            "displayName": "Test User", 
            "emailAddress": "test@example.com"
        }
        self.assertTrue(self.service.verify_connection())

    def test_verify_connection_failure(self):
        self.mock_client.get.return_value = None
        self.assertFalse(self.service.verify_connection())

    def test_create_issue_success(self):
        self.mock_client.post.return_value = {"key": "TEST-1"}
        key = self.service.create_issue("Summary", "Description")
        self.assertEqual(key, "TEST-1")
        self.mock_client.post.assert_called_once()

    def test_add_comment_success(self):
        self.mock_client.post.return_value = {}
        result = self.service.add_comment("TEST-1", "Comment")
        self.assertTrue(result)

    def test_transition_issue_success(self):
        # Mock transitions response
        self.mock_client.get.return_value = {
            "transitions": [{"id": "11", "name": "In Progress"}]
        }
        # Mock transition execution response
        self.mock_client.post.return_value = {}
        
        result = self.service.transition_issue("TEST-1", "In Progress")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
