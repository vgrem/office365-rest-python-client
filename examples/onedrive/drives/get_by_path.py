"""
Demonstrates how to get a drive by path.
"""

from office365.graph_client import GraphClient
from tests import (
    test_client_id,
    test_client_secret,
    test_site_url,
    test_tenant,
)

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
drive_abs_url = f"{test_site_url}/Documents"
result = client.shares.by_url(drive_abs_url).site.drive.get().execute_query()
print(f"Drive url: {result}")
