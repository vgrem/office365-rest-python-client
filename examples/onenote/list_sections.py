"""
List all sections in a OneNote notebook.

Requires delegated permission ``Notes.Read`` or ``Notes.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/onenote-list-sections?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

notebooks = client.me.onenote.notebooks.get().execute_query()
if len(notebooks) > 0:
    sections = notebooks[0].sections.get().execute_query()
    print(f"Sections in '{notebooks[0].display_name}':")
    for s in sections:
        print(f"  {s.display_name}  (ID: {s.id})")
