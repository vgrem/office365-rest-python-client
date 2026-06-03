"""
List all channels in a team.

Requires delegated permission ``Channel.ReadBasic.All`` or ``Channel.Read.All``.

https://learn.microsoft.com/en-us/graph/api/channel-list?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

teams = client.me.joined_teams.get().execute_query()
if len(teams) == 0:
    sys.exit("No teams found")

team = teams[0]
channels = team.channels.get().execute_query()
print(f"Channels in '{team.display_name}':")
for ch in channels:
    print(f"  {ch.display_name:30s}  {ch.membership_type:10s}  {ch.id}")
