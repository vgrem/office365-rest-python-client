"""
Find teams without owners — orphaned teams that no one administers.

Requires application permission TeamMember.Read.All and
Team.ReadBasic.All.

https://learn.microsoft.com/en-us/graph/api/team-list-members
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

orphans = []
for team in client.teams.get_all().select(["id", "displayName"]).execute_query():
    members = team.members.get().execute_query()
    owners = [m for m in members if "owner" in (m.properties.get("roles") or [])]
    if not owners:
        orphans.append(team.display_name)
        print(f"  {team.display_name}")

print(f"\nTeams without owners: {len(orphans)}")
