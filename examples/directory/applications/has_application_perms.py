"""
Determines whether application permissions are granted to the client app.

https://learn.microsoft.com/en-us/graph/permissions-grant-via-msgraph?tabs=http&pivots=grant-application-permissions
"""

from office365.directory.permissions.resource_name import ResourceName
from office365.graph_client import GraphClient
from tests import (
    test_client_id,
    test_client_secret,
    test_tenant,
)

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)


resource = client.service_principals.get_by_name(ResourceName.Graph)
app_role = "IdentityRiskyUser.Read.All"
result = resource.get_application_permissions(test_client_id).execute_query()
# if app_role not in result.value:
if not any(role.value == app_role for role in result.value):
    print(f"Application permission '{app_role}' is not granted")
else:
    print(result.value)
