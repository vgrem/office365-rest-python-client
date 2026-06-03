"""
Get the trend of active users per Microsoft 365 app (Outlook, Word, Excel,
PowerPoint, OneNote, Teams) over the specified period.

Period: D7, D30, D90, or D180.

Requires delegated permission ``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/reportroot-getm365appusercounts?view=graph-rest-1.0
"""

import os
import tempfile

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
result = client.reports.get_m365_app_user_counts("D180").execute_query()
download_path = os.path.join(tempfile.mkdtemp(), "Report.csv")
with open(download_path, "wb") as f:
    f.write(result.value)
print(f"Report saved into : {download_path}")
