"""
List the teams the signed-in user is a direct member of.

Requires delegated permission ``Team.ReadBasic.All``.

https://learn.microsoft.com/en-us/graph/api/user-list-joinedteams
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)
teams = client.me.joined_teams.get().execute_query()
for team in teams:
    print(team.display_name)
