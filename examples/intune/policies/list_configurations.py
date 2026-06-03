"""
List device configuration profiles in Intune.

Requires delegated permission ``DeviceManagementConfiguration.Read.All``.

https://learn.microsoft.com/en-us/graph/api/intune-deviceconfig-deviceconfiguration-list?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

configs = client.device_management.device_configurations.get().execute_query()
for c in configs:
    print(f"  {c.display_name:40s}")
