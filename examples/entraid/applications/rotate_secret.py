"""
Generate a new client secret for an application.

After finding an expired secret, use this to create a replacement.
The secretText is only visible at creation time — save it.

Requires delegated permission Application.ReadWrite.All.

https://learn.microsoft.com/en-us/graph/api/application-addpassword
"""

import sys

from office365.directory.permissions.guard import has_role
from office365.graph_client import GraphClient
from tests import test_admin_principal_name, test_client_id, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_token_interactive(test_client_id, test_admin_principal_name)
    if not has_role(client, "Global Administrator", "Privileged Role Administrator"):
        print("Need Global Administrator or Privileged Role Administrator role to grant permissions.")
        sys.exit(1)

    app = client.applications.get_by_app_id(test_client_id)
    result = app.add_password("Rotated secret").execute_query()
    print(f"CLIENT_SECRET={result.value.secretText}")


if __name__ == "__main__":
    main()
