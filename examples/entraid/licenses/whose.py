"""Who holds a licence, or what one person holds.

``--sku`` starts from ``get_licensed()`` — the collection filters itself to users holding
anything — and keeps the users whose assigned SKU id matches. ``--user`` reads that person's
``licenseDetails``, where every plan carries a provisioning status: a plan that is not
``Success`` is bought but not usable yet.

    python whose.py --sku SPE_E5
    python whose.py --user ada@contoso.com

Requires ``User.Read.All`` and ``Organization.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-list-licensess
"""

import argparse

from office365.directory.licenses.tenant import Licences
from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main() -> None:
    parser = argparse.ArgumentParser(description="Who holds a SKU, or what one user holds")
    who = parser.add_mutually_exclusive_group(required=True)
    who.add_argument("--sku", help="SKU part number, e.g. SPE_E5")
    who.add_argument("--user", help="User principal name")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    if args.sku:
        sku = client.subscribed_skus.find_by_part_number(args.sku, required=True).execute_query()
        licensed = client.users.get_licensed().select(["userPrincipalName"]).get().execute_query()
        holders = [user for user in licensed if any(lic.skuId == sku.sku_id for lic in user.assigned_licenses)]
        print(f"{len(holders)} users hold {sku.sku_part_number}")
        for user in holders:
            print(f"  {user.user_principal_name}")
        return
    details = client.users.get_by_principal_name(args.user).license_details.get().execute_query()
    for licence in Licences(details):
        print(licence.sku_part_number)
        for plan in licence.service_plans:
            print(f"  {plan.servicePlanName} {plan.provisioningStatus}")


if __name__ == "__main__":
    main()
