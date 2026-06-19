"""
Find application certificates that are expiring soon.

Requires delegated permission Application.Read.All.
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
    cutoff = datetime.now(timezone.utc) + timedelta(days=30)

    for app in client.applications.get().execute_query():
        for cred in app.key_credentials:
            if cred.endDateTime and cred.endDateTime <= cutoff:
                days = (cred.endDateTime - datetime.now(timezone.utc)).days
                hint = cred.display_name or cred.key_id or ""
                print(f"  {app.display_name}  hint={hint}  expires={cred.endDateTime.date()}  ({days}d)")


if __name__ == "__main__":
    main()
