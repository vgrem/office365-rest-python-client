"""
Find apps where all credentials have expired — these apps can no longer
authenticate and are candidates for cleanup or renewal.

Requires delegated permission Application.Read.All.

https://learn.microsoft.com/en-us/graph/api/resources/application
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

stale = []
for app in client.applications.get_all().execute_query():
    passwords = app.password_credentials
    certs = app.key_credentials
    all_creds = passwords + certs

    if not all_creds:
        stale.append((app, "no credentials"))
        continue

    if all(c.is_expired for c in all_creds):
        newest = min(c.endDateTime for c in all_creds if c.endDateTime)
        stale.append((app, f"all expired (newest expired {newest.date()})"))

print(f"Stale apps ({len(stale)}):\n")
for app, reason in stale:
    print(f"  {app.display_name:45s}  {reason}  app_id={app.app_id}")
