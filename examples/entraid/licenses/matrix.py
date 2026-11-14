"""The licence matrix: one row per user and SKU, with the service plans inside that seat.

An assignment names the SKU by ``skuId`` and the plans it disables by id, while the SKU
catalogue names both — so the matrix is a join, not a guess. The plans a user actually holds are
the SKU's provisioned plans minus the disabled ones, which is why the catalogue has to be read
first: only it knows what a ``skuId`` or a plan id stands for.

    python matrix.py                        # print the matrix as CSV
    python matrix.py --out licences.csv
    python matrix.py --sku DEVELOPERPACK_E5

Requires application ``Organization.Read.All`` and ``User.Read.All``.

https://learn.microsoft.com/en-us/graph/api/resources/assignedlicense
"""

import argparse
import csv
import sys

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

COLUMNS = ["userPrincipalName", "skuPartNumber", "enabledPlans", "disabledPlans"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Licence matrix: users against the SKUs they hold")
    parser.add_argument("--out", help="Write the CSV to this file instead of stdout")
    parser.add_argument("--sku", help="Only the rows for this SKU part number")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    held = client.licences.get_all().execute_query().value
    skus = held.by_id

    rows = []
    for user in client.users.get_licensed().get_all().execute_query():
        for assignment in user.assigned_licenses:
            sku = skus.get(assignment.skuId or "")
            if sku is None or (args.sku and sku.sku_part_number != args.sku):
                continue
            disabled = [sku.plan_name(plan_id) for plan_id in assignment.disabledPlans]
            enabled = [
                plan.service_plan_name
                for plan in sku.service_plans
                if plan.provisioning_status == "Success" and plan.service_plan_name not in disabled
            ]
            rows.append(
                {
                    "userPrincipalName": user.user_principal_name,
                    "skuPartNumber": sku.sku_part_number,
                    "enabledPlans": ";".join(filter(None, enabled)),
                    "disabledPlans": ";".join(disabled),
                }
            )

    stream = open(args.out, "w", newline="", encoding="utf-8") if args.out else sys.stdout
    with stream:
        writer = csv.DictWriter(stream, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
