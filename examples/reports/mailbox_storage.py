"""
Mailbox storage usage report — storage trend and total.

Shows how much mailbox storage the tenant consumes over the selected period,
with a per-day breakdown and the overall trend.

Requires delegated permission ``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/reportroot-getmailboxusagestorage
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
    parser = argparse.ArgumentParser(description="Mailbox storage usage report")
    parser.add_argument("--period", default="D30", help="Report period (D7/D30/D90/D180)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    data = client.reports.get_mailbox_usage_storage(args.period).execute_query()

    rows = list(csv.DictReader(io.StringIO(_content(data).decode("utf-8"))))
    print(f"Mailbox storage ({args.period}) — {len(rows)} days:")
    for row in rows:
        date = row.get("Report Date", "?")[:10]
        storage = row.get("Storage Used (Byte)") or row.get("Storage Used (MB)") or 0
        try:
            value = float(storage)
            if "MB)" in " ".join(row.keys()) or int(value) < 10**10:
                gib = value / 1024
            else:
                gib = value / GIB
        except ValueError:
            gib = 0.0
        print(f"  {date}  {gib:.2f} GiB")

    latest = rows[-1] if rows else {}
    storage = latest.get("Storage Used (Byte)") or latest.get("Storage Used (MB)") or 0
    print(f"\nLatest storage used: {storage} ({'bytes' if 'Byte' in ' '.join(latest.keys()) else 'MB'})")


if __name__ == "__main__":
    main()
