"""
Paginate through all messages in a folder using $top and $skip.

When a mailbox has thousands of messages, you need pagination to
iterate through them all. This example walks every message and
counts them.

Requires delegated permission ``Mail.Read``.

https://learn.microsoft.com/en-us/graph/api/user-list-messages
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

folder_path = input("Folder (e.g. inbox): ").strip() or "inbox"
page_size = 50

folder = client.me.mail_folders[folder_path]
total = 0
skip = 0

while True:
    batch = folder.messages.top(page_size).skip(skip).select(["subject", "receivedDateTime"]).get().execute_query()
    if len(batch) == 0:
        break
    for m in batch:
        print(f"  {m.received_date_time}  {m.subject}")
    total += len(batch)
    skip += page_size

print(f"\nTotal messages in '{folder_path}': {total}")
