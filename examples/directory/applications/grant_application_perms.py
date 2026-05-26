"""
Grant an application permission (app role) to your app via admin consent.

This script checks whether the permission is already granted, and if not,
prompts an admin to sign in interactively and grant it.

Requires a Global Administrator or Privileged Role Administrator role.

https://learn.microsoft.com/en-us/graph/permissions-grant-via-msgraph?tabs=http&pivots=grant-application-permissions
"""

from office365.directory.permissions.guard import has_app_permission, has_role
from office365.graph_client import GraphClient
from tests import test_admin_principal_name, test_client_id, test_tenant

scope = input("Application permission (app role): ")

client = GraphClient(tenant=test_tenant).with_token_interactive(test_client_id, test_admin_principal_name)

if not has_role(client, "Global Administrator") and not has_role(client, "Privileged Role Administrator"):
    print("❌ Need Global Administrator or Privileged Role Administrator role to grant permissions.")
    exit(1)

if has_app_permission(client, scope, test_client_id):
    print(f"Permission '{scope}' is already granted.")
else:
    print(f"Permission '{scope}' is not granted.")
    answer = input("Grant it now via admin consent? (y/N): ")
    if answer.lower() == "y":
        resource = client.service_principals.get_by_name("Microsoft Graph")
        app = client.applications.get_by_app_id(test_client_id)
        resource.grant_application_permissions(app, scope).execute_query()
        print(f"Permission '{scope}' granted.")
    else:
        print("Skipped.")
