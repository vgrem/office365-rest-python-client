"""
Create a calendar event with attendees and details.

The most common scenario — schedule a meeting with subject,
time, body, and attendees.

Requires delegated permission ``Calendars.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/user-post-events
"""

from datetime import datetime, timedelta

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, user_principal, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

when = datetime.utcnow() + timedelta(days=1)
event = client.me.calendar.events.add(
    subject="Team Lunch",
    body="Let's grab lunch together.",
    start=when,
    end=when + timedelta(hours=1),
    attendees=[user_principal],
).execute_query()
print(f"Event created: {event.subject}  (ID: {event.id})")
