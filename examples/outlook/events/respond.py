"""
Respond to a meeting event — accept, decline, or cancel.

Shows how meeting attendees can accept or decline,
and how the organizer can cancel a meeting.

Requires delegated permission ``Calendars.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/event-accept
https://learn.microsoft.com/en-us/graph/api/event-decline
https://learn.microsoft.com/en-us/graph/api/event-cancel
"""

import sys

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

events = client.me.events.top(3).get().execute_query()
if len(events) == 0:
    sys.exit("No events found")

for event in events:
    if event.is_organizer:
        event.cancel(comment="Rescheduled to next week.").execute_query()
        print(f"Cancelled (as organizer): {event.subject}")
    else:
        event.accept(comment="I'll be there.").execute_query()
        print(f"Accepted: {event.subject}")
