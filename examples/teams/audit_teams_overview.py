"""
Audit: tenant-wide Teams report with owners, member counts,
visibility, and archive status.

Requires application permissions Team.ReadBasic.All,
TeamMember.Read.All, and Directory.Read.All.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

teams = client.teams.get_all().select(["id", "displayName", "visibility", "mailNickname", "description"]).execute_query()
print(f"Found {len(teams)} teams\n")

for team in teams:
    members = team.members.get().execute_query()
    owners = [m for m in members if "owner" in (m.properties.get("roles") or [])]
    guests = [m for m in members if "#EXT#" in (m.properties.get("email", "") or "")]
    extra = ""
    if guests:
        extra = f"  {len(guests)} guest"
    status = "archived" if team.is_archived else "active"
    print(f"  {team.display_name}: {len(members)} members ({len(owners)} owners){extra}  {team.visibility}  {status}")
