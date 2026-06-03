"""
How to list delegated permissions for an app using Microsoft Graph.
Delegated permissions, also called scopes or OAuth2 permissions, allow an app to call an API
on behalf of a signed-in user.


https://learn.microsoft.com/en-us/graph/permissions-grant-via-msgraph?tabs=http&pivots=grant-delegated-permissions

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


app = client.applications.get_by_app_id(test_client_id)
result = client.get_delegated_permissions(test_client_id).execute_query()

for scope in result.value:
    print(scope)
