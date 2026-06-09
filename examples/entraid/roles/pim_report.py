"""
PIM (Privileged Identity Management): list role assignments
and report on privileged role members.

Eligible and active role assignments for administrative roles.

Requires delegated permission ``RoleManagement.Read.All``.

https://learn.microsoft.com/en-us/graph/api/rolemanagement-list-roleassignments
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

# Directory roles (Global Admin, User Admin, etc.)
roles = client.role_management.directory.role_assignments.get().expand(["roleDefinition"]).execute_query()
print(f"PIM directory role assignments ({len(roles)}):")
for r in roles:
    print(f"  Principal: {r.principal_id}  Role: {r.role_definition}")
