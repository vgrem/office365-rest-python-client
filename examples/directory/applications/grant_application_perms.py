"""
Grant an application permission (app role) to your app via admin consent.

This script checks whether the permission is already granted, and if not,
prompts an admin to sign in interactively and grant it.

Requires a Global Administrator or Privileged Role Administrator role.

https://learn.microsoft.com/en-us/graph/permissions-grant-via-msgraph?tabs=http&pivots=grant-application-permissions
"""

from office365.directory.permissions.guard import has_app_permission
from office365.directory.permissions.resource_name import ResourceName
from office365.graph_client import GraphClient
from tests import test_admin_principal_name, test_client_id, test_tenant

scope = input("Application permission (app role): ") or "IdentityRiskyUser.Read.All"

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

if has_app_permission(client, scope, test_client_id, ResourceName.Graph):
    print(f"Permission '{scope}' is already granted.")
else:
    print(f"Permission '{scope}' is not granted.")
    answer = input("Grant it now via admin consent? (y/N): ")
    if answer.lower() == "y":
        admin = GraphClient(tenant=test_tenant).with_token_interactive(test_client_id, test_admin_principal_name)
        resource = admin.service_principals.get_by_name(ResourceName.Graph.value)
        app = admin.applications.get_by_app_id(test_client_id)
        resource.grant_application_permissions(app, scope).execute_query()
        print(f"Permission '{scope}' granted.")
    else:
        print("Skipped.")
