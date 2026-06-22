"""
Site pages — create, get, update web parts, publish, and delete.

Covers the full page lifecycle in a SharePoint site.

Requires delegated permission ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/sitepage-create
https://learn.microsoft.com/en-us/graph/api/sitepage-publish
"""

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

site = client.sites.root

# 1. Create a page
page_name = create_unique_name("Status-Report")
page = site.pages.add(title=page_name).execute_query()
print(f"Page created: {page.title}")

# 2. Get page by title
page = site.pages.get_by_title(page_name).get().execute_query()
print(f"  Found by title: {page.title}")

# 3. Update page properties (show comments)
page.set_property("showComments", True)
page.update().execute_query()
print(f"  Updated: show_comments={page.show_comments}")

# 4. Publish
page.publish().execute_query()
print("  Published")

# 5. List all pages
for p in site.pages.get().execute_query():
    print(f"  {p.title}")

# 6. Delete the test page
page.delete_object().execute_query()
print("  Deleted")
