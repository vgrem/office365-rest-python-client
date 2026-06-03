"""
List all messages in the primary (General) channel of a team.

Requires delegated permission ``ChannelMessage.Read.All``.

https://learn.microsoft.com/en-us/graph/api/channel-list-messages?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

teams = client.me.joined_teams.get().execute_query()
if len(teams) == 0:
    sys.exit("No teams found")

team = teams[0]
messages = team.primary_channel.messages.get().execute_query()
print(f"Messages in '{team.display_name}' / General:")
for msg in messages:
    print(f"  [{msg.created_datetime:%Y-%m-%d %H:%M}] {msg.from_user.display_name}: {msg.body.content[:80]}")
