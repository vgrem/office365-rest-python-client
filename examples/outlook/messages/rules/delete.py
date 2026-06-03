"""
Delete an inbox rule by name.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/messagerule-delete?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

rules = client.me.mail_folders["Inbox"].message_rules.get().execute_query()
target = next((r for r in rules if r.display_name == "Move from Fanny"), None)
if target is None:
    sys.exit("Rule not found")

target.delete_object().execute_query()
print(f"Rule '{target.display_name}' deleted")
