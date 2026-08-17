"""
License usage report: SKU inventory, assigned counts, and per-user breakdown.

Exports a comprehensive report useful for audits — combines inventory,
unlicensed users, and per-SKU user lists into a single view.

Requires delegated permission ``User.Read.All``, ``Organization.Read.All``.

https://learn.microsoft.com/en-us/graph/api/subscribedsku-list
https://learn.microsoft.com/en-us/graph/api/user-list
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

# 1. SKU inventory
skus = client.subscribed_skus.get().execute_query()
print("=" * 80)
print("LICENSE INVENTORY")
print("=" * 80)
print(f"{'SKU':35s}  {'Enabled':>8s}  {'Consumed':>8s}  {'Status':12s}")
print("-" * 80)
for s in sorted(skus, key=lambda x: x.sku_part_number or ""):
    enabled = s.prepaid_units.enabled if s.prepaid_units else 0
    consumed = s.consumed_units or 0
    status = s.capability_status or ""
    print(f"{s.sku_part_number or '':35s}  {enabled:8d}  {consumed:8d}  {status:12s}")

# 2. All users with their licenses
all_users = (
    client.users.select(["displayName", "userPrincipalName", "assignedLicenses"])
    .order_by("userPrincipalName")
    .get()
    .execute_query()
)

sku_map = {s.sku_id: s.sku_part_number for s in skus}

print()
print("=" * 80)
print("USER LICENSE ASSIGNMENTS")
print("=" * 80)
for u in all_users:
    if u.assigned_licenses:
        names = [sku_map.get(lic.skuId, lic.skuId[:8]) for lic in u.assigned_licenses]
        print(f"  {u.user_principal_name:45s}  {', '.join(names)}")

# 3. Unlicensed users
unlicensed = [u for u in all_users if not u.assigned_licenses]
print()
print("=" * 80)
print(f"UNLICENSED USERS ({len(unlicensed)})")
print("=" * 80)
for u in unlicensed:
    print(f"  {u.user_principal_name:45s}  {u.display_name or ''}")
