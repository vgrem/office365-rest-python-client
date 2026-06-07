"""
Get mail tips for a recipient before sending a message.

Mail tips provide actionable information about a recipient —
such as out-of-office status, automatic replies, moderated
mailbox, or oversized message warnings — before you send.

Requires delegated permission ``Mail.Read`` or ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/user-getmailtips
"""

from office365.graph_client import GraphClient
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

tips = client.me.get_mail_tips([test_user_principal_name]).execute_query()
for tip in tips.value or []:
    print(f"Recipient: {tip.email_address.address}")
    print(f"  Auto-replies: {tip.automatic_replies.message if tip.automatic_replies else 'none'}")
    print(f"  Out of office: {tip.out_of_office}")
    print(f"  Mailbox full: {tip.mailbox_full}")
    print(f"  Max message size: {tip.max_message_size}")
