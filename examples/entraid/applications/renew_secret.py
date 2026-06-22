"""
Check if the app's newest password is expiring soon — if so, add a replacement.

Avoids AADSTS7000222 by renewing before expiry.

Requires delegated permission Application.ReadWrite.All.

https://learn.microsoft.com/en-us/graph/api/application-addpassword
"""

from datetime import datetime, timezone

from office365.graph_client import GraphClient
from tests.settings import admin_username, client_id, tenant

WARN_DAYS = 30


def main():
    client = (
        GraphClient(tenant=tenant)
        .with_token_interactive(client_id, admin_username)
        .require_role("Global Administrator", "Privileged Role Administrator")
    )

    app = client.applications.get_by_app_id(client_id).get().execute_query()
    passwords = app.password_credentials

    if not passwords:
        print("No passwords found. Creating initial secret...")
        result = app.add_password("Initial secret").execute_query()
        print(f"CLIENT_SECRET={result.value.secretText}")
        return

    newest = max(passwords, key=lambda p: p.endDateTime or datetime.min)
    days = newest.days_until_expiry

    if days is None or days > WARN_DAYS:
        print(f"Newest password expires in {days} days (hint: {newest.hint}) — no renewal needed.")
        return

    print(f"Newest password expires in {days} days — renewing...")
    result = app.add_password(f"Rotated {datetime.now(timezone.utc).strftime('%Y-%m-%d')}").execute_query()
    print(f"CLIENT_SECRET={result.value.secretText}")


if __name__ == "__main__":
    main()
