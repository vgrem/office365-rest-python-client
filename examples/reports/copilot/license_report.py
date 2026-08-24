"""
Report Microsoft 365 Copilot license adoption across the tenant.

Shows which Copilot-related SKUs are subscribed and how many licenses are
consumed vs enabled.

Requires delegated permission ``Organization.Read.All``.

https://learn.microsoft.com/en-us/graph/api/subscribedsku-list
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Report Copilot license adoption")
    parser.add_argument(
        "--keyword",
        default="COPILOT",
        help="SKU part-number substring to match (default: COPILOT)",
    )
    args = parser.parse_args()

    keyword = args.keyword.upper()
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    skus = client.subscribed_skus.get().execute_query()

    print(f"SKUs matching '{keyword}':\n")
    found = False
    for sku in skus:
        part_number = sku.sku_part_number or ""
        if keyword not in part_number.upper():
            continue
        found = True
        enabled = sku.prepaid_units.enabled if sku.prepaid_units else 0
        print(f"  {part_number:40s} consumed: {sku.consumed_units or 0} / enabled: {enabled}")

    if not found:
        print("  (no matching SKUs found)")


if __name__ == "__main__":
    main()
