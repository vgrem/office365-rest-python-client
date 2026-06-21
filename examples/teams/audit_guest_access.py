"""
Security audit: find all teams with external guest users.

Guest users in Azure AD have ``#EXT#`` in their user principal name.
This script scans every team in the tenant and reports which ones
contain guest members.

Requires application permission ``TeamMember.Read.All`` and
``Directory.Read.All``.

https://learn.microsoft.com/en-us/graph/api/team-list-members
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

teams = client.teams.get_all().select(["id", "displayName"]).execute_query()
print(f"Scanning {len(teams)} teams for guest access...\n")

found = 0
for team in teams:
    members = team.members.get().execute_query()
    guests = [m for m in members if "#EXT#" in (m.properties.get("email", "") or "")]
    if guests:
        found += 1
        print(f"  {team.display_name}")
        for g in guests:
            email = g.properties.get("email", "?")
            roles = g.properties.get("roles", [])
            print(f"      {email}  ({', '.join(roles) if roles else 'member'})")

if not found:
    print("  No guest users found.")
print(f"\nSummary: {found} / {len(teams)} teams have guest access.")
