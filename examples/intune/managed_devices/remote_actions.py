"""
Remote actions on a managed device: wipe, retire, and force sync.

WARNING: These actions are destructive and irreversible.
- Wipe: factory reset (removes all data)
- Retire: removes company data only
- Sync: forces device to check in with Intune

Requires delegated permission ``DeviceManagementManagedDevices.PrivilegedOperations.All``.

https://learn.microsoft.com/en-us/graph/api/intune-devices-manageddevice-wipe
https://learn.microsoft.com/en-us/graph/api/intune-devices-manageddevice-retire
https://learn.microsoft.com/en-us/graph/api/intune-devices-manageddevice-syncdevice
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

devices = client.device_management.managed_devices.get().execute_query()
target = next((d for d in devices if d.device_name and "DESKTOP" in d.device_name.upper()), None)
if target is None:
    sys.exit("No matching device found. Try a different device name filter.")

print(f"Target device: {target.device_name}  (compliance: {target.compliance_state})\n")

# 1. Force sync
target.sync_device().execute_query()
print("  ✓ Sync command issued")

# 2. Retire (remove company data)
target.retire().execute_query()
print("  ✓ Retire command issued")

# 3. Wipe (factory reset — uncomment with caution)
# target.wipe().execute_query()
# print(f"  ✓ Wipe command issued")
