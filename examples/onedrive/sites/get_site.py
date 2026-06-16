"""
Get SharePoint/OneDrive sites by URL and view followed sites.

Sites are the top-level container for teams, document libraries,
and lists.

Requires delegated permission ``Sites.Read.All``.

https://learn.microsoft.com/en-us/graph/api/site-get
https://learn.microsoft.com/en-us/graph/api/sites-list-followed
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_tenant_name, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

# 1. Get root site
root = client.sites.root.get().execute_query()
print(f"Root site: {root.display_name}  ({root.web_url})")

# 2. Get site by URL
site = client.sites.get_by_url(f"https://{test_tenant_name}.sharepoint.com/sites/project").get().execute_query()
print(f"Team site: {site.display_name}  (id: {site.id})")

# 3. Followed sites
sites = client.me.followed_sites.get().execute_query()
print(f"\nFollowed sites ({len(sites)}):")
for s in sites:
    print(f"  {s.display_name}")
