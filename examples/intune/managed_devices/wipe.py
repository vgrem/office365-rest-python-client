"""
Wipe a managed device (factory reset).

Requires delegated permission ``DeviceManagementManagedDevices.PrivilegedOperations.All``.

https://learn.microsoft.com/en-us/graph/api/intune-devices-manageddevice-wipe?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

devices = client.device_management.managed_devices.get().execute_query()
target = next((d for d in devices if d.device_name and "DESKTOP" in d.device_name.upper()), None)
if target is None:
    sys.exit("No matching device found")

target.wipe().execute_query()
print(f"Wipe command issued for '{target.device_name}'")
