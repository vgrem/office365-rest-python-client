"""
Download and parse Microsoft Graph CSV usage reports.

The Graph reports API returns CSV files. Pick a report and period.

Requires delegated permission ``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/reportroot-getemailactivitycounts
"""

import argparse
import csv
import io

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

REPORTS = {
    "email_activity_counts": "get_email_activity_counts",
    "mailbox_usage_storage": "get_mailbox_usage_storage",
    "onedrive_activity_user_counts": "get_onedrive_activity_user_counts",
    "sharepoint_activity_user_counts": "get_sharepoint_activity_user_counts",
    "sharepoint_site_usage_site_counts": "get_sharepoint_site_usage_site_counts",
    "teams_user_activity_user_counts": "get_teams_user_activity_user_counts",
    "teams_team_counts": "get_teams_team_counts",
    "m365_app_user_counts": "get_m365_app_user_counts",
    "office365_activations_user_counts": "get_office365_activations_user_counts",
}


def _content(result) -> bytes:
    """Extract the CSV bytes from a report result (bytes or Report.content)."""
    value = result.value
    if isinstance(value, bytes):
        return value
    return value.content or b""


def main():
    parser = argparse.ArgumentParser(description="Download and parse a Graph CSV usage report")
    parser.add_argument(
        "--report",
        choices=sorted(REPORTS),
        default="teams_user_activity_user_counts",
        help="Report to download",
    )
    parser.add_argument("--period", default="D90", help="Report period (D7/D30/D90/D180)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    result = getattr(client.reports, REPORTS[args.report])(args.period).execute_query()

    rows = list(csv.DictReader(io.StringIO(_content(result).decode("utf-8"))))
    print(f"{args.report} ({args.period}) — {len(rows)} rows:")
    for row in rows[:20]:
        print(dict(row))


if __name__ == "__main__":
    main()
