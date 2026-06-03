"""
Get the trend of Teams user activity (active users by work, mobile, etc.) over the specified period.

Period: D7, D30, D90, or D180.

Requires delegated permission ``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/reportroot-getteamsuseractivityusercounts?view=graph-rest-1.0
"""

import os
import tempfile

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

result = client.reports.get_teams_user_activity_user_counts("D90").execute_query()
download_path = os.path.join(tempfile.mkdtemp(), "TeamsUserActivity.csv")
with open(download_path, "wb") as f:
    f.write(result.value)
print(f"Teams user activity report saved: {download_path}")
