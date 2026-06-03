"""
Reply to an existing channel message thread.

Replying creates a new message in the same thread as the parent message.

Requires delegated permission ``ChannelMessage.Send``.

https://learn.microsoft.com/en-us/graph/api/chatmessage-post?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

teams = client.me.joined_teams.get().execute_query()
if len(teams) == 0:
    sys.exit("No teams found")

channel = teams[0].primary_channel
messages = channel.messages.top(1).get().execute_query()
if len(messages) == 0:
    sys.exit("No messages found")

reply = messages[0].replies.add(
    body=dict(content="Thanks for the update!")
).execute_query()
print(f"Reply sent: {reply.id}")
