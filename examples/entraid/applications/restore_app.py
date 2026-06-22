"""
Restore a deleted application and re-add credentials.

Deleting an app without permanent_delete moves it to the deleted items
container where it can be restored within 30 days. Credentials and
permissions are NOT preserved — they must be re-added.

Requires delegated permission Application.ReadWrite.All.

https://learn.microsoft.com/en-us/graph/api/directory-deleteditems-list
https://learn.microsoft.com/en-us/graph/api/directory-deleteditems-restore
"""

import sys

from office365.graph_client import GraphClient
from tests.settings import admin_username, client_id, tenant

client = (
    GraphClient(tenant=tenant)
    .with_token_interactive(client_id, admin_username)
    .require_role("Global Administrator", "Privileged Role Administrator")
)

deleted_apps = client.directory.deleted_applications.get().execute_query()
target = next((a for a in deleted_apps if a.properties.get("appId") == client_id), None)

if not target:
    print(f"Deleted app with appId '{client_id}' not found.")
    print("Available deleted apps:")
    for a in deleted_apps:
        print(f"  {a.properties.get('displayName', '?')}  appId={a.properties.get('appId', '?')}")
    sys.exit(1)

print(f"Found: {target.properties.get('displayName')}")
target.restore().execute_query()
print("Restored.")

app = client.applications.get_by_app_id(client_id).get().execute_query()
result = app.add_password("Restored secret").execute_query()
print(f"New secret: hint={result.value.hint}")
print(f"CLIENT_SECRET={result.value.secretText}")
