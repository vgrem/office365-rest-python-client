"""
Mail flow: detect forwarding rules and find users with
auto-forwarding configured.

Common security concern — external forwarding can be a data
exfiltration vector.

Requires delegated permission ``User.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-list-mailboxsettings
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

# Check users for forwarding configuration
users = client.users.select(["id", "displayName"]).top(20).get().execute_query()
print(f"Checking {len(users)} users for mail forwarding: \n")
forwarding_found = False
for u in users:
    try:
        settings = client.users[u.id].mailbox_settings.get().execute_query()
        fwd = settings.get_property("forwardingAddress")
        if fwd:
            print(f"  ⚠ {u.display_name:25s}  forwards to: {fwd}")
            forwarding_found = True
    except Exception:
        pass

if not forwarding_found:
    print("  ✅ No forwarding found in checked users.")
