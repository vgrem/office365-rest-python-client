"""
Get storage usage for each site — find sites near or over quota.

Requires delegated permission Sites.Read.All.

https://learn.microsoft.com/en-us/graph/api/drive-get
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

WARN_PCT = 85

client = (
    GraphClient(tenant=tenant)
    .with_client_secret(client_id, client_secret)
    .require_application_permission("Sites.Read.All")
)

sites = client.sites.order_by("displayName").get_all().execute_query()
print(f"{'Site':45s}  {'Used':>10s}  {'Quota':>10s}  {'%':>6s}")
print("-" * 75)
for s in sites:
    drive = s.drive.get().execute_query()
    used = drive.quota.used or 0
    total = drive.quota.total or 1
    pct = used / total * 100
    used_gb = used / (1024**3)
    total_gb = total / (1024**3)
    warn = " <<<" if pct > WARN_PCT else ""
    print(f"{s.display_name or '':45s}  {used_gb:>6.1f}G  {total_gb:>6.1f}G  {pct:>5.1f}%{warn}")
