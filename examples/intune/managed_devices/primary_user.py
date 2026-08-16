"""
Primary user and ownership management for a managed device.

Shows how to read a device's primary user, set device ownership
(corporate vs. personal), and assign/remove a primary user.

Requires delegated permissions ``DeviceManagementManagedDevices.Read.All``
and ``DeviceManagementManagedDevices.PrivilegedOperations.All``.

https://learn.microsoft.com/en-us/graph/api/intune-devices-manageddevice-users
https://learn.microsoft.com/en-us/graph/api/intune-devices-manageddevice-update
"""

import argparse
import sys

from office365.graph_client import GraphClient
from office365.intune.devices.management.managed.ownertype import ManagedDeviceOwnerType
from tests import test_client_id, test_client_secret, test_tenant


def main():
    parser = argparse.ArgumentParser(description="Manage the primary user of a managed device")
    parser.add_argument("--device-name", default="DESKTOP", help="Substring to match a device name")
    parser.add_argument("--user-id", help="User ID to assign as primary user (or remove)")
    parser.add_argument(
        "--action",
        choices=["show", "assign", "remove", "set-ownership"],
        default="show",
        help="Action to run (default: show)",
    )
    args = parser.parse_args()

    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
    devices = client.device_management.managed_devices.get().execute_query()
    target = next((d for d in devices if d.device_name and args.device_name.upper() in d.device_name.upper()), None)
    if target is None:
        sys.exit(f"No device matching '{args.device_name}' found.")

    print(f"Target device: {target.device_name}  (compliance: {target.compliance_state})\n")

    if args.action == "show":
        print(f"  Primary user: {target.user_display_name or '?'} ({target.user_principal_name or '?'})")
        print(f"  Email: {target.email_address or '?'}")
        print(f"  Ownership: {target.managed_device_owner_type or '?'}")
    elif args.action == "assign":
        if not args.user_id:
            sys.exit("--user-id is required for assign")
        target.set_primary_user(args.user_id).execute_query()
        print(f"  ✓ Primary user {args.user_id} assigned")
    elif args.action == "remove":
        if not args.user_id:
            sys.exit("--user-id is required for remove")
        target.remove_primary_user(args.user_id).execute_query()
        print(f"  ✓ User {args.user_id} removed")
    elif args.action == "set-ownership":
        target.set_property("managedDeviceOwnerType", ManagedDeviceOwnerType.company, True)
        target.update().execute_query()
        print("  ✓ Device ownership set to corporate")


if __name__ == "__main__":
    main()
