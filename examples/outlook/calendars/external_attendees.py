"""
Find meetings with external attendees — attendees outside the tenant domain.

Security governance: detect when users invite external guests to
meetings, which may have compliance implications.

Requires delegated permission ``Calendars.Read``.

https://learn.microsoft.com/en-us/graph/api/user-list-events
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = (
    GraphClient(tenant=tenant)
    .with_client_secret(client_id, client_secret)
    .require_application_permission("Calendars.Read")
)

tenant_domain = tenant.split("@")[-1] if "@" in tenant else tenant

events = client.me.events.get().execute_query()
external = []
for e in events:
    if not e.attendees:
        continue
    for att in e.attendees:
        addr = att.emailAddress.address or ""
        if addr and tenant_domain not in addr:
            external.append((e.subject, att.emailAddress.name, addr))
            break

DISPLAY_LIMIT = 20

print(f"Meetings with external attendees: {len(external)}\n")
for subject, name, addr in external[:DISPLAY_LIMIT]:
    print(f"  {subject:40s}  {name:20s}  {addr}")
if len(external) > DISPLAY_LIMIT:
    print(f"  ... and {len(external) - DISPLAY_LIMIT} more")
