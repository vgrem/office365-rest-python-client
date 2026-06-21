"""
Find application certificates that are expiring soon.

Requires delegated permission Application.Read.All.
"""

from datetime import datetime, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

NOW = datetime.now(timezone.utc)
WARN_DAYS = 30

client = (
    GraphClient(tenant=tenant)
    .with_client_secret(client_id, client_secret)
    .require_application_permission("Application.Read.All")
)

for app in client.applications.get_all().execute_query():
    passwords = app.password_credentials or []
    certs = app.key_credentials or []
    if not passwords and not certs:
        continue

    print(f"\n{app.display_name}  (app_id={app.app_id})")
    for p in passwords:
        remaining = (p.endDateTime - NOW).days if p.endDateTime and p.endDateTime != datetime.min else None
        warn = " <<<" if remaining is not None and remaining < WARN_DAYS else ""
        status = f"expires in {remaining}d{warn}" if remaining is not None else "  no_expiry"
        print(f"  [P] {p.displayName or '(unnamed)':30s}  {status}")
    for k in certs:
        remaining = (k.endDateTime - NOW).days if k.endDateTime and k.endDateTime != datetime.min else None
        warn = " <<<" if remaining is not None and remaining < WARN_DAYS else ""
        status = f"expires in {remaining}d{warn}" if remaining is not None else "  no_expiry"
        print(f"  [C] {k.displayName or '(unnamed)':30s}  {status}")
