"""
Search and follow SharePoint sites.

Requires delegated permission ``Sites.Read.All``, ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/site-search
https://learn.microsoft.com/en-us/graph/api/user-followsite
"""

from office365.graph_client import GraphClient
from tests import (
    test_client_id,
    test_client_secret,
    test_tenant,
    test_user_principal_name,
)

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)

# 1. Search sites by keyword
results = client.sites.search("team").execute_query()
print(f"Sites matching 'team' ({len(results)}):")
for s in results:
    print(f"  {s.display_name:40s}  {s.web_url}")

# 2. Follow a site
user = client.users[test_user_principal_name]
sites = results  # reuse search results
if len(sites) > 0:
    user.follow_site(sites[0]).execute_query()
    print(f"\nFollowed: {sites[0].display_name}")
