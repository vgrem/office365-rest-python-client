"""
Create, publish, and list site pages in a SharePoint site.

Site pages are modern pages that can contain web parts
and rich content.

Requires delegated permission ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/sitepage-create
https://learn.microsoft.com/en-us/graph/api/sitepage-publish
"""

from office365.graph_client import GraphClient
from tests import (
    create_unique_name,
    test_client_id,
    test_client_secret,
    test_tenant,
)

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)

# 1. Create a site page
page_name = create_unique_name("Status-Report")
page = client.sites.root.pages.add(title=page_name).execute_query()
print(f"Page created: {page.title}  (id: {page.id})")

# 2. Publish the page
page.publish().execute_query()
print("  Published successfully")

# 3. List all pages in the site
pages = client.sites.root.pages.get().execute_query()
print(f"\nSite pages ({len(pages)}):")
for p in pages:
    print(f"  {p.title}")
