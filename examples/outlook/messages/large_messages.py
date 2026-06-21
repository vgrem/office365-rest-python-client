"""
Find large messages — messages over a specified size threshold.

Useful for mailbox cleanup and storage management. Sorted by size
(descending) so the biggest offenders appear first.

Requires delegated permission ``Mail.Read``.

https://learn.microsoft.com/en-us/graph/api/user-list-messages
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

min_mb = int(input("Minimum size in MB (e.g. 5): ") or "5")
min_bytes = min_mb * 1024 * 1024

messages = (
    client.me.mail_folders["inbox"]
    .messages.filter(f"size ge {min_bytes}")
    .select(["subject", "from", "size", "receivedDateTime"])
    .order_by("size desc")
    .get()
    .execute_query()
)

print(f"\nMessages over {min_mb} MB in inbox ({len(messages)}):\n")
for m in messages:
    sender = m.from_.emailAddress.address if m.from_ else ""
    size_mb = (m.size or 0) / (1024 * 1024)
    print(f"  {size_mb:6.1f} MB  {m.subject:40s}  {sender:30s}  {m.receivedDateTime}")
