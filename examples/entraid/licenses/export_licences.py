"""Export every user's licence assignments as CSV — the input ``import_licences.py`` reads.

One row per user and SKU, with the plans disabled inside that SKU written by name. A SKU id is
only meaningful next to the tenant that issued it, and a plan id less so; the names are what
``import_licences.py`` accepts back.

    python export_licences.py > licences.csv

Requires ``User.Read.All`` and ``Organization.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-list-licensedetails
"""

import argparse
import csv
import sys

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    catalogue = {str(sku.sku_id): sku for sku in client.subscribed_skus.get().execute_query()}
    holders = client.users.select(["userPrincipalName", "assignedLicenses"]).get_licensed()
    holders.get_all().execute_query()

    writer = csv.writer(sys.stdout)
    writer.writerow(["user_principal_name", "sku", "disabled_plans"])
    for user in holders:
        for licence in user.assigned_licenses:
            sku = catalogue.get(str(licence.skuId))
            sku_name = sku.sku_part_number if sku else str(licence.skuId)
            writer.writerow([user.user_principal_name, sku_name, ",".join(sorted(licence.disabled_plan_names(sku)))])


if __name__ == "__main__":
    main()
