"""
Office 365 activations report — activated installs per product.

Shows which Office products (Outlook, Word, Excel, ...) are activated in the
tenant and whether users are activated on desktop/mobile/web.

Requires delegated permission ``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/reportroot-getoffice365activationcounts
"""

import argparse
import csv
import io

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def _content(result) -> bytes:
    value = result.value
    if isinstance(value, bytes):
        return value
    return value.content or b""


def main():
    parser = argparse.ArgumentParser(description="Office 365 activations report")
    parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    data = client.reports.get_office365_activation_counts().execute_query()

    rows = list(csv.DictReader(io.StringIO(_content(data).decode("utf-8"))))
    print(f"Office 365 activations ({len(rows)} rows):\n")
    print(f"{'Product':20s}  {'Total':>7s}  {'Activated':>10s}")
    for row in rows:
        product = row.get("Product") or "?"
        total = row.get("Total") or 0
        activated = row.get("Is Activated") or 0
        print(f"{product:20s}  {total:>7}  {activated:>10}")


if __name__ == "__main__":
    main()
