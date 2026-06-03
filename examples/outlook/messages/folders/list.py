"""
List all mail folders in the user's mailbox.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/user-list-mailfolders?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

folders = client.me.mail_folders.get().execute_query()
for folder in folders:
    total = folder.total_item_count or 0
    unread = folder.unread_item_count or 0
    print(f"{folder.display_name:30s}  {total:4d} items ({unread} unread)")
