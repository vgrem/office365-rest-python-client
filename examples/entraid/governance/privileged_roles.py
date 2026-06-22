"""
List eligible and active PIM role assignments.

Shows who has privileged directory roles via PIM.

Requires delegated permission ``RoleManagement.Read.Directory``.

https://learn.microsoft.com/en-us/graph/api/rbacapplication-list-roleassignments
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

assignments = client.role_management.directory.role_assignments.get().execute_query()
print(f"Role assignments ({len(assignments)}):\n")
for a in assignments:
    principal = a.principal_id or "?"
    role_def = client.role_management.directory.role_definitions.get_by_id(a.role_definition_id).get().execute_query()
    print(f"  user={principal:40s}  role={role_def.display_name}")
