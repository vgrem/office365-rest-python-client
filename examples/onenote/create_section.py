"""
Create a new section in a OneNote notebook.

Requires delegated permission ``Notes.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/onenote-post-sections?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

notebooks = client.me.onenote.notebooks.get().execute_query()
if len(notebooks) == 0:
    sys.exit("No notebooks found")

section = notebooks[0].sections.add("Meeting Notes").execute_query()
print(f"Section created: {section.display_name}  (ID: {section.id})")
