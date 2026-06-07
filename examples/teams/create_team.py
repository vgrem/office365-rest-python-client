"""
Create a new team (async, waits for provisioning to complete).

Team creation is async — ``execute_query_and_wait`` polls until the
team is ready, then returns the fully-provisioned team object.

Requires delegated permission ``Team.Create`` or ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/team-post?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import (
    create_unique_name,
    test_client_id,
    test_password,
    test_tenant,
    test_username,
)

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

team_name = create_unique_name("Team")
print(f"Creating team '{team_name}' (this may take ~30-60 seconds)...")
team = client.teams.create(team_name).execute_query_and_wait()
print(f"Team created: {team.display_name}  ({team.web_url})")
