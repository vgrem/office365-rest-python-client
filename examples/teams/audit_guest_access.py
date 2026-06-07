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
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)

groups = (
    client.groups.get()
    .filter("resourceProvisioningOptions/Any(x:x eq 'Team')")
    .select(["id", "displayName"])
    .top(999)
    .execute_query()
)

print(f"Scanning {len(groups)} teams for guest access...\n")

teams_with_guests = []

for group in groups:
    team = client.teams[group.id].get().execute_query()
    members = team.members.get().execute_query()

    guests = [
        m
        for m in members
        if "#EXT#" in (m.properties.get("email", "") or "")
    ]

    if guests:
        teams_with_guests.append((group.display_name, guests))
        print(f"  ⚠ {group.display_name}")
        for g in guests:
            email = g.properties.get("email", "?")
            roles = g.properties.get("roles", [])
            print(f"      {email}  ({', '.join(roles) if roles else 'member'})")

if not teams_with_guests:
    print("  ✅ No guest users found in any team.")

print(f"\nSummary: {len(teams_with_guests)} / {len(groups)} teams have guest access.")
