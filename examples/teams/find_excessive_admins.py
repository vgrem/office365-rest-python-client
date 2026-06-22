"""
Find teams with excessive owners — security risk and least-privilege
violation.

A team should typically have 2-5 owners. More than 5 is a red flag.

Requires application permission TeamMember.Read.All.

https://learn.microsoft.com/en-us/graph/api/team-list-members
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

MAX_OWNERS = 5

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

for team in client.teams.get_all().execute_query():
    members = team.members.get().execute_query()
    owners = [m for m in members if "owner" in (m.properties.get("roles") or [])]
    if len(owners) > MAX_OWNERS:
        print(f"  {team.display_name:45s}  {len(owners)} owners")
        for o in owners:
            email = o.properties.get("email", "?")
            print(f"      {o.display_name:30s}  {email}")
