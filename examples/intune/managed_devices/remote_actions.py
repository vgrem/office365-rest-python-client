"""
Remote actions on a managed device: sync, retire, reboot, and wipe.

WARNING: These actions are destructive and irreversible.
- Wipe: factory reset (removes all data)
- Retire: removes company data only
- Reboot / lock / shut down: immediate device disruption

Requires delegated permission ``DeviceManagementManagedDevices.PrivilegedOperations.All``.

https://learn.microsoft.com/en-us/graph/api/intune-devices-manageddevice-wipe
https://learn.microsoft.com/en-us/graph/api/intune-devices-manageddevice-retire
https://learn.microsoft.com/en-us/graph/api/intune-devices-manageddevice-syncdevice
"""

import argparse
import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    parser = argparse.ArgumentParser(description="Run a remote action on a managed device")
    parser.add_argument(
        "--device-name",
        default="DESKTOP",
        help="Substring to match a device name (default: DESKTOP)",
    )
    parser.add_argument(
        "--action",
        choices=["sync", "retire", "reboot", "lock", "shutdown", "wipe"],
        default="sync",
        help="Remote action to run (default: sync)",
    )
    args = parser.parse_args()

    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
    devices = client.device_management.managed_devices.get().execute_query()
    target = next((d for d in devices if d.device_name and args.device_name.upper() in d.device_name.upper()), None)
    if target is None:
        sys.exit(f"No device matching '{args.device_name}' found.")

    print(f"Target device: {target.device_name}  (compliance: {target.compliance_state})\n")

    actions = {
        "sync": target.sync_device,
        "retire": target.retire,
        "reboot": target.reboot_now,
        "lock": target.remote_lock,
        "shutdown": target.shut_down,
        "wipe": target.wipe,
    }
    actions[args.action]().execute_query()
    print(f"  ✓ {args.action} command issued")


if __name__ == "__main__":
    main()
