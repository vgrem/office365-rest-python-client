"""
List alerts from Microsoft 365 Defender (v2 API).

Requires delegated permission ``SecurityAlert.Read.All`` or
``SecurityAlert.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/security-list-alerts_v2?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)

alerts = client.security.alerts_v2.top(20).get().execute_query()
for alert in alerts:
    sev = alert.severity or "N/A"
    status = alert.status or "unknown"
    title = alert.title or "(no title)"
    print(f"  [{sev:10s}] [{status:15s}] {title}")
