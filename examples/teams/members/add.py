"""
Add a member to a team by email (owner role).

The user must exist in the tenant's Azure AD directory.

Requires delegated permission ``TeamMember.ReadWrite.All`` or
``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/team-post-members?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import (
    test_client_id,
    test_password,
    test_tenant,
    test_user_principal_name_alt,
    test_username,
)

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

teams = client.me.joined_teams.get().execute_query()
if len(teams) == 0:
    sys.exit("No teams found")

team = teams[0]
member = team.members.add(user=test_user_principal_name_alt, roles=["owner"]).execute_query()
print(f"Member '{member.display_name}' added to '{team.display_name}'")
