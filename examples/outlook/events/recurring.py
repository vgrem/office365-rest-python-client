"""
Create a recurring event (weekly, 4 occurrences).

Shows how to set a recurrence pattern on an event.

Requires delegated permission ``Calendars.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/user-post-events
https://learn.microsoft.com/en-us/graph/api/resources/recurrencepattern
"""

from datetime import datetime, timedelta

from office365.graph_client import GraphClient
from office365.outlook.mail.patterned_recurrence import PatternedRecurrence
from office365.outlook.mail.recurrence_pattern import RecurrencePattern
from office365.outlook.mail.recurrence_range import RecurrenceRange
from office365.outlook.mail.recurrencepatterntype import RecurrencePatternType
from office365.outlook.mail.recurrencerangetype import RecurrenceRangeType
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

when = datetime.utcnow() + timedelta(days=1)

event = client.me.calendar.events.add(
    subject="Weekly Standup",
    body="Team sync meeting.",
    start=when,
    end=when + timedelta(hours=1),
).execute_query()

event.set_property(
    "recurrence",
    PatternedRecurrence(
        pattern=RecurrencePattern(
            type=RecurrencePatternType.weekly.value,
            interval=1,
        ),
        range=RecurrenceRange(
            type=RecurrenceRangeType.numbered.value,
            numberOfOccurrences=4,
            startDate=when.date(),
        ),
    ),
).update().execute_query()

print(f"Recurring event created: {event.subject}  (ID: {event.id})")
