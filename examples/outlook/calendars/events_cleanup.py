"""
Clean up old calendar events — dry-run, then delete.

Finds events older than a specified number of days and optionally
deletes them. Useful for mailbox maintenance and governance.

Requires delegated permission ``Calendars.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/event-delete
"""

from datetime import datetime, timedelta

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

cutoff_days = int(input("Delete events older than (days): ") or "90")
confirm = input(f"Delete events older than {cutoff_days} days? (dry-run / yes / no): ").strip().lower()

cutoff = datetime.utcnow() - timedelta(days=cutoff_days)

events = client.me.calendar.events.filter(f"end/dateTime lt '{cutoff.isoformat()}Z'").get().execute_query()
print(f"Found {len(events)} events older than {cutoff_days} days")

PREVIEW_LIMIT = 5

if confirm == "yes":
    for e in events:
        e.delete_object().execute_query()
    print(f"Deleted {len(events)} events")
elif confirm == "dry-run":
    for e in events[:PREVIEW_LIMIT]:
        print(f"  {e.subject}  ({e.start} — {e.end})")
    if len(events) > PREVIEW_LIMIT:
        print(f"  ... and {len(events) - PREVIEW_LIMIT} more")
else:
    print("Cancelled.")
