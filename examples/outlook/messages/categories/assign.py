"""
Assign a category to a message.

Categories are assigned by setting the ``categories`` property on the
message to one or more category names.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/message-update?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

messages = client.me.messages.top(1).get().execute_query()
if len(messages) == 0:
    sys.exit("No messages were found")

message = messages[0]
message.set_property("categories", ["Urgent"]).update().execute_query()
print(f"Category 'Urgent' assigned to message: {message.subject}")
