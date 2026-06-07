"""
Device inventory: list all managed devices with compliance state,
OS, last sync, and management agent.

The enriched report admins actually need — not just a list of names.

Requires delegated permission ``DeviceManagementManagedDevices.Read.All``.

https://learn.microsoft.com/en-us/graph/api/intune-devices-manageddevice-list
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

devices = client.device_management.managed_devices.get().execute_query()
print(f"Found {len(devices)} managed devices\n")

by_compliance = {}

for d in devices:
    status = d.compliance_state or "unknown"
    by_compliance[status] = by_compliance.get(status, 0) + 1
    print(
        f"  {d.device_name or '(unnamed)':30s}  {d.operating_system or '?':12s}  [{status}]"
        f"  last sync: {d.last_sync_date_time or 'never'}"
    )

print("\nSummary:")
for status, count in sorted(by_compliance.items()):
    print(f"  {status}: {count}")
