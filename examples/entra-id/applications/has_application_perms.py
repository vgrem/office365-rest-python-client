"""
Check if an application permission (app role) is granted to your app.

https://learn.microsoft.com/en-us/graph/permissions-grant-via-msgraph

Requires delegated permission ``AppRoleAssignment.ReadWrite.All``.
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
if not client.has_app_permission("AppRoleAssignment.ReadWrite.All", test_client_id):
    print("❌ App needs AppRoleAssignment.ReadWrite.All to grant permissions.")
    sys.exit(1)

scope = input("Application permission (app role): ")


if client.has_app_permission(scope, test_client_id):
    print(f"✅ Permission '{scope}' is granted.")
else:
    print(f"❌ Permission '{scope}' is not granted.")
