"""
List all registered applications.

Retrieves the first 100 app registrations in the tenant, showing
the display name, app (client) ID, and creation date.

https://learn.microsoft.com/en-us/graph/api/application-list

https://learn.microsoft.com/en-us/graph/api/resources/application

Requires delegated permission ``Application.Read.All`` or ``Application.ReadWrite.All``.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

apps = client.applications.top(100).execute_query()

for app in apps:
    print(f"{app.display_name:40s}  {app.app_id:40s}  {app.created_datetime}")
