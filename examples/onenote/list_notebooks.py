"""
List all OneNote notebooks for the signed-in user.

Requires delegated permission ``Notes.Read`` or ``Notes.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/onenote-list-notebooks
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)
notebooks = client.me.onenote.notebooks.get().execute_query()
for notebook in notebooks:
    print(notebook.display_name)
