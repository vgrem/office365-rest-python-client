"""
List all master categories on the user's mailbox.

Categories are used to color-code and organize messages and events.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/outlookuser-list-mastercategories?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

categories = client.me.outlook.master_categories.get().execute_query()
for cat in categories:
    print(f"  {cat.display_name:25s}  ({cat.color})")
