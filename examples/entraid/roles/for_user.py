"""
List the directory roles for the user.

https://learn.microsoft.com/en-us/graph/api/directoryrole-list?view=graph-rest-1.0

Requires delegated permission ``RoleManagement.ReadWrite.Directory``.
"""

from office365.graph_client import GraphClient
from tests import test_admin_principal_name, test_client_id, test_tenant

privileged_client = (
    GraphClient(tenant=test_tenant)
    .with_token_interactive(test_client_id, test_admin_principal_name)
    .require_role("Global Reader", "Global Administrator", "Privileged Role Administrator")
)

principal_name = input("User name: ")

result = privileged_client.users.get_by_principal_name(principal_name).get_directory_roles().execute_query()

for role in result:
    print(f"User has role: {role.display_name}")
