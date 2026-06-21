"""
Grant delegate access to your calendar.

Requires delegated permission Calendars.ReadWrite.
"""

from office365.graph_client import GraphClient
from office365.outlook.calendar.role_type import CalendarRoleType
from tests.settings import client_id, password, tenant, user_principal_alt, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

perm = client.me.calendar.calendar_permissions.add(
    user_principal_alt, CalendarRoleType.delegateWithPrivateEventAccess
).execute_query()
print(f"Delegate access granted: {perm.id}")
