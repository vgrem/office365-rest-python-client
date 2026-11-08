"""Whether a seat, or a capability inside it, is actually held.

``require_license`` stops the run before the first request when the tenant owns no matching
SKU. ``Licences`` answers the same question as a value — and it is the only answer that
survives the trap: a SKU part number is packaging, a service plan is capability, so
``DEVELOPERPACK_E5`` carries ``RECORDS_MANAGEMENT`` even though no retail SKU does.

    python check.py
    python check.py --sku M365_E5 --plan RECORDS_MANAGEMENT

Requires application ``Organization.Read.All``.

https://learn.microsoft.com/en-us/graph/api/subscribedsku-list
"""

import argparse

from office365.directory.licenses.tenant import Licences
from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main() -> None:
    parser = argparse.ArgumentParser(description="Check the tenant holds a seat, or the plan inside it")
    parser.add_argument("--sku", default="DEVELOPERPACK_E5", help="SKU part number, or a substring of one")
    parser.add_argument("--plan", help="Service plan the seat must carry, e.g. RECORDS_MANAGEMENT")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret).require_license(args.sku)
    held = Licences.of_tenant(client)
    print(f"{len(held)} licences held: {', '.join(sorted(held.names))}")
    if args.plan:
        carriers = [sku.sku_part_number for sku in held.carrying(args.plan)]
        if not carriers:
            raise SystemExit(f"no held licence carries {args.plan}")
        print(f"{args.plan} comes from {', '.join(carriers)}")


if __name__ == "__main__":
    main()
