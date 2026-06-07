"""
Audit: full tenant-wide Teams report with owners, member counts,
visibility, and archive status.

Uses the Groups endpoint with OData filter to find all teams in the
tenant — the recommended approach for tenant-wide enumeration.

Requires application permission ``Team.ReadBasic.All``,
``TeamMember.Read.All``, and ``Directory.Read.All``.

https://learn.microsoft.com/en-us/graph/teams-list-all-teams
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)

# Step 1 — find all groups that have the "Team" provisioning flag
groups = (
    client.groups.get()
    .filter("resourceProvisioningOptions/Any(x:x eq 'Team')")
    .select(["id", "displayName", "visibility", "mailNickname", "description"])
    .top(999)
    .execute_query()
)

print(f"Found {len(groups)} teams in the tenant\n")

for group in groups:
    team = client.teams[group.id].get().select(["isArchived"]).execute_query()

    # Step 2 — get members and owners
    members = team.members.get().execute_query()
    owners = [m for m in members if "owner" in (m.properties.get("roles") or [])]
    guests = [
        m
        for m in members
        if "#EXT#" in (m.properties.get("email", "") or "")
    ]

    print(f"  {group.display_name}")
    print(f"    Visibility : {group.visibility or '?'}")
    print(f"    Archived  : {'⚠ YES' if team.is_archived else 'No'}")
    print(f"    Members   : {len(members)}  (owners: {len(owners)})")
    if guests:
        print(f"    Guests    : {len(guests)} — {', '.join(m.properties.get('email','?') for m in guests)}")
    print()
