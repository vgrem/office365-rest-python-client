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
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

events = client.me.events.top(3).get().execute_query()
if len(events) == 0:
    sys.exit("No events found")

for event in events:
    if event.is_organizer:
        # As organizer: cancel the event
        event.cancel(comment="Rescheduled to next week.").execute_query()
        print(f"Cancelled (as organizer): {event.subject}")
    else:
        # As attendee: accept or decline
        event.accept(comment="I'll be there.").execute_query()
        print(f"Accepted: {event.subject}")
