"""
List new/changed messages since the last sync using delta query.

Delta queries track incremental changes without re-fetching the
entire mailbox each time.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/message-delta?view=graph-rest-1.0
"""

from office365.delta_collection import ChangeType
from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)
messages = client.me.mail_folders["Inbox"].messages.delta.change_type(ChangeType.created).get().execute_query()
for m in messages:
    print(m.subject)
