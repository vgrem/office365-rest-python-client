"""
Find all apps with expired passwords and rotate them.

Scans every app registration, checks password credentials,
and adds a new secret for any that have expired.

Requires delegated permission Application.ReadWrite.All.

https://learn.microsoft.com/en-us/graph/api/application-addpassword
"""

from datetime import datetime, timezone

from office365.graph_client import GraphClient
from tests.settings import admin_username, client_id, tenant


def main():
    client = (
        GraphClient(tenant=tenant)
        .with_token_interactive(client_id, admin_username)
        .require_role("Global Administrator", "Privileged Role Administrator")
    )

    now = datetime.now(timezone.utc)
    rotated = 0

    for app in client.applications.get().execute_query():
        for cred in app.password_credentials or []:
            if cred.is_expired:
                result = app.add_password(f"Rotated {now.strftime('%Y-%m-%d')}").execute_query()
                print(f"  {app.display_name:40s}  old hint={cred.hint}  new secret={result.value.secretText}")
                rotated += 1
                break

    print(f"\nRotated {rotated} apps with expired secrets.")


if __name__ == "__main__":
    main()
