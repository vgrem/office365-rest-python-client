"""
List all registered applications.

Retrieves the first 100 app registrations in the tenant, showing
the display name, app (client) ID, and creation date.

https://learn.microsoft.com/en-us/graph/api/application-list

https://learn.microsoft.com/en-us/graph/api/resources/application

Requires delegated permission ``Application.Read.All`` or ``Application.ReadWrite.All``.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

apps = client.applications.top(100).execute_query()

for app in apps:
    print(f"{app.display_name:40s}  {app.app_id:40s}  {app.created_datetime}")
