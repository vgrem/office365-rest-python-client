"""
List eDiscovery cases in Microsoft Purview.

Requires delegated permission ``eDiscovery.Read.All`` or
``eDiscovery.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/security-list-ediscoverycases?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

cases = client.security.cases.ediscovery_cases.get().execute_query()
for case in cases:
    status = case.status if hasattr(case, "status") else "N/A"
    print(f"  {case.display_name:40s}  status: {case.status or 'active'}")
