"""
Get the full HTML content of a OneNote page.

Requires delegated permission ``Notes.Read`` or ``Notes.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/page-get?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

pages = client.me.onenote.pages.top(1).get().execute_query()
if len(pages) == 0:
    sys.exit("No pages found")

page = pages[0]
# Download the HTML content of the page
with open("page_content.html", "wb") as f:
    page.download(f).execute_query()
print(f"Page '{page.title}' content saved to page_content.html")
