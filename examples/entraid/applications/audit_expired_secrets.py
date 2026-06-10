"""
Find apps with already-expired client secrets.

A practical response to the AADSTS7000222 error — find every
app registration whose password credentials have passed their
endDateTime so they can be rotated.

Requires delegated permission Application.Read.All.

https://learn.microsoft.com/en-us/graph/api/resources/application
"""

import sys
from datetime import datetime, timezone

from office365.directory.permissions.guard import has_role
from office365.graph_client import GraphClient
from tests import test_admin_principal_name, test_client_id, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_token_interactive(test_client_id, test_admin_principal_name)
    if not has_role(client, "Global Administrator", "Privileged Role Administrator"):
        print("❌ Need Global Administrator or Privileged Role Administrator role to grant permissions.")
        sys.exit(1)

    apps = client.applications.get().execute_query()

    now = datetime.now(timezone.utc)
    expired = []

    for app in apps:
        for cred in app.password_credentials or []:
            if cred.endDateTime and cred.endDateTime <= now:
                expired.append((app.display_name or "Unnamed", cred))

    print(f"Apps with expired secrets: {len(expired)}\n")
    for name, cred in expired:
        print(f"  {name}")
        print(f"    hint={cred.hint}  key_id={cred.keyId}  expired={cred.endDateTime}")


if __name__ == "__main__":
    main()
