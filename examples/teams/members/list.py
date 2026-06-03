"""
List all members of a team.

Requires delegated permission ``TeamMember.Read.All`` or
``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/team-list-members?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

teams = client.me.joined_teams.get().execute_query()
if len(teams) == 0:
    sys.exit("No teams found")

team = teams[0]
members = team.members.get().execute_query()
print(f"Members of '{team.display_name}':")
for m in members:
    print(f"  {m.display_name:30s}  {m.email if m.email else ''}")
