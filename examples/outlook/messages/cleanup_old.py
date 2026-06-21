"""
Clean up old messages — dry-run, then delete or archive.

Finds messages older than a specified number of days in a folder
and optionally deletes them. Useful for mailbox retention policies.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/message-delete
"""

from datetime import datetime, timedelta

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

PREVIEW_LIMIT = 5

folder_path = input("Folder (e.g. inbox): ").strip() or "inbox"
cutoff_days = int(input("Delete messages older than (days): ") or "180")
msg = f"Delete messages older than {cutoff_days}d from '{folder_path}'? (dry-run / yes / no): "
confirm = input(msg).strip().lower()

cutoff = datetime.utcnow() - timedelta(days=cutoff_days)
folder = client.me.mail_folders[folder_path]
messages = folder.messages.filter(f"receivedDateTime lt '{cutoff.isoformat()}Z'").get().execute_query()

print(f"Found {len(messages)} messages older than {cutoff_days} days")

if confirm == "yes":
    for m in messages:
        m.delete_object().execute_query()
    print(f"Deleted {len(messages)} messages")
elif confirm == "dry-run":
    for m in messages[:PREVIEW_LIMIT]:
        print(f"  {m.subject:40s}  {m.receivedDateTime}")
    if len(messages) > PREVIEW_LIMIT:
        print(f"  ... and {len(messages) - PREVIEW_LIMIT} more")
else:
    print("Cancelled.")
