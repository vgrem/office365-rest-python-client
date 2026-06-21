"""
List calendar permissions — who has access to your calendar and what role.

Governance: audit all users and groups with access to the default
calendar, their role (read, write, delegate), and status.

Requires delegated permission ``Calendars.Read``.

https://learn.microsoft.com/en-us/graph/api/calendar-list-calendarpermissions
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant, user_principal

client = (
    GraphClient(tenant=tenant)
    .with_client_secret(client_id, client_secret)
    .require_application_permission("Calendars.Read")
)

perms = client.users[user_principal].calendar.calendar_permissions.get().execute_query()
print(f"Calendar permissions ({len(perms)}):\n")
for p in perms:
    print(f"  {p.email_address:35}  {p.role}")
    print(f"  allowed roles: {p.allowed_roles}")
    print()
