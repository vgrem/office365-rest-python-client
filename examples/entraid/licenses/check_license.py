"""
Verify a subscription SKU is present and show its details — a practical
use of the ``require_license`` guard.

Defaults to the Microsoft 365 E5 Developer subscription (DEVELOPERPACK_E5).
Requires delegated permission ``Organization.Read.All`` (+ ``User.Read.All``
for the user list).

https://learn.microsoft.com/en-us/graph/api/subscribedsku-list
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Check a subscription SKU and show its details")
    parser.add_argument("--sku-keyword", default="DEVELOPERPACK_E5", help="SKU part-number substring to require")
    args = parser.parse_args()

    # The guard: exits with a friendly message if the tenant lacks the SKU
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret).require_license(args.sku_keyword)

    # Resolve the matching SKU and show seat usage + service plans
    skus = client.subscribed_skus.get().execute_query()
    sku = next((s for s in skus if s.sku_part_number and args.sku_keyword.lower() in s.sku_part_number.lower()), None)
    if sku is None:
        raise SystemExit(f"SKU '{args.sku_keyword}' not found")

    enabled = sku.prepaid_units.enabled if sku.prepaid_units else 0
    consumed = sku.consumed_units or 0
    print(f"SKU: {sku.sku_part_number}  ({sku.applies_to or '?'})")
    print(f"  Seats: {consumed}/{enabled} used   Status: {sku.capability_status or '?'}")
    plans = sku.service_plans or []
    print(f"  Service plans: {len(plans)}")
    for plan in list(plans)[:10]:
        print(f"    - {plan.servicePlanName}")

    # Users currently holding this SKU
    users = client.users.select(["displayName", "userPrincipalName", "assignedLicenses"]).get().execute_query()
    holders = [u for u in users if u.assigned_licenses and any(lic.skuId == sku.sku_id for lic in u.assigned_licenses)]
    print(f"\nUsers with this SKU: {len(holders)}")
    for u in holders[:20]:
        print(f"  {u.user_principal_name}")


if __name__ == "__main__":
    main()
