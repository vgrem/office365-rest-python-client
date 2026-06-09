"""
Find apps with already-expired client secrets.

A practical response to the AADSTS7000222 error — find every
app registration whose password credentials have passed their
endDateTime so they can be rotated.

Requires delegated permission Application.Read.All.

https://learn.microsoft.com/en-us/graph/api/resources/application
"""

from datetime import datetime, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    apps = client.applications.get().execute_query()

    now = datetime.now(timezone.utc)
    expired = []

    for app in apps:
        for cred in app.password_credentials or []:
            if cred.end_date_time and cred.end_date_time <= now:
                expired.append((app.display_name or "Unnamed", cred))

    print(f"Apps with expired secrets: {len(expired)}\n")
    for name, cred in expired:
        print(f"  {name}")
        print(f"    hint={cred.hint}  key_id={cred.key_id}  expired={cred.end_date_time}")


if __name__ == "__main__":
    main()
