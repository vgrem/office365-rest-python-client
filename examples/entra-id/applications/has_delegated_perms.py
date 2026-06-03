"""
Check if a delegated permission (OAuth scope) is granted to your app.

https://learn.microsoft.com/en-us/graph/permissions-grant-via-msgraph

Requires delegated permission ``AppRoleAssignment.ReadWrite.All``.
"""

import sys

from office365.directory.permissions.guard import has_role
from office365.graph_client import GraphClient
from tests import test_admin_principal_name, test_client_id, test_tenant

client = GraphClient(tenant=test_tenant).with_token_interactive(test_client_id, test_admin_principal_name)

if not has_role(client, "Global Administrator", "Privileged Role Administrator"):
    print("❌ Need Global Administrator or Privileged Role Administrator role to grant permissions.")
    sys.exit(1)


scope = input("Permission scope: ")

if client.has_delegated_permission(scope, test_client_id):
    print(f"✅ Permission '{scope}' is granted.")
else:
    print(f"❌ Permission '{scope}' is not granted.")
