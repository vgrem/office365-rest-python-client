"""
Create a new mail folder under the Inbox.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/user-post-mailfolders?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

folder = client.me.mail_folders.add("Projects").execute_query()
print(f"Folder created: {folder.display_name}  (ID: {folder.id})")
