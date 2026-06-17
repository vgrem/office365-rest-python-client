"""
Create a recurring event (weekly, 4 occurrences).

Shows how to set a recurrence pattern on an event.

Requires delegated permission ``Calendars.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/user-post-events
https://learn.microsoft.com/en-us/graph/api/resources/recurrencepattern
"""

from datetime import datetime, timedelta

from office365.graph_client import GraphClient
from office365.outlook.mail.recurrencepatterntype import RecurrencePatternType
from office365.outlook.mail.recurrencerangetype import RecurrenceRangeType
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

when = datetime.utcnow() + timedelta(days=1)

event = client.me.calendar.events.add(
    subject="Weekly Standup",
    body="Team sync meeting.",
    start=when,
    end=when + timedelta(hours=1),
).execute_query()

event.set_recurrence(
    pattern_type=RecurrencePatternType.weekly,
    days_of_week=["monday", "wednesday", "friday"],
    interval=1,
    range_type=RecurrenceRangeType.numbered,
    occurrences=4,
    start_date=when.date(),
).update().execute_query()

print(f"Recurring event created: {event.subject}  (ID: {event.id})")
