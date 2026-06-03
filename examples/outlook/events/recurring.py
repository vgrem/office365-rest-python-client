"""
Create a recurring event in the user's default calendar.

Uses a weekly recurrence pattern for 4 occurrences.

Requires delegated permission ``Calendars.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/user-post-events?view=graph-rest-1.0
https://learn.microsoft.com/en-us/graph/api/resources/recurrencepattern
"""

from datetime import datetime, timedelta

from office365.graph_client import GraphClient
from office365.outlook.calendar.recurrence.range_type import RecurrenceRangeType
from office365.outlook.calendar.recurrence.pattern_type import RecurrencePatternType
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

when = datetime.utcnow() + timedelta(days=1)

new_event = (
    client.me.calendar.events.add(
        subject="Weekly Standup",
        body="Team sync meeting.",
        start=when,
        end=when + timedelta(hours=1),
        attendees=["samanthab@contoso.onmicrosoft.com"],
    )
    .with_recurrence(
        pattern_type=RecurrencePatternType.Weekly,
        interval=1,
        range_type=RecurrenceRangeType.Numbered,
        number_of_occurrences=4,
    )
    .execute_query()
)
print(f"Recurring event created: {new_event.subject}  (ID: {new_event.id})")
