"""
Share your default calendar with another user.

Sets permissions at the calendar level, granting a specified role
(read, write, delegate) to the recipient.

Requires delegated permission ``Calendars.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/calendar-post-calendarpermissions
"""

from office365.graph_client import GraphClient
from office365.outlook.calendar.role_type import CalendarRoleType
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

perm = client.me.calendar.calendar_permissions.add(
    "samanthab@adatum.onmicrosoft.com", CalendarRoleType.read
).execute_query()
print(f"Calendar shared — permission ID: {perm.id}")
