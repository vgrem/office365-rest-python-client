"""
Usage report: team counts and user activity over multiple periods.

Compares D7, D30, and D90 activity levels — useful for adoption
tracking, chargeback reporting, and identifying inactive teams.

Requires delegated permission ``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/reportroot-getteamsuseractivityusercounts
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

PERIODS = ["D7", "D30", "D90"]

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

print("Teams activity report\n")
for p in PERIODS:
    counts = client.reports.get_teams_team_counts(p).execute_query()
    activity = client.reports.get_teams_user_activity_counts(p).execute_query()
    print(f"  {p}: {counts.value} teams, {activity.value} active users")

detail = client.reports.get_teams_user_activity_user_counts("D90").execute_query()
print(f"\n  Per-user activity (D90): {detail.value}")
