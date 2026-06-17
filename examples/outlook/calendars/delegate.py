"""
Grant delegate access to your calendar.

Requires delegated permission Calendars.ReadWrite.
"""

from office365.graph_client import GraphClient
from office365.outlook.calendar.role_type import CalendarRoleType
from tests import test_client_id, test_password, test_tenant, test_username, test_user_principal_name_alt

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

perm = client.me.calendar.calendar_permissions.add(
    test_user_principal_name_alt, CalendarRoleType.delegateWithPrivateEventAccess
).execute_query()
print(f"Delegate access granted: {perm.id}")
