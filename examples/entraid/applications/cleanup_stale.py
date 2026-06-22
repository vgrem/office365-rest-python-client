"""
Delete apps where all credentials have expired — they can no longer
authenticate and are safe to remove.

Requires delegated permission Application.ReadWrite.All.

https://learn.microsoft.com/en-us/graph/api/application-delete
"""

from office365.graph_client import GraphClient
from tests.settings import admin_username, client_id, tenant

client = (
    GraphClient(tenant=tenant)
    .with_token_interactive(client_id, admin_username)
    .require_role("Global Administrator", "Privileged Role Administrator")
)

deleted = 0
for app in client.applications.get_all().execute_query():
    passwords = app.password_credentials
    certs = app.key_credentials
    all_creds = passwords + certs

    if not all_creds or all(c.is_expired for c in all_creds):
        print(f"  Deleting {app.display_name}  (app_id={app.app_id})")
        app.delete_object().execute_query()
        deleted += 1

print(f"\nDeleted {deleted} stale apps.")
