"""What the tenant owns: seats, status, and how many of each are left.

One line per SKU, then one line for the users holding nothing. ``--plans`` adds the service
plans each SKU turns on — the part that answers a capability question rather than a seat one.

    python inventory.py
    python inventory.py --plans

Requires application ``Organization.Read.All`` (``User.Read.All`` for the unlicensed count).

https://learn.microsoft.com/en-us/graph/api/subscribedsku-list
"""

import argparse

from office365.directory.licenses.tenant import Licences
from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main() -> None:
    parser = argparse.ArgumentParser(description="Licence inventory: seats, status and plans")
    parser.add_argument("--plans", action="store_true", help="Also list the service plans of each SKU")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    for sku in sorted(Licences.of_tenant(client).skus, key=lambda item: item.sku_part_number or ""):
        total, used = sku.prepaid_units.enabled or 0, sku.consumed_units or 0
        print(f"{sku.sku_part_number}: {used}/{total} seats, {total - used} left, {sku.capability_status}")
        for plan in sku.service_plans if args.plans else ():
            print(f"  {plan.servicePlanName} {plan.provisioningStatus}")
    print(f"{client.users.get_unlicensed().count().execute_query().value} users hold no licence")


if __name__ == "__main__":
    main()
