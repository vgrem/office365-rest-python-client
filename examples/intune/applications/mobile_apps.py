"""
Mobile apps inventory: apps by platform, publisher, and publishing state.

Lists all managed mobile apps plus the categories used to organize them.

Requires delegated permission ``DeviceManagementApps.Read.All``.

https://learn.microsoft.com/en-us/graph/api/intune-apps-mobileapp-list
https://learn.microsoft.com/en-us/graph/api/intune-apps-mobileappcategory-list
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

# 1. List all mobile apps
apps = client.device_app_management.mobile_apps.get().execute_query()
print(f"Mobile apps ({len(apps)}):")
for app in apps:
    publisher = app.publisher or "?"
    state = app.publishing_state or "?"
    print(f"  {app.display_name or '(unnamed)':35s} {publisher:20s} [{state}]")

# 2. List app categories
categories = client.device_app_management.mobile_app_categories.get().execute_query()
print(f"\nCategories ({len(categories)}):")
for c in categories:
    print(f"  {c.display_name}")
