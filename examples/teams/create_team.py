"""
Create a new team (async, waits for provisioning to complete).

Team creation is async — ``execute_query_and_wait`` polls until the
team is ready, then returns the fully-provisioned team object.

Requires delegated permission ``Team.Create`` or ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/team-post?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

team_name = create_unique_name("Team")
print(f"Creating team '{team_name}' (this may take ~30-60 seconds)...")
team = client.teams.create(team_name).execute_query_and_wait()
print(f"Team created: {team.display_name}  ({team.web_url})")
