"""
Report: all tags across all teams with member count.

Requires application permission ``TeamworkTag.Read.All`` and
``Team.ReadBasic.All``.

https://learn.microsoft.com/en-us/graph/api/teamworktag-list
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

all_teams = client.teams.get_all().execute_query()
tagged = set()
for team in all_teams:
    for tag in team.tags.get().execute_query():
        tagged.add(team.display_name)
        print(f"  [{team.display_name}]  {tag.display_name}  ({tag.member_count} members)")

untagged = [t.display_name for t in all_teams if t.display_name not in tagged]
if untagged:
    print(f"\nTeams without tags ({len(untagged)}): {', '.join(untagged)}")
