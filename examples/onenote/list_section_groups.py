"""
List section groups in a OneNote notebook.

Section groups are containers for organizing sections within a notebook.

Requires delegated permission ``Notes.Read`` or ``Notes.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/onenote-list-sectiongroups?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

notebooks = client.me.onenote.notebooks.get().execute_query()
if len(notebooks) > 0:
    groups = notebooks[0].section_groups.get().execute_query()
    print(f"Section groups in '{notebooks[0].display_name}':")
    for g in groups:
        print(f"  {g.display_name}  (ID: {g.id})")
