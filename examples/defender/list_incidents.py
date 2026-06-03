"""
List incidents from Microsoft 365 Defender.

Requires delegated permission ``Incidents.Read.All`` or
``Incidents.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/security-list-incidents?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)

incidents = client.security.incidents.get().execute_query()
for inc in incidents:
    status = inc.status or "unknown"
    severity = inc.severity or "N/A"
    print(f"  [{severity:10s}] [{status:15s}] {inc.display_name}")
