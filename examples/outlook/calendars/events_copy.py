"""
Copy events between calendars — for migration, backup, or reorganization.

Selects events from a source calendar and creates them in a target
calendar. Useful when moving events between shared and personal
calendars, or during user offboarding.

Requires delegated permission ``Calendars.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/user-post-events
"""

from datetime import datetime, timedelta

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

target_calendar_id = input("Target calendar ID (leave empty for default): ").strip() or None

end = datetime.utcnow()
start = end - timedelta(days=30)

events = (
    client.me.calendar.events.filter(
        f"start/dateTime ge '{start.isoformat()}Z' and end/dateTime le '{end.isoformat()}Z'"
    )
    .get()
    .execute_query()
)

print(f"Found {len(events)} events to copy\n")
for e in events:
    target = client.me.calendars[target_calendar_id] if target_calendar_id else client.me.calendar
    target.events.add(
        subject=e.subject,
        body=e.bodyPreview or "",
        start=e.start,
        end=e.end,
    ).execute_query()
    print(f"  Copied: {e.subject}")

print(f"\nCopied {len(events)} events to target calendar")
