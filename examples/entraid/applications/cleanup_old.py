"""
Remove old credentials from apps that have been superseded by rotation.

When a new secret is added to replace an expiring one, the old credential
remains on the app. This removes all but the newest credential on each app
to keep the list clean and prevent authentication confusion.

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
        creds = app.password_credentials
        if len(creds) <= 1:
            continue
        newest = max(creds, key=lambda c: c.startDateTime or c.endDateTime)
        for cred in creds:
            if cred is not newest and cred.keyId:
                app.remove_password(cred.keyId).execute_query()
                print(f"  {app.display_name:40s}  removed hint={cred.hint}  {cred.endDateTime.date()}")
                removed += 1

    print(f"\nRemoved {removed} old credentials (kept newest on each app).")


if __name__ == "__main__":
    main()
