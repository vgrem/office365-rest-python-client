"""
Create a new public channel in a team.

Requires delegated permission ``Channel.Create`` or ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/channel-post?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

teams = client.me.joined_teams.get().execute_query()
if len(teams) == 0:
    sys.exit("No teams found")

team = teams[0]
channel = team.channels.add("Announcements", "Public announcement channel").execute_query()
print(f"Channel created: {channel.display_name}  (ID: {channel.id})")
