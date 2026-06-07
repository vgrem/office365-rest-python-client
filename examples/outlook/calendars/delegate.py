"""
Grant delegate access to your calendar — giving another user
editor-level control to create and modify events on your behalf.

Different from read-level sharing: delegates can also respond to
meeting requests.

Requires delegated permission ``Calendars.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/calendar-post-calendarpermissions
"""

from office365.graph_client import GraphClient
from office365.outlook.calendar.role_type import CalendarRoleType
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

perm = client.me.calendar.calendar_permissions.add(
    "samanthab@adatum.onmicrosoft.com", CalendarRoleType.delegate
).execute_query()
print(f"Delegate access granted — permission ID: {perm.get_property('id')}")
