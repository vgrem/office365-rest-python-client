"""
Microsoft 365 apps usage report — includes Copilot usage.

For the Copilot-focused view, see ``examples/reports/copilot/usage_report.py``.

Requires delegated permission ``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/reportroot-getm365appusercounts
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
    parser = argparse.ArgumentParser(description="M365 apps usage report")
    parser.add_argument("--period", default="D7", help="Report period (D7/D30/D90/D180)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    data = client.reports.get_m365_app_user_counts(args.period).execute_query()
    rows = list(csv.DictReader(io.StringIO(_content(data).decode("utf-8"))))
    print(f"M365 apps user counts ({args.period}) — {len(rows)} rows (includes Copilot):")
    for row in rows[:20]:
        print(dict(row))


if __name__ == "__main__":
    main()
