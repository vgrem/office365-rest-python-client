"""
Report stale registered devices — devices not recently used for sign-in.

Stale devices are a security risk (unmanaged endpoints with valid tokens).
This script lists registered devices with no recent sign-in activity,
organized by operating system, for cleanup decisions.

Inspired by Report-EntraRegisteredDevices.PS1 and
Remove-ObsoleteMobileDevices.PS1 from Office 365 for IT Pros.

Required delegated permissions:
    Device.Read.All             Read registered device information
    Directory.Read.All          (optional) resolve device owner details

https://learn.microsoft.com/en-us/graph/api/resources/device
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

_DISPLAY_LIMIT = 30


def find_stale_devices(days_threshold: int = 180) -> list[dict]:
    """Find registered devices without sign-in activity.

    Args:
        days_threshold: Days since last sign-in to flag a device.

    Returns:
        List of device dicts sorted by last sign-in (ascending).
    """
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    cutoff = datetime.now(timezone.utc) - timedelta(days=days_threshold)
    stale = []

    devices = client.devices.get().execute_query()
    for device in devices:
        name = getattr(device, "display_name", "Unnamed")
        os = getattr(device, "operating_system", "Unknown")
        os_version = getattr(device, "operating_system_version", "")
        trust_type = getattr(device, "trust_type", "Unknown")
        device_id = getattr(device, "device_id", device.id)

        # Last sign-in time
        last_signin = getattr(device, "approximate_last_sign_in_date_time", None)
        if not last_signin:
            last_signin = getattr(device, "registration_date_time", None)

        if last_signin and last_signin < cutoff:
            stale.append(
                {
                    "name": name,
                    "device_id": device_id,
                    "os": f"{os} {os_version}".strip(),
                    "trust_type": trust_type,
                    "last_signin": last_signin,
                    "days_since": (datetime.now(timezone.utc) - last_signin).days,
                }
            )

    stale.sort(key=lambda x: x["days_since"], reverse=True)
    return stale


def main():
    print("Finding stale registered devices...\n")
    devices = find_stale_devices(days_threshold=180)

    if not devices:
        print("No stale devices found.")
        return

    print(f"Stale devices (no sign-in in 180+ days): {len(devices)}\n")
    print(f"{'Device':30s} {'OS':20s} {'Trust Type':15s} {'Last Sign-in':15s} {'Days'}")
    print("-" * 85)
    for d in devices[:_DISPLAY_LIMIT]:
        last = d["last_signin"].strftime("%Y-%m-%d")
        print(f"{d['name'][:28]:30s} {d['os'][:18]:20s} {d['trust_type'][:13]:15s} {last:15s} {d['days_since']:>4d}")

    if len(devices) > _DISPLAY_LIMIT:
        print(f"\n... and {len(devices) - _DISPLAY_LIMIT} more")

    # OS breakdown
    os_counts = {}
    for d in devices:
        os_counts[d["os"]] = os_counts.get(d["os"], 0) + 1
    print("\nBreakdown by OS:")
    for os_name, count in sorted(os_counts.items(), key=lambda x: -x[1]):
        print(f"  {os_name or 'Unknown':30s} {count}")


if __name__ == "__main__":
    main()
