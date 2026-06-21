"""
Remove a member from a team by email.

Requires application permission ``TeamMember.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/team-delete-members?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant, user_principal

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

teams = client.teams.get().top(10).execute_query()
if len(teams) == 0:
    sys.exit("No teams found")

team = teams[0]
members = team.members.get().execute_query()
member = next((m for m in members if m.properties.get("email") == user_principal), None)
if member is None:
    sys.exit("Member not found")

member.delete_object().execute_query()
print(f"Member '{member.display_name}' removed from '{team.display_name}'")
