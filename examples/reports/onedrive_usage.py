"""
OneDrive usage report — active users and file counts.

Shows daily OneDrive activity: active users, files, synced users, and internal
vs external sharing.

Requires delegated permission ``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/reportroot-getonedriveactivityusercounts
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
    parser = argparse.ArgumentParser(description="OneDrive activity usage report")
    parser.add_argument("--period", default="D30", help="Report period (D7/D30/D90/D180)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    data = client.reports.get_onedrive_activity_user_counts(args.period).execute_query()

    rows = list(csv.DictReader(io.StringIO(_content(data).decode("utf-8"))))
    print(f"OneDrive activity ({args.period}) — {len(rows)} days:\n")
    print(f"{'Date':12s}  {'Active':>7s}  {'Files':>8s}  {'Synced':>7s}")
    for row in rows:
        date = row.get("Report Date", "?")[:10]
        print(f"{date:12s}  {row.get('Active Users', 0):>7}  {row.get('Files', 0):>8}  {row.get('Synced Users', 0):>7}")


if __name__ == "__main__":
    main()
