"""
Move a draft message to another folder.

Creates a copy in the destination folder and removes the original.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/message-move?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)
folder_name = "Archive"
to_folder = client.me.mail_folders[folder_name]

message = client.me.messages.add(
    subject="Meet for lunch?",
    body="The new cafeteria is open.",
    to_recipients=["fannyd@contoso.onmicrosoft.com"],
)
message.move(to_folder).execute_query()
print(f"Draft message is created and moved into {folder_name} folder")
