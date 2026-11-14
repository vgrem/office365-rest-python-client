"""What the tenant owns: seats, status, and how many of each are left.

One line per SKU, then one line for the users holding nothing. ``--plans`` adds the service
plans each SKU turns on — the part that answers a capability question rather than a seat one.

    python inventory.py
    python inventory.py --plans
    python inventory.py --csv > seats.csv

Requires application ``Organization.Read.All`` (``User.Read.All`` for the unlicensed count).

https://learn.microsoft.com/en-us/graph/api/subscribedsku-list
"""

import argparse
import csv
import sys

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main() -> None:
    parser = argparse.ArgumentParser(description="Licence inventory: seats, status and plans")
    parser.add_argument("--plans", action="store_true", help="Also list the service plans of each SKU")
    parser.add_argument("--csv", action="store_true", help="Write one row per SKU as CSV")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    held = client.licences.get_all().execute_query().value
    if args.csv:
        rows = held.to_rows()
        writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]) if rows else ["skuId"])
        writer.writeheader()
        writer.writerows(rows)
        return
    for sku in sorted(held.skus, key=lambda item: item.sku_part_number or ""):
        total, used = sku.prepaid_units.enabled or 0, sku.consumed_units or 0
        print(f"{sku.sku_part_number}: {used}/{total} seats, {total - used} left, {sku.capability_status}")
        for plan in sku.service_plans if args.plans else ():
            print(f"  {plan.service_plan_name} {plan.provisioning_status}")
    print(f"unassigned seats: {', '.join(sku.sku_part_number or '' for sku in held.unassigned) or 'none'}")
    print(f"{client.users.get_unlicensed().count().execute_query().value} users hold no licence")


if __name__ == "__main__":
    main()
