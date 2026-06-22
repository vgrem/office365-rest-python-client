"""
List application permissions granted to the client app.

https://learn.microsoft.com/en-us/graph/permissions-grant-via-msgraph?tabs=http&pivots=grant-application-permissions

Requires delegated permission ``AppRoleAssignment.ReadWrite.All``.
"""

from office365.graph_client import GraphClient
from tests.settings import admin_username, client_id, tenant

privileged_client = (
    GraphClient(tenant=tenant)
    .with_token_interactive(client_id, admin_username)
    .require_role("Global Administrator", "Privileged Role Administrator")
)

result = privileged_client.get_application_permissions(client_id).execute_query()
for app_role in result.value:
    print(app_role)
