"""
Create a 1-on-1 chat with another user and send a message.

A chat is scoped to a set of participants (two users for 1-on-1).
After creation, you can send messages directly into it.

Requires delegated permission ``Chat.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/chat-post
https://learn.microsoft.com/en-us/graph/api/chat-post-messages
"""

from office365.graph_client import GraphClient
from office365.outlook.mail.item_body import ItemBody
from office365.teams.chats.type import ChatType
from tests import (
    test_client_id,
    test_password,
    test_tenant,
    test_user_principal_name,
    test_username,
)

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

# Resolve the authenticated user and the target user
me = client.me.get().execute_query()
other = client.users[test_user_principal_name].get().execute_query()

if not me.id or not other.id:
    exit("Could not resolve user IDs")

# Create a 1-on-1 chat
chat = client.chats.add(
    ChatType.oneOnOne, owner_ids=[me.id, other.id]
).execute_query()
print(f"Chat created: {chat.id}  (topic: {chat.topic})")

# Send a message in the chat
msg = chat.messages.add(
    body=ItemBody("Hey, this message was sent via the Graph API!")
).execute_query()
print(f"Message sent: {msg.id}")
