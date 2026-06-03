"""
List all Intune-managed devices in the tenant.

Requires delegated permission ``DeviceManagementManagedDevices.Read.All``.

https://learn.microsoft.com/en-us/graph/api/intune-devices-manageddevice-list?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

devices = client.device_management.managed_devices.get().execute_query()
for d in devices:
    status = d.compliance_state or "unknown"
    os = d.operating_system or ""
    print(f"  {d.device_name:35s}  {os:15s}  [{status}]")
