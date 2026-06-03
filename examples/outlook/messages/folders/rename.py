"""
Rename a mail folder.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/mailfolder-update?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

folder = client.me.mail_folders["Projects"]
folder.set_property("displayName", "Archive - Projects").update().execute_query()
print(f"Folder renamed to: {folder.display_name}")
