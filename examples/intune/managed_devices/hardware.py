"""
Device hardware inventory: OS, manufacturer, model, storage, and enrollment.

Goes beyond device names — surfaces the hardware detail admins need for
refresh, support, and audit decisions.

Requires delegated permission ``DeviceManagementManagedDevices.Read.All``.

https://learn.microsoft.com/en-us/graph/api/intune-devices-manageddevice-list
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def _gib(value) -> str:
    return f"{value / (1024**3):.1f} GiB" if value else "?"


client = (
    GraphClient(tenant=tenant)
    .with_client_secret(client_id, client_secret)
    .require_application_permission(
        "DeviceManagementManagedDevices.Read.All", "DeviceManagementManagedDevices.ReadWrite.All"
    )
)
devices = client.device_management.managed_devices.get().execute_query()
print(f"Found {len(devices)} managed devices\n")

for d in devices:
    print(f"{d.device_name or '(unnamed)':30s}  [{d.compliance_state or 'unknown'}]")
    print(f"    OS: {d.operating_system or '?'} {d.os_version or ''}".rstrip())
    print(f"    Hardware: {d.manufacturer or '?'} {d.model or ''}".rstrip())
    print(f"    Serial: {d.serial_number or '?'}  IMEI: {d.imei or '?'}")
    print(
        f"    Memory: {_gib(d.physical_memory_in_bytes)}  "
        f"Storage: {_gib(d.total_storage_space_in_bytes)} (free {_gib(d.free_storage_space_in_bytes)})"
    )
    print(f"    Enrolled: {d.enrolled_date_time or '?'}  Last sync: {d.last_sync_date_time or '?'}")
    print()
