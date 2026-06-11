"""
License management: assign licenses, report usage, and find
unlicensed users.

Core identity admin tasks — manage service plans and licensing.

Requires delegated permission ``User.ReadWrite.All``,
``Organization.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-assignlicense
https://learn.microsoft.com/en-us/graph/api/subscribedsku-list
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

# 1. List available SKUs (license plans)
skus = client.subscribed_skus.get().execute_query()
print(f"Available SKUs ({len(skus)}):")
for s in skus:
    enabled = s.prepaid_units.enabled if s.prepaid_units else 0
    consumed = s.consumed_units or 0
    print(f"  {s.sku_part_number:30s}  enabled: {enabled:5d}  used: {consumed:5d}")

# 2. Find unlicensed users
users = client.users.get_unlicensed().top(100).select(["displayName", "userPrincipalName"]).execute_query()
print(f"\nUnlicensed users: {len(users)}")
for u in users:
    print(f"  {u.display_name or '':30s}  {u.user_principal_name}")
