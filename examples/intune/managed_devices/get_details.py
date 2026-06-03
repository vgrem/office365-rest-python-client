"""
Get details and compliance state for a specific managed device by name.

Requires delegated permission ``DeviceManagementManagedDevices.Read.All``.

https://learn.microsoft.com/en-us/graph/api/intune-devices-manageddevice-get?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)

devices = client.device_management.managed_devices.get().execute_query()
target = next((d for d in devices if d.device_name and "DESKTOP" in d.device_name.upper()), None)
if target is None:
    sys.exit("No matching device found")

print(f"Device: {target.device_name}")
print(f"  OS: {target.operating_system} {target.os_version}")
print(f"  Compliance: {target.compliance_state}")
print(f"  Last sync: {target.last_sync_date_time}")
print(f"  Managed by: {target.management_agent}")
print(f"  Jailbroken: {target.jail_broken}")
print(f"  Enrolled: {target.enrolled_date_time}")
