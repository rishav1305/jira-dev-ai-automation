import unittest
from unittest.mock import MagicMock, patch
import json

# We need to import the functions from mcp_server. 
# Since mcp_server instantiates FastMCP and JiraService at top level, 
# importing it might trigger side effects or need mocking of dependencies during import if not careful.
# However, FastMCP initialization is usually side-effect free until run().
# JiraService initialization creates a JiraClient which reads env vars. 
# We should mock JiraService class in mcp_server module.

class TestMcpServer(unittest.TestCase):
    
    def setUp(self):
        # Patch the jira_service instance in mcp_server
        self.patcher = patch('src.mcp_server.jira_service')
        self.mock_service = self.patcher.start()
        
    def tearDown(self):
        self.patcher.stop()
        
    def test_create_project_success(self):
        from src.mcp_server import create_project
        self.mock_service.create_project.return_value = True
        
        result = create_project("TEST", "Test Project")
        self.assertIn("created successfully", result)
        self.mock_service.create_project.assert_called_with("TEST", "Test Project")

    def test_create_issue_success(self):
        from src.mcp_server import create_issue
        self.mock_service.create_issue.return_value = "TEST-10"
        
        result = create_issue("Summary", "Desc")
        self.assertIn("TEST-10", result)
        self.mock_service.create_issue.assert_called()

    def test_search_tasks(self):
        from src.mcp_server import search_tasks
        # Mock client response for search
        self.mock_service.client.post.return_value = {
            "issues": [
                {"key": "TEST-1", "fields": {"summary": "Task 1"}},
                {"key": "TEST-2", "fields": {"summary": "Task 2"}}
            ]
        }
        
        result = search_tasks("project = TEST")
        data = json.loads(result)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['key'], "TEST-1")

if __name__ == '__main__':
    unittest.main()
