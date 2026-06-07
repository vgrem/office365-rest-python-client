"""
Create a calendar event with attendees and details.

The most common scenario — schedule a meeting with subject,
time, body, and attendees.

Requires delegated permission ``Calendars.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/user-post-events
"""

from datetime import datetime, timedelta

from office365.graph_client import GraphClient
from tests import (
    test_client_id,
    test_password,
    test_tenant,
    test_user_principal_name,
    test_username,
)

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

when = datetime.utcnow() + timedelta(days=1)
event = client.me.calendar.events.add(
    subject="Team Lunch",
    body="Let's grab lunch together.",
    start=when,
    end=when + timedelta(hours=1),
    attendees=[test_user_principal_name],
).execute_query()
print(f"Event created: {event.subject}  (ID: {event.id})")
