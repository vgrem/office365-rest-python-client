"""
Remove expired passwords from all apps.

After rotating secrets, the old ones remain on the app. This removes
every expired password to keep the credential list clean.

Requires delegated permission Application.ReadWrite.All.

https://learn.microsoft.com/en-us/graph/api/application-delete-password
"""

from office365.graph_client import GraphClient
from tests.settings import admin_username, client_id, tenant


def main():
    client = (
        GraphClient(tenant=tenant)
        .with_token_interactive(client_id, admin_username)
        .require_role("Global Administrator", "Privileged Role Administrator")
    )
    removed = 0

    for app in client.applications.get().execute_query():
        for cred in app.password_credentials:
            if cred.is_expired and cred.keyId:
                app.remove_password(cred.keyId).execute_query()
                print(f"  {app.display_name:40s}  removed hint={cred.hint}  expired {cred.endDateTime.date()}")
                removed += 1

    print(f"\nRemoved {removed} expired passwords.")


if __name__ == "__main__":
    main()
