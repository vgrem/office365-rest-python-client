"""
Remove a member from a team by email.

Requires delegated permission ``TeamMember.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/team-delete-members?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import (
    test_client_id,
    test_password,
    test_tenant,
    test_user_principal_name,
    test_username,
)

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

teams = client.me.joined_teams.get().execute_query()
if len(teams) == 0:
    sys.exit("No teams found")

team = teams[0]
members = team.members.get().execute_query()
target = next((m for m in members if m.email == test_user_principal_name), None)
if target is None:
    sys.exit("Member not found")

target.delete_object().execute_query()
print(f"Member '{target.display_name}' removed from '{team.display_name}'")
