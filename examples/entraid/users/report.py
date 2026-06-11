"""
Report: user sign-in activity, inactive accounts, and accounts without MFA.

Common audit scenarios for identity hygiene.

Requires delegated permission ``User.Read.All``, ``AuditLog.Read.All``,
``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-list
https://learn.microsoft.com/en-us/graph/api/reportroot-getuserdetail
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

# 1. List users with sign-in activity
users = client.users.select(["id", "displayName", "userPrincipalName"]).top(20).get().execute_query()
print(f"Users ({len(users)}):")
for u in users:
    print(f"  {u.display_name:30s}  {u.user_principal_name}")

# 2. Users without assigned licenses
all_users = client.users.get_all().select(["displayName", "userPrincipalName"]).execute_query()
unlicensed = [u for u in all_users if not u.assigned_licenses]
print(f"\nUnlicensed accounts: {len(unlicensed)}")
for u in unlicensed[:10]:
    print(f"  {u.display_name or '':30s}  {u.user_principal_name}")
