"""
Grant an application permission (app role) to your app via admin consent.

This script checks whether the permission is already granted, and if not,
prompts an admin to sign in interactively and grant it.

Requires a Global Administrator or Privileged Role Administrator role.

https://learn.microsoft.com/en-us/graph/permissions-grant-via-msgraph?tabs=http&pivots=grant-application-permissions
"""

import sys

from office365.directory.permissions.guard import has_app_permission, has_role
from office365.graph_client import GraphClient
from tests import test_admin_principal_name, test_client_id, test_tenant

privileged_client = GraphClient(tenant=test_tenant).with_token_interactive(test_client_id, test_admin_principal_name)

if not has_role(privileged_client, "Global Administrator", "Privileged Role Administrator"):
    print("❌ Need Global Administrator or Privileged Role Administrator role to grant permissions.")
    sys.exit(1)

scope = input("Application permission (app role): ")

if has_app_permission(privileged_client, scope, test_client_id):
    print(f"Permission '{scope}' is already granted.")
else:
    print(f"Permission '{scope}' is not granted.")
    answer = input("Grant it now via admin consent? (y/N): ")
    if answer.lower() == "y":
        resource = privileged_client.service_principals.get_by_name("Microsoft Graph")
        resource.grant_application_permissions(test_client_id, scope).execute_query()
        print(f"Permission '{scope}' granted.")
    else:
        print("Skipped.")
