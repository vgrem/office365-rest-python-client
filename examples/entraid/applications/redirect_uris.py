"""
Add or update redirect URIs for an application.

Most common app configuration task after registration.

Requires delegated permission Application.ReadWrite.All.

https://learn.microsoft.com/en-us/graph/api/application-update
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

app_id = input("App client ID: ").strip()
app = client.applications.get_by_app_id(app_id).get().execute_query()

uri = input("Redirect URI (e.g. https://localhost:3000/callback): ").strip()
current = app.properties.get("web", {}).get("redirectUris", [])
if uri not in current:
    current.append(uri)
    app.set_property("web", {"redirectUris": current})
    app.update().execute_query()
    print(f"Added redirect URI: {uri}")
else:
    print("Redirect URI already exists.")
