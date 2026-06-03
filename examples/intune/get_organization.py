"""
Get the tenant's organization profile.

Requires delegated permission ``Organization.Read.All``.

https://learn.microsoft.com/en-us/graph/api/organization-get?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

org = client.organization.get().execute_query()
for o in org:
    print(f"  {o.display_name:40s}  {o.verified_domains[0]['name'] if o.verified_domains else ''}")
