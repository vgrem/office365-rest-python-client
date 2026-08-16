"""
App Protection (MAM) policies and registrations.

Lists mobile app management (MAM) policies and the apps registered with them —
the core of "bring your own device" app-level protection.

Requires delegated permission ``DeviceManagementApps.Read.All``.

https://learn.microsoft.com/en-us/graph/api/intune-mam-managedapppolicy-list
https://learn.microsoft.com/en-us/graph/api/intune-mam-managedappregistration-list
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = (
    GraphClient(tenant=tenant)
    .with_client_secret(client_id, client_secret)
    .require_application_permission("DeviceManagementApps.Read.All", "DeviceManagementApps.ReadWrite.All")
)

# 1. List app protection (MAM) policies
policies = client.device_app_management.managed_app_policies.get().execute_query()
print(f"App protection policies ({len(policies)}):")
for p in policies:
    print(f"  {p.display_name or '(unnamed)':40s} created: {p.created_date_time or '?'}")

# 2. List managed app registrations
registrations = client.device_app_management.managed_app_registrations.get().execute_query()
print(f"\nManaged app registrations ({len(registrations)}):")
for r in registrations:
    print(f"  {r.entity_type_name or '?'}")
