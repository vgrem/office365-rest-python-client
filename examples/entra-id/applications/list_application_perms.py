"""
List application permissions granted to the client app.

https://learn.microsoft.com/en-us/graph/permissions-grant-via-msgraph?tabs=http&pivots=grant-application-permissions

Requires delegated permission ``AppRoleAssignment.ReadWrite.All``.
"""

from office365.graph_client import GraphClient
from tests import (
    test_client_id,
    test_client_secret,
    test_tenant,
)

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

result = client.get_application_permissions(test_client_id).execute_query()
for app_role in result.value:
    print(app_role)
