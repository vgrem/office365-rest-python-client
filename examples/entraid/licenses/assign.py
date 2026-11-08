"""Add a licence to a user, or take one away, after checking that the call can succeed.

Graph refuses an assignment when the user has no ``usageLocation`` or when the SKU has no seat
left, and the refusal arrives as a 400 after the write was attempted. Both facts are one
property away, so the script checks them first, and ``--dry-run`` does everything but the call.

    python assign.py --user ada@contoso.com --sku SPE_E5 --dry-run
    python assign.py --user ada@contoso.com --sku SPE_E5
    python assign.py --user ada@contoso.com --sku SPE_E5 --remove

Requires delegated ``User.ReadWrite.All`` and ``Organization.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-assignlicense
"""

import argparse

from office365.directory.licenses.assigned_license import AssignedLicense
from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main() -> None:
    parser = argparse.ArgumentParser(description="Assign or remove one licence, with the checks Graph would make")
    parser.add_argument("--user", required=True, help="User principal name")
    parser.add_argument("--sku", required=True, help="SKU part number, e.g. SPE_E5")
    parser.add_argument("--remove", action="store_true", help="Remove the licence instead of adding it")
    parser.add_argument("--dry-run", action="store_true", help="Print the call instead of making it")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    sku = client.subscribed_skus.find_by_part_number(args.sku, required=True).execute_query()
    user = client.users.get_by_principal_name(args.user).get().execute_query()
    holds = any(licence.skuId == sku.sku_id for licence in user.assigned_licenses)
    if holds == args.remove:
        raise SystemExit(f"{args.user} {'does not hold' if args.remove else 'already holds'} {sku.sku_part_number}")
    if not args.remove and not user.usage_location:
        raise SystemExit(f"{args.user} has no usageLocation, so no licence can be assigned")
    if not args.remove and (sku.prepaid_units.enabled or 0) - (sku.consumed_units or 0) <= 0:
        raise SystemExit(f"{sku.sku_part_number} has no seat left")
    print(f"{'remove' if args.remove else 'assign'} {sku.sku_part_number} {'from' if args.remove else 'to'} {args.user}")
    if args.dry_run:
        return
    user.assign_license(
        add_licenses=[] if args.remove else [AssignedLicense(skuId=sku.sku_id)],
        remove_licenses=[sku.sku_id or ""] if args.remove else [],
    ).execute_query()


if __name__ == "__main__":
    main()
