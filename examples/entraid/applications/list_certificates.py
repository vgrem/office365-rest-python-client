"""List certificates registered on the app with their validity status.

Requires delegated permission ``Application.ReadWrite.All``.

Usage:
    python list_certificates.py
"""

import sys
from datetime import datetime, timedelta, timezone

from office365.directory.permissions.guard import has_role
from office365.graph_client import GraphClient
from tests import test_admin_principal_name, test_client_id, test_tenant

client = GraphClient(tenant=test_tenant).with_token_interactive(test_client_id, test_admin_principal_name)
if not has_role(client, "Global Administrator", "Privileged Role Administrator"):
    print("Need Global Administrator or Privileged Role Administrator role.")
    sys.exit(1)

app = client.applications.get_by_app_id(test_client_id).get().execute_query()

now = datetime.now(timezone.utc)
soon = now + timedelta(days=30)

for cred in app.key_credentials:
    name = cred.displayName or "<unnamed>"
    start, end = cred.startDateTime, cred.endDateTime
    if not start or not end:
        print(f"{name:<20} {'NO DATES':<16}")
        continue
    if isinstance(start, str):
        start = datetime.fromisoformat(start.replace("Z", "+00:00"))
    if isinstance(end, str):
        end = datetime.fromisoformat(end.replace("Z", "+00:00"))
    if end < now:
        status = "EXPIRED"
    elif start > now:
        status = "NOT YET VALID"
    elif end < soon:
        status = "EXPIRING SOON"
    else:
        status = "VALID"
    tid = cred.customKeyIdentifier or ""
    print(f"{name:<16} {status:<14} {start.strftime('%Y-%m-%d'):<10} {end.strftime('%Y-%m-%d'):<10} {tid}")
