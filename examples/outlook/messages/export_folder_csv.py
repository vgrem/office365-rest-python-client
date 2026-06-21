"""
Export messages from a folder to CSV — subject, sender, date, size, attachments.

For audit, backup, or analysis of mailbox contents.

Requires delegated permission ``Mail.Read``.

https://learn.microsoft.com/en-us/graph/api/user-list-messages
"""

import csv

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

folder_path = input("Folder path (e.g. inbox, sentitems, or folder ID): ") or "inbox"

folder = client.me.mail_folders[folder_path]
fields = ["subject", "from", "receivedDateTime", "size", "hasAttachments"]
messages = folder.messages.select(fields).get().execute_query()

with open("mail_export.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Subject", "From", "Received", "Size (KB)", "Has Attachments"])
    for m in messages:
        sender = m.from_.emailAddress.address if m.from_ else ""
        size_kb = (m.size or 0) // 1024
        w.writerow([m.subject, sender, m.receivedDateTime, size_kb, m.hasAttachments])

print(f"Exported {len(messages)} messages to mail_export.csv")
