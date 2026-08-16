"""
Audit: view Intune audit events and device categories.

Audit events track admin actions across Intune. Device categories
help organize devices by group.

Requires delegated permission ``DeviceManagementServiceConfig.Read.All``.

https://learn.microsoft.com/en-us/graph/api/intune-auditing-auditevent-list
https://learn.microsoft.com/en-us/graph/api/intune-devices-devicecategory-list
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

# 1. List audit events
events = client.device_management.audit_events.top(10).get().execute_query()
print(f"Recent audit events ({len(events)}):")
for e in events:
    props = e.properties
    actor = props.get("actor") or {}
    actor_id = actor.get("userId", "?") if isinstance(actor, dict) else "?"
    print(f"  [{props.get('activityOperationType', '?'):14s}] {props.get('displayName', '(unnamed)')}  user: {actor_id}")

# 2. List device categories
categories = client.device_management.device_categories.get().execute_query()
print(f"\nDevice categories ({len(categories)}):")
for c in categories:
    print(f"  {c.properties.get('displayName', '(unnamed)')} (id: {c.id})")
