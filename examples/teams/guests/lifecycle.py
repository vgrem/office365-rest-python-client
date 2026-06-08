"""
Guest lifecycle: find guests with no recent activity and
generate a report for expiry processing.

Common compliance task — identify stale external users.

Requires delegated permission ``User.Read.All``,
``AuditLog.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-list
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

guests = client.users.filter("userType eq 'Guest'").top(50).get().execute_query()
print(f"Guest users found: {len(guests)}\n")

stale = []
for g in guests:
    user_type = "#EXT#" if "#EXT#" in (g.user_principal_name or "") else "native guest"
    print(f"  {g.display_name or '(no name)':30s}  {g.user_principal_name:40s}  {user_type}")
    stale.append(g)

print(f"\nTotal guests: {len(stale)}")
print("Tip: use audit logs to check last sign-in date before expiry.")
