"""
Get mail tips for a recipient before sending a message.

Mail tips provide actionable information about a recipient —
such as out-of-office status, automatic replies, moderated
mailbox, or oversized message warnings — before you send.

Requires delegated permission ``Mail.Read`` or ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/user-getmailtips
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, user_principal, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

result = client.me.get_mail_tips([user_principal]).execute_query()
for tip in result.value:
    print(f"Recipient: {tip.emailAddress}")
    print(f"  Auto-replies: {tip.automaticReplies.message}")
    print(f"  Out of office: {tip.out_of_office}")
    print(f"  Mailbox full: {tip.mailbox_full}")
    print(f"  Max message size: {tip.max_message_size}")
