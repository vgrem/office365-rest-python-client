"""
Email activity report — sends, receives, and reads over time.

The Exchange Online activity report shows how many emails were sent, received,
and read each day over the selected period.

Requires delegated permission ``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/reportroot-getemailactivitycounts
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
    parser = argparse.ArgumentParser(description="Email activity counts report")
    parser.add_argument("--period", default="D30", help="Report period (D7/D30/D90/D180)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    data = client.reports.get_email_activity_counts(args.period).execute_query()

    rows = list(csv.DictReader(io.StringIO(_content(data).decode("utf-8"))))
    print(f"Email activity ({args.period}) — {len(rows)} days:\n")
    print(f"{'Date':12s}  {'Sent':>8s}  {'Received':>10s}  {'Read':>8s}")
    total_sent = total_received = total_read = 0
    for row in rows:
        date = row.get("Report Date", "?")[:10]
        sent = int(row.get("Send") or 0)
        received = int(row.get("Receive") or 0)
        read = int(row.get("Read") or 0)
        total_sent += sent
        total_received += received
        total_read += read
        print(f"{date:12s}  {sent:>8,}  {received:>10,}  {read:>8,}")

    print(f"\nTotals: {total_sent:,} sent, {total_received:,} received, {total_read:,} read")


if __name__ == "__main__":
    main()
