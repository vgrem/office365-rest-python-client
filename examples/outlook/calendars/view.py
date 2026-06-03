"""
Get the calendar view (events in a date range).

The calendar view returns single-instance expanded occurrences of
recurring events within the specified start/end window.

Requires delegated permission ``Calendars.Read``.

https://learn.microsoft.com/en-us/graph/api/calendar-list-calendarview?view=graph-rest-1.0
"""

from datetime import datetime, timedelta

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

start = datetime.utcnow()
end = start + timedelta(days=7)

events = client.me.calendar.calendar_view(start, end).get().execute_query()
print(f"Events from {start.date()} to {end.date()}:\n")
for ev in events:
    print(f"  {ev.start.strftime('%a %H:%M')}  {ev.subject}")
