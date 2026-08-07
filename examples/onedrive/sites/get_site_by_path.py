"""
Get a site by its server-relative path (no full URL required).

Requires delegated permission ``Sites.Read.All``.

https://learn.microsoft.com/en-us/graph/api/site-getbypath
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = (
    GraphClient(tenant=tenant)
    .with_client_secret(client_id, client_secret)
    .require_application_permission("Sites.Read.All")
)

path = input("Server-relative path (e.g. /sites/project): ").strip()
site = client.sites.get_by_path(path).get().execute_query()
print(f"Site: {site.display_name}  ({site.web_url})")
