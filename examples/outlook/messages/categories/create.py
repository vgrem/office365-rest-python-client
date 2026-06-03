"""
Create a new master category on the user's mailbox.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/outlookuser-post-mastercategories?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

category = (
    client.me.outlook.master_categories.add(
        display_name="Urgent", color="preset5"
    )
    .execute_query()
)
print(f"Category created: {category.display_name}  (ID: {category.id})")
