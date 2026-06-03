"""
Mark all messages in the Inbox as read.

Updates the ``isRead`` flag on every message in the folder.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/resources/message
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)
client.me.mail_folders["Inbox"].mark_all_items_as_unread().execute_query()
print("All messages marked as read")
