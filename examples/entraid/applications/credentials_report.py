"""
Consolidated credentials report — all apps with their passwords
and certificate expiry dates in one view.

Requires delegated permission Application.Read.All.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

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
        days = p.days_until_expiry
        warn = " <<<" if days is not None and days < WARN_DAYS else ""
        status = f"expires in {days}d{warn}" if days is not None else "  no_expiry"
        print(f"  [P] {p.displayName or '(unnamed)':30s}  {status}")
    for k in certs:
        days = k.days_until_expiry
        warn = " <<<" if days is not None and days < WARN_DAYS else ""
        status = f"expires in {days}d{warn}" if days is not None else "  no_expiry"
        print(f"  [C] {k.displayName or '(unnamed)':30s}  {status}")
