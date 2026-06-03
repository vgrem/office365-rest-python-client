"""
List all devices registered in Microsoft Entra ID.

Requires delegated permission ``Device.Read.All``.

https://learn.microsoft.com/en-us/graph/api/device-list?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

devices = client.devices.top(20).get().execute_query()
for device in devices:
    print(f"  {device.display_name:40s}  {device.operating_system or ''}  {device.trust_type or ''}")
