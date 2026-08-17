"""
Remove a license from a user.

Requires delegated permission ``User.ReadWrite.All``, ``Organization.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-assignlicense
"""

import sys

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant, user_principal

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

# 1. Pre-fetch SKUs for display
skus = {s.sku_id: s.sku_part_number for s in client.subscribed_skus.get().execute_query()}

# 2. Find the user and their current licenses
user = client.users.get_by_principal_name(user_principal).get().execute_query()
print(f"User: {user.user_principal_name}")
if not user.assigned_licenses:
    sys.exit("No licenses assigned to this user.")

print("\nAssigned licenses:")
for lic in user.assigned_licenses:
    name = skus.get(lic.skuId, lic.skuId)
    print(f"  {name}  ({lic.skuId})")

# 3. Remove the license
sku_id = input("\nSKU ID to remove: ").strip()
user.assign_license(add_licenses=[], remove_licenses=[sku_id]).execute_query()
print(f"License removed from {user_principal}")
