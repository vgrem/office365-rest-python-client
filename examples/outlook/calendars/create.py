"""
Create a new calendar in the user's calendar group.

Requires delegated permission ``Calendars.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/user-post-calendars?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

calendar = client.me.calendars.add("Team Events").execute_query()
print(f"Calendar created: {calendar.name}  (ID: {calendar.id})")
