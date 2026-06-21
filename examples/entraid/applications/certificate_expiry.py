"""
Find application certificates that are expiring soon.

Requires delegated permission Application.Read.All.
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    cutoff = datetime.now(timezone.utc) + timedelta(days=30)

    for app in client.applications.get().execute_query():
        for cred in app.key_credentials:
            if cred.endDateTime and cred.endDateTime <= cutoff:
                days = (cred.endDateTime - datetime.now(timezone.utc)).days
                hint = cred.displayName or cred.keyId or ""
                print(f"  {app.display_name}  hint={hint}  expires={cred.endDateTime.date()}  ({days}d)")


if __name__ == "__main__":
    main()
