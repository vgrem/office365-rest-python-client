"""
List user sign-in logs.

Retrieves the most recent sign-in activity for users in the tenant.
Each entry shows who signed in, from where, the app used, and the status.

https://learn.microsoft.com/en-us/graph/api/signin-list

https://learn.microsoft.com/en-us/graph/api/resources/signin

Requires delegated permission ``AuditLog.Read.All``.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
signins = client.audit_logs.signins.top(20).execute_query()

for s in signins:
    line = f"{s.created_datetime:%Y-%m-%d %H:%M}  {s.user_principal_name:9}  {s.app_display_name}  {s.status}"
    print(line)
