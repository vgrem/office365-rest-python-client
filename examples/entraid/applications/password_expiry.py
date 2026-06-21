"""
Find application passwords that are expiring soon.

Requires delegated permission Application.Read.All.
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_admin_principal_name, test_client_id, test_tenant


def main():
    client = (
        GraphClient(tenant=test_tenant)
        .with_token_interactive(test_client_id, test_admin_principal_name)
        .require_role("Global Administrator", "Privileged Role Administrator")
    )

    cutoff = datetime.now(timezone.utc) + timedelta(days=30)

    for app in client.applications.get().execute_query():
        for cred in app.password_credentials:
            if cred.endDateTime and cred.endDateTime <= cutoff:
                days = (cred.endDateTime - datetime.now(timezone.utc)).days
                print(f"  {app.display_name}  hint={cred.hint}  expires={cred.endDateTime.date()}  ({days}d)")


if __name__ == "__main__":
    main()
