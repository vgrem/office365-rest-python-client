"""
Add a member to a team by email (owner role).

The user must exist in the tenant's Azure AD directory.

Requires delegated permission ``TeamMember.ReadWrite.All`` or
``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/team-post-members?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, user_principal_alt, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

teams = client.me.joined_teams.get().execute_query()
if len(teams) == 0:
    sys.exit("No teams found")

team = teams[0]
member = team.members.add(user=user_principal_alt, roles=["owner"]).execute_query()
print(f"Member '{member.display_name}' added to '{team.display_name}'")
