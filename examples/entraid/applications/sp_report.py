"""
Service principals: list registered apps, delegated permissions,
and find expiring secrets.

Critical for security hygiene — identify app permissions and
expiring credentials before they cause outages.

Requires delegated permission ``Application.Read.All``.

https://learn.microsoft.com/en-us/graph/api/serviceprincipal-list
https://learn.microsoft.com/en-us/graph/api/application-list
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)

# 1. List service principals
sps = client.service_principals.top(20).get().execute_query()
print(f"Service principals ({len(sps)}):")
for sp in sps:
    print(f"  {sp.display_name:40s}  app_id: {sp.app_id or '?'}")
