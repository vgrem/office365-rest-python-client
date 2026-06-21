"""
Archive old messages — move messages older than X days to an archive folder.

Typical retention workflow: find messages in inbox older than a
cutoff date and move them to an "Archive" folder.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/message-move
"""

from datetime import datetime, timedelta

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

cutoff_days = int(input("Archive messages older than (days): ") or "30")

# Ensure archive folder exists
inbox = client.me.mail_folders["inbox"]
archive = next((f for f in inbox.child_folders.get().execute_query() if f.display_name == "Archive"), None)
if archive is None:
    archive = inbox.child_folders.add("Archive").execute_query()
    print("Created 'Archive' folder")

cutoff = datetime.utcnow() - timedelta(days=cutoff_days)
messages = inbox.messages.filter(f"receivedDateTime lt '{cutoff.isoformat()}Z'").get().execute_query()

count = 0
for m in messages:
    m.move(archive.id).execute_query()
    count += 1

print(f"Moved {count} messages to Archive")
