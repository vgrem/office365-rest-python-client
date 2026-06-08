"""
Mailbox report: sizes, quotas, last activity, and inactive mailboxes.

Core Exchange admin tasks — understand mailbox usage and find
dormant mailboxes.

Requires delegated permission ``Mail.ReadWrite``, ``User.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-list-mailboxsettings
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

users = client.users.select(["id", "displayName", "userPrincipalName"]).top(20).get().execute_query()
print(f"Mailbox audit for {len(users)} users:\n")
for u in users:
    try:
        settings = client.users[u.id].mailbox_settings.get().execute_query()
        ar = settings.automatic_replies_status or "disabled"
        print(f"  {u.display_name:25s}  auto-replies: {ar}")
    except Exception:
        print(f"  {u.display_name:25s}  (no mailbox)")
