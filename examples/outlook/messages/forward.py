"""
Forward the most recent message to additional recipients.

Requires delegated permission ``Mail.ReadWrite`` and ``Mail.Send``.

https://learn.microsoft.com/en-us/graph/api/message-forward?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

messages = client.me.messages.top(1).get().execute_query()
if len(messages) == 0:
    sys.exit("No messages were found")

first_message = messages[0]
first_message.forward(
    comment="FYI — please take a look.",
    to_recipients=["fannyd@contoso.onmicrosoft.com"],
).execute_query()
print("Message forwarded")
