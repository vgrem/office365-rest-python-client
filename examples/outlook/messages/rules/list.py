"""
List all inbox rules for the user's mailbox.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/mailfolder-list-messagerules?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

rules = client.me.mail_folders["Inbox"].message_rules.get().execute_query()
for rule in rules:
    status = "enabled" if rule.is_enabled else "disabled"
    print(f"  [{status}]  {rule.display_name}")
