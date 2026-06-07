"""
Usage report: team counts and user activity over multiple periods.

Compares D7, D30, and D90 activity levels — useful for adoption
tracking, chargeback reporting, and identifying inactive teams.

Requires delegated permission ``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/reportroot-getteamsuseractivityusercounts
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

PERIODS = ["D7", "D30", "D90"]

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

print("Teams activity report\n")

# — Team counts per period —
print("  Team counts by period:")
for p in PERIODS:
    report = client.reports.get_teams_team_counts(p).execute_query()
    print(f"    {p}: {report.value}")

print()

# — User activity counts —
print("  Active users by period:")
for p in PERIODS:
    report = client.reports.get_teams_user_activity_counts(p).execute_query()
    print(f"    {p}: {report.value}")

print()

# — Individual user activity detail (last 90 days) —
detail = client.reports.get_teams_user_activity_user_counts("D90").execute_query()
print(f"  Per-user activity (D90): {detail.value}")
