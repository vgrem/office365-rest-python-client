"""
Find application passwords that are expiring soon.

Requires delegated permission Application.Read.All.
"""

from office365.graph_client import GraphClient
from tests.settings import admin_username, client_id, tenant

WARN_DAYS = 30


def main():
    client = (
        GraphClient(tenant=tenant)
        .with_token_interactive(client_id, admin_username)
        .require_role("Global Administrator", "Privileged Role Administrator")
    )

    for app in client.applications.get().execute_query():
        for cred in app.password_credentials:
            days = cred.days_until_expiry
            if days is not None and 0 <= days <= WARN_DAYS:
                print(f"  {app.display_name}  hint={cred.hint}  expires={cred.endDateTime.date()}  ({days}d)")


if __name__ == "__main__":
    main()
