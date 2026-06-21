"""
Grant an application permission (app role) to your app via admin consent.

This script checks whether the permission is already granted, and if not,
prompts an admin to sign in interactively and grant it.

Requires a Global Administrator or Privileged Role Administrator role.

https://learn.microsoft.com/en-us/graph/permissions-grant-via-msgraph?tabs=http&pivots=grant-application-permissions
"""

from office365.graph_client import GraphClient
from tests import test_admin_principal_name, test_client_id, test_tenant

privileged_client = (
    GraphClient(tenant=test_tenant)
    .with_token_interactive(test_client_id, test_admin_principal_name)
    .require_role("Global Administrator", "Privileged Role Administrator")
)

scope = input("Application permission (app role): ")

if privileged_client.has_app_permission(scope, test_client_id):
    print(f"Permission '{scope}' is already granted.")
else:
    print(f"Permission '{scope}' is not granted.")
    privileged_client.grant_application_permissions(test_client_id, scope).execute_query()
    print(f"Permission '{scope}' granted.")
