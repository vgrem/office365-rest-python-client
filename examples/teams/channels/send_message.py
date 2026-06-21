"""
Send a message to a team channel.

The most common Teams operation — send a message in a specific
channel.

Requires delegated permission ``ChannelMessage.Send``.

https://learn.microsoft.com/en-us/graph/api/channel-post-messages
"""

from office365.graph_client import GraphClient
from office365.outlook.mail.item_body import ItemBody
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

teams = client.me.joined_teams.get().execute_query()
team = teams[0] if teams else client.teams.get_all().execute_query()[0]
channel = team.channels.get().execute_query()[0]

msg = channel.messages.add(body=ItemBody(f"Hello from the Graph API — {__file__}")).execute_query()
print(f"Message sent to [{team.display_name}] / [{channel.display_name}]: {msg.id}")
