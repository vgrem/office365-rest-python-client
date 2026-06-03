"""
Delete a OneNote notebook by display name.

Requires delegated permission ``Notes.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/onenote-delete-notebook?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

notebooks = client.me.onenote.notebooks.get().execute_query()
target = next((nb for nb in notebooks if nb.display_name == "My Private notebook"), None)
if target is None:
    sys.exit("Notebook not found")

target.delete_object().execute_query()
print(f"Notebook '{target.display_name}' deleted")
