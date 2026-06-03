"""
List recently accessed OneNote notebooks.

Requires delegated permission ``Notes.Read`` or ``Notes.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/onenote-list-recentnotebooks?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

notebooks = client.me.onenote.notebooks.get_recent().execute_query()
for nb in notebooks:
    print(f"  {nb.display_name}")
