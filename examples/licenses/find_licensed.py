"""
Find users with a specific license SKU.

Requires delegated permission ``User.Read.All``, ``Organization.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-list
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

# 1. Find the target SKU
sku_part = input("SKU part number (e.g. SPE_E5): ").strip()
skus = client.subscribed_skus.get().execute_query()
sku = next((s for s in skus if s.sku_part_number == sku_part), None)
if not sku:
    raise SystemExit(f"SKU '{sku_part}' not found.")

# 2. Find all users and filter by assigned SKU
all_users = client.users.select(["displayName", "userPrincipalName", "assignedLicenses"]).get().execute_query()
licensed = [u for u in all_users if u.assigned_licenses and any(lic.skuId == sku.sku_id for lic in u.assigned_licenses)]

print(f"\nUsers with {sku.sku_part_number} ({len(licensed)}):")
for u in licensed:
    print(f"  {u.display_name or '':30s}  {u.user_principal_name}")
