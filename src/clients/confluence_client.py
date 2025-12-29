from atlassian import Confluence
import os
from dotenv import load_dotenv

class ConfluenceClient:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv("CONFLUENCE_URL")
        self.username = os.getenv("CONFLUENCE_USER_EMAIL")
        self.api_token = os.getenv("CONFLUENCE_API_TOKEN")

        if not all([self.url, self.username, self.api_token]):
            raise ValueError("Missing Confluence configuration variables.")

        self.confluence = Confluence(
            url=self.url,
            username=self.username,
            password=self.api_token,
            cloud=True
        )

    def get_page(self, page_id):
        return self.confluence.get_page_by_id(page_id, expand='body.storage,version')

    def create_page(self, space_id, title, body, parent_id=None):
        return self.confluence.create_page(
            space=space_id, # Note: Wrapper might expect space key or id depending on method, check docs. 
                            # actually create_page takes space (key) normally, but v2 uses IDs. 
                            # The library abstracts this. 'space' arg usually is key.
                            # But if user passes ID, we might need to adjust.
                            # For simplicity, we assume 'space_id' param maps to 'space' arg which often is KEY.
                            # Let's rename arg to space_key to be safe or just pass it.
            title=title,
            body=body,
            parent_id=parent_id,
            representation='storage'
        )

    def update_page(self, page_id, title, body, version_number):
        # The library's update_page automatically handles version increment if plain update is called?
        # update_page(page_id, title, body, parent_id=None, type='page', representation='storage', minor_edit=False, version_comment=None)
        return self.confluence.update_page(
            page_id=page_id,
            title=title,
            body=body,
            representation='storage',
            version_comment="Updated via AI Agent"
        )
    
    def search_pages(self, cql):
        return self.confluence.cql(cql)

    def get_page_id(self, title, space_key=None):
        return self.confluence.get_page_id(space_key, title)

    def create_space(self, key, name, description=None):
        # NOTE: Library might not strictly support create_space for Cloud with API token easily?
        # It sends XML/JSON.
        return self.confluence.create_space(key, name, description)
