"""Licence a group once, and let Graph keep its members licensed.

Group-based licensing is the assignment an administrator wants: membership grants the seat,
leaving the group takes it away, and no per-user call is ever written. Graph maintains it, so
the script only moves the group's own assignment.

    python group_license.py --group "E5 users" --sku SPE_E5
    python group_license.py --group "E5 users" --sku SPE_E5 --remove

Requires delegated ``Group.ReadWrite.All``, ``User.ReadWrite.All`` and ``Organization.Read.All``.

https://learn.microsoft.com/en-us/graph/api/group-assignlicense
"""

import argparse
from uuid import UUID

from office365.directory.licenses.assigned_license import AssignedLicense
from office365.graph_client import GraphClient
from office365.runtime.client_value_collection import ClientValueCollection
from tests.settings import client_id, client_secret, tenant


def main() -> None:
    parser = argparse.ArgumentParser(description="Assign or remove a licence on a group")
    parser.add_argument("--group", required=True, help="Group display name")
    parser.add_argument("--sku", required=True, help="SKU part number, e.g. SPE_E5")
    parser.add_argument("--remove", action="store_true", help="Remove the licence from the group")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    sku = client.subscribed_skus.find_by_part_number(args.sku, required=True).execute_query()
    group = client.groups.find_by_name(args.group, required=True).execute_query()
    held = [licence.skuId for licence in group.assigned_licenses]
    if (sku.sku_id in held) == args.remove:
        raise SystemExit(f"{args.group} {'does not hold' if args.remove else 'already holds'} {sku.sku_part_number}")
    group.assign_license(
        ClientValueCollection(AssignedLicense, [] if args.remove else [AssignedLicense(skuId=sku.sku_id)]),
        [UUID(sku.sku_id or "")] if args.remove else [],
    ).execute_query()
    print(f"{'removed' if args.remove else 'assigned'} {sku.sku_part_number}: {args.group}")


if __name__ == "__main__":
    main()
