"""
Download and parse Microsoft Graph CSV usage reports.

The Graph reports API returns CSV files. This example shows how
to download any report and parse it into structured data.

Available reports:
  - get_email_activity_counts
  - get_mailbox_usage_storage
  - get_mailbox_usage_mailbox_counts
  - get_onedrive_activity_user_counts
  - get_onedrive_usage_storage
  - get_sharepoint_activity_user_counts
  - get_sharepoint_site_usage_site_counts
  - get_teams_user_activity_user_counts
  - get_teams_team_counts
  - get_office365_activations_user_counts
  - get_m365_app_user_detail
  - get_app_user_counts

Requires delegated permission ``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/reportroot-getemailactivitycounts
"""

import csv
import os
import tempfile

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

REPORT_NAME = "EmailActivityCounts"
PERIOD = "D90"

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

method = getattr(client.reports, f"get_{REPORT_NAME.lower()}")
result = method(PERIOD).execute_query()

path = os.path.join(tempfile.mkdtemp(), f"{REPORT_NAME}.csv")
with open(path, "wb") as f:
    f.write(result.value)

with open(path) as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(dict(row))
