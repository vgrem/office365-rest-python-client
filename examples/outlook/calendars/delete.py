"""
Delete a calendar (except the default calendar).

The default calendar cannot be deleted.

Requires delegated permission ``Calendars.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/calendar-delete?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

calendars = client.me.calendars.get().execute_query()
target = next(
    (c for c in calendars if c.name != "Calendar" and c.name != "Kalender"), None
)
if target is None:
    sys.exit("No removable calendar found. Cannot delete default calendar.")

target.delete_object().execute_query()
print(f"Calendar '{target.name}' deleted")
