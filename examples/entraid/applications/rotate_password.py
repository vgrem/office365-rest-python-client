"""
Adds a strong password or secret to an application.
https://learn.microsoft.com/en-us/graph/api/application-addpassword?view=graph-rest-1.0

Requires delegated permission ``Application.ReadWrite.All``.
"""

from office365.graph_client import GraphClient
from tests.settings import (
    admin_username,
    client_id,
    tenant,
)

client = (
    GraphClient(tenant=tenant)
    .with_token_interactive(client_id, admin_username)
    .require_role("Global Administrator", "Privileged Role Administrator")
)

target_app = client.applications.get_by_app_id(client_id)
result = target_app.add_password("Password friendly name").execute_query()
print(result.value.secretText)
