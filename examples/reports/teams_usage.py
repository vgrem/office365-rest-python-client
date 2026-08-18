"""
Teams user activity report — active users per channel/chat and totals.

Requires delegated permission ``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/reportroot-getteamsuseractivityusercounts
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
    parser = argparse.ArgumentParser(description="Teams user activity report")
    parser.add_argument("--period", default="D7", help="Report period (D7/D30/D90/D180)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    data = client.reports.get_teams_user_activity_user_counts(args.period).execute_query()
    rows = list(csv.DictReader(io.StringIO(_content(data).decode("utf-8"))))
    print(f"Teams user activity ({args.period}) — {len(rows)} rows:")
    for row in rows[:20]:
        print(dict(row))


if __name__ == "__main__":
    main()
