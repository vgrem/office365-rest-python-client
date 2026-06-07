"""
Audit: view Intune audit events and device categories.

Audit events track admin actions across Intune. Device categories
help organize devices by group.

Requires delegated permission ``DeviceManagementServiceConfig.Read.All``.

https://learn.microsoft.com/en-us/graph/api/intune-auditing-auditevent-list
https://learn.microsoft.com/en-us/graph/api/intune-devices-devicecategory-list
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

# 1. List audit events
events = client.device_management.audit_events.top(10).get().execute_query()
print(f"Recent audit events ({len(events)}):")
for e in events:
    print(f"  [{e.activity_operation_type or '?'}] {e.display_name or '(unnamed)'}")
    print(f"       User: {e.user_id or '?'}  Target: {e.target_id or '?'}")

# 2. List device categories
categories = client.device_management.device_categories.get().execute_query()
print(f"\nDevice categories ({len(categories)}):")
for c in categories:
    print(f"  {c.display_name} (id: {c.id})")
