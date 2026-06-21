"""
Register a new application (app registration).

Creates a new application with a display name and sign‑in audience.
The returned app object includes the app/client ID needed for authentication.

https://learn.microsoft.com/en-us/graph/api/application-post-applications

https://learn.microsoft.com/en-us/graph/api/resources/application

Requires delegated permission ``Application.ReadWrite.All``.
"""

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

app = client.applications.add(
    create_unique_name("DemoApp"),
    signInAudience="AzureADMyOrg",
).execute_query()
print(f"App created: {app.display_name} (appId: {app.app_id})")

app.delete_object(True).execute_query()
print("App cleaned up.")
