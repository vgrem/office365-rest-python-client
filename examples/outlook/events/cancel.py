"""
Cancel a meeting event and notify all attendees.

Sends a cancellation message to all attendees. The event is removed
from the organizer's calendar.

Requires delegated permission ``Calendars.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/event-cancel?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

events = client.me.events.top(1).get().execute_query()
if len(events) == 0:
    sys.exit("No events were found")

event = events[0]
event.cancel(comment="This meeting has been cancelled.").execute_query()
print(f"Event '{event.subject}' cancelled")
