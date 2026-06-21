"""
List all SharePoint sites in the tenant with pagination.

The /sites?search=* endpoint returns a nextLink when there are more
sites. This example uses get_all() to walk every page automatically.

Requires delegated permission Sites.Read.All.

https://learn.microsoft.com/en-us/graph/api/site-list
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = (
    GraphClient(tenant=tenant)
    .with_client_secret(client_id, client_secret)
    .require_application_permission("Sites.Read.All")
)

all_sites = client.sites.order_by("displayName").get_all().execute_query()
print(f"Total sites: {len(all_sites)}")
for s in all_sites:
    print(f"  {s.display_name:50s}  {s.web_url}")
