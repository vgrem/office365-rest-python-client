"""
Check if the app's certificate is expiring soon — if so, upload a replacement.

Requires the new cert file at the configured CERT_PATH.

Requires delegated permission Application.ReadWrite.All.

https://learn.microsoft.com/en-us/graph/api/application-addcertificate
"""

from datetime import datetime, timezone

from office365.graph_client import GraphClient
from tests.settings import admin_username, client_id, tenant

WARN_DAYS = 30
CERT_PATH = "../../selfsigncert.pem"


def main():
    client = (
        GraphClient(tenant=tenant)
        .with_token_interactive(client_id, admin_username)
        .require_role("Global Administrator", "Privileged Role Administrator")
    )

    app = client.applications.get_by_app_id(client_id).get().execute_query()
    certs = app.key_credentials

    if not certs:
        print("No certificates found. Uploading initial cert...")
        with open(CERT_PATH, "rb") as f:
            app.add_certificate(f.read(), "Initial cert").execute_query()
        print("Certificate uploaded.")
        return

    newest = max(certs, key=lambda k: k.endDateTime or datetime.min)
    days = newest.days_until_expiry

    if days is None or days > WARN_DAYS:
        print(f"Newest cert expires in {days} days — no renewal needed.")
        return

    print(f"Newest cert expires in {days} days — renewing...")
    with open(CERT_PATH, "rb") as f:
        app.add_certificate(f.read(), f"Renewed {datetime.now(timezone.utc).strftime('%Y-%m-%d')}").execute_query()
    print("Certificate renewed.")


if __name__ == "__main__":
    main()
