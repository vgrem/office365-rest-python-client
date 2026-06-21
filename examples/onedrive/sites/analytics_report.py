"""
Get site activity analytics — views, visits, and edits per site.

Requires delegated permission Sites.Read.All.

https://learn.microsoft.com/en-us/graph/api/itemanalytics-get
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = (
    GraphClient(tenant=tenant)
    .with_client_secret(client_id, client_secret)
    .require_application_permission("Sites.Read.All")
)

sites = client.sites.order_by("displayName").get_all().execute_query()
print(f"{'Site':45s}  {'Views':>8s}  {'Visits':>8s}  {'Edits':>8s}")
print("-" * 75)
for s in sites:
    try:
        analytics = s.analytics.get().execute_query()
        views = analytics.all_time.views or 0
        visits = analytics.all_time.visits or 0
        edits = analytics.all_time.edits or 0
        print(f"{s.display_name or '':45s}  {views:>8d}  {visits:>8d}  {edits:>8d}")
    except Exception:
        print(f"{s.display_name or '':45s}  {'N/A':>8s}")
