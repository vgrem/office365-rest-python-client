"""
List the directory roles that are activated in the tenant.

https://learn.microsoft.com/en-us/graph/api/directoryrole-list?view=graph-rest-1.0

Requires delegated permission ``RoleManagement.ReadWrite.Directory``.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = (
    GraphClient(tenant=tenant)
    .with_client_secret(client_id, client_secret)
    .require_application_permission(
        "RoleManagement.Read.Directory",
        "RoleManagement.ReadWrite.Directory",
        "Directory.Read.All",
        "Directory.ReadWrite.All",
    )
)

roles = client.directory_roles.get().execute_query()
for role in roles:
    print(role)
