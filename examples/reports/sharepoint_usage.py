"""
SharePoint site usage — storage per site and total.

The per-site usage report is the basis for SharePoint storage governance: which
sites consume the most, and what the tenant total is.

Requires delegated permission ``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/reportroot-getsharepointsiteusagesitecounts
"""

import argparse
import csv
import io

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

GIB = 1024**3


def _content(result) -> bytes:
    value = result.value
    if isinstance(value, bytes):
        return value
    return value.content or b""


def main():
    parser = argparse.ArgumentParser(description="SharePoint site usage / storage report")
    parser.add_argument("--period", default="D90", help="Report period (D7/D30/D90/D180)")
    parser.add_argument("--top", type=int, default=15, help="how many sites to list by storage (default: 15)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    data = client.reports.get_sharepoint_site_usage_site_counts(args.period).execute_query()

    rows = list(csv.DictReader(io.StringIO(_content(data).decode("utf-8"))))
    usable = [r for r in rows if r.get("Site Url")]
    print(f"SharePoint sites ({args.period}) — {len(usable)} rows:\n")

    def storage(row):
        try:
            return float(row.get("Storage Used (Byte)") or 0)
        except ValueError:
            return 0.0

    total = sum(storage(r) for r in usable)
    print(f"Total storage used: {total / GIB:.2f} GiB across {len(usable)} sites\n")
    print("Largest sites:")
    for row in sorted(usable, key=storage, reverse=True)[: args.top]:
        print(f"  {storage(row) / GIB:8.2f} GiB  {row.get('Site Url')}")


if __name__ == "__main__":
    main()
