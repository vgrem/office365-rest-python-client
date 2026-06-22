"""
Export all team memberships to CSV using CollectionCsvWriter.

Each row represents one membership — teams with multiple members
produce multiple rows.

Requires application permission TeamMember.Read.All.

https://learn.microsoft.com/en-us/graph/api/team-list-members
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

with open("teams_membership.csv", "w", newline="") as f:
    client.teams.get_all().select(["displayName", "members/displayName", "members/email", "members/roles"]).expand(
        ["members"]
    ).to_csv(f).execute_query()

print("Exported to teams_membership.csv")
