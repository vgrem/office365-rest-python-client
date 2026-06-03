"""
Delete a channel by display name (default channels like General cannot be
deleted).

Requires delegated permission ``Channel.Delete.All`` or ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/channel-delete?view=graph-rest-1.0
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
target = next((ch for ch in channels if ch.display_name != "General"), None)
if target is None:
    sys.exit("No removable channel found (only General channel exists)")

target.delete_object().execute_query()
print(f"Channel '{target.display_name}' deleted")
