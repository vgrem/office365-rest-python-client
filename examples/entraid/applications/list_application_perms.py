"""
List application permissions granted to the client app.

https://learn.microsoft.com/en-us/graph/permissions-grant-via-msgraph?tabs=http&pivots=grant-application-permissions

Requires delegated permission ``AppRoleAssignment.ReadWrite.All``.
"""

import sys

from office365.directory.permissions.guard import has_role
from office365.graph_client import GraphClient
from tests import (
    test_admin_principal_name,
    test_client_id,
    test_tenant,
)

# client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
privileged_client = GraphClient(tenant=test_tenant).with_token_interactive(test_client_id, test_admin_principal_name)
if not has_role(privileged_client, "Global Administrator", "Privileged Role Administrator"):
    print("❌ Need Global Administrator or Privileged Role Administrator role to check permissions.")
    sys.exit(1)


result = privileged_client.get_application_permissions(test_client_id).execute_query()
for app_role in result.value:
    print(app_role)
