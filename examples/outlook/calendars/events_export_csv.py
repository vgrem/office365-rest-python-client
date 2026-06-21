"""
Export calendar events to CSV — subject, organizer, attendees, time, recurrence.

Useful for auditing, reporting, or migrating calendar data.

Requires delegated permission ``Calendars.Read``.

https://learn.microsoft.com/en-us/graph/api/user-list-events
"""

import csv
from datetime import datetime, timedelta

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = (
    GraphClient(tenant=tenant)
    .with_client_secret(client_id, client_secret)
    .require_application_permission("Calendars.Read")
)

end = datetime.utcnow()
start = end - timedelta(days=90)

events = (
    client.me.calendar.events.filter(
        f"start/dateTime ge '{start.isoformat()}Z' and end/dateTime le '{end.isoformat()}Z'"
    )
    .get()
    .execute_query()
)

with open("calendar_export.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Subject", "Organizer", "Start", "End", "Attendees", "Recurrence"])
    for e in events:
        organizer = e.organizer.emailAddress.name if e.organizer else ""
        attendees = "; ".join(a.emailAddress.name for a in e.attendees) if e.attendees else ""
        recurrence = str(e.recurrence.pattern.type if e.recurrence else "")
        w.writerow([e.subject, organizer, e.start, e.end, attendees, recurrence])

print(f"Exported {len(events)} events to calendar_export.csv")
