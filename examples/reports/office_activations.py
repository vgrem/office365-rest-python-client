"""
Get the count of Microsoft 365 activations across the tenant.

Shows activation counts per product (Office ProPlus, Visio, Project, etc.).

Requires delegated permission ``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/reportroot-getoffice365activationcounts?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)

result = client.reports.get_office365_activation_counts().execute_query()
for item in result.value:
    print(
        f"{item.product_type:30s} "
        f"assigned: {item.assigned:4d}  "
        f"activated: {item.activated:4d}  "
        f"(shared: {item.shared_activated})"
    )
