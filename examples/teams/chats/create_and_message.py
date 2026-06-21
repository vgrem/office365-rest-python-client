"""
Create a 1-on-1 chat with another user and send a message.

Requires delegated permission ``Chat.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/chat-post
https://learn.microsoft.com/en-us/graph/api/chat-post-messages
"""

import sys

from office365.graph_client import GraphClient
from office365.outlook.mail.item_body import ItemBody
from office365.teams.chats.type import ChatType
from tests.settings import client_id, password, tenant, user_principal, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

me = client.me.get().execute_query()
other = client.users[user_principal].get().execute_query()

if not me.id or not other.id:
    sys.exit("Could not resolve user IDs")

chat = client.chats.add(ChatType.oneOnOne, owner_ids=[me.id, other.id]).execute_query()
print(f"Chat created: {chat.id}  (topic: {chat.topic})")

msg = chat.messages.add(body=ItemBody("Hey, this message was sent via the Graph API!")).execute_query()
print(f"Message sent: {msg.id}")
