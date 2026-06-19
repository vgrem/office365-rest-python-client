"""
Adds a strong password or secret to an application.
https://learn.microsoft.com/en-us/graph/api/application-addpassword?view=graph-rest-1.0

Requires delegated permission ``Application.ReadWrite.All``.
"""

import sys

from office365.directory.permissions.guard import has_role
from office365.graph_client import GraphClient
from tests import (
    test_client_id,
    test_tenant,
    test_admin_principal_name,
)

client = GraphClient(tenant=test_tenant).with_token_interactive(test_client_id, test_admin_principal_name)
if not has_role(client, "Global Administrator", "Privileged Role Administrator"):
    print("Need Global Administrator or Privileged Role Administrator role to grant permissions.")
    sys.exit(1)

target_app = client.applications.get_by_app_id(test_client_id)
result = target_app.add_password("Password friendly name").execute_query()
print(result.value.secretText)
