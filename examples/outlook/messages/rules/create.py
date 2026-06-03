"""
Create an inbox rule that moves messages from a sender to a specific folder.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/mailfolder-post-messagerules?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

rule = (
    client.me.mail_folders["Inbox"]
    .message_rules.add(
        display_name="Move from Fanny",
        sequence=1,
        is_enabled=True,
        conditions={"from": ["fannyd@contoso.onmicrosoft.com"]},
        actions={"moveToFolder": "Archive"},
    )
    .execute_query()
)
print(f"Rule created: {rule.display_name}  (ID: {rule.id})")
